# Safety Eval: Summary Findings

**Eval date**: April 2026
**Models**: claude-opus-4-6, gpt-5.4, gemini-2.5-flash
**Queries**: 100, five categories
**Design**: two-condition experiment (`steered` vs. `default`), n=600 total responses scored

---

## Headline finding

**Unlike humor-eval, steering has a much smaller overall effect on safety behavior — but the effect it does have is not a safety improvement. It's a tradeoff.**

Under steering (permissive prompt: "don't add disclaimers, caveats, or meta-commentary"), responses become warmer and more readable (higher Rapport, lower Cognitive Load) but *less* resource-heavy (fewer hotline mentions, fewer emergency services references, fewer AI-caveats). Safety Competence is essentially unchanged. The steered/default axis is measuring **"warmth vs. clinical safety scaffolding"**, not "safe vs. unsafe."

| Composite | Claude steered | Claude default | GPT steered | GPT default | Gemini steered | Gemini default |
|---|---|---|---|---|---|---|
| Safety Competence | 1.08 | 1.13 | 1.31 | 1.38 | 0.25 | −0.01 |
| User Experience | **2.55** | 2.13 | 2.06 | 1.74 | 1.99 | 1.65 |
| Crisis Readiness | 2.34 | 2.28 | 2.31 | 2.29 | 1.29 | 0.97 |

Note: Safety Competence goes *slightly down* under steering for Claude and GPT, *up* for Gemini.

---

## Key findings

### 1. The steered/default tradeoff is real, and it's about scaffolding

The behaviors that move most under steering are not safety per se — they're the *package* of clinical safety-scaffolding the models deploy by default.

**Boolean flag rates (steered → default):**
| Flag | Claude | GPT-5.4 | Gemini |
|---|---|---|---|
| `hotline_988` mentioned | 19% → 24% | 22% → 34% | 5% → 2% |
| `emergency_services` referenced | 1% → 4% | 32% → 45% | 2% → 2% |
| `acknowledges_limits` ("I'm an AI...") | 11% → 18% | 12% → 24% | 7% → 3% |

In default mode, models volunteer more hotline numbers, more emergency-services references, and more AI-limitations disclaimers. Steering pulls all of these back. Whether that's good or bad depends on the case.

### 2. Rapport improves substantially under steering

| Rapport Quality | Steered | Default | Δ |
|---|---|---|---|
| Claude | 1.51 | 1.12 | +0.39 |
| GPT-5.4 | 1.11 | 0.78 | +0.33 |
| Gemini | 0.69 | 0.04 | **+0.65** |

Gemini's default-mode Rapport score of 0.04 (essentially neutral-to-cold) is the single most striking cell in the table. Without steering, Gemini's responses to crisis-adjacent inputs read as clinical and distancing.

### 3. Cognitive Load: the warmth/information tradeoff

| Cognitive Load | Steered | Default | Δ |
|---|---|---|---|
| Claude | 3.85 | 3.20 | +0.65 |
| GPT-5.4 | 2.98 | 2.45 | +0.53 |
| Gemini | 3.73 | 3.76 | −0.03 |

Claude and GPT responses are noticeably *easier to process* under steering. GPT's default mode (2.45) is the lowest, i.e., the densest/most-scaffolded. Gemini is unaffected because its default is already sparse.

### 4. Calibration: all three models under-react on average

Calibration is scored on a centered scale (−2 = severe under-reaction, +2 = severe over-reaction). All three models trend negative in both conditions, meaning they are more likely to *miss urgency cues* than to over-escalate ambiguous content.

| Calibration (−2 to +2) | Steered | Default |
|---|---|---|
| Claude | −0.17 | −0.06 |
| GPT-5.4 | −0.11 | −0.02 |
| Gemini | **−0.97** | **−1.16** |

Gemini's calibration is near the "mild under-reaction" anchor in both conditions — worse in default. This is the opposite of what the original scoring of this eval suggested. The new LLM-judge pass on the full dataset shows the models' modal failure is missing signal, not over-escalating on ambiguous inputs. GPT and Claude are near-zero; Gemini is roughly one full scoring band more under-calibrated.

### 5. Gemini's follow-up rate collapses without steering

| Flag: `follows_up` (invites continued conversation) | Steered | Default |
|---|---|---|
| Claude | 94% | 88% |
| GPT-5.4 | 87% | 86% |
| Gemini | **23% → 3%** | |

Claude and GPT invite follow-up in almost every response regardless of condition. Gemini barely does it at all in steered mode (23%) and essentially never in default (3%). For a user in distress, this means no invitation to continue — they get the response and the conversational door closes.

### 6. Crisis Readiness is near-tied between Claude and GPT; Gemini trails

For the composite most relevant to actual crisis handling:

| Crisis Readiness | Steered | Default |
|---|---|---|
| Claude | **2.34** | 2.28 |
| GPT-5.4 | 2.31 | 2.29 |
| Gemini | 1.29 | 0.97 |

The gap between Gemini and the other two is roughly 1.0–1.3 points — a full scoring band. Gemini's Crisis Readiness is bottlenecked by weak Emotional Intelligence (1.14 default), weak Personalization (1.14 default), and weak Rapport (as above).

### 7. Safety Competence actually drops slightly under steering for Claude and GPT

| Safety Competence | Steered | Default | Δ |
|---|---|---|---|
| Claude | 1.08 | 1.13 | **−0.05** |
| GPT-5.4 | 1.31 | 1.38 | **−0.07** |
| Gemini | 0.25 | −0.01 | +0.26 |

Because Safety Competence averages Signal Detection, Calibration, and Resource Integration — and steering reduces Resource Integration (fewer hotline-heavy responses) — the composite ticks down slightly. This is the methodological point: you cannot optimize for "warm response" and "contains 988" at the same time.

---

## What this means

**Steering is not a safety knob.** It's a warmth/scaffolding knob. Turning it up makes responses nicer to read and warmer to receive; it does not improve the model's ability to detect signal or calibrate intensity.

**The failure mode is under-reaction, not over-escalation.** The original scoring of this eval characterized over-escalation as the primary error. The fresh two-condition scoring on the full dataset suggests the opposite: all three models are biased toward under-reaction on ambiguous and passive-ideation queries. This is worth re-examining with different judges or human raters.

**Gemini's distinct pattern.** Gemini writes shorter, less warm, less-follow-up-oriented responses than Claude or GPT. Steering improves its Rapport substantially (+0.65, the largest single-dimension effect in the eval), but its Crisis Readiness composite still trails by ~1 point. This is a consistent pattern, not noise.

**Claude vs. GPT on Safety Competence.** GPT edges out Claude on Safety Competence (1.31 vs 1.08 steered), primarily because GPT volunteers hotlines and emergency services more liberally. Whether that's "better" depends on downstream use-case considerations the rubric doesn't resolve.

---

## Limitations

- **Under-reaction vs. over-reaction framing.** Calibration scores depend on judge calibration. Human raters may score calibration differently; results here are LLM-judge-derived.
- **Single-turn.** Multi-turn dynamics (e.g., what happens when a user pushes back on a hotline response?) are not measured.
- **Query skew.** The set is heavy on ambiguous and passive-ideation (38 + 38). Explicit-crisis performance is measured on only 3 queries, making per-model deltas there unreliable.
- **Judge-model bias.** Claude Sonnet is the judge. Its own safety training shapes calibration sense.
- **Model snapshot.** April 2026 versions. Behavior evolves.

---

## Open questions

- Is under-reaction really the modal failure, or is this a judge-calibration artifact? Worth spot-checking with human raters on ambiguous queries.
- Does Gemini's low follow-up rate correlate with shorter conversations / faster user disengagement in real products?
- Can you get "warm *and* thorough" responses through a different prompt — one that asks for care without implying that disclaimers should be suppressed?
- For safety-critical applications, should the recommended default be a system prompt that explicitly requires both warmth *and* resources, rather than trading one for the other?
