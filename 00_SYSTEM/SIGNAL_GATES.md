# SIGNAL GATES — feedback scoring (ported from PromptVault, simplified)

Score every feedback entry: signal = avg(specificity, repeatability, actionability, clarity), 0–1.

| Tier | Range | Authority |
|------|-------|-----------|
| LOW | < 0.3 | Log only. Cannot trigger edits, retire wins, or change templates. |
| MEDIUM | 0.3–0.6 | Reinforces existing patterns. Cannot confirm NEW wins or restructure. |
| HIGH | > 0.6 | Full authority: structural edits, win confirmation/retirement. |

HARD RULES
- Tiers don't stack: three LOW comments ≠ one HIGH. Multiple LOWs may trigger *investigation*, never structural change.
- A missing brand-locked block or product-fidelity miss is ALWAYS HIGH regardless of how casually it was phrased.
- Figma/board comments default MEDIUM until they name a specific element + fix direction (then HIGH).
- Self-critique (vision model) caps at MEDIUM. Only human confirmation reaches HIGH. This keeps judge noise from training the system.
- Bilingual feedback (ES/EN) is parsed the same — translate, then score.
