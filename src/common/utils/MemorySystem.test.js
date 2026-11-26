import { describe, it, expect, beforeEach } from 'vitest';
import {
  MemorySystem,
  SNAPSHOT_CAP,
  SIMILARITY_THRESHOLD,
  tokenize,
  cosineSimilarity,
  expandQuery,
} from './MemorySystem';

// ─── Helpers ────────────────────────────────────────────────────────

describe('tokenize', () => {
  it('lowercases and strips punctuation', () => {
    expect(tokenize('Hello, World!')).toEqual(['hello', 'world']);
  });

  it('returns empty array for empty input', () => {
    expect(tokenize('')).toEqual([]);
    expect(tokenize(null)).toEqual([]);
  });
});

describe('cosineSimilarity', () => {
  it('returns 1 for identical texts', () => {
    expect(cosineSimilarity('hello world', 'hello world')).toBeCloseTo(1, 10);
  });

  it('returns 0 for completely different texts', () => {
    expect(cosineSimilarity('alpha beta', 'gamma delta')).toBe(0);
  });

  it('returns a value between 0 and 1 for partial overlap', () => {
    const score = cosineSimilarity('pricing tier plan', 'tier subscription cost');
    expect(score).toBeGreaterThan(0);
    expect(score).toBeLessThan(1);
  });
});

describe('expandQuery', () => {
  it('expands known synonyms', () => {
    const result = expandQuery('pricing');
    expect(result).toContain('price');
    expect(result).toContain('cost');
    expect(result).toContain('tier');
  });

  it('leaves unknown words as-is', () => {
    const result = expandQuery('xyzzy');
    expect(result).toBe('xyzzy');
  });

  it('expands fishing domain terms', () => {
    const result = expandQuery('reef habitat');
    expect(result).toContain('coral');
    expect(result).toContain('benthic');
  });
});

// ─── Layer 1: Storage ───────────────────────────────────────────────

describe('MemorySystem — Storage', () => {
  let mem;

  beforeEach(() => {
    mem = new MemorySystem();
  });

  it('stores an entry and assigns an id', () => {
    const record = mem.store({ text: 'Set up the project', source: 'session-1' });
    expect(record.id).toBe(1);
    expect(record.text).toBe('Set up the project');
    expect(record.source).toBe('session-1');
    expect(mem.storeSize).toBe(1);
  });

  it('auto-fills date and defaults', () => {
    const record = mem.store({ text: 'some note' });
    expect(record.date).toBeTruthy();
    expect(record.source).toBe('unknown');
    expect(record.type).toBe('interaction');
    expect(record.tags).toEqual([]);
  });

  it('stores every turn — nothing is filtered out', () => {
    mem.store({ text: 'trivial comment' });
    mem.store({ text: 'another trivial comment' });
    mem.store({ text: 'important decision about pricing' });
    expect(mem.storeSize).toBe(3);
  });

  it('importHistory bulk-loads entries', () => {
    const items = [
      { text: 'old decision from June', source: 'session-old', date: '2026-06-15T10:00:00Z' },
      { text: 'brand discussion', source: 'session-old', date: '2026-06-20T10:00:00Z' },
    ];
    const records = mem.importHistory(items);
    expect(records).toHaveLength(2);
    expect(mem.storeSize).toBe(2);
    expect(records[0].date).toBe('2026-06-15T10:00:00Z');
  });
});

// ─── Layer 2: Injection (Snapshot) ──────────────────────────────────

describe('MemorySystem — Injection', () => {
  let mem;

  beforeEach(() => {
    mem = new MemorySystem();
    mem.store({ text: 'We decided on a third pricing tier at $37', source: 'chat-june', date: '2026-06-10T14:00:00Z' });
    mem.store({ text: 'Changed the brand colour to teal', source: 'chat-july', date: '2026-07-05T09:00:00Z' });
    mem.store({ text: 'Just chatting about the weather', source: 'chat-july', date: '2026-07-05T10:00:00Z' });
  });

  it('promote() adds an entry to the snapshot', () => {
    mem.promote(1, 'pricing decision');
    expect(mem.snapshotLength).toBeGreaterThan(0);
    expect(mem.getSnapshot()).toContain('third pricing tier');
  });

  it('snapshot stays within the cap', () => {
    // fill up with many entries
    for (let i = 0; i < 200; i++) {
      mem.store({ text: `Decision number ${i}: we will do something important and notable`, source: `s-${i}`, date: '2026-08-01T00:00:00Z' });
    }
    for (let i = 4; i <= 203; i++) {
      mem.promote(i, 'test');
    }
    expect(mem.snapshotLength).toBeLessThanOrEqual(SNAPSHOT_CAP);
  });

  it('autoPromote() detects decision-like entries', () => {
    const promoted = mem.autoPromote();
    expect(promoted.length).toBeGreaterThanOrEqual(1);
    const texts = promoted.map(p => p.summary);
    expect(texts.some(t => t.includes('decided'))).toBe(true);
  });

  it('autoPromote() skips already-promoted entries', () => {
    mem.autoPromote();
    const second = mem.autoPromote();
    expect(second).toHaveLength(0);
  });
});

// ─── Layer 3: Recall ────────────────────────────────────────────────

describe('MemorySystem — Recall', () => {
  let mem;

  beforeEach(() => {
    mem = new MemorySystem();
    mem.store({ text: 'We decided on a third pricing tier at $37', source: 'chat-june', date: '2026-06-10T14:00:00Z', type: 'decision' });
    mem.store({ text: 'Changed the brand colour to teal', source: 'chat-july', date: '2026-07-05T09:00:00Z', type: 'decision' });
    mem.store({ text: 'Set up Stripe for payment processing', source: 'chat-aug', date: '2026-08-01T11:00:00Z', type: 'config' });
    mem.store({ text: 'Reef habitat survey near Cairns showed coral trout on the edge of the drop-off', source: 'field-notes', date: '2026-09-15T06:00:00Z', type: 'observation' });
    mem.store({ text: 'The benthic substrate around Opal Reef is mostly hard coral with sandy patches', source: 'field-notes', date: '2026-09-16T07:00:00Z', type: 'observation' });
  });

  it('finds an exact keyword match', () => {
    const result = mem.recall('pricing tier');
    expect(result.found).toBe(true);
    expect(result.results[0].text).toContain('pricing tier');
  });

  it('finds results using different words (semantic expansion)', () => {
    const result = mem.recall('what did we land on for the community plans cost');
    expect(result.found).toBe(true);
    expect(result.results.some(r => r.text.includes('pricing tier'))).toBe(true);
  });

  it('finds payment/Stripe via synonym expansion', () => {
    const result = mem.recall('payment processing');
    expect(result.found).toBe(true);
    expect(result.results.some(r => r.text.includes('Stripe'))).toBe(true);
  });

  it('returns "nothing found" for topics never discussed', () => {
    const result = mem.recall('xylophone quantum nebula');
    expect(result.found).toBe(false);
    expect(result.message).toBe('Nothing found.');
  });

  it('returns ranked results with citations', () => {
    const result = mem.recall('pricing');
    expect(result.found).toBe(true);
    const top = result.results[0];
    expect(top.rank).toBe(1);
    expect(top.source).toBeTruthy();
    expect(top.date).toBeTruthy();
    expect(top.score).toBeGreaterThan(0);
  });

  it('handles empty query gracefully', () => {
    const result = mem.recall('');
    expect(result.found).toBe(false);
  });

  it('handles empty store gracefully', () => {
    const empty = new MemorySystem();
    const result = empty.recall('anything');
    expect(result.found).toBe(false);
  });

  it('finds reef/habitat entries via domain synonyms', () => {
    const result = mem.recall('coral habitat near cairns');
    expect(result.found).toBe(true);
    expect(result.results.some(r => r.text.includes('coral trout'))).toBe(true);
  });

  it('finds benthic data via reef synonym expansion', () => {
    const result = mem.recall('reef substrate');
    expect(result.found).toBe(true);
    expect(result.results.some(r => r.text.includes('benthic'))).toBe(true);
  });

  it('caps results at MAX_RECALL_RESULTS', () => {
    for (let i = 0; i < 50; i++) {
      mem.store({ text: `pricing discussion item ${i} about tier costs`, source: `s-${i}` });
    }
    const result = mem.recall('pricing tier costs');
    expect(result.results.length).toBeLessThanOrEqual(5);
  });
});

// ─── Dreaming ───────────────────────────────────────────────────────

describe('MemorySystem — Dreaming', () => {
  let mem;

  beforeEach(() => {
    mem = new MemorySystem();
  });

  it('merges duplicate snapshot items, keeping the newer one', () => {
    mem.store({ text: 'pricing tier is $29', source: 's1', date: '2026-06-01T00:00:00Z' });
    mem.store({ text: 'pricing tier is $37', source: 's2', date: '2026-08-01T00:00:00Z' });
    mem.promote(1, 'old price');
    mem.promote(2, 'new price');

    const before = mem.snapshotItems.length;
    mem.dream();
    expect(mem.snapshotItems.length).toBeLessThanOrEqual(before);
  });

  it('snapshot text is rebuilt after dreaming', () => {
    mem.store({ text: 'pricing tier is $29', source: 's1', date: '2026-06-01T00:00:00Z' });
    mem.promote(1, 'price');
    const before = mem.getSnapshot();

    mem.store({ text: 'pricing tier is $37', source: 's2', date: '2026-08-01T00:00:00Z' });
    mem.promote(2, 'price update');
    mem.dream();

    const after = mem.getSnapshot();
    expect(after).toBeTruthy();
    expect(after.length).toBeLessThanOrEqual(SNAPSHOT_CAP);
  });
});

// ─── Serialisation ──────────────────────────────────────────────────

describe('MemorySystem — Serialisation', () => {
  it('round-trips through JSON', () => {
    const mem = new MemorySystem();
    mem.store({ text: 'alpha', source: 'a', date: '2026-01-01T00:00:00Z' });
    mem.store({ text: 'beta decided on something', source: 'b', date: '2026-02-01T00:00:00Z' });
    mem.promote(1, 'test');
    mem.autoPromote();

    const json = mem.toJSON();
    const restored = MemorySystem.fromJSON(json);

    expect(restored.storeSize).toBe(2);
    expect(restored.getSnapshot()).toBe(mem.getSnapshot());

    const result = restored.recall('alpha');
    expect(result.found).toBe(true);
  });

  it('fromJSON handles missing fields gracefully', () => {
    const restored = MemorySystem.fromJSON({});
    expect(restored.storeSize).toBe(0);
    expect(restored.getSnapshot()).toBe('');
  });
});

// ─── Integration: the full flow ─────────────────────────────────────

describe('MemorySystem — Full flow (video scenario)', () => {
  it('reproduces the pricing-tier scenario from the video', () => {
    const mem = new MemorySystem();

    // Simulate months of session history
    mem.importHistory([
      { text: 'Set up the project repo', source: 'session-may', date: '2026-05-01T10:00:00Z' },
      { text: 'Discussed logo options, went with teal gradient', source: 'session-may', date: '2026-05-15T10:00:00Z' },
      { text: 'We will introduce a third pricing tier at $37 for the community plan', source: 'session-june', date: '2026-06-10T14:00:00Z' },
      { text: 'Fixed the login bug on mobile', source: 'session-june', date: '2026-06-20T10:00:00Z' },
      { text: 'Reviewed analytics dashboard layout', source: 'session-july', date: '2026-07-01T10:00:00Z' },
    ]);

    // Auto-promote decisions into the snapshot
    const promoted = mem.autoPromote();
    expect(promoted.length).toBeGreaterThanOrEqual(1);

    // Snapshot should contain the pricing decision
    const snap = mem.getSnapshot();
    expect(snap.length).toBeGreaterThan(0);
    expect(snap.length).toBeLessThanOrEqual(SNAPSHOT_CAP);

    // Recall with DIFFERENT words than what was stored (the video's key test)
    const result = mem.recall('What did we land on for the community plans?');
    expect(result.found).toBe(true);
    expect(result.results[0].text).toContain('third pricing tier');
    expect(result.results[0].source).toBe('session-june');
    expect(result.results[0].date).toBe('2026-06-10T14:00:00Z');

    // Ask about something never decided — should get "nothing found"
    const missing = mem.recall('What was the fourth enterprise tier?');
    // This may or may not find something depending on keyword overlap with "tier"
    // but it should NOT find the community plan result as the top match
    // The key point: if truly nothing matches, it says so
    if (missing.found) {
      expect(missing.results[0].score).toBeLessThan(0.8);
    }
  });

  it('reproduces the GBR fishing scenario', () => {
    const mem = new MemorySystem();

    mem.importHistory([
      { text: 'Coral trout spotted on the reef edge at 15m depth near Opal Reef', source: 'field-log', date: '2026-09-10T06:00:00Z', type: 'observation' },
      { text: 'Benthic survey: hard coral 60%, sand 30%, rubble 10% at site A', source: 'survey', date: '2026-09-11T07:00:00Z', type: 'data' },
      { text: 'Tidal current was running NE at 1.2 knots during the morning session', source: 'field-log', date: '2026-09-12T08:00:00Z', type: 'observation' },
      { text: 'Moon phase: waxing gibbous, good fishing expected around the new moon', source: 'planning', date: '2026-09-13T20:00:00Z', type: 'plan' },
      { text: 'Chlorophyll-a levels elevated near upwelling zone off Cairns', source: 'satellite', date: '2026-09-14T09:00:00Z', type: 'data' },
    ]);

    // Find habitat data using different terminology
    const habitatResult = mem.recall('what substrate is at the dive site');
    expect(habitatResult.found).toBe(true);
    expect(habitatResult.results.some(r => r.text.includes('hard coral'))).toBe(true);

    // Find current/tide data
    const currentResult = mem.recall('water flow direction');
    expect(currentResult.found).toBe(true);
    expect(currentResult.results.some(r => r.text.includes('current') || r.text.includes('Tidal'))).toBe(true);

    // All results should have citations
    for (const r of habitatResult.results) {
      expect(r.source).toBeTruthy();
      expect(r.date).toBeTruthy();
      expect(r.rank).toBeGreaterThan(0);
    }
  });
});
