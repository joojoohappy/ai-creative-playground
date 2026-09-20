#!/usr/bin/env bash
# HTTP contract smoke test. Unit tests cover the pipeline; this covers the six ifs in
# main.py and proves the documented status codes are the real ones.
#
#   ./test_api.sh                 # starts its own server on :8001
#   BASE=http://localhost:3000 ./test_api.sh   # through the Next.js proxy
set -uo pipefail
cd "$(dirname "$0")"

if [ -z "${BASE:-}" ]; then
  ./.venv/bin/uvicorn main:app --port 8001 >/tmp/mosaic-test-api.log 2>&1 &
  trap 'kill $! 2>/dev/null' EXIT
  BASE=http://localhost:8001
  until curl -sf "$BASE/api/health" >/dev/null 2>&1; do sleep 0.2; done
fi

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' RETURN 2>/dev/null || true
printf '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01' > "$TMP/ok.jpg"; head -c 512 /dev/urandom >> "$TMP/ok.jpg"
echo "definitely not an image" > "$TMP/fake.jpg"
{ printf '\x89PNG\r\n\x1a\n'; head -c 9000000 /dev/urandom; } > "$TMP/big.png"

pass=0; fail=0
check() { # name expected_code curl-args...
  local name=$1 want=$2; shift 2
  local got; got=$(curl -s -o /dev/null -w '%{http_code}' "$@")
  if [ "$got" = "$want" ]; then pass=$((pass+1)); printf '  ok    %-34s %s\n' "$name" "$got"
  else fail=$((fail+1)); printf '  FAIL  %-34s got %s want %s\n' "$name" "$got" "$want"; fi
}

echo "smoke: $BASE"
check "health"                200 "$BASE/api/health"
check "missing recipeId"      400 -F image=@"$TMP/ok.jpg"                        "$BASE/api/generate"
check "missing image"         400 -F recipeId=seed-01                            "$BASE/api/generate"
check "unknown recipe"        404 -F recipeId=seed-99 -F image=@"$TMP/ok.jpg"    "$BASE/api/generate"
check "text renamed .jpg"     400 -F recipeId=seed-01 -F image=@"$TMP/fake.jpg"  "$BASE/api/generate"
check "oversize upload"       400 -F recipeId=seed-01 -F image=@"$TMP/big.png"   "$BASE/api/generate"
check "bad result id"         404 "$BASE/api/results/nope"
check "path traversal"        404 "$BASE/api/results/..%2F..%2Fetc%2Fpasswd"
check "unknown result id"     404 "$BASE/api/results/00000000000000000000000000000000"
check "generate"              200 -F recipeId=seed-01 -F image=@"$TMP/ok.jpg"    "$BASE/api/generate"

RID=$(curl -s -F recipeId=seed-01 -F image=@"$TMP/ok.jpg" "$BASE/api/generate" \
      | sed -n 's/.*"resultId":"\([0-9a-f]*\)".*/\1/p')
check "fetch result"          200 "$BASE/api/results/$RID"

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
