"""MOSAIC backend — three routes and a static mount. That is the whole HTTP layer.

Run:  uvicorn main:app --port 8000     (no --reload for a demo: one less variable)

No CORS middleware, deliberately. Person 1's next.config.js proxies /api/* and
/static/* here, so the browser only ever talks to localhost:3000.

Routes are `def`, not `async def`. Starlette runs sync routes in a threadpool, so a
blocking 40-second provider SDK call cannot freeze the event loop — /api/health stays
responsive while a generation is in flight, which is exactly the Checkpoint 1 test.
"""

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from generate import (
    FALLBACK_DIR,
    MAX_BYTES,
    RESULTS_DIR,
    STORAGE,
    _is_image,
    get_recipe,
    load_result,
    run_generation,
)

app = FastAPI(title="MOSAIC backend")

for d in (STORAGE, FALLBACK_DIR, RESULTS_DIR):
    d.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STORAGE), name="static")


def _err(code: int, error: str) -> JSONResponse:
    return JSONResponse({"error": error}, status_code=code)


@app.get("/api/health")
def health():
    # Two lines that tell Person 1 "backend is down" instead of a generic error.
    return {"ok": True}


@app.post("/api/generate")
def generate(
    # Both default to None so a missing field is our own 400, not FastAPI's 422.
    # The documented contract says 400; the code has to actually return 400.
    recipeId: str | None = Form(None),  # noqa: N803 - wire contract is camelCase
    image: UploadFile | None = File(None),
):
    if not recipeId:
        return _err(400, "missing_recipe_id")

    # recipeId in, prompt out. The client never supplies prompt text, or the API key
    # becomes a free image generator for anyone who opens devtools.
    recipe = get_recipe(recipeId)
    if recipe is None:
        return _err(404, "unknown_recipe")

    if image is None:
        return _err(400, "missing_image")

    # Read one byte past the limit: enough to know it's too large, without pulling an
    # unbounded upload into memory.
    data = image.file.read(MAX_BYTES + 1)
    if not data:
        return _err(400, "missing_image")
    if len(data) > MAX_BYTES:
        return _err(400, "too_large")
    if _is_image(data) is None:
        return _err(400, "unsupported_type")

    return {"resultId": run_generation(recipe, data)["resultId"]}


@app.get("/api/results/{result_id}")
def read_result(result_id: str):
    # load_result rejects anything that isn't 32 hex chars before touching a path.
    result = load_result(result_id)
    return result if result is not None else _err(404, "unknown_result")
