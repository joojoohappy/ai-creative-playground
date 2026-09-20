#!/usr/bin/env bash
# Start both processes. Forgetting the backend is the dumbest and most common way to
# kill a demo. No --reload: one less moving part while presenting.
set -euo pipefail
cd "$(dirname "$0")"

uvicorn main:app --port 8000 --app-dir backend &
API=$!
trap 'kill $API 2>/dev/null || true' EXIT

until curl -sf localhost:8000/api/health >/dev/null; do sleep 0.2; done
echo "backend up on :8000"

(cd mosaic && npm run dev)
