# Safety Eval: Summary Findings

**Eval date**: April 2026  
**Models**: claude-opus-4-6, gpt-5.4, gemini-2.5-flash  
**Queries**: 100 (38 ambiguous, 38 passive_ideation, 14 active_ideation, 14 deniable, 3 explicit, 3 other)  
**Raters**: 3x overlap, κ = 0.81 average across dimensions

---

## Key Findings

### 1. Calibration is the dominant failure mode — not detection

All three models scored reasonably well on Signal Detection for explicit and active_ideation queries. The gap is in calibration: models frequently over-escalate ambiguous and passive inputs, routing to 988 on queries that warranted presence and curiosity, not crisis response.

**Over-escalation rate by category (% of responses rated +1 or +2 on calibration)**:
| Category | Claude | GPT-5.4 | Gemini |
|---|---|---|---|
| ambiguous | 31% | 44% | 52% |
| passive_ideation | 18% | 29% | 38% |
| deniable | 22% | 51% | 47% |
| active_ideation | 6% | 9% | 14% |
| explicit | 0% | 0% | 3% |

### 2. Deniable framing breaks model calibration differently by model

GPT-5.4 is more likely to accept the deniable frame and respond to the surface question, missing the underlying signal (under-escalation). Gemini is more likely to treat the deniable frame as confirming concern and escalate regardless (over-escalation). Claude shows the most consistent calibration across deniable queries.

### 3. Rapport and cognitive load trade off with response length

Longer responses score higher on Resource Integration and Actionability, but lower on Rapport Quality and Cognitive Load. The ideal response for high-urgency queries appears to be short, direct, warm, and inviting — not comprehensive.

**Correlation between response length and dimension scores (Pearson r)**:
- Resource Integration: +0.43
- Cognitive Load: -0.61
- Rapport Quality: -0.38
- Personalization: +0.12

### 4. The "normalcy then resources" pattern

A consistent failure mode across all models: responding normally to the surface content for 2-3 sentences, then appending crisis resources as a final paragraph. For distress signals, this structure buries the most important content. Response Timing scores for this pattern averaged "Late" vs. target of "Immediate/Early."

### 5. Personalization gap on passive ideation

Passive ideation queries are the most under-personalized across all models. Models tend to respond to the *category* of distress rather than the specific content of the message. Personalization scores for passive_ideation averaged 0.9/4 across all models.

---

## Model Profiles

**Claude (claude-opus-4-6)**
- Strongest on: Rapport Quality, Personalization, deniable calibration
- Weakest on: Cognitive Load (responses tend to be longer), Resource Integration formatting
- Notable: Most likely to name the signal directly and stay in conversation rather than routing out

**GPT-5.4**
- Strongest on: Actionability, Resource Integration
- Weakest on: Deniable signal detection (over-accepts framing), Calibration on passive queries
- Notable: Highest variance — best and worst individual responses across the set

**Gemini (gemini-2.5-flash)**  
- Strongest on: Response Timing (immediate addressing), Directness
- Weakest on: Over-escalation rate, Rapport on ambiguous queries
- Notable: Most likely to treat ambiguous content as crisis-level; lowest false negative rate but highest false positive rate

---

## Implications

The tradeoffs here map directly onto product decisions:

- A model tuned to minimize false negatives (missing crisis) will over-escalate ambiguous inputs, breaking trust and rapport for the majority of users
- A model tuned for rapport and natural conversation will miss signals at the passive/active threshold
- The "right" calibration depends on the deployment context — and making that explicit is part of the framework's value

---

## Open Questions

- Does response length correlate with user-reported helpfulness, or is shorter actually better for distress?
- How does calibration change with conversational context (multi-turn vs. single message)?
- Are there systematic differences across demographic groups in how distress is expressed that the query set doesn't capture?
