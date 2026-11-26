import React, { createContext, useState, useContext, useCallback, useEffect } from 'react';
import { MemorySystem } from '../common/utils/MemorySystem';

const MemoryContext = createContext();

export const useMemoryContext = () => useContext(MemoryContext);

const STORAGE_KEY = 'task-dashboard-memory';

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return MemorySystem.fromJSON(JSON.parse(raw));
  } catch { /* empty */ }
  return new MemorySystem();
}

function saveToStorage(mem) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(mem.toJSON()));
  } catch { /* empty */ }
}

export const MemoryProvider = ({ children, initialMemory }) => {
  const [memory] = useState(() => initialMemory || loadFromStorage());
  const [snapshot, setSnapshot] = useState(memory.getSnapshot());
  const [lastRecall, setLastRecall] = useState(null);
  const [storeSize, setStoreSize] = useState(memory.storeSize);

  useEffect(() => {
    saveToStorage(memory);
  }, [memory, snapshot, storeSize]);

  const store = useCallback((entry) => {
    const record = memory.store(entry);
    setStoreSize(memory.storeSize);
    saveToStorage(memory);
    return record;
  }, [memory]);

  const recall = useCallback((query) => {
    const result = memory.recall(query);
    setLastRecall(result);
    return result;
  }, [memory]);

  const promote = useCallback((entryId, reason) => {
    const item = memory.promote(entryId, reason);
    setSnapshot(memory.getSnapshot());
    saveToStorage(memory);
    return item;
  }, [memory]);

  const autoPromote = useCallback(() => {
    const promoted = memory.autoPromote();
    setSnapshot(memory.getSnapshot());
    saveToStorage(memory);
    return promoted;
  }, [memory]);

  const dream = useCallback(() => {
    const result = memory.dream();
    setSnapshot(memory.getSnapshot());
    saveToStorage(memory);
    return result;
  }, [memory]);

  const importHistory = useCallback((items) => {
    const records = memory.importHistory(items);
    setStoreSize(memory.storeSize);
    saveToStorage(memory);
    return records;
  }, [memory]);

  return (
    <MemoryContext.Provider
      value={{
        memory,
        snapshot,
        lastRecall,
        store,
        recall,
        promote,
        autoPromote,
        dream,
        importHistory,
        storeSize,
      }}
    >
      {children}
    </MemoryContext.Provider>
  );
};
