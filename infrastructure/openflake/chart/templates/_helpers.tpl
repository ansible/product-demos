{{/*
Chart name, overridable.
*/}}
{{- define "openflake.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Release-qualified base name for every resource this chart creates.
*/}}
{{- define "openflake.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "openflake.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "openflake.backend.fullname" -}}
{{- printf "%s-backend" (include "openflake.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "openflake.frontend.fullname" -}}
{{- printf "%s-frontend" (include "openflake.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "openflake.postgresql.fullname" -}}
{{- printf "%s-postgresql" (include "openflake.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Labels applied to every object.
*/}}
{{- define "openflake.labels" -}}
helm.sh/chart: {{ include "openflake.chart" . }}
app.kubernetes.io/name: {{ include "openflake.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: openflake
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end -}}

{{/*
Selector labels for one component. Call as:
  {{ include "openflake.selectorLabels" (dict "context" . "component" "backend") }}
*/}}
{{- define "openflake.selectorLabels" -}}
app.kubernetes.io/name: {{ include "openflake.name" .context }}
app.kubernetes.io/instance: {{ .context.Release.Name }}
app.kubernetes.io/component: {{ .component }}
{{- end -}}

{{- define "openflake.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "openflake.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}

{{/*
Name of the Secret holding application credentials.
*/}}
{{- define "openflake.secretName" -}}
{{- if .Values.auth.existingSecret -}}
{{- .Values.auth.existingSecret -}}
{{- else -}}
{{- include "openflake.fullname" . -}}
{{- end -}}
{{- end -}}

{{- define "openflake.backend.image" -}}
{{- $tag := default .Values.image.tag .Values.backend.image.tag -}}
{{- printf "%s/%s:%s" .Values.image.registry .Values.backend.image.repository $tag -}}
{{- end -}}

{{- define "openflake.frontend.image" -}}
{{- $tag := default .Values.image.tag .Values.frontend.image.tag -}}
{{- printf "%s/%s:%s" .Values.image.registry .Values.frontend.image.repository $tag -}}
{{- end -}}

{{/*
Data of the chart-managed Secret as it already exists in the cluster, as JSON.
Lets `helm upgrade` reuse previously generated credentials instead of rolling
them. Returns "{}" on first install and during `helm template`, where the
cluster is not consulted.
*/}}
{{- define "openflake.existingSecretData" -}}
{{- $found := lookup "v1" "Secret" .Release.Namespace (include "openflake.secretName" .) -}}
{{- if and $found $found.data -}}
{{- toJson $found.data -}}
{{- else -}}
{{- "{}" -}}
{{- end -}}
{{- end -}}

{{/*
Credential resolution order: explicit value, then the value already stored in
the cluster, then a freshly generated one.

Each of these calls randAlphaNum, so a single render must resolve each value
exactly once and reuse it through a variable. Only templates/secret.yaml calls
them; every workload reads the resulting Secret.
*/}}
{{- define "openflake.postgresPassword" -}}
{{- if .Values.postgresql.password -}}
{{- .Values.postgresql.password -}}
{{- else -}}
{{- $data := fromJson (include "openflake.existingSecretData" .) -}}
{{- if $data.POSTGRESQL_PASSWORD -}}
{{- b64dec $data.POSTGRESQL_PASSWORD -}}
{{- else -}}
{{- randAlphaNum 24 -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "openflake.secretKey" -}}
{{- if .Values.auth.secretKey -}}
{{- .Values.auth.secretKey -}}
{{- else -}}
{{- $data := fromJson (include "openflake.existingSecretData" .) -}}
{{- if $data.SECRET_KEY -}}
{{- b64dec $data.SECRET_KEY -}}
{{- else -}}
{{- randAlphaNum 48 -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "openflake.adminPassword" -}}
{{- if .Values.auth.adminPassword -}}
{{- .Values.auth.adminPassword -}}
{{- else -}}
{{- $data := fromJson (include "openflake.existingSecretData" .) -}}
{{- if $data.ADMIN_PASSWORD -}}
{{- b64dec $data.ADMIN_PASSWORD -}}
{{- else -}}
{{- randAlphaNum 20 -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
In-cluster DNS name of the backend Service. nginx resolves `set`-assigned
upstreams through its `resolver` directive, which ignores the search domains
in /etc/resolv.conf, so the frontend needs the fully qualified name.
*/}}
{{- define "openflake.backend.serviceFqdn" -}}
{{- printf "%s.%s.svc.cluster.local" (include "openflake.backend.fullname" .) .Release.Namespace -}}
{{- end -}}

{{/*
Public URL users reach OpenFlake on. Derived from the Route unless overridden.
Empty when route.host was not supplied and no explicit baseUrl was given.
*/}}
{{- define "openflake.publicUrl" -}}
{{- if .Values.config.baseUrl -}}
{{- .Values.config.baseUrl | trimSuffix "/" -}}
{{- else if and .Values.route.enabled .Values.route.host -}}
{{- $scheme := ternary "https" "http" .Values.route.tls.enabled -}}
{{- printf "%s://%s" $scheme .Values.route.host -}}
{{- end -}}
{{- end -}}

{{/*
BASE_URL for the backend. Falls back to the in-cluster frontend Service when
the public hostname is not known yet, so generated links stay resolvable from
inside the cluster. NOTES.txt tells the installer how to correct this.
*/}}
{{- define "openflake.baseUrl" -}}
{{- $public := include "openflake.publicUrl" . -}}
{{- if $public -}}
{{- $public -}}
{{- else -}}
{{- printf "http://%s.%s.svc.cluster.local:%v" (include "openflake.frontend.fullname" .) .Release.Namespace .Values.frontend.service.port -}}
{{- end -}}
{{- end -}}

{{/*
CORS origins for API clients calling from a browser. The UI itself is served
same-origin through nginx and does not need an entry here.
*/}}
{{- define "openflake.corsOrigins" -}}
{{- if .Values.config.corsOrigins -}}
{{- .Values.config.corsOrigins -}}
{{- else -}}
{{- include "openflake.baseUrl" . -}}
{{- end -}}
{{- end -}}
