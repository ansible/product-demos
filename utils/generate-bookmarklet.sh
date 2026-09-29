#!/usr/bin/env bash
#
# Generate an "Import Domains" bookmarklet from domains.json.
# Usage: ./generate-bookmarklet.sh [path/to/domains.json]
#
# The output is a javascript: URL you can save as a browser bookmark.
# Click it while on the AAP UI to load the domains config into localStorage.

set -euo pipefail

JSON_FILE="${1:-$(dirname "$0")/apd-domains.json}"

if [[ ! -f "$JSON_FILE" ]]; then
  echo "Error: $JSON_FILE not found" >&2
  exit 1
fi

COMPACT=$(jq -c . "$JSON_FILE")

ESCAPED=$(printf '%s' "$COMPACT" | sed "s/'/\\\\'/g")

echo "javascript:void(localStorage.setItem('domains','${ESCAPED}'),location.reload())"
