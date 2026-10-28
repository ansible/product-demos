package apd

import rego.v1

pac_vars := object.get(input.extra_vars, "policy_as_code_vars", {})

# =============================================================================
# Maintenance window
# =============================================================================

_mw_start_str := object.get(pac_vars, "maintenance_window_start", null)
_mw_end_str := object.get(pac_vars, "maintenance_window_end", null)
_mw_tz := object.get(pac_vars, "maintenance_window_timezone", "UTC")

_mw_parse_minutes(hhmm) := (to_number(parts[0]) * 60) + to_number(parts[1]) if {
  parts := split(hhmm, ":")
  count(parts) == 2
  to_number(parts[0]) >= 0
  to_number(parts[0]) <= 23
  to_number(parts[1]) >= 0
  to_number(parts[1]) <= 59
}

_mw_start_min := _mw_parse_minutes(_mw_start_str)
_mw_end_min := _mw_parse_minutes(_mw_end_str)

_mw_clock := time.clock([time.parse_rfc3339_ns(input.created), _mw_tz])
_mw_now_min := (_mw_clock[0] * 60) + _mw_clock[1]

_mw_configured if {
  _mw_start_str != null
  _mw_end_str != null
}

violations contains msg if {
  _mw_configured
  not _mw_start_min
  msg := sprintf("Invalid maintenance_window_start value '%s' — use HH:MM format (00:00-23:59)", [_mw_start_str])
}

violations contains msg if {
  _mw_configured
  not _mw_end_min
  msg := sprintf("Invalid maintenance_window_end value '%s' — use HH:MM format (00:00-23:59)", [_mw_end_str])
}

_mw_wrapping if {
  _mw_start_min > _mw_end_min
}

_mw_in_window if {
  not _mw_wrapping
  _mw_now_min >= _mw_start_min
  _mw_now_min < _mw_end_min
}

_mw_in_window if {
  _mw_wrapping
  _mw_now_min >= _mw_start_min
}

_mw_in_window if {
  _mw_wrapping
  _mw_now_min < _mw_end_min
}

violations contains msg if {
  _mw_configured
  _mw_start_min == _mw_end_min
  msg := sprintf(
    "maintenance_window_start and maintenance_window_end are both '%s' — start and end times must differ",
    [_mw_start_str],
  )
}

violations contains msg if {
  _mw_configured
  _mw_start_min
  _mw_end_min
  _mw_start_min != _mw_end_min
  not _mw_in_window
  msg := sprintf(
    "Job execution is only allowed between %s and %s (%s)",
    [_mw_start_str, _mw_end_str, _mw_tz],
  )
}

# =============================================================================
# Deny superuser accounts
# =============================================================================

violations contains msg if {
  input.created_by.is_superuser
  not object.get(pac_vars, "allow_superuser", false) in {true, "true"}
  msg := sprintf(
    "Superuser account '%v' is not allowed to run jobs — use an account with a different role",
    [input.created_by.username],
  )
}

# =============================================================================
# Combined result
# =============================================================================

default common_policies := {
  "allowed": true,
  "violations": [],
}

common_policies := {
  "allowed": false,
  "violations": [v | some v in violations],
} if {
  count(violations) > 0
}
