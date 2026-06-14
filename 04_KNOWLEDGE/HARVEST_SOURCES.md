# HARVEST SOURCES — every Figma file + asset folder the system trains on
# Librarian walks ALL active rows on "harvest all sources". Paste links — the
# file key is the string after /design/ or /board/ in the URL.

## APPROVED-FRAME RULE (how the harvester decides what to learn from)
A frame counts as APPROVED — and is ingested — when it has COMPOSED COPY + CTA on it
(real text layers: an H1 / eyebrow / CTA present on the frame). Bare scene images with
NO text layers are SKIPPED for layout+copy training (they may still be saved as scene
references). This is structural + deterministic — no reliance on a fuzzy "approved" label.
Rationale (Nick, 2026-06-14): "only the ones that already have the text, copy, and CTA
button" — the team only finishes the keepers, so composed-copy IS the approval signal.

## RS — Figma ad boards (NEW keys, 2026-06-14 — these REPLACE the old April/May/June)
| brand | figma file (name — key) | contains | naming dialect | last harvested | status |
|-------|-------------------------|----------|----------------|----------------|--------|
| RS | ADS_June_26 (Copy) — key RPpRdldT5cAxK9nFxgR0XD | live shipped ad boards (layout ground truth) | B22 scheme | never | ACTIVE |
| RS | Ads_May_26 (Copy) — key oDysBQ5SHX6GLbIrJ5XqNz | live shipped ad boards (layout ground truth) | B22 scheme | never | ACTIVE |
| RS | ADS_April_26 (Copy) — key 64AFyh5dvl6vUR5IzHpeIB | live shipped ad boards (layout ground truth) | B22 scheme | never | ACTIVE |

# SUPERSEDED (old RS ad-board keys — kept only as a record; do NOT harvest):
#   Ads_May_26  = RKALaxBpCT1nYPAb1XYI26   (→ replaced by oDysBQ5SHX6GLbIrJ5XqNz)
#   ADS_June_26 = jFpdxSDRrkog95AJKiIgvN   (→ replaced by RPpRdldT5cAxK9nFxgR0XD)
#   ADS_April_26= Z2LyHxkBaKmNHNqnXwuozD   (→ replaced by 64AFyh5dvl6vUR5IzHpeIB)

## RS — Higgsfield training folder (scene images + their prompts)
| brand | source (Higgsfield, via MCP) | contains | what to pull | last harvested | status |
|-------|------------------------------|----------|--------------|----------------|--------|
| RS | Higgsfield assets folder `(don't touch)_training` | good team-generated scene images + their prompts | download each image + capture its prompt; TAG from_scratch vs edit/ref-anchor (see HF_TRAINING_INGEST below) | never | ACTIVE |

## ARK / CACHE — forward-training (their OWN boards; RS rules never apply)
| brand | figma file (name or link/key) | contains | naming dialect | last harvested | status |
|-------|-------------------------------|----------|----------------|----------------|--------|
| ARK | [paste link] | approved ARK creative | Nick scheme | never | PENDING |
| CACHE | [paste link] | capsule creative | Nick scheme | never | PENDING |

## HF_TRAINING_INGEST — how to process the Higgsfield `(don't touch)_training` folder
For each image in the folder (via Higgsfield MCP):
1. DOWNLOAD the image → 01_BRANDS/RS/REFS/_hf_training/<id>.<ext>
2. CAPTURE its prompt (the generation prompt on the job).
3. CLASSIFY + TAG the prompt:
   - `from_scratch`  → a full scene-creation prompt ("Create a {room} with a {fixture}…",
     describes the whole scene). These feed the SCENE-PROMPT library (the composer's
     preferred source for NEW scenes).
   - `edit`/`ref-anchor` → an EDIT of a prior image or references another image
     ("the switches should follow the structure of image 2", "same scene, closer", "most
     important side is the right side"). KEEP these, but tag them — they are RETAINED as
     REF-ANCHOR EXAMPLES (Nick's canonical method: build the scene from a prompt + add the
     product via a reference image). The composer PREFERS from_scratch for new scenes and
     uses edit/ref-anchor as worked examples of the ref-anchor technique.
4. APPEND a row to 01_BRANDS/RS/KNOWLEDGE/_research/hf-training-prompts.json
   (schema: {id, image, prompt, tag, product?, notes?}). Reference-on-demand — never
   auto-loaded into the per-run token budget.
Skip duplicates by image id. Do NOT modify anything in the Higgsfield folder (read-only).
