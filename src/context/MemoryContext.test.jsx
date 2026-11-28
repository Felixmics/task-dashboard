import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryProvider, useMemoryContext } from './MemoryContext';
import { MemorySystem } from '../common/utils/MemorySystem';

function TestConsumer() {
  const { store, recall, promote, autoPromote, dream, snapshot, storeSize, lastRecall } = useMemoryContext();
  const [output, setOutput] = React.useState('');

  return (
    <div>
      <span data-testid="store-size">{storeSize}</span>
      <span data-testid="snapshot">{snapshot}</span>
      <span data-testid="output">{output}</span>
      <span data-testid="last-recall">{lastRecall ? JSON.stringify(lastRecall) : 'none'}</span>
      <button data-testid="store-btn" onClick={() => {
        const r = store({ text: 'We decided the pricing tier is $37', source: 'test-session', date: '2026-06-10T14:00:00Z' });
        setOutput(`stored:${r.id}`);
      }}>Store</button>
      <button data-testid="store-reef-btn" onClick={() => {
        store({ text: 'Coral trout on the reef edge near Opal Reef at 15m', source: 'field-log', date: '2026-09-10T06:00:00Z' });
      }}>Store Reef</button>
      <button data-testid="recall-btn" onClick={() => {
        const r = recall('community plan cost');
        setOutput(r.found ? `found:${r.results.length}` : 'not-found');
      }}>Recall</button>
      <button data-testid="recall-reef-btn" onClick={() => {
        const r = recall('reef habitat');
        setOutput(r.found ? `found:${r.results.length}` : 'not-found');
      }}>Recall Reef</button>
      <button data-testid="promote-btn" onClick={() => {
        const item = promote(1, 'pricing decision');
        setOutput(item ? `promoted:${item.id}` : 'no-entry');
      }}>Promote</button>
      <button data-testid="auto-promote-btn" onClick={() => {
        const items = autoPromote();
        setOutput(`auto:${items.length}`);
      }}>Auto Promote</button>
      <button data-testid="dream-btn" onClick={() => {
        const result = dream();
        setOutput(`dreamed:${result.merged}`);
      }}>Dream</button>
    </div>
  );
}

describe('MemoryContext', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('provides a fresh memory system', () => {
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );
    expect(screen.getByTestId('store-size').textContent).toBe('0');
    expect(screen.getByTestId('snapshot').textContent).toBe('');
  });

  it('stores an entry and updates size', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('store-btn'));
    expect(screen.getByTestId('store-size').textContent).toBe('1');
    expect(screen.getByTestId('output').textContent).toBe('stored:1');
  });

  it('recalls stored entries', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('store-btn'));
    await user.click(screen.getByTestId('recall-btn'));
    expect(screen.getByTestId('output').textContent).toMatch(/^found:/);
  });

  it('returns not-found for unrelated queries on empty store', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('recall-btn'));
    expect(screen.getByTestId('output').textContent).toBe('not-found');
  });

  it('promotes an entry and updates snapshot', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('store-btn'));
    await user.click(screen.getByTestId('promote-btn'));
    expect(screen.getByTestId('output').textContent).toBe('promoted:1');
    expect(screen.getByTestId('snapshot').textContent).toContain('pricing tier');
  });

  it('auto-promotes decision entries', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('store-btn'));
    await user.click(screen.getByTestId('auto-promote-btn'));
    expect(screen.getByTestId('output').textContent).toMatch(/^auto:\d+/);
    expect(screen.getByTestId('snapshot').textContent.length).toBeGreaterThan(0);
  });

  it('dream cleans up the snapshot', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('store-btn'));
    await user.click(screen.getByTestId('promote-btn'));
    await user.click(screen.getByTestId('dream-btn'));
    expect(screen.getByTestId('output').textContent).toMatch(/^dreamed:/);
  });

  it('updates lastRecall after a recall', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    expect(screen.getByTestId('last-recall').textContent).toBe('none');
    await user.click(screen.getByTestId('store-btn'));
    await user.click(screen.getByTestId('recall-btn'));
    const lr = screen.getByTestId('last-recall').textContent;
    expect(lr).not.toBe('none');
    const parsed = JSON.parse(lr);
    expect(parsed).toHaveProperty('found');
    expect(parsed).toHaveProperty('results');
  });

  it('handles reef/fishing domain recall through context', async () => {
    const user = userEvent.setup();
    render(
      <MemoryProvider initialMemory={new MemorySystem()}>
        <TestConsumer />
      </MemoryProvider>
    );

    await user.click(screen.getByTestId('store-reef-btn'));
    await user.click(screen.getByTestId('recall-reef-btn'));
    expect(screen.getByTestId('output').textContent).toMatch(/^found:/);
  });
});
