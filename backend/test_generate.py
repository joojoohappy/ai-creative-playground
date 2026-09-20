"""The two properties the whole demo rests on.

Run:  python test_generate.py
"""

import json

from generate import (
    FALLBACK_DIR,
    _is_image,
    _read_sidecar,
    get_recipe,
    live_timeout,
    load_result,
    run_generation,
)

recipe = get_recipe("seed-01")
assert recipe is not None, "seed-01 missing from data/recipes.json"
assert get_recipe("seed-99") is None, "unknown recipe returns None, not raises"

# --- 1. No working provider still produces an honest, readable result -------------
result = run_generation(recipe, b"\xff\xd8\xff pretend jpeg")

assert result["mode"] in {"cached", "mock"}, f"expected fallback, got {result['mode']}"
assert result["sourceNote"], "a fallback with no disclosure is a lie"
assert "你這次上傳" not in result["sourceNote"], "fallback must not claim it used the user's photo"
assert result["fallbackReason"], "every non-live result must say why it isn't live"
assert result["sourcePostUrl"], "attribution must survive to the result"
assert (result["imageUrl"] is None) == (result["mode"] == "mock"), \
    "imageUrl is null exactly when mode is mock"

reloaded = load_result(result["resultId"])
assert reloaded == result, "result must survive a refresh"
assert load_result("../../etc/passwd") is None, "path traversal must not reach the filesystem"
assert load_result("nope") is None

# --- 2. Non-image bytes are rejected at both trust boundaries ---------------------
assert _is_image(b"<html>nope</html>") is None, "html is not an image"
assert _is_image(b"\xff\xd8\xffanything") == "jpg"
assert _is_image(b"\x89PNG\r\n\x1a\n...") == "png"
assert _is_image(b"RIFF1234WEBPVP8 ") == "webp"

# --- 3. A broken sidecar degrades to mock instead of raising ----------------------
FALLBACK_DIR.mkdir(parents=True, exist_ok=True)
broken = FALLBACK_DIR / "seed-99.json"
broken.write_text(json.dumps({"image": "seed-99.png", "provider": "x"}), encoding="utf-8")
assert _read_sidecar("seed-99") is None, "incomplete sidecar must not count as cached"
broken.write_text("{ not json", encoding="utf-8")
assert _read_sidecar("seed-99") is None, "corrupt sidecar must not raise"
broken.unlink()

assert 0 < live_timeout() <= 60, "timeout must be bounded"

print(f"ok — mode={result['mode']}, reason={result['fallbackReason']}, timeout={live_timeout()}s")
