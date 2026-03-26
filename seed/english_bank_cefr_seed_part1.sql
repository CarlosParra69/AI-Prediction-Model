-- Generado por scripts/generate_bank_seeds.py (no editar a mano; volver a ejecutar el script).
-- FILL_BLANK: interaction drag_drop_fill_blank + allow_manual_input para UI híbrida.

-- Idempotent column/index (por si el esquema base no los tiene)
ALTER TABLE pie_pt_exams ADD COLUMN IF NOT EXISTS external_code text;
ALTER TABLE pie_pt_questions ADD COLUMN IF NOT EXISTS external_code text;
CREATE UNIQUE INDEX IF NOT EXISTS uq_pie_pt_exams_external_code
  ON pie_pt_exams(external_code) WHERE external_code IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_pie_pt_questions_external_code
  ON pie_pt_questions(external_code) WHERE external_code IS NOT NULL;

BEGIN;

INSERT INTO pie_pt_exams (id, language, title, is_active, external_code)
SELECT '00000000-0000-0000-0000-000000000301'::uuid, 'EN', 'PIE English Placement Test 2026', true, 'ex-english-bank-cefr-001'
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_exams e WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid);
UPDATE pie_pt_exams SET language = 'EN', title = 'PIE English Placement Test 2026', is_active = true, deleted_at = NULL,
  external_code = COALESCE(external_code, 'ex-english-bank-cefr-001')
WHERE id = '00000000-0000-0000-0000-000000000301'::uuid;
DELETE FROM pie_pt_exam_sections WHERE exam_id = '00000000-0000-0000-0000-000000000301'::uuid AND type IN ('READING','WRITING','SPEAKING') AND deleted_at IS NULL;
INSERT INTO pie_pt_exam_sections (exam_id, type, title, display_order)
SELECT '00000000-0000-0000-0000-000000000301'::uuid, s.type, s.title, s.display_order FROM (VALUES
  ('READING','AUTO READING',1),
  ('WRITING','AUTO WRITING',2),
  ('SPEAKING','AUTO SPEAKING',3)
) AS s(type,title,display_order);

UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Write a short message about your day (what you did and how you felt).',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_1';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Write a short message about your day (what you did and how you felt).', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_1'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_1' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Describe your favourite hobbies and explain why you enjoy them.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_2';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Describe your favourite hobbies and explain why you enjoy them.', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_2'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_2' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Which sentence is grammatically correct?',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_3';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Which sentence is grammatically correct?', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_3'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_3' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Choose the word that is closest in meaning to "difficult" in: "The exam was very difficult."',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_4';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Choose the word that is closest in meaning to "difficult" in: "The exam was very difficult."', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_4'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_4' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Describe an important day in your life and why it mattered to you.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_5';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Describe an important day in your life and why it mattered to you.', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_5'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_5' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Which preposition completes the sentence correctly? "She is really interested ___ improving her pronunciation."',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_6';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Which preposition completes the sentence correctly? "She is really interested ___ improving her pronunciation."', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_6'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_6' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Explain step by step how you make a simple dish you often cook (ingredients and main stages).',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_7';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Explain step by step how you make a simple dish you often cook (ingredients and main stages).', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_7'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_7' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Choose the correct past simple form: "Yesterday afternoon I ___ English vocabulary for an hour."',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_8';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Choose the correct past simple form: "Yesterday afternoon I ___ English vocabulary for an hour."', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_8'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_8' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Describe the study environment where you learn English best (place, noise, tools, routine).',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_9';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Describe the study environment where you learn English best (place, noise, tools, routine).', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_9'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_9' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Which option correctly completes this second conditional? "If I ___ more free time, I would practise speaking every day."',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_10';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Which option correctly completes this second conditional? "If I ___ more free time, I would practise speaking every day."', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_10'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_10' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Write about a trip or journey you remember well (where you went, what happened, how you felt).',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_11';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Write about a trip or journey you remember well (where you went, what happened, how you felt).', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_11'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_11' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Which collocation is natural in English?',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_12';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Which collocation is natural in English?', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_12'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_12' AND q2.deleted_at IS NULL);
COMMIT;
