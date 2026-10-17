from src.differ import diff, fingerprint, has_pending, summarize, top_severity
from src.explain import build_message, grounded
from src.sources import Record

BASE = [{"id": "MR-1", "date": "2024-03-02", "status": "Approved"}]


def rec(muts, extent="2-10", owners=("A",)):
    return Record(list(owners), extent, muts)


def test_no_change():
    s = summarize(rec(BASE))
    assert diff(s, s) == []
    assert top_severity([]) is None


def test_new_mutation_is_high_and_grounded_in_all_languages():
    old = summarize(rec(BASE))
    new = summarize(rec(BASE + [{"id": "MR-2", "date": "2026-10-10", "status": "Pending"}]))
    changes = diff(old, new)
    assert top_severity(changes) == "high"
    for lang in ("en", "kn", "hi"):
        assert grounded(build_message("Test plot", changes, lang), changes)


def test_owner_change_is_critical_and_names_are_hashed():
    old = summarize(rec(BASE, owners=("Alice",)))
    new = summarize(rec(BASE, owners=("Bob",)))
    changes = diff(old, new)
    assert top_severity(changes) == "critical"
    assert "Bob" not in str(new) and "Alice" not in str(old)
    assert all(len(h) == 16 for h in new["owners"])
    assert "Bob" not in build_message("Test plot", changes, "en")


def test_fingerprint_is_stable_and_changes():
    a = summarize(rec(BASE))
    assert fingerprint(a) == fingerprint(summarize(rec(BASE)))
    assert fingerprint(a) != fingerprint(summarize(rec(BASE, extent="2-05")))


def test_pending_detection():
    pending = summarize(rec(BASE + [{"id": "MR-2", "date": "d", "status": "Pending"}]))
    assert has_pending(pending) and not has_pending(summarize(rec(BASE)))
