"""
VoIP.ms API Error Codes

This file contains error codes that are not available in the official HTML documentation
but were discovered from other sources. The main error codes are now loaded from the
API definition which extracts them directly from the official VoIP.ms documentation.

These additional codes supplement the official documentation.
"""

ERROR_CODES = {
    # Queue-related error codes not found in official HTML documentation
    "invalid_if_announce_position_enabled_report_estimated_hold_time": "This is not a Report estimated hold time type",
    "missing_if_announce_position_enabled_report_estimated_hold_time": "If announce position enabled report estimated hold time type was not provided",
}