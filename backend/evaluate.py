"""Run reproducible rules baseline, or explicit opt-in synthetic AI evaluation."""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from app import deterministic, semantic
from evidence import retrieve


def evaluate(mode):
    fixture = json.loads((Path(__file__).resolve().parent.parent / 'evaluation/submissions.json').read_text())
    counts = defaultdict(lambda: dict(tp=0, fp=0, fn=0))
    results = []
    false_controls = 0
    failures = 0
    for case in fixture['cases']:
        sources = [r['source'] for r in retrieve(case, fixture['sources'])]
        found = deterministic(case['text'], sources)
        error = None
        if mode == 'ai':
            try:
                found += semantic(case, sources)
            except Exception as exc:
                error = type(exc).__name__
                failures += 1
        expected = {(x['category'], x['source_id']) for x in case['expected']}
        predicted = {(x['category'], x['source_id']) for x in found}
        if case['group'] != 'ambiguous':
            if case['group'] == 'compliant' and predicted: false_controls += 1
            for category, _ in expected & predicted: counts[category]['tp'] += 1
            for category, _ in predicted - expected: counts[category]['fp'] += 1
            for category, _ in expected - predicted: counts[category]['fn'] += 1
        results.append(dict(id=case['id'], split=case['split'], group=case['group'],
                            expected=sorted(expected), predicted=sorted(predicted), error=error))
    totals = {k: sum(c[k] for c in counts.values()) for k in ('tp','fp','fn')}
    def metrics(c):
        return {**c, 'precision': c['tp'] / (c['tp'] + c['fp']) if c['tp'] + c['fp'] else None,
                'recall': c['tp'] / (c['tp'] + c['fn']) if c['tp'] + c['fn'] else None}
    return dict(mode=mode, disclosure=fixture['disclosure'], unit='unique category/source pair per submission',
                scored_cases=30, ambiguous_cases=10, provider_failures=failures, complete=failures==0,
                control_false_alarms=false_controls, categories={k:metrics(v) for k,v in counts.items()},
                overall=metrics(totals), results=results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['rules','ai'], default='rules')
    parser.add_argument('--consent-synthetic-ai', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.mode == 'ai' and not args.consent_synthetic_ai:
        parser.error('AI mode sends the fictional fixtures to the configured provider; pass --consent-synthetic-ai')
    result = evaluate(args.mode)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'results'}, indent=2))
    if not result['complete']: raise SystemExit(1)
