#!/usr/bin/env python3
"""stress_test_fast.py — matching actual module APIs."""
import sys, os, time, random, shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sticky_dual_sync import LocalSessionStore
from semantic_search_cache import SemanticSearchCache
from ab_model_compare import ABModelCompare

def test_sync():
    print("  1 SessionStore 1k write+read...", end=" ")
    st = LocalSessionStore()
    n = 1000
    t0 = time.time()
    for i in range(n): st.save(f"t1_{i:04d}", {"i": i})
    w = (time.time() - t0) * 1000
    t0 = time.time()
    for i in range(n): st.load(f"t1_{i:04d}")
    r = (time.time() - t0) * 1000
    print(f"write={w:.0f}ms read={r:.0f}ms avg={(w+r)/n/2:.1f}us")

def test_search():
    print("  3 SearchCache 1k idx 500 q...", end=" ")
    sc = SemanticSearchCache(db_path="/tmp/st_s.db")
    topics = ["deploy", "cycles", "settlement", "canister"]
    for i in range(1000):
        sc.index_session(f"s{i:04d}", [{"role":"user","content":f"How to {random.choice(topics)}?"}])
    q = []
    for _ in range(500):
        t0 = time.time()
        sc.search(f"{random.choice(topics)}")
        q.append((time.time() - t0) * 1000)
    Path("/tmp/st_s.db").unlink(missing_ok=True)
    print(f"avg={sum(q)/len(q):.0f}ms max={max(q):.0f}ms")

def test_ab():
    print("  4 ABCompare 100x...", end=" ")
    ab = ABModelCompare()
    t0 = time.time()
    for _ in range(100): ab.compare("test")
    print(f"{(time.time()-t0)*1000:.0f}ms total (all errors, no gateway)")

def test_e2e():
    print("  5 E2E 100x (store+search)...", end=" ")
    st = LocalSessionStore()
    sc = SemanticSearchCache(db_path="/tmp/st_e.db")
    pts = []
    for i in range(100):
        sid = f"e{i:04d}"
        d = {"messages":[{"role":"user","content":f"test {i}"}]}
        t0 = time.time()
        st.save(sid, d)
        sc.index_session(sid, d["messages"])
        sc.search("test")
        pts.append((time.time()-t0)*1000)
    print(f"avg={sum(pts)/len(pts):.0f}ms max={max(pts):.0f}ms")

if __name__ == "__main__":
    print("═══ ODYSSEUS STRESS TEST ═══\n")
    for fn in [test_sync, test_search, test_ab, test_e2e]:
        fn()
    print("\nDone.")
