#!/usr/bin/env bash
# Start both processes. Forgetting the backend is the dumbest and most common way to
# kill a demo. No --reload: one less moving part while presenting.
set -euo pipefail
cd "$(dirname "$0")"

UV=backend/.venv/bin/uvicorn
if [ ! -x "$UV" ]; then
  echo "no venv yet. run:"
  echo "  python3 -m venv backend/.venv && backend/.venv/bin/pip install -r backend/requirements.txt"
  exit 1
fi

"$UV" main:app --port 8000 --app-dir backend &
API=$!
trap 'kill $API 2>/dev/null || true' EXIT

# Bounded wait that also notices a dead process — an unbounded `until curl` loop
# spins silently forever when the backend fails to boot.
up=""
for _ in $(seq 60); do
  if curl -sf localhost:8000/api/health >/dev/null 2>&1; then up=1; break; fi
  if ! kill -0 $API 2>/dev/null; then echo "backend exited during startup (see above)"; exit 1; fi
  sleep 0.25
done
[ -n "$up" ] || { echo "backend did not answer /api/health within 15s"; exit 1; }
echo "backend up on :8000"

if [ ! -f mosaic/package.json ]; then
  echo "mosaic/ has no package.json yet — running backend only. Ctrl-C to stop."
  wait $API
fi
cd mosaic && npm run dev
