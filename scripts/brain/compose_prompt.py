#!/usr/bin/env python3
"""Compose an on-brand RS lifestyle ad prompt for ANY product.

Implements 04_KNOWLEDGE/scene-grammar.md mechanically: product TYPE -> accurate placement, + the
on-brand SCENE (neutral plaster shell + ONE rationed jewel accent carried on material-bound contents + warm/cool tension + textures +
statement art + golden-hour/moody light + film grain) from the color-texture playbook. Deterministic
per --seed so one product yields a repeatable, varied creative pack.

Usage:
  python scripts/compose_prompt.py --product "Aerlis Chandelier" --type chandelier --aspect 4:5 --seed 1
  python scripts/compose_prompt.py --product "Aine Wall Lamp" --type sconce --archetype bedroom --light night
Then:
  python scripts/generate.py --ref packshot.png --prompt "$(python scripts/compose_prompt.py ...)"
"""
from __future__ import annotations
import argparse, hashlib

# --- product type -> placement + role + valid archetypes (Part A) ---
TYPE = {
    "chandelier":   ("hung from the ceiling, centered above the table",       "the overhead hero",   ["dining", "foyer", "stairwell"]),
    "pendant":      ("hung over the table / island",                          "the overhead hero",   ["dining", "kitchen", "nook"]),
    "sconce":       ("mounted on the wall as a matched pair flanking the artwork/mirror", "wall accents", ["bedroom", "hallway", "bathroom", "living"]),
    "wall_lamp":    ("mounted on the wall beside the artwork",                "a wall accent",       ["bedroom", "hallway", "living"]),
    "picture_light":("mounted on the frame above a large artwork",           "the art accent",      ["living", "hallway", "study"]),
    "table_lamp":   ("set on the console / nightstand",                       "a surface accent",    ["living", "bedroom", "entry"]),
    "floor_lamp":   ("standing in the corner beside the seating",            "a floor accent",      ["living", "reading"]),
    "flush":        ("mounted flat to the ceiling",                           "the overhead ambient light", ["hallway", "bedroom", "kitchen"]),
    "ceiling_light":("mounted to the ceiling",                                "the overhead light",  ["hallway", "bedroom", "kitchen"]),
    "knob":         ("installed on the cabinet drawer front, in tight close-up", "the razor-sharp detail hero", ["cabinetry"]),
    "pull":         ("installed on the cabinet/door front, in tight close-up","the razor-sharp detail hero", ["cabinetry"]),
    "handle":       ("installed on the door/drawer, in tight close-up",       "the razor-sharp detail hero", ["cabinetry"]),
    "mirror":       ("mounted on the wall above the vanity/console",          "the wall hero",       ["bathroom", "entry"]),
    "sofa":         ("placed on the floor as the main seating",               "the room hero",       ["living"]),
    "chair":        ("placed in the room",                                    "the seating hero",    ["living", "reading"]),
    "outdoor":      ("mounted on the exterior wall",                          "an outdoor accent",   ["patio", "garden"]),
    "unknown":      ("placed correctly in the vignette",                      "the accent",          ["living", "entry", "bedroom"]),
}

# --- archetype -> setting + supporting props (Part C). {anchor} = color only; material spelled per slot ---
ARCH = {
    "bedroom":   "a sophisticated bedroom: a bed with a {anchor} velvet upholstered headboard, crisp linen, {art} above it, a matching nightstand on EACH side of the bed (one per side), floor-length drapery aligned to its window",
    "living":    "an elegant living room: a {anchor} velvet sofa, {art}, a walnut coffee table with a brass tray",
    "dining":    "a refined dining room: a walnut table with a MATCHING set of identical dining chairs upholstered in {anchor} velvet (one cohesive set, never mixed or mismatched), {art}, a window with a soft view",
    "kitchen":   "a warm kitchen: a stone-topped island, walnut cabinetry, {anchor} leather bar stools, brass fixtures, a cooking range with exactly FOUR control knobs (never more)",
    "nook":      "a cozy breakfast nook: a round walnut table, a {anchor} velvet bench, {art}, a bright window",
    "hallway":   "an elegant hallway: a walnut console, {art}, a {anchor} wool runner rug, an arched doorway to a sunlit room",
    "entry":     "a welcoming entry: a console, {art}, a {anchor} wool runner, a ceramic vase with branches",
    "bathroom":  "a believable, properly-scaled powder room: warm plaster upper walls BROKEN UP by a half-height handmade zellige tile wainscot (or a tiled feature wall behind the vanity) and a differentiated ceiling, a dark forest-green marble vanity over reeded walnut, an arched mirror, a brass towel bar mounted ABOVE the wainscot on the plaster and clear of the sink with {anchor} linen towels, a framed statement painting filling the empty plaster wall, a single contrasting-color rose in a slim vase placed away from the towels, a patterned cement-tile floor; a small frosted/clerestory window (never full-length glass); no tonal/blend-in props",
    "study":     "a moody study: a walnut desk, a {anchor} leather chair, a wall of books, {art}",
    "reading":   "a reading corner: a {anchor} velvet armchair, a bookshelf, a trailing plant",
    "foyer":     "a grand foyer: a sweeping staircase with a patterned runner, an arched window, paired {anchor} velvet benches, a large vibrant statement painting, a colored-stone or checkerboard floor; plaster shell dominant, one rationed jewel accent",
    "stairwell": "a dramatic stairwell: a double-height plaster wall, an arched window, a {anchor} wool runner on the stairs",
    "cabinetry": "a tight close-up of a {anchor}-lacquer cabinet with a honed marble top and aged brass hardware, shallow depth of field",
    "patio":     "a sunlit garden patio: weathered teak furniture with {anchor} cushions, lush greenery, terracotta pots, soft string lights",
    "garden":    "a lush garden terrace: a stone wall, {anchor} outdoor seating, greenery, golden light",
}

# color anchor — GREEN-FIRST per the approved corpus (green is the modal jewel accent), then oxblood/rust/navy.
# 2nd value is a vestigial cool-note (used only by editorial-bold / door); the default lane rations ONE accent.
PALETTES = [
    ("olive green",     "warm brass and ochre accents"),
    ("forest green",    "walnut wood and a warm gold-leaf accent"),
    ("sage green",      "aged brass and cream linen"),
    ("oxblood",         "a deep blue-green landscape painting"),
    ("rust terracotta", "deep navy textiles"),
    ("deep navy",       "a warm gold-leaf abstract canvas"),
]
ART = ["a large moody blue-green landscape in a gilt frame", "a bold gold-leaf abstract canvas",
       "a vibrant figurative painting", "an arched antique foxed mirror", "a textured ochre abstract in a brass frame"]
TEXTURES = ["velvet pile", "reeded fluted wood", "veined honed stone", "harlequin checkerboard tile",
            "handwoven wool rug", "trowelled lime plaster", "aged leather", "brass patina"]
LIGHT = {
    "golden":   "warm low golden-hour sun through sheer curtains casting soft window-pane shadows across the plaster",
    "night":    "low-key moody evening light, lamps and fixtures glowing warm, deep rich shadows",
    "daylight": "soft bright north-window daylight, airy but warm",
    "twilight": "dusk; the fixture's warm amber glow fills and DOMINATES the center of the frame, with cool blue-grey only at the edges, corners and windows; deep shadows — never an overall blue cast",
}

# --- VALUE/TIER invariant (Denys rule): the product is ALWAYS the least expensive object in the room ---
TIER = ("This is an affluent, professionally designed home where the {product} is the LEAST expensive object in "
        "the frame: surround it with even more valuable things — designer and antique furniture, original framed "
        "art, genuine stone and solid hardwood, layered high-end textiles, collected decor — in a substantial, "
        "architecturally considered room. The {product} stays the lit styled hero, but everything around it reads "
        "as higher-end; never a cheap, budget, low-income, sparse, or empty interior.")

# --- SCALE/PROPORTION realism per type: believable size, ceiling height, mounting/hang height ---
SCALE = {
    "chandelier":    "Scale & placement: a large, generously proportioned room with a TALL ceiling (double-height or at least ~11 ft); hang it high and centered, well above head height (~30-36 in above the tabletop), in correct proportion to the big room — never oversized for the space, never near the floor.",
    "pendant":       "Scale & placement: ample ceiling height; hang ~30-36 in above the island/table surface, proportioned to the room.",
    "sconce":        "Scale & placement: mount at ~62-66 in on a substantial wall, sized correctly to the wall and adjacent furniture.",
    "wall_lamp":     "Scale & placement: mount at ~62-66 in on a substantial wall, correctly scaled.",
    "picture_light": "Scale & placement: mount on/just above the artwork, scaled to the frame.",
    "table_lamp":    "Scale & placement: on a substantial console/nightstand at believable table-lamp scale.",
    "floor_lamp":    "Scale & placement: believable floor-lamp height beside the seating.",
    "flush":         "Scale & placement: flat to a ceiling of believable height, scaled to the room.",
    "ceiling_light": "Scale & placement: to a ceiling of believable height, scaled to the room.",
    "mirror":        "Scale & placement: mounted at correct height over the vanity/console, scaled to the wall.",
}
SCALE_DEFAULT = "Scale & placement: size and position the product believably for a generously proportioned room."

# Global STAGING realism (appended to every scene) — plausibility rules distilled from human review feedback.
STAGING = ("Staging must be realistic and plausible: furniture placed sensibly (exactly ONE nightstand per side of a "
           "bed, never two on one side), dining and seating chairs are a MATCHING set (never mixed or mismatched), "
           "window drapery hung on its own window and aligned to it on a STRAIGHT horizontal rod (never an arched or curved rod), any throw blanket is chunky wool or linen and "
           "NEVER leather, walls and ceilings are plausible architectural surfaces (plaster, paint, wood, tile, stone or wallpaper) and NEVER felt or other non-architectural coverings, cooking ranges have exactly four control knobs and a range hood/extractor above them, kitchen/dining art is a food or fruit "
           "still-life, decor is contemporary (at most ONE clock, modern style — no antique 'old-timey' clocks), the "
           "ONLY branded light fixture in the scene is the hero product (no other-brand or random extra lamps/sconces "
           "— omit them), light transitions smoothly from window to shadow with no harsh gap, no duplicated or "
           "nonsensical objects, no mangled text or signage.")

# Food/fruit still-life art for kitchen/dining/nook (overrides the generic ART pick).
FOOD_ART = "a framed food or fruit still-life painting (kitchen/dining art is food or fruit, never figurative or landscape)"

# THE #1 approved premium signal (549-frame corpus + team feedback): the fixture lights itself.
ONSTATE = ("The {product} is switched ON, glowing warm ~2700K as the brightest point in the frame and casting a soft "
           "visible pool of light on the adjacent wall/surface.")

# --- STYLE presets: the look lane. Invariants (TIER + SCALE + product accuracy) apply to ALL styles ---
STYLES = {
    "editorial": {
        "descriptor": "a high-end interiors editorial photograph",
        "shell": ("Warm shell, NEVER pale flat beige: a deeper, moodier warm plaster OR a treated wall (wood paneling, "
                  "handmade zellige/tile, or a colored feature wall) so the background reads rich and characterful, never "
                  "bland or washed-out; warm, never cool-white."),
        "color": ("Commit to ONE confident jewel color FAMILY (GREEN first — emerald/forest/olive, then oxblood/burgundy, "
                  "deep teal, terracotta) in {anchor} and deploy it GENEROUSLY across material-rich surfaces: colored "
                  "marble + cabinetry/tile, or velvet seating + a patterned rug, against brass + walnut. Saturated and "
                  "PRESENT within that one family — rich, never timid or beige; disciplined to a single scheme, never a "
                  "chaotic multi-color mix."),
        "light_default": "golden",
        "finish": "warm, rich, slightly moody low-key grade, soft light, soft shadows, subtle 35mm film grain, editorial and realistic.",
    },
    "editorial-bold": {
        "descriptor": "a high-end interiors editorial photograph",
        "shell": ("Warm limewash plaster walls in a deeper, moodier tone, kept recessive and broken up (wood paneling, "
                  "tile, large art, or drapery)."),
        "color": ("Richer material-bound color: {anchor} upholstery + a colored rug + a statement artwork against aged "
                  "brass, walnut and stone — bolder than the default, but still anchored on a warm-neutral shell (the "
                  "rare Denys bold lane, not the approved baseline)."),
        "light_default": "golden",
        "finish": "soft light, soft shadows, subtle 35mm film grain, editorial and realistic.",
    },
    "cinematic-twilight": {
        "descriptor": "a cinematic fine-art interiors photograph at twilight, in the spirit of Todd Hido and Gregory Crewdson",
        "shell": ("The substantial plaster or wood-paneled walls and ceiling stay dim and recessive; the architecture "
                  "reads refined and high-end even in shadow."),
        "color": ("Heavily desaturated, faded-film color. The {product} glows warm from within and its warm amber light "
                  "DOMINATES the center of the frame, washing the scene warm; the cool blue-grey gloom is confined to the "
                  "EDGES, corners and windows only — warm center, cool periphery, NEVER an overall blue cast. ONE "
                  "restrained jewel accent in {anchor} (upholstery or a feature wall) emerges softly from shadow — "
                  "refined and sparse, NOT empty or cheap."),
        "light_default": "twilight",
        "finish": "atmospheric haze, a gentle halation bloom around the fixture, pronounced 35mm film grain, soft focus, editorial and realistic.",
    },
}
# Optional per-product FIDELITY notes — distinctive design cues appended to the preservation clause when
# the generic packshot ref isn't enough (model simplifies a signature detail). Keyed by lowercase substring
# of the product name. Add an entry whenever a product drifts in generation.
PRODUCT_NOTES = {
    "lugna":   "a round disc wall sconce with a softly swirled, rippled translucent alabaster face in cream and pale gold, a slim brushed-gold rim, and a warm glowing center — keep the swirled marbled face pattern and the clean round gold rim; do NOT flatten it into a plain disc",
    "teva":    "graduated SLIM, low-profile alabaster rings (thin flat cross-section), large-to-small, on a brushed-brass canopy with fine cables — keep the rings slim, never chunky",
    "carissa": "a single amber/cognac ribbed glass globe pendant on a thin cord with a small brass canopy — keep the amber ribbed glass sphere",
}

# Lit product types (for "keep the ... turned on") + Higgsfield team EDIT-style variations off a ref
LIT = {"chandelier", "pendant", "sconce", "wall_lamp", "picture_light", "table_lamp",
       "floor_lamp", "flush", "ceiling_light", "outdoor"}
EDIT_VARIATIONS = {
    "closer":  "make a closer image of the {p} in the scene. {lens}. editorial style. no blurry background. {ctrl}",
    "closeup": "make a editorial close up shot of the {p}. same scene, different angle. product shot. editorial and realistic. {lens}. no blurry background.",
    "angle":   "same scene, a different angle on the {p}. editorial and realistic. {lens}. no blurry background. {ctrl}",
    "wide":    "pull back to a wider editorial shot of the whole room featuring the {p}. editorial and realistic. {lens}. no blurry background. {ctrl}",
    "relight": "have direct morning sun come through the window, no dust no glow. editorial and realistic. more contrast, more shadows.{lit} {lens}.",
    "night":   "make it night time, warm ambient mood, editorial and realistic. more contrast, more shadows.{lit} {lens}.",
}
ASPECT_WORD = {"4:5": "4:5 vertical", "9:16": "9:16 vertical", "1:1": "1:1 square", "16:9": "16:9 horizontal"}

# --- door hardware (lever/knob shown as a DOOR IN A ROOM) ---
DOOR_TYPES = {"door", "door_handle", "door_lever"}
DOOR_COLOURS = {  # on-brand painted-door colour per room — warm/cool variety across a set
    "bathroom": "deep charcoal-green", "hallway": "olive-green", "kitchen": "slate-blue",
    "bedroom": "warm greige", "entry": "clay-terracotta", "foyer": "clay-terracotta",
    "living": "deep olive-green", "study": "deep forest-green", "dining": "muted teal",
}


def pick(seq, seed, salt):
    h = int(hashlib.md5(f"{seed}-{salt}".encode()).hexdigest(), 16)
    return seq[h % len(seq)]


# --- Higgsfield Reference Element injection (product-fidelity path) ---------------------
# When an --element <id> is supplied, the Higgsfield backend (MCP generate_image, model
# nano_banana_pro) auto-injects that element's reference image and rewrites the literal
# token `<<<id>>>` -> `@element_name`. So we (a) embed the `<<<id>>>` token into the
# product/hero clause and (b) PREPEND an EMPHATIC finish+gang directive — the element
# defaults to a darker finish unless the finish/gang is stated forcefully.
# Source of the contract: Higgsfield MCP show_reference_elements docs + the RS-Brass-Dimmer-1
# bake-off (Pro + exact-variant packshot 2nd ref matches ref-injection fidelity).
# NOTE: this wrapper is applied ONLY when --element is set; with no --element the composer
# output is byte-identical to before (the wrapper is never invoked).

def element_directive(finish, gang):
    """The EMPHATIC finish+gang directive prepended when --element is set. Stated forcefully
    (finish UPPER-CASED) because the element otherwise defaults to a darker finish
    (patina/bronze/black). The finish is emitted verbatim so callers control the exact wording
    (e.g. finish='bright polished satin brass' -> 'in a BRIGHT POLISHED SATIN BRASS finish ...')."""
    return (f"in a {finish.upper()} finish (NOT dark/patina/bronze/black), {gang}")


def apply_element(prompt, product, element_id, finish, gang):
    """Wrap a composed prompt for Higgsfield Reference Element generation.

    Prepends the emphatic finish+gang directive AND embeds the literal `<<<element_id>>>`
    token next to the product in the hero clause (the backend resolves the token to the
    element's reference image). Returns the wrapped prompt. Called ONLY when --element is set.
    """
    directive = element_directive(finish, gang)
    # (a) emphatic finish+gang directive up front, naming the product + embedding the token so
    #     the element's reference image is conditioned on the correct bright finish from the start.
    head = (f"The {product} <<<{element_id}>>> {directive}. ")
    # (b) re-assert the token + finish at the EXACT-product preservation tail so fidelity holds.
    tail = (f" The {product} <<<{element_id}>>> must render {directive} — keep it that exact "
            f"bright finish, never a darker patina/bronze/black variant.")
    return head + prompt + tail


def compose(product, ptype, archetype=None, palette=None, light=None, aspect="4:5", seed=0, style="editorial", note=None, dims=None):
    placement, role, archs = TYPE.get(ptype, TYPE["unknown"])
    arch = archetype or pick(archs, seed, "arch")
    setting_t = ARCH.get(arch, ARCH["living"])
    anchor, cool = PALETTES[palette] if isinstance(palette, int) else pick(PALETTES, seed, "pal")
    art = FOOD_ART if arch in ("kitchen", "dining", "nook") else pick(ART, seed, "art")
    setting = setting_t.format(anchor=anchor, art=art)
    tex = ", ".join(dict.fromkeys(pick(TEXTURES, seed, f"t{i}") for i in range(2)))  # curated-minimal: 2 textures
    st = STYLES.get(style, STYLES["editorial"])
    lt = LIGHT.get(light or st["light_default"], LIGHT["golden"])
    scale = SCALE.get(ptype, SCALE_DEFAULT)
    on = (ONSTATE.format(product=product) + " ") if ptype in LIT else ""
    dimc = (f"The {product} measures {dims}; size it true-to-scale against the furniture anchor below it — do not oversize. ") if dims else ""
    tier = TIER.format(product=product)
    shell = st["shell"]
    color = st["color"].format(anchor=anchor, cool=cool, product=product)

    p = (
        f"Photorealistic {st['descriptor']}, {ASPECT_WORD.get(aspect, aspect)}, full-bleed, edge to edge "
        f"(no borders or blank margins). Eye-level, straight-on, 50mm, verticals plumb. Scene: {setting}. {shell} "
        f"The {product} is {placement}, as {role}. {on}{scale} {dimc}{tier} "
        f"{color} A few tactile textures ({tex}); curated-minimal styling with generous negative copy space on one side "
        f"and a believability cue (a cropped piece of furniture at the frame edge, floor-length drapery on its own "
        f"window). Lighting: {lt}; {st['finish']} {STAGING} Output: {aspect}. "
        f"Exclusions: no AI / render / CGI / pasted-or-floating look (integrate the product into the scene's light and "
        f"perspective), no fake diffuse 'commercial' beam, no cool/blue or flat midday light, no all-beige / washed-out / "
        f"bland scene (the shell must be warm and rich, not pale), no chaotic multi-color clash (commit to ONE jewel "
        f"family), no cheap / empty / sterile room, no cramped space or low ceiling, no fixture too low or oversized, no mixed chair sets, no two "
        f"nightstands on one side, no leather throw blankets, no antique or duplicated clocks, no other-brand or extra "
        f"light fixtures, no AI-tell props (generic perfumes, fake books, deformed cutlery, fake flowers), no tonal "
        f"camouflaged props, no European outlets/switches, no mangled text or signage, no people or faces, no distorted "
        f"logos or warped/duplicated product. "
        f"Use the attached product photo as the EXACT {product}. Do NOT change its shape, design, finish, materials, "
        f"color, or proportions. Match its lighting and color temperature to the scene."
    )
    note = note or next((v for k, v in PRODUCT_NOTES.items() if k in product.lower()), None)
    if note:
        p += f" Distinctive design of the {product} to preserve exactly: {note}."
    return p


def compose_edit(product, ptype, variation="closer", lens=None, seed=0):
    """Short Higgsfield-team-style EDIT prompt to iterate a variation off a ref image
    (their method: closer / macro / different angle / relight). See 04_KNOWLEDGE/higgsfield-team-prompts.md."""
    lens = lens or ("70mm camera lens" if variation == "closeup" else "50mm camera lens")
    lit = f" keep the {product} turned on." if ptype in LIT else ""
    ctrl = "no dust no glow. more contrast, more shadows."
    t = EDIT_VARIATIONS.get(variation, EDIT_VARIATIONS["closer"])
    return t.format(p=product, lens=lens, ctrl=ctrl, lit=lit).strip()


# Higgsfield team MASTER TEMPLATE (their #1 pattern from the 8,056-prompt corpus) — ref-driven base scene.
FIXTURE_WORD = {
    "chandelier": "chandelier", "pendant": "pendant lamp", "sconce": "wall lamp", "wall_lamp": "wall lamp",
    "table_lamp": "table lamp", "floor_lamp": "floor lamp", "flush": "ceiling light", "ceiling_light": "ceiling light",
    "picture_light": "picture light", "mirror": "mirror", "sofa": "sofa", "chair": "armchair", "outdoor": "outdoor light",
}


def compose_refroom(room, ptype, bold=False):
    """The team's REAL master template (corpus #1 pattern): short, ref-anchored, soft/editorial. This is the
    PRIMARY path when an approved frame ref exists. --bold = the rare richer lane."""
    fx = FIXTURE_WORD.get(ptype, ptype.replace("_", " ") if ptype != "unknown" else "light fixture")
    p = f"Create a {room} with a {fx} inspired by these references design. soft light, soft shadows. editorial and realistic"
    if ptype in LIT:
        p += f". keep the {fx} turned on, glowing warm"
    if bold:
        p += (". warm-neutral plaster shell stays dominant with ONE jewel accent (olive/forest green, or oxblood) on "
              "brass + walnut, subtle film grain. no all-beige, no busy/over-colored scene, no flat light, no people")
    return p


def compose_door(product, archetype=None, door_colour=None, palette=None, light="golden", aspect="4:5", seed=0):
    """Door hardware (lever/knob) as a DOOR IN A ROOM — the validated door-as-object recipe.
    Reuses the ARCH scene block + bold-contents/texture rules, wrapped so the PANELLED door reads as a
    door (not a wall): wood texture, brass latch + keyhole, plain edges, 3/4 angle, furnished room behind.
    See 01_PROMPTS/winning/2026-06-05-door-hardware-door-in-room.md."""
    arch = archetype or pick(["hallway", "bathroom", "kitchen", "bedroom", "entry"], seed, "darch")
    anchor, cool = PALETTES[palette] if isinstance(palette, int) else pick(PALETTES, seed, "pal")
    setting = ARCH.get(arch, ARCH["hallway"]).format(anchor=anchor, art=pick(ART, seed, "art"))
    tex = ", ".join(dict.fromkeys(pick(TEXTURES, seed, f"t{i}") for i in range(3)))
    lt = LIGHT.get(light, LIGHT["golden"])
    dc = door_colour or DOOR_COLOURS.get(arch, "deep olive-green")
    return (
        f"Editorial interior-design advertising photograph, {ASPECT_WORD.get(aspect, aspect)}, full-bleed, "
        f"three-quarter angle. Foreground hero: a tall PANELLED interior door — Shaker style with square "
        f"stiles and rails framing two recessed flat panels and subtle painted wood texture, so it is "
        f"unmistakably a DOOR and never a flat wall — finished in {dc} limewash, standing slightly ajar. Its "
        f"near vertical EDGE and the door JAMB are clearly visible; on the latch edge a brushed-brass latch "
        f"tongue and strike plate show. Plain square door edges, no crown molding or decorative trim. Mounted "
        f"at lever height: the {product} as the crisp lit hero, with a small matching brass keyhole escutcheon "
        f"just below it. Through and just beyond the ajar door, the room: {setting}. Walls and ceiling are warm "
        f"limewash plaster in a DEEPER, moodier tone, kept recessive and broken up so the background never "
        f"overpowers. Bold material-bound color: {anchor} with {cool} for warm/cool tension; aged brass, "
        f"walnut, leathered stone. Rich tactile textures: {tex}. Keep the warm-neutral plaster shell DOMINANT "
        f"(~70%) with ONE rationed {anchor} accent (upholstery OR rug OR art, not all three) on brass + walnut. "
        f"Lighting: {lt}; subtle 35mm film grain. Generous negative copy space upper-left. "
        f"{TIER.format(product=product)} "
        f"Exclusions: no all-beige or monochrome, no flat wall-looking door, no large empty plaster, no "
        f"mismatched furniture, no random nonsensical props, no flat even lighting, no people, no extra text, "
        f"no CGI look. "
        f"PRESERVE THE PRODUCT EXACTLY as in the attached reference image — do not change the lever shape, the "
        f"diagonal knurl, the proportions, the round rose, or the satin-brass finish; the reference is the "
        f"ground truth for the hardware."
    )


# --- wall hardware: brass dimmer / toggle switch / outlet (a WALL DETAIL — macro or half-room) ---
SWITCH_TYPES = {"switch", "dimmer", "outlet", "toggle"}
DIMMER_DESC = ("the brass dimmer switch — a solid satin/brushed-brass rectangular wall plate with a recessed inner "
               "panel, two slotted brass screws (top and bottom), and a small round brass dimmer knob centered low "
               "(warm brass, smooth)")


def compose_switch(product, room="living", shot="half", palette=None, light=None, aspect="4:5", seed=0, desc=None, preserve=None):
    """Brass dimmer / toggle switch as a WALL DETAIL. shot = macro (tight close-up) | half (medium half-room).
    Realigned RICH aesthetic; the dimmer controls a warm GLOWING fixture in-scene. Anchor to the packshot --ref."""
    anchor, _ = PALETTES[palette] if isinstance(palette, int) else pick(PALETTES, seed, "pal")
    setting = ARCH.get(room, ARCH["living"]).format(anchor=anchor, art=(FOOD_ART if room in ("kitchen", "dining", "nook") else pick(ART, seed, "art")))
    d = desc or DIMMER_DESC
    grade = ("ultra high-resolution commercial product PHOTOGRAPH (not a 3D render, not CGI, not illustration), shot on a "
             "full-frame DSLR with natural directional light, true-to-life materials and micro-texture, subtle 35mm film "
             "grain; warm, rich, slightly moody low-key editorial grade, soft light, soft shadows")
    material = ("Brass + studio lighting: warm brushed-satin gold-brass (never chrome/silver/plastic), lit by ONE large "
                "soft key (window or softbox) raking ~25 degrees to reveal the brushed grain, a single clean specular "
                "along the top edge, gentle fill; no multiple hotspots, no blown/clipped highlights, no mirror reflections "
                "of the room or camera.")
    excl = ("no AI/render/CGI/pasted look, no cool/blue or flat light, no pale/washed-out bland wall, no chaotic "
            "multi-color clash, no felt or other non-architectural wall covering, no extra or duplicate switch plates, no European sockets/switches, no oversized or "
            "giant switch plate (it is a small palm-sized plate), no front-facing plate on a wall angled to the camera "
            "(the plate must match the wall's perspective), no oversized crystal chandelier in a small or utility room, "
            "no mangled text, no people")
    preserve = preserve or (f"Use the attached product photo as the EXACT {product}: preserve the satin-brass plate, the recessed "
                f"panel, the two screws and the round dimmer knob; do not alter its design, finish, or proportions.")
    size = ("It is a SMALL single-gang wall plate — only ~2.75 in / 7 cm wide and ~4.5 in / 11 cm tall, about the width "
            "of a hand; size it true-to-scale against the door frame and furniture (a standard doorway is ~32-36 in wide, "
            "so the plate spans only about one-twelfth of it), never oversized or comically large.")
    geom = ("The plate lies flat and flush against its wall, sharing that wall's exact perspective plane — if the wall "
            "recedes at an angle to the camera the plate foreshortens with it; never a front-facing plate on an angled wall.")
    fixture = (f"The warm glowing fixture the dimmer controls is appropriate to the {room} (a sconce, pendant, or simple "
               f"flush mount — never an oversized crystal chandelier in a small or utility room).")
    # AD-COPY COMPOSITION: force a large, deliberately-empty zone OPPOSITE the product so the headline has
    # real estate. Scenes that fill both sides leave nowhere clean for text (the 5/10 placement problem).
    copyzone = ("AD-COPY COMPOSITION (critical): keep the dimmer and all furniture, art and fixtures to ONE side "
                "(or the lower third), and leave the OPPOSITE ~45% of the frame as a single LARGE, calm, deliberately "
                "EMPTY expanse — one uninterrupted plane of plain wall, or soft single-tone out-of-focus bokeh, with "
                "NOTHING on it (no art, furniture, windows, fixtures or props). That clean band is reserved negative "
                "space for headline text and must read as intentional.")
    excl = excl + (", no art/furniture/windows/props intruding into the reserved empty copy-zone side, no centered or "
                   "symmetric clutter that leaves nowhere clean for text, no 3D-render/octane/unreal/CGI look, no "
                   "hyper-glossy plastic sheen, no chrome or silver drift on the brass")
    if shot == "macro":
        return (
            f"Photorealistic editorial MACRO close-up, {ASPECT_WORD.get(aspect, aspect)}, full-bleed edge to edge. "
            f"Hero, razor-sharp and in focus: {d}, mounted flush on a rich {room} wall; crisp brass detail, intimate "
            f"close-up, shallow depth of field. {geom} The foreground wall plane reads at a distinctly different "
            f"value/material from the softer background so the brass plate pops (clear tonal separation, not the same "
            f"flat color). Behind it, soft warm bokeh of a {room} in the RS rich aesthetic — a deeper warm {anchor} "
            f"jewel-toned wall, brass + walnut, a warm GLOWING fixture out of focus (the dimmer controls it). {material} {copyzone} "
            f"{grade}. Eye-level, straight-on, 70mm. {preserve} "
            f"Exclusions: {excl}."
        )
    return (
        f"Photorealistic editorial HALF-ROOM shot, {ASPECT_WORD.get(aspect, aspect)}, full-bleed edge to edge. "
        f"Foreground, crisp, in focus and PROMINENT — large and close, clearly the subject filling a meaningful part of "
        f"the frame, NEVER a small or distant wall detail: {d}, mounted where a real light switch goes — on the wall just beside the door "
        f"frame / room entrance at ~48 in switch height, within reach; never floating mid-wall, never beside a bed or "
        f"behind furniture. {size} {geom} Beyond it, only a NARROW SLICE — about one-third of the frame — of {setting} "
        f"shows through a doorway/opening, while the dimmer sits on a LARGE {anchor} wall in a RICH surface — limewash / "
        f"venetian plaster with subtle troweled texture and a soft directional light falloff, or a velvet / grasscloth "
        f"feature wall; NEVER a flat, uniform block of color — that dominates the frame "
        f"(the majority left as clean, calm copy space). {fixture} Warm/moody RICH shell (NEVER "
        f"pale beige), ONE jewel family ({anchor}, green-first) on brass + walnut; the glowing fixture is the brightest "
        f"point. {material} {copyzone} {grade}. Eye-level, straight-on, 50mm. {preserve} "
        f"Staging is realistic and physically plausible: matching chair sets, exactly one nightstand per side of a bed, "
        f"window drapery on a STRAIGHT horizontal rod (never arched or curved), any throw blanket chunky wool or linen and "
        f"NEVER leather, a cooking range has exactly FOUR control knobs and a range hood/extractor above it, at most ONE "
        f"modern clock (no antique 'old-timey' clocks), walls and ceilings are plausible architectural surfaces "
        f"(plaster, wood, tile, stone or wallpaper) and NEVER felt, light transitions smoothly from window to shadow with "
        f"no harsh gap, no duplicated or nonsensical props. Exclusions: {excl}."
    )


# =====================================================================================
# S3 — reusable MACRO close-up template (compose_macro) — the team-favorite ad format.
# Generalizes the validated dimmer-macro recipe (compose_switch shot='macro') to ANY
# product category. The winning recipe = product razor-sharp on a foreground plane held
# at a DISTINCT value/material from a soft bokeh background (tonal separation so the
# product pops), a warm GLOWING fixture in the bokeh (for light fixtures), low-key moody
# grade, 70mm, a reserved negative-space copy zone, and a product-fidelity clause.
# Source: 00_SYSTEM/systems-roadmap.md S3 + 04_KNOWLEDGE/approved-aesthetic-model.md.
# =====================================================================================

# Per-category macro placement: how the product is mounted/placed + the foreground surface
# plane it sits on + the hero noun. The foreground plane is what carries the tonal-separation
# contrast against the bokeh room. ('mount phrase', 'foreground surface', 'hero noun').
MACRO_MOUNT = {
    "chandelier":   ("its glowing arms/rings reaching into frame as the lit hero, the nearest tier razor-sharp",
                     "the crisp nearest tier/arm of the fixture itself against the out-of-focus rest of the chandelier",
                     "chandelier detail"),
    "pendant":      ("hanging into frame as the lit hero, the glass globe/shade razor-sharp and front-lit",
                     "the crisp glowing globe/shade against the soft bokeh room behind",
                     "pendant globe"),
    "sconce":       ("mounted on the wall as the lit hero, glowing warm, razor-sharp",
                     "the rich wall plane it is mounted on (a deeper jewel-toned or treated wall)",
                     "wall sconce"),
    "wall_lamp":    ("mounted on the wall as the lit hero, glowing warm, razor-sharp",
                     "the rich wall plane it is mounted on (a deeper jewel-toned or treated wall)",
                     "wall lamp"),
    "picture_light":("mounted on the frame above the artwork as the lit hero, glowing warm, razor-sharp",
                     "the crisp artwork frame / wall plane it is mounted on",
                     "picture light"),
    "table_lamp":   ("set on the console/nightstand as the lit hero, glowing warm, razor-sharp",
                     "the crisp foreground surface of the console/nightstand it sits on",
                     "table lamp"),
    "floor_lamp":   ("standing into frame as the lit hero, the shade glowing warm, razor-sharp",
                     "the crisp lit shade / upper fixture against the soft bokeh room behind",
                     "floor lamp"),
    "flush":        ("mounted flat to the ceiling as the glowing hero, razor-sharp from just below",
                     "the crisp ceiling plane it is mounted to",
                     "flush ceiling light"),
    "ceiling_light":("mounted to the ceiling as the glowing hero, razor-sharp from just below",
                     "the crisp ceiling plane it is mounted to",
                     "ceiling light"),
    "faucet":       ("installed on the vanity/counter as the crisp hero, water-ready spout razor-sharp",
                     "the crisp honed-stone vanity/counter deck it is mounted on",
                     "faucet"),
    "faucet_kitchen":("installed on the kitchen counter / sink deck as the crisp hero, the gooseneck spout razor-sharp",
                     "the crisp honed-stone counter / sink deck it is mounted on",
                     "kitchen faucet"),
    "faucet_bath":  ("installed on the bathroom vanity as the crisp hero, the spout and handles razor-sharp",
                     "the crisp honed-stone vanity deck it is mounted on",
                     "bathroom faucet"),
    "mirror":       ("mounted on the wall above the vanity/console, its brass frame and edge razor-sharp",
                     "the crisp framed edge of the mirror and the wall plane around it",
                     "mirror frame"),
    "knob":         ("installed on the cabinet drawer front, razor-sharp",
                     "the crisp lacquered cabinet front it is installed on",
                     "cabinet knob"),
    "pull":         ("installed on the cabinet/drawer front, razor-sharp",
                     "the crisp lacquered cabinet front it is installed on",
                     "cabinet pull"),
    "handle":       ("installed on the door/drawer, razor-sharp",
                     "the crisp painted door / lacquered cabinet front it is installed on",
                     "handle"),
    "door_handle":  ("mounted at lever height on a panelled interior door, the lever/rose razor-sharp",
                     "the crisp painted panelled door face it is mounted on",
                     "door handle"),
    "door_lever":   ("mounted at lever height on a panelled interior door, the lever and rose razor-sharp",
                     "the crisp painted panelled door face it is mounted on",
                     "door lever"),
    "dimmer":       ("mounted flush on the wall, the brass plate and knob razor-sharp",
                     "the rich wall plane it is mounted flush against (a deeper jewel-toned wall)",
                     "brass dimmer"),
    "switch":       ("mounted flush on the wall, the brass plate razor-sharp",
                     "the rich wall plane it is mounted flush against (a deeper jewel-toned wall)",
                     "switch plate"),
    "outlet":       ("mounted flush on the wall, the brass plate razor-sharp",
                     "the rich wall plane it is mounted flush against (a deeper jewel-toned wall)",
                     "outlet plate"),
    "sofa":         ("filling the foreground as the hero, the upholstery weave and frame razor-sharp",
                     "the crisp upholstered arm/cushion in the foreground",
                     "upholstery detail"),
    "chair":        ("filling the foreground as the hero, the upholstery and joinery razor-sharp",
                     "the crisp upholstered seat-back / joinery in the foreground",
                     "chair detail"),
    "outdoor":      ("mounted on the exterior wall as the lit hero, glowing warm, razor-sharp",
                     "the crisp weathered exterior wall plane it is mounted on",
                     "outdoor fixture"),
    "unknown":      ("placed correctly for its kind as the crisp hero, razor-sharp",
                     "the crisp foreground surface/plane it sits on",
                     "product"),
}

# Categories whose macro bokeh should feature a warm GLOWING fixture (the #1 premium cue).
# For a light fixture, the hero IS the glowing fixture; for non-light products (faucet,
# mirror, door, hardware) the glow belongs to a separate fixture in the bokeh room behind.
MACRO_LIGHT_CATS = {"chandelier", "pendant", "sconce", "wall_lamp", "picture_light", "table_lamp",
                    "floor_lamp", "flush", "ceiling_light", "outdoor"}

# Per-aspect copy-zone sizing — guarantee the empty negative space Denys praised (twice),
# sized to the frame so ad text always lands cleanly. {side} = copy_side.
MACRO_COPY_ZONE = {
    "4:5":  "Reserve a clean, empty negative-space copy zone down the {side} ~35% of this 4:5 vertical frame "
            "(kept soft, dark and uncluttered) for ad headline text.",
    "9:16": "Reserve a clean, empty negative-space copy zone across the {side} portion AND the upper third of this "
            "tall 9:16 frame (kept soft, dark and uncluttered) for stacked ad text.",
    "1:1":  "Reserve a clean, empty negative-space copy zone down the {side} ~40% of this 1:1 square frame "
            "(kept soft, dark and uncluttered) for ad headline text.",
}


def _macro_dims_note(product, category, dims):
    """True-scale note. dims may be a string ('28x26 in') or pulled from the catalog row.
    Returns '' when no dims are available (note is additive, never fabricated)."""
    if not dims:
        return ""
    return (f"The {product} measures {dims}; render it true-to-scale for a {category} — keep its real proportions, "
            f"do not oversize or shrink it relative to the surface it sits on. ")


def compose_macro(product, category, room=None, palette=None, copy_side="right",
                  aspect="4:5", seed=0, dims=None):
    """Reusable MACRO close-up ad template for ANY product category (the team-favorite format).

    Generalizes the validated dimmer-macro recipe to chandelier / sconce / pendant / faucet /
    dimmer / door_handle / mirror / hardware / etc. Pairs with a packshot --ref for fidelity.

    Args:
      product   : product name (e.g. "Teva Round Alabaster Chandelier").
      category  : catalog category / --type (chandelier, sconce, pendant, faucet_bath, dimmer,
                  door_handle, mirror, knob, ...). Falls back to a generic hero if unknown.
      room      : bokeh room behind (default: seeded from the category's valid archetypes).
      palette   : palette index 0-5 (default: seeded). Drives the ONE jewel accent.
      copy_side : 'left' | 'right' — which side reserves the negative-space copy zone.
      aspect    : '4:5' | '9:16' | '1:1' — sizes the copy zone to the frame.
      seed      : determinism seed for the seeded picks.
      dims      : real dimensions string for the true-scale note (e.g. '28x26 in'); optional.
    """
    cat = category if category in MACRO_MOUNT else "unknown"
    mount, fg_surface, hero = MACRO_MOUNT[cat]

    # bokeh room: explicit override, else a sensible default from the type's archetypes.
    _, _, archs = TYPE.get(cat, TYPE["unknown"])
    room = room or pick([a for a in archs if a in ARCH] or ["living"], seed, "mroom")
    anchor, _ = PALETTES[palette] if isinstance(palette, int) else pick(PALETTES, seed, "pal")

    is_light = cat in MACRO_LIGHT_CATS
    if is_light:
        # the hero itself glows — the brightest point in frame.
        glow = (f"The {product} is switched ON, glowing warm ~2700K as the brightest point in the frame and casting a "
                f"soft visible halo into the surrounding bokeh.")
        bokeh_fixture = ""
    else:
        # non-light hero: a SEPARATE warm fixture glows in the soft background room.
        glow = ""
        bokeh_fixture = ("a warm GLOWING light fixture out of focus in the background (a sconce, pendant or lamp lit warm "
                         "~2700K, the brightest point in the bokeh), ")

    copy = MACRO_COPY_ZONE.get(aspect, MACRO_COPY_ZONE["4:5"]).format(side=copy_side)
    dimc = _macro_dims_note(product, cat, dims)

    grade = ("warm, rich, slightly moody low-key grade, soft light, soft shadows, subtle 35mm film grain, "
             "editorial and realistic")
    preserve = (f"Use the attached product photo as the EXACT {product}. Do NOT change its shape, design, finish, "
                f"materials, color, or proportions; match its lighting and color temperature to the scene.")
    # tonal separation — the core macro mechanic (the kitchen-macro nit fix).
    separation = (f"The foreground plane ({fg_surface}) reads at a distinctly different value/material from the softer "
                  f"background so the {hero} pops off it — clear tonal separation, never the same flat color or value.")
    excl = ("no AI/render/CGI/pasted-or-floating look (integrate the product into the scene's light and perspective), "
            "no fake diffuse 'commercial' beam, no cool/blue or flat midday light, no pale/washed-out bland background "
            "(the bokeh shell must be warm and rich, not beige), no chaotic multi-color clash (commit to ONE jewel "
            "family), no busy or cluttered copy zone, no oversized or mis-scaled product, no duplicated or warped "
            "product, no European outlets/switches, no mangled text or signage, no people or faces")

    p = (
        f"Photorealistic editorial MACRO close-up, {ASPECT_WORD.get(aspect, aspect)}, full-bleed edge to edge. "
        f"Hero, razor-sharp and in focus: the {product} — {mount}; intimate 70mm close-up, shallow depth of field, "
        f"crisp tactile detail on the product. {glow} "
        f"Behind it, soft warm bokeh of a {room} in the RS rich aesthetic — a deeper warm {anchor} jewel-toned shell, "
        f"{bokeh_fixture}brass + walnut, ONE disciplined jewel accent (green-first), gently out of focus. "
        f"{separation} {dimc}{copy} {grade}. Eye-level, straight-on, 70mm. {preserve} Exclusions: {excl}."
    )
    # append any distinctive-design fidelity note for this product (e.g. Teva slim rings, Lugna swirled face).
    note = next((v for k, v in PRODUCT_NOTES.items() if k in product.lower()), None)
    if note:
        p += f" Distinctive design of the {product} to preserve exactly: {note}."
    return p


def main():
    ap = argparse.ArgumentParser(description="Compose an on-brand RS lifestyle prompt for any product")
    ap.add_argument("--product", required=True)
    ap.add_argument("--type", default="unknown", help=f"one of: {', '.join(TYPE)}, door (door hardware -> door-in-room)")
    ap.add_argument("--archetype", help=f"override scene: {', '.join(ARCH)}")
    ap.add_argument("--palette", type=int, help="palette index 0-5 (default: seeded)")
    ap.add_argument("--light", default=None, choices=list(LIGHT), help="override light mode (default: per --style)")
    ap.add_argument("--style", default="editorial", choices=list(STYLES), help="look lane: editorial (default: warm-neutral shell + ONE accent, fixture ON) | editorial-bold | cinematic-twilight")
    ap.add_argument("--note", help="extra product fidelity note appended to the preservation clause (overrides PRODUCT_NOTES)")
    ap.add_argument("--dims", help="real product dimensions for true-scale guidance, e.g. '90cm drop x 55cm dia'")
    ap.add_argument("--pair", action="store_true", help="also emit the matching close-up (Archetype B); approved set ships establishing+close-up pairs")
    ap.add_argument("--shot", default="half", choices=["macro", "half"], help="wall-hardware shot (switch/dimmer/outlet): macro close-up | half-room")
    ap.add_argument("--macro", action="store_true", help="emit the reusable MACRO close-up template (compose_macro) for ANY category — the team-favorite ad format")
    ap.add_argument("--copy-side", dest="copy_side", default="right", choices=["left", "right"], help="side reserved for the negative-space copy zone (--macro)")
    ap.add_argument("--aspect", default="4:5")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--edit", choices=list(EDIT_VARIATIONS),
                    help="emit a short Higgsfield-style EDIT/variation prompt off a ref (instead of a full scene)")
    ap.add_argument("--lens", help="override lens, e.g. '50mm camera lens'")
    ap.add_argument("--refroom", action="store_true", help="emit the Higgsfield team master template (ref-driven base scene)")
    ap.add_argument("--room", default="living room", help="room for --refroom")
    ap.add_argument("--bold", action="store_true", help="append Denys's bold-contents refinements to --refroom")
    ap.add_argument("--door-colour", "--door-color", dest="door_colour", help="door paint colour for --type door (default: seeded per room)")
    ap.add_argument("--element", help="Higgsfield Reference Element id — embeds the literal <<<id>>> token in the product/hero clause (backend auto-injects the element's reference image on model nano_banana_pro) + prepends an EMPHATIC finish+gang directive. Omit for byte-identical legacy output.")
    ap.add_argument("--finish", default="bright polished satin brass", help="product finish, stated EMPHATICALLY when --element is set (the element defaults darker otherwise)")
    ap.add_argument("--gang", default="single-gang", help="gang/config descriptor, stated EMPHATICALLY when --element is set")
    a = ap.parse_args()

    # --element wrapper: applied ONLY when set, so no-element output stays byte-identical.
    def _emit(p):
        if a.element:
            p = apply_element(p, a.product, a.element, a.finish, a.gang)
        print(p)

    if a.macro:
        dims = a.dims
        if not dims:  # auto-pull real dims from the catalog (additive; silent if unavailable)
            try:
                import catalog
                row = catalog.find_by_name(a.product)
                if row and row.get("dims_in", "").strip():
                    dims = row["dims_in"].strip() + " in"
            except Exception:
                pass
        _emit(compose_macro(a.product, a.type, a.archetype, a.palette, a.copy_side, a.aspect, a.seed, dims))
        return
    if a.type in SWITCH_TYPES:
        _emit(compose_switch(a.product, a.archetype or "living", a.shot, a.palette, a.light, a.aspect, a.seed))
        return
    if a.type in DOOR_TYPES:
        _emit(compose_door(a.product, a.archetype, a.door_colour, a.palette, a.light, a.aspect, a.seed))
        return
    if a.refroom:
        _emit(compose_refroom(a.room, a.type, a.bold))
        return
    if a.edit:
        _emit(compose_edit(a.product, a.type, a.edit, a.lens, a.seed))
        return
    _emit(compose(a.product, a.type, a.archetype, a.palette, a.light, a.aspect, a.seed, a.style, a.note, a.dims))
    if a.pair:
        print("\n--- PAIR (close-up) ---")
        _emit(compose_edit(a.product, a.type, "closeup", a.lens, a.seed))


if __name__ == "__main__":
    main()
