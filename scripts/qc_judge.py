#!/usr/bin/env python3
"""creative-os — independent QC judge (Gemini via OpenRouter).

Usage:
  export OPENROUTER_API_KEY=...   # NEVER store the key in any vault file (R9)
  python scripts/qc_judge.py --image 02_RUNS/<run>/img.png --brand RS \
      [--packshot path/to/packshot.png] [--model google/gemini-3.1-pro-preview]

Writes <image>.judge.json and prints the verdict. Exit 0 = PASS, 1 = FAIL, 2 = error.
Stdlib only — no pip installs needed.
"""
import argparse, base64, json, mimetypes, os, re, sys, time, urllib.request

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-3.1-pro-preview"   # verified current on OpenRouter, Jun 2026 (vision, structured output)
TIEBREAK_MODEL = "google/gemini-3.5-flash"        # updated Jun 2026: gemini-3-flash-preview superseded by 3.5-flash

SCHEMA = {
    "photorealism": "0-5", "product_fidelity": "0-5 (5 = pixel-true to packshot; <4 is a HARD FAIL)",
    "brand_fit": "0-5 vs the BRAND_ESSENTIALS checklist", "lighting_composition": "0-5",
    "ad_usability": "0-5", "hard_fails": "[] list any: warped logo/label, banned-list hit, extra text, watermark",
    "biggest_issue": "one sentence", "fix": "ONE composer field + the exact change",
    "verdict": "PASS or FAIL",
}

JUDGE_SYSTEM = """You are an independent QC judge for advertising images. You did NOT
create this image and have no stake in it passing. Score strictly.
Rules: judge ONLY what is visible. Product fidelity is judged against the attached
packshot reference if provided — any logo/label/proportion/color drift caps it at 3.
Score brand_fit ONLY against the brand checklist provided. Respond with ONLY a JSON
object matching the given schema — no prose, no markdown fences. Verdict = PASS only
if: no hard_fails AND product_fidelity >= 4 AND mean of the five scores >= 4.5."""


def img_part(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    data = base64.b64encode(open(path, "rb").read()).decode()
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}}


def load_brand_essentials(brand):
    card = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "01_BRANDS", brand.upper(), "BRAND_CARD.md")
    if not os.path.exists(card):
        sys.exit(f"error: brand card not found: {card}")
    txt = open(card, encoding="utf-8").read()
    m = re.search(r"BRAND_ESSENTIALS.*?(?=\nDEEP_REFERENCE|\Z)", txt, re.S)
    banned = re.search(r"BANNED.*?(?=\n\n|\nVISUAL|\nBRAND_ESSENTIALS)", txt, re.S)
    return (m.group(0) if m else txt[:1200]) + "\n" + (banned.group(0) if banned else "")


def call(model, messages, key, retries=3):
    body = json.dumps({"model": model, "messages": messages, "temperature": 0,
                       "max_tokens": 4000}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "X-Title": "creative-os-qc"})
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)["choices"][0]["message"]["content"]
        except Exception as e:
            if i == retries - 1:
                sys.exit(f"error: judge API failed after {retries} tries: {e}")
            time.sleep(2 ** (i + 1))


def parse_json(text):
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            return json.loads(m.group(0))
        sys.exit(f"error: judge returned non-JSON: {text[:300]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--brand", required=True, choices=["ARK", "CACHE", "RS", "ark", "cache", "rs"])
    ap.add_argument("--packshot", default=None)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    a = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("error: set OPENROUTER_API_KEY env var (never store it in the vault)")

    content = [{"type": "text", "text":
                "BRAND CHECKLIST + BANNED LIST:\n" + load_brand_essentials(a.brand) +
                "\n\nOUTPUT SCHEMA (respond with exactly this JSON shape):\n" +
                json.dumps(SCHEMA, indent=1)},
               {"type": "text", "text": "IMAGE UNDER REVIEW:"}, img_part(a.image)]
    if a.packshot:
        content += [{"type": "text", "text": "PACKSHOT REFERENCE (judge product fidelity against this):"},
                    img_part(a.packshot)]
    else:
        content.append({"type": "text", "text":
                        "No packshot provided — score product_fidelity 5 only if no product "
                        "is present (background mode); otherwise cap at 3 and note it."})

    verdict = parse_json(call(a.model, [
        {"role": "system", "content": JUDGE_SYSTEM},
        {"role": "user", "content": content}], key))

    scores = [verdict.get(k, 0) for k in
              ("photorealism", "product_fidelity", "brand_fit", "lighting_composition", "ad_usability")]
    verdict["total"] = round(sum(scores) / 5, 1)
    verdict["model"] = a.model
    # enforce verdict rules locally — never trust the model's own PASS alone
    ok = (not verdict.get("hard_fails")) and verdict.get("product_fidelity", 0) >= 4 and verdict["total"] >= 4.5
    verdict["verdict"] = "PASS" if ok else "FAIL"

    out = a.image + ".judge.json"
    json.dump(verdict, open(out, "w"), indent=1)
    print(json.dumps(verdict, indent=1))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
