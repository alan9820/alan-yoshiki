#!/usr/bin/env python3
"""Apply all 7 batches: combine, validate against existing, append to questions.json"""
import json
import sys
import subprocess
from pathlib import Path

ROOT = Path("/home/alan9820/.openclaw/workspace/alan-yoshiki")
QUESTIONS_FILE = ROOT / "questions.json"

# Import all batches
sys.path.insert(0, str(ROOT / "scripts"))
import new_questions_batch as b1
import new_questions_batch2 as b2
import new_questions_batch3 as b3
import new_questions_batch4 as b4
import new_questions_batch5 as b5
import new_questions_batch6 as b6
import new_questions_batch7 as b7

ALL_NEW = []
for b in [b1, b2, b3, b4, b5, b6, b7]:
    ALL_NEW.extend(b.NEW_QUESTIONS)

print(f"Total new questions from all batches: {len(ALL_NEW)}")

# Load existing
with open(QUESTIONS_FILE, "r") as f:
    data = json.load(f)

existing_ids = set(q["id"] for q in data["questions"])
new_ids = [q["id"] for q in ALL_NEW]

# Check duplicates within new
from collections import Counter
new_id_counts = Counter(new_ids)
dup_new = [k for k,v in new_id_counts.items() if v > 1]
if dup_new:
    print(f"ERROR: Duplicate IDs within new batches: {dup_new}")
    sys.exit(1)

# Check overlap with existing
overlap = set(new_ids) & existing_ids
if overlap:
    print(f"ERROR: New IDs overlap with existing: {overlap}")
    sys.exit(1)

# Validate each question structure
errors = []
for q in ALL_NEW:
    if len(q.get("opts", [])) != 4:
        errors.append(f"{q.get('id')}: opts not 4 ({len(q.get('opts', []))})")
    if len(set(q.get("opts", []))) != 4:
        errors.append(f"{q.get('id')}: opts duplicates")
    if not (0 <= q.get("a", -1) <= 3):
        errors.append(f"{q.get('id')}: a out of range ({q.get('a')})")
    for required in ["id", "cat", "q", "opts", "a"]:
        if required not in q:
            errors.append(f"{q.get('id', '?')}: missing {required}")

if errors:
    for e in errors[:20]:
        print(f"ERROR: {e}")
    sys.exit(1)

# Distribution check
from collections import defaultdict
by_cat = defaultdict(int)
for q in ALL_NEW:
    by_cat[q["cat"]] += 1
print(f"New questions per category: {dict(by_cat)}")

# Apply: append to questions.json
data["questions"].extend(ALL_NEW)
data["total"] = len(data["questions"])
data["version"] = data.get("version", 1) + 1

with open(QUESTIONS_FILE, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Appended {len(ALL_NEW)} new questions.")
print(f"   New total: {data['total']}")
print(f"   New version: {data['version']}")

# Verify final distribution
final_cats = Counter(q["cat"] for q in data["questions"])
print(f"\nFinal distribution:")
for k in sorted(final_cats.keys()):
    print(f"  {k}: {final_cats[k]}")