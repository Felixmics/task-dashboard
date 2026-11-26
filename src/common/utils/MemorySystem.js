/**
 * MemorySystem — trial implementation inspired by Simon Scrapes' "Agentic OS" memory architecture.
 *
 * Three layers:
 *   1. Storage  — every interaction is saved to a long-term store (nothing depends on
 *                 the system "deciding" something is worth keeping).
 *   2. Injection — a short, curated snapshot (≤ SNAPSHOT_CAP chars) of the most
 *                  important items, loaded at session start.
 *   3. Recall   — hybrid keyword + cosine-similarity search over the long-term store,
 *                 with ranked results that cite source, date and line.  Returns an
 *                 explicit "nothing found" when no result passes the threshold.
 */

const SNAPSHOT_CAP = 2000;
const SIMILARITY_THRESHOLD = 0.3;
const MAX_RECALL_RESULTS = 5;

// ── helpers ──────────────────────────────────────────────────────────

function tokenize(text) {
  return (text || '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')
    .split(/\s+/)
    .filter(Boolean);
}

function cosineSimilarity(a, b) {
  const freqA = wordFreq(a);
  const freqB = wordFreq(b);
  const allWords = new Set([...Object.keys(freqA), ...Object.keys(freqB)]);

  let dot = 0, magA = 0, magB = 0;
  for (const w of allWords) {
    const va = freqA[w] || 0;
    const vb = freqB[w] || 0;
    dot += va * vb;
    magA += va * va;
    magB += vb * vb;
  }
  if (magA === 0 || magB === 0) return 0;
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

function wordFreq(text) {
  const tokens = tokenize(text);
  const freq = {};
  for (const t of tokens) {
    freq[t] = (freq[t] || 0) + 1;
  }
  return freq;
}

// ── synonyms for lightweight semantic expansion ─────────────────────

const SYNONYM_MAP = {
  price: ['pricing', 'cost', 'tier', 'plan', 'rate', 'fee'],
  pricing: ['price', 'cost', 'tier', 'plan', 'rate', 'fee'],
  cost: ['price', 'pricing', 'tier', 'fee'],
  tier: ['price', 'pricing', 'plan', 'level'],
  plan: ['tier', 'pricing', 'subscription'],
  payment: ['stripe', 'billing', 'invoice', 'checkout'],
  stripe: ['payment', 'billing', 'checkout'],
  decide: ['decision', 'agreed', 'chose', 'settled', 'landed'],
  decision: ['decide', 'agreed', 'chose', 'settled', 'landed'],
  community: ['plan', 'tier', 'group', 'users'],
  brand: ['branding', 'logo', 'identity', 'design'],
  task: ['todo', 'item', 'action', 'work'],
  fishing: ['reef', 'bait', 'lure', 'catch', 'trawl', 'troll', 'angling'],
  reef: ['coral', 'habitat', 'benthic', 'gbr', 'barrier'],
  habitat: ['reef', 'benthic', 'substrate', 'environment'],
  substrate: ['benthic', 'habitat', 'reef', 'bottom', 'seabed', 'coral', 'sand', 'rubble'],
  benthic: ['substrate', 'habitat', 'reef', 'bottom', 'seabed', 'coral'],
  coral: ['reef', 'habitat', 'benthic', 'substrate', 'hard'],
  dive: ['reef', 'underwater', 'snorkel', 'site', 'survey'],
  survey: ['benthic', 'dive', 'site', 'data', 'observation'],
  flow: ['current', 'drift', 'tide', 'upwelling', 'water'],
  water: ['current', 'tide', 'flow', 'tidal', 'ocean', 'sea'],
  direction: ['running', 'heading', 'bearing', 'ne', 'nw', 'se', 'sw'],
  tidal: ['tide', 'current', 'flow', 'water', 'moon'],
  upwelling: ['current', 'chlorophyll', 'nutrient', 'flow'],
  knots: ['current', 'speed', 'flow', 'drift'],
  current: ['tide', 'flow', 'drift', 'upwelling'],
  tide: ['current', 'tidal', 'moon', 'lunar'],
};

function expandQuery(text) {
  const tokens = tokenize(text);
  const expanded = new Set(tokens);
  for (const t of tokens) {
    const syns = SYNONYM_MAP[t];
    if (syns) syns.forEach(s => expanded.add(s));
  }
  return [...expanded].join(' ');
}

// ── MemorySystem class ──────────────────────────────────────────────

export class MemorySystem {
  constructor() {
    this.entries = [];       // long-term store (every turn)
    this.snapshot = '';      // curated injection snapshot
    this.snapshotItems = []; // items promoted to snapshot
  }

  // ── 1. Storage ──────────────────────────────────────────────────

  /** Save an interaction to the long-term store. */
  store(entry) {
    const record = {
      id: this.entries.length + 1,
      text: entry.text,
      source: entry.source || 'unknown',
      date: entry.date || new Date().toISOString(),
      type: entry.type || 'interaction',
      tags: entry.tags || [],
      metadata: entry.metadata || {},
    };
    this.entries.push(record);
    return record;
  }

  /** Bulk-import from existing session history. */
  importHistory(items) {
    return items.map(item => this.store(item));
  }

  get storeSize() {
    return this.entries.length;
  }

  // ── 2. Injection (curated snapshot) ─────────────────────────────

  /** Promote an entry to the snapshot if it's important (decision, config change, etc.). */
  promote(entryId, reason) {
    const entry = this.entries.find(e => e.id === entryId);
    if (!entry) return null;

    const item = {
      id: entry.id,
      summary: entry.text.slice(0, 200),
      reason: reason || 'decision',
      date: entry.date,
      source: entry.source,
    };

    this.snapshotItems.push(item);
    this._rebuildSnapshot();
    return item;
  }

  /** Let the system auto-promote entries that look like decisions. */
  autoPromote() {
    const decisionPatterns = [
      /decided|agreed|settled|confirmed|approved|chose|picked/i,
      /will use|going with|switching to|set .+ to/i,
      /pricing|tier|plan|budget|deadline|milestone/i,
    ];

    const promoted = [];
    for (const entry of this.entries) {
      const alreadyPromoted = this.snapshotItems.some(s => s.id === entry.id);
      if (alreadyPromoted) continue;
      if (decisionPatterns.some(p => p.test(entry.text))) {
        const item = this.promote(entry.id, 'auto-detected decision');
        if (item) promoted.push(item);
      }
    }
    return promoted;
  }

  _rebuildSnapshot() {
    let text = '';
    for (const item of this.snapshotItems) {
      const line = `[${item.date}] (${item.source}) ${item.summary}\n`;
      if (text.length + line.length > SNAPSHOT_CAP) break;
      text += line;
    }
    this.snapshot = text;
  }

  getSnapshot() {
    return this.snapshot;
  }

  get snapshotLength() {
    return this.snapshot.length;
  }

  // ── 3. Recall ───────────────────────────────────────────────────

  /** Search the long-term store by meaning + keyword. Returns ranked, cited results. */
  recall(query) {
    if (!query || this.entries.length === 0) {
      return { found: false, results: [], message: 'Nothing found.' };
    }

    const expandedQuery = expandQuery(query);

    const scored = this.entries.map(entry => {
      const expandedEntry = expandQuery(entry.text);
      const semanticScore = cosineSimilarity(expandedQuery, expandedEntry);
      const keywordScore = this._keywordMatch(query, entry.text);
      const combined = semanticScore * 0.6 + keywordScore * 0.4;

      return { entry, score: combined };
    });

    scored.sort((a, b) => b.score - a.score);

    const results = scored
      .filter(s => s.score >= SIMILARITY_THRESHOLD)
      .slice(0, MAX_RECALL_RESULTS)
      .map((s, rank) => ({
        rank: rank + 1,
        score: Math.round(s.score * 100) / 100,
        text: s.entry.text,
        source: s.entry.source,
        date: s.entry.date,
        id: s.entry.id,
        type: s.entry.type,
      }));

    if (results.length === 0) {
      return { found: false, results: [], message: 'Nothing found.' };
    }

    return { found: true, results, message: `Found ${results.length} result(s).` };
  }

  _keywordMatch(query, text) {
    const queryTokens = tokenize(query);
    const textTokens = new Set(tokenize(text));
    if (queryTokens.length === 0) return 0;
    const matches = queryTokens.filter(t => textTokens.has(t)).length;
    return matches / queryTokens.length;
  }

  // ── Dreaming (note cleanup) ─────────────────────────────────────

  /** Merge duplicate/contradictory snapshot items (simplified dreaming). */
  dream() {
    const seen = new Map();
    const cleaned = [];

    for (const item of this.snapshotItems) {
      const key = tokenize(item.summary).sort().join(' ');
      const existing = seen.get(key);
      if (existing) {
        // keep the newer one
        if (item.date > existing.date) {
          cleaned[cleaned.indexOf(existing)] = item;
          seen.set(key, item);
        }
      } else {
        seen.set(key, item);
        cleaned.push(item);
      }
    }

    this.snapshotItems = cleaned.filter(Boolean);
    this._rebuildSnapshot();
    return { merged: this.snapshotItems.length, original: seen.size };
  }

  // ── Serialisation ───────────────────────────────────────────────

  toJSON() {
    return {
      entries: this.entries,
      snapshotItems: this.snapshotItems,
      snapshot: this.snapshot,
    };
  }

  static fromJSON(data) {
    const mem = new MemorySystem();
    mem.entries = data.entries || [];
    mem.snapshotItems = data.snapshotItems || [];
    mem.snapshot = data.snapshot || '';
    return mem;
  }
}

// ── Exports ─────────────────────────────────────────────────────────

export { SNAPSHOT_CAP, SIMILARITY_THRESHOLD, MAX_RECALL_RESULTS };
export { tokenize, cosineSimilarity, expandQuery };
export default MemorySystem;
