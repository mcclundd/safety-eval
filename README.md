# safety-eval

**AI Safety Response Evaluation: Mental Health & Crisis Signal Detection**

A competitive evaluation framework for assessing how frontier AI models respond to ambiguous, crisis-adjacent user inputs — with a focus on calibration, signal detection, and user experience for someone who may actually be in distress.

---

## Background

Standard AI safety evals treat safety as binary: did the model refuse, or not? This project takes a different approach. The interesting failure modes aren't refusals — they're miscalibrated responses that either:

- **Over-escalate**: Treat vague distress as imminent crisis, flooding the user with hotline numbers and breaking conversational rapport
- **Under-escalate**: Miss clear signals, respond with generic wellness tips, or treat explicit ideation as a "topic" rather than a moment requiring care

Both failure modes have real consequences for users. This framework measures the space between them.

## Query Set

100 synthetic user inputs (`data/queries.jsonl`) representing a spectrum of crisis-adjacent signals — from ambiguous and deniable ("just curious") to explicit and urgent. Inputs are intentionally naturalistic: typos, hedging, casual register, false framings ("asking for a story," "just hypothetically"). This reflects how people actually communicate distress.

Queries are categorized by signal type:
- `ambiguous` — could be innocent, could be concerning
- `passive_ideation` — suggests detachment, not wanting to be here
- `active_ideation` — clearer signals of intent or planning
- `deniable` — framed to deflect ("not about me," "for research")
- `explicit` — direct, urgent

## Evaluation Framework

Ten dimensions scored per response, grouped into three composite scores:

| Composite | Dimensions |
|-----------|-----------|
| **Safety Competence** | Signal Detection, Calibration, Resource Integration |
| **User Experience** | Rapport Quality, Cognitive Load, Personalization |
| **Crisis Readiness** | Response Timing, Directness, Actionability, Emotional Intelligence |

Full rubric with operational definitions, anchor examples, and inter-rater guidelines: [`rubric/framework.md`](rubric/framework.md)

## Models Evaluated

- `claude-opus-4-6` (Anthropic)
- `gpt-5.4` (OpenAI)  
- `gemini-2.5-flash` (Google)

## Running the Eval

```bash
# Install dependencies
pip install -r requirements.txt

# Set API keys
export ANTHROPIC_API_KEY=your_key
export OPENAI_API_KEY=your_key
export GOOGLE_API_KEY=your_key

# Run full eval (100 queries × 3 models)
python scripts/run_eval.py

# Demo mode — 10 representative queries, streamed output
python scripts/run_eval.py --demo

# Single model
python scripts/run_eval.py --model anthropic

# Score existing responses
python scripts/score_responses.py --input results/responses.jsonl
```

## Results

Preliminary results in [`results/`](results/). Summary findings:

- Calibration failures are more common than detection failures across all models
- Over-escalation on ambiguous inputs is the dominant error pattern
- Rapport and cognitive load scores are inversely correlated with response length
- Models perform significantly differently on "deniable" framings vs. explicit signals

See [`results/summary.md`](results/summary.md) for full analysis.

## Repo Structure

```
safety-eval/
├── viewer.html                # Interactive response viewer
├── data/
│   ├── queries.jsonl          # 100 eval queries with metadata
│   └── categories.md          # Query categorization rationale
├── rubric/
│   ├── framework.md           # Full evaluation framework
│   └── anchor_examples.md     # Scored anchor responses for calibration
├── scripts/
│   ├── run_eval.py            # Main eval runner (multi-model)
│   ├── score_responses.py     # Scoring script
│   └── analyze_results.py     # Analysis and visualization
├── results/
│   ├── responses.jsonl        # Raw model responses
│   ├── scores.csv             # Dimension scores per response
│   └── summary.md             # Key findings
└── docs/
    └── methodology.md         # Extended methodology notes
```

## Viewing Responses

Open `viewer.html` in a browser to explore all model responses in a polished, interactive UI. It supports search, filtering by category, model toggles, and side-by-side comparison.

To auto-load the results, serve the repo locally:

```bash
python -m http.server 8000
# then open http://localhost:8000/viewer.html
```

Or just open `viewer.html` directly and drag in `results/responses.jsonl`.

## Notes

This framework was developed for internal evaluation use. Query set is synthetic. No real user data. Framework design informed by crisis counseling literature and safe messaging guidelines.

Inter-rater reliability target: κ > 0.75 on all dimensions. Recommend calibration session on anchor examples before independent coding.

---

*Part of an ongoing effort to move AI safety evaluation beyond binary pass/fail toward measurement of response quality, calibration, and real-world usability.*
