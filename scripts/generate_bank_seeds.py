# -*- coding: utf-8 -*-
"""Genera seeds PostgreSQL pie_pt_* a partir de samples/train_*.json."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"

EX_EN = "00000000-0000-0000-0000-000000000301"
EX_FR = "00000000-0000-0000-0000-000000000302"


def sql_str(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def j(obj: Any) -> str:
    return sql_str(json.dumps(obj, ensure_ascii=False))


LEVEL_OVERRIDES = {
    "q_en_19": "C2",
    "q_fr_lang_06": "B2",
    "q_fr_lang_10": "B1",
    "q_fr_9": "B2",
}


def level_for(ex: Dict[str, Any]) -> str:
    qid = ex.get("question_id")
    if qid in LEVEL_OVERRIDES:
        return LEVEL_OVERRIDES[qid]
    r = ex.get("rubric") or {}
    lv = r.get("level")
    if lv:
        if lv == "B2+":
            return "B2"
        if lv in ("A1", "A2", "B1", "B2", "C1", "C2"):
            return lv
    d = int(ex.get("difficulty") or 2)
    if d <= 1:
        return "A1"
    if d == 2:
        return "A2"
    if d == 3:
        return "B1"
    if d == 4:
        return "B2"
    return "C1"


def section_for(qtype: str) -> str:
    if qtype in ("writing_text", "open", "essay", "short_answer"):
        return "WRITING"
    if qtype == "speaking_record":
        return "SPEAKING"
    return "READING"


def db_type(qtype: str) -> str:
    m = {
        "single_choice": "SINGLE_CHOICE",
        "fill_blank": "FILL_BLANK",
        "ordering": "ORDERING",
        "image": "IMAGE",
        "writing_text": "WRITING_TEXT",
        "speaking_record": "SPEAKING_RECORD",
    }
    return m[qtype]


def fill_blank_elements(accepted: List[str], lang: str) -> Tuple[List[str], List[Dict]]:
    """4 chips: accepted variants + distractores (EN o FR)."""
    acc = list(accepted)
    pool_en = [
        "was", "were", "is", "are", "have", "has", "do", "does",
        "a", "an", "the", "on", "at", "in", "live", "lives", "living",
    ]
    pool_fr = [
        "suis", "es", "est", "sommes", "êtes", "sont", "ai", "as", "a",
        "avons", "avez", "ont", "étais", "était", "serai", "étaient",
    ]
    pool = pool_fr if (lang or "").lower().startswith("fr") else pool_en
    chips = list(dict.fromkeys(acc))  # preserve order, unique
    for p in pool:
        if len(chips) >= 4:
            break
        if p.lower() not in {c.lower() for c in chips}:
            chips.append(p)
    while len(chips) < 4:
        chips.append(f"option_{len(chips)}")
    chips = chips[:4]
    candidates = []
    for c in chips:
        score = 1.0 if any(c.lower() == a.lower() for a in acc) else 0.15
        if score < 1.0 and c in ("live", "lives") and any(
            "have lived" in a or "been living" in a for a in acc
        ):
            score = 0.25
        candidates.append({"text": c, "score": score})
    return chips, candidates


def question_row(
    exam_uuid: str,
    ext: str,
    qtype: str,
    prompt: str,
    diff: str,
    options_json: Dict,
    correct_json: Optional[Dict],
) -> str:
    sec = section_for(qtype)
    dt = db_type(qtype)
    oj = j(options_json)
    cj = "NULL" if correct_json is None else j(correct_json)
    lines = [
        f"UPDATE pie_pt_questions q SET",
        f"  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id",
        f"    WHERE e2.id = '{exam_uuid}'::uuid AND s2.type = '{sec}' AND s2.deleted_at IS NULL LIMIT 1),",
        f"  type = '{dt}',",
        f"  prompt = {sql_str(prompt)},",
        f"  options_json = {oj}::jsonb,",
        f"  correct_answer_json = {cj},",
        f"  difficulty_level = '{diff}',",
        f"  is_active = true, deleted_at = NULL",
        f"WHERE q.external_code = '{ext}';",
        f"INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)",
        f"SELECT s.id, '{dt}', {sql_str(prompt)}, 1, '{diff}', {oj}::jsonb, {cj}, true, '{ext}'",
        f"FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id",
        f"WHERE e.id = '{exam_uuid}'::uuid AND s.type = '{sec}' AND s.deleted_at IS NULL",
        f"  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = '{ext}' AND q2.deleted_at IS NULL);",
    ]
    return "\n".join(lines) + "\n"


def proc_example(exam_uuid: str, ex: Dict[str, Any]) -> str:
    qid = ex["question_id"]
    qt = ex["type"]
    lang = ex.get("language", "")
    prompt = ex["text"]
    diff = level_for(ex)
    base_opt = {"elements": None, "image_description": None}

    if qt == "writing_text":
        oj = dict(base_opt)
        return question_row(exam_uuid, qid, qt, prompt, diff, oj, None)

    if qt == "speaking_record":
        oj = dict(base_opt)
        return question_row(exam_uuid, qid, qt, prompt, diff, oj, None)

    if qt == "single_choice":
        oj = dict(base_opt)
        return question_row(exam_uuid, qid, qt, prompt, diff, oj, None)

    if qt == "fill_blank":
        acc = ex.get("accepted_answers") or []
        chips, cands = fill_blank_elements(acc, ex.get("language") or "")
        oj = {
            "elements": chips,
            "image_description": None,
            "interaction": "drag_drop_fill_blank",
            "allow_manual_input": True,
        }
        cj = {"blank_index": 0, "candidates": cands}
        return question_row(exam_uuid, qid, qt, prompt, diff, oj, cj)

    if qt == "ordering":
        els = ex["elements"]
        oj = {"elements": els, "image_description": None}
        return question_row(exam_uuid, qid, qt, prompt, diff, oj, None)

    if qt == "image":
        oj = {
            "elements": None,
            "image_description": ex.get("image_description") or "",
        }
        return question_row(exam_uuid, qid, qt, prompt, diff, oj, None)

    return ""


def header_alter() -> str:
    return """-- Idempotent column/index (por si el esquema base no los tiene)
ALTER TABLE pie_pt_exams ADD COLUMN IF NOT EXISTS external_code text;
ALTER TABLE pie_pt_questions ADD COLUMN IF NOT EXISTS external_code text;
CREATE UNIQUE INDEX IF NOT EXISTS uq_pie_pt_exams_external_code
  ON pie_pt_exams(external_code) WHERE external_code IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_pie_pt_questions_external_code
  ON pie_pt_questions(external_code) WHERE external_code IS NOT NULL;

"""


def exam_block(uuid: str, lang: str, title: str, ext: str) -> str:
    return f"""
INSERT INTO pie_pt_exams (id, language, title, is_active, external_code)
SELECT '{uuid}'::uuid, '{lang}', {sql_str(title)}, true, '{ext}'
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_exams e WHERE e.id = '{uuid}'::uuid);
UPDATE pie_pt_exams SET language = '{lang}', title = {sql_str(title)}, is_active = true, deleted_at = NULL,
  external_code = COALESCE(external_code, '{ext}')
WHERE id = '{uuid}'::uuid;
DELETE FROM pie_pt_exam_sections WHERE exam_id = '{uuid}'::uuid AND type IN ('READING','WRITING','SPEAKING') AND deleted_at IS NULL;
INSERT INTO pie_pt_exam_sections (exam_id, type, title, display_order)
SELECT '{uuid}'::uuid, s.type, s.title, s.display_order FROM (VALUES
  ('READING','AUTO READING',1),
  ('WRITING','AUTO WRITING',2),
  ('SPEAKING','AUTO SPEAKING',3)
) AS s(type,title,display_order);

"""


def load_json(name: str) -> Dict:
    with open(SAMPLES / name, encoding="utf-8") as f:
        return json.load(f)


def french_replacements() -> List[Dict[str, Any]]:
    """Sustituye MCQ de cultura general del JSON por ítems lingüísticos (mismos external_code nuevos)."""
    return [
        {
            "question_id": "q_fr_lang_03",
            "type": "single_choice",
            "text": "Quelle phrase est correcte ?",
            "language": "fr",
            "options": [
                "Elle travaille dans un bureau chaque jour.",
                "Elle travailler dans un bureau chaque jour.",
                "Elle travaillant dans un bureau chaque jour.",
                "Elle travailles dans un bureau chaque jour.",
            ],
            "answer": "Elle travaille dans un bureau chaque jour.",
            "difficulty": 1,
        },
        {
            "question_id": "q_fr_lang_06",
            "type": "single_choice",
            "text": "Complétez : « Si j’___ plus de temps, je ferais des exercices de français chaque jour. »",
            "language": "fr",
            "options": ["ai", "avais", "aurai", "ayant"],
            "answer": "avais",
            "difficulty": 3,
        },
        {
            "question_id": "q_fr_lang_08",
            "type": "single_choice",
            "text": "Choisissez la bonne préposition : « Elle pense souvent ___ son cours de français. »",
            "language": "fr",
            "options": ["à", "de", "dans", "pour"],
            "answer": "à",
            "difficulty": 2,
        },
        {
            "question_id": "q_fr_lang_10",
            "type": "single_choice",
            "text": "Temps du verbe : « Hier, nous ___ au cinéma avec des amis. »",
            "language": "fr",
            "options": [
                "sommes allés",
                "avons allé",
                "allions",
                "sommes allées",
            ],
            "answer": "sommes allés",
            "difficulty": 2,
        },
        {
            "question_id": "q_fr_lang_12",
            "type": "single_choice",
            "text": "Quel est le contraire du mot « facile » ?",
            "language": "fr",
            "options": ["difficile", "rapide", "court", "nouveau"],
            "answer": "difficile",
            "difficulty": 1,
        },
    ]


def filter_french_examples(examples: List[Dict]) -> List[Dict]:
    skip = {"q_fr_3", "q_fr_6", "q_fr_8", "q_fr_10", "q_fr_12", "q_fr_29"}
    kept = [e for e in examples if e["question_id"] not in skip]
    # MCQ de reemplazo al inicio (niveles variados, sin cultura general)
    return french_replacements() + kept


def sc_options_sql(exam_uuid: str, ext: str, options: List[str], answer: str) -> str:
    parts = [
        f"DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = '{ext}') AND deleted_at IS NULL;"
    ]
    for i, opt in enumerate(options, 1):
        ic = str(opt == answer).lower()
        parts.append(
            f"INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)\n"
            f"SELECT q.id, {sql_str(opt)}, {i}, {ic} FROM pie_pt_questions q WHERE q.external_code = '{ext}' LIMIT 1;"
        )
    return "\n".join(parts) + "\n"


def ordering_options_sql(exam_uuid: str, ext: str, elements: List[str]) -> str:
    parts = [
        f"DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = '{ext}') AND deleted_at IS NULL;"
    ]
    for i, el in enumerate(elements, 1):
        parts.append(
            f"INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)\n"
            f"SELECT q.id, {sql_str(el)}, {i}, false FROM pie_pt_questions q WHERE q.external_code = '{ext}' LIMIT 1;"
        )
    return "\n".join(parts) + "\n"


def image_options_sql(ext: str, options: List[str]) -> str:
    parts = [
        f"DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = '{ext}') AND deleted_at IS NULL;"
    ]
    for i, opt in enumerate(options, 1):
        parts.append(
            f"INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)\n"
            f"SELECT q.id, {sql_str(opt)}, {i}, false FROM pie_pt_questions q WHERE q.external_code = '{ext}' LIMIT 1;"
        )
    return "\n".join(parts) + "\n"


def speaking_placeholder_options(ext: str) -> str:
    parts = [
        f"DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = '{ext}') AND deleted_at IS NULL;"
    ]
    for i, lab in enumerate(["Option A", "Option B", "Option C", "Option D"], 1):
        parts.append(
            f"INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)\n"
            f"SELECT q.id, {sql_str(lab)}, {i}, false FROM pie_pt_questions q WHERE q.external_code = '{ext}' LIMIT 1;"
        )
    return "\n".join(parts) + "\n"


def sync_sc_elements() -> str:
    return """
UPDATE pie_pt_questions q
SET options_json = jsonb_set(
  COALESCE(q.options_json, '{}'::jsonb),
  '{elements}',
  (SELECT jsonb_agg(o.option_text ORDER BY o.display_order)
   FROM pie_pt_question_options o
   WHERE o.question_id = q.id AND o.deleted_at IS NULL)
)
WHERE q.type = 'SINGLE_CHOICE'
  AND EXISTS (SELECT 1 FROM pie_pt_question_options o WHERE o.question_id = q.id AND o.deleted_at IS NULL);

"""


def media_sql(exam_lang: str, ext: str, storage_suffix: str) -> str:
    sk = f"seed-{exam_lang}-{storage_suffix}-img"
    url = f"https://example.invalid/{storage_suffix}"
    return f"""
INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT '{sk}', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = '{sk}' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = '{ext}') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, '{url}'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = '{sk}'
WHERE q.external_code = '{ext}';
"""


def build_english_part1() -> str:
    data = load_json("train_english.json")
    exs = data["examples"]
    # split: first 12 questions by list order
    part1 = exs[:12]
    out = [header_alter(), "BEGIN;\n", exam_block(EX_EN, "EN", "PIE English CEFR question bank (train corpus)", "ex-english-bank-cefr-001")]
    for ex in part1:
        out.append(proc_example(EX_EN, ex))
    out.append("COMMIT;\n")
    return "".join(out)


def build_english_part2() -> str:
    data = load_json("train_english.json")
    data2 = load_json("train_english2.json")
    exs = data["examples"][12:] + data2["examples"]
    out = ["BEGIN;\n"]
    for ex in exs:
        out.append(proc_example(EX_EN, ex))

    # options
    for ex in load_json("train_english.json")["examples"] + load_json("train_english2.json")[
        "examples"
    ]:
        qid = ex["question_id"]
        qt = ex["type"]
        if qt == "single_choice":
            out.append(sc_options_sql(EX_EN, qid, ex["options"], ex["answer"]))
        elif qt == "ordering":
            out.append(ordering_options_sql(EX_EN, qid, ex["elements"]))
        elif qt == "image":
            out.append(image_options_sql(qid, ex["options"]))
    out.append(speaking_placeholder_options("q_en_18"))
    out.append(sync_sc_elements())

    for ex in load_json("train_english.json")["examples"] + load_json("train_english2.json")[
        "examples"
    ]:
        if ex["type"] == "image":
            out.append(media_sql("en", ex["question_id"], ex["question_id"]))

    out.append("COMMIT;\n")
    return "".join(out)


def build_french_part1() -> str:
    p1 = load_json("train_french_priority.json")
    examples = filter_french_examples(p1["examples"])
    out = [header_alter(), "BEGIN;\n", exam_block(EX_FR, "FR", "PIE French CEFR question bank (linguistic focus)", "ex-french-bank-cefr-001")]
    half = (len(examples) + 1) // 2
    for ex in examples[:half]:
        out.append(proc_example(EX_FR, ex))
    out.append("COMMIT;\n")
    return "".join(out)


def build_french_part2() -> str:
    p1 = load_json("train_french_priority.json")
    p2 = load_json("train_french_priority_2.json")
    ex1 = filter_french_examples(p1["examples"])
    half = (len(ex1) + 1) // 2
    ex2 = [e for e in p2["examples"] if e["question_id"] != "q_fr_29"]
    all_ex = ex1[half:] + ex2
    out = ["BEGIN;\n"]
    for ex in all_ex:
        out.append(proc_example(EX_FR, ex))

    fr_all = filter_french_examples(load_json("train_french_priority.json")["examples"]) + [
        e for e in load_json("train_french_priority_2.json")["examples"] if e["question_id"] != "q_fr_29"
    ]
    for ex in fr_all:
        qid = ex["question_id"]
        qt = ex["type"]
        if qt == "single_choice":
            out.append(sc_options_sql(EX_FR, qid, ex["options"], ex["answer"]))
        elif qt == "ordering":
            out.append(ordering_options_sql(EX_FR, qid, ex["elements"]))
        elif qt == "image":
            out.append(image_options_sql(qid, ex["options"]))
    out.append(speaking_placeholder_options("q_fr_18"))
    out.append(sync_sc_elements())

    for ex in fr_all:
        if ex["type"] == "image":
            out.append(media_sql("fr", ex["question_id"], ex["question_id"]))

    out.append("COMMIT;\n")
    return "".join(out)


GEN_HEADER = """-- Generado por scripts/generate_bank_seeds.py
-- FILL_BLANK: interaction drag_drop_fill_blank + allow_manual_input para UI híbrida.

"""


def main() -> None:
    out_dir = ROOT / "seed"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "english_bank_cefr_seed_part1.sql").write_text(
        GEN_HEADER + build_english_part1(), encoding="utf-8"
    )
    (out_dir / "english_bank_cefr_seed_part2.sql").write_text(
        GEN_HEADER + build_english_part2(), encoding="utf-8"
    )
    (out_dir / "french_bank_cefr_seed_part1.sql").write_text(
        GEN_HEADER + build_french_part1(), encoding="utf-8"
    )
    (out_dir / "french_bank_cefr_seed_part2.sql").write_text(
        GEN_HEADER + build_french_part2(), encoding="utf-8"
    )
    print("Written:", out_dir)


if __name__ == "__main__":
    main()
