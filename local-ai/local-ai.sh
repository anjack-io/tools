#!/usr/bin/env bash

set -euo pipefail

OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
MODEL="${MODEL:-gemma3:27b}"
PROMPT="${1:-Tell me a joke about Linux shells.}"

full=""
curl -sN "$OLLAMA_URL/api/generate" \
  -d "$(jq -nc --arg m "$MODEL" --arg p "$PROMPT" '{model:$m, prompt:$p}')" |
while IFS= read -r line; do
  # Print tokens as they arrive
  piece=$(jq -r '.response // empty' <<<"$line")
  printf "%s" "$piece"

  # Also accumulate for a future need
  full+="$piece"

  # When stream ends, we get done=true
  if jq -e '.done == true' >/dev/null <<<"$line"; then
    echo
    echo
    echo "++++++++++++++++++++++++++++++++++++++++"
    echo "             ---- stats ----            "
    echo "++++++++++++++++++++++++++++++++++++++++"
    jq -r '"reason: \(.done_reason)  prompt_tokens: \(.prompt_eval_count)  completion_tokens: \(.eval_count)"' <<<"$line"
  fi
done

