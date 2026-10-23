#!/usr/bin/env bash
#jq '.steps[] | {step_id, timestamp, source, message, tool_calls, observation}' "$1"
#jq '.steps[] | {step_id, timestamp, source, message}' "$1"
jq '.steps[] | {step_id, message}' "$1" | sed -e 's/\\n/\n/g;'
