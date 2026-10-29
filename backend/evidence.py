"""Deterministic lexical retrieval, with explicit structured-rule precedence."""
import math
import re
from collections import Counter

STOP = set('a an the of to for and or in on with is are our your up'.split())


def tokens(text):
    return [x for x in re.findall(r'\w+', text.lower()) if x not in STOP]


def retrieve(revision, sources):
    query = set(tokens(revision['text'] + ' ' + revision['purpose']))
    eligible = [s for s in sources if s['scope'] in ('all', revision['channel'])]
    docs = [tokens(s['title'] + ' ' + s['text'] + ' ' + s['match']) for s in eligible]
    avg = sum(map(len, docs)) / max(len(docs), 1)
    ranked = []
    for source, words in zip(eligible, docs):
        freq = Counter(words)
        score = 0.0
        for word in query:
            if word in freq:
                df = sum(word in d for d in docs)
                idf = math.log(1 + (len(docs) - df + .5) / (df + .5))
                score += idf * freq[word] * 2.2 / (freq[word] + 1.2 * (.25 + .75 * len(words) / max(avg, 1)))
        exact = bool(source['match'] and source['match'].lower() in revision['text'].lower())
        global_rule = source['kind'] == 'tone' or (source['kind'] in ('dimension', 'logo') and revision.get('attachment_id'))
        if exact or global_rule or score > 0:
            ranked.append({'source': source, 'score': round(score + (10 if exact else 0), 5),
                           'reason': 'structured match' if exact else 'channel rule' if global_rule else 'lexical overlap'})
    return sorted(ranked, key=lambda x: (-x['score'], x['source']['id']))


def conflicts(sources):
    groups = {}
    for source in sources:
        if source['kind'] == 'fact' and source['match'].strip():
            groups.setdefault(source['match'].strip().lower(), []).append(source)
    return [{'match': match, 'source_ids': [s['id'] for s in group],
             'message': 'Multiple active facts for the same attribute differ; a manager must resolve them.'}
            for match, group in groups.items() if len({s['text'].strip().lower() for s in group}) > 1]
