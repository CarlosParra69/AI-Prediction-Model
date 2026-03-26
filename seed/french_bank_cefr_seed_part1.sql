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
SELECT '00000000-0000-0000-0000-000000000302'::uuid, 'FR', 'PIE French Placement Test 2026', true, 'ex-french-bank-cefr-001'
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_exams e WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid);
UPDATE pie_pt_exams SET language = 'FR', title = 'PIE French Placement Test 2026', is_active = true, deleted_at = NULL,
  external_code = COALESCE(external_code, 'ex-french-bank-cefr-001')
WHERE id = '00000000-0000-0000-0000-000000000302'::uuid;
DELETE FROM pie_pt_exam_sections WHERE exam_id = '00000000-0000-0000-0000-000000000302'::uuid AND type IN ('READING','WRITING','SPEAKING') AND deleted_at IS NULL;
INSERT INTO pie_pt_exam_sections (exam_id, type, title, display_order)
SELECT '00000000-0000-0000-0000-000000000302'::uuid, s.type, s.title, s.display_order FROM (VALUES
  ('READING','AUTO READING',1),
  ('WRITING','AUTO WRITING',2),
  ('SPEAKING','AUTO SPEAKING',3)
) AS s(type,title,display_order);

UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Quelle phrase est correcte ?',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_lang_03';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Quelle phrase est correcte ?', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_lang_03'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_lang_03' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Complétez : « Si j’___ plus de temps, je ferais des exercices de français chaque jour. »',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_lang_06';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Complétez : « Si j’___ plus de temps, je ferais des exercices de français chaque jour. »', 1, 'B2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_lang_06'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_lang_06' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Choisissez la bonne préposition : « Elle pense souvent ___ son cours de français. »',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_lang_08';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Choisissez la bonne préposition : « Elle pense souvent ___ son cours de français. »', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_lang_08'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_lang_08' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Temps du verbe : « Hier, nous ___ au cinéma avec des amis. »',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_lang_10';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Temps du verbe : « Hier, nous ___ au cinéma avec des amis. »', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_lang_10'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_lang_10' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Quel est le contraire du mot « facile » ?',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_lang_12';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Quel est le contraire du mot « facile » ?', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_lang_12'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_lang_12' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Écrivez un message court sur votre journée.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_1';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Écrivez un message court sur votre journée.', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_1'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_1' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Parlez de vos loisirs préférés et pourquoi vous les aimez.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_2';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Parlez de vos loisirs préférés et pourquoi vous les aimez.', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_2'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_2' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Quel est le contraire du mot ''grand''?',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_4';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Quel est le contraire du mot ''grand''?', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_4'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_4' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Décrivez un jour important de votre vie en détail.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_5';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Décrivez un jour important de votre vie en détail.', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_5'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_5' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Expliquez comment vous préparez votre repas préféré.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_7';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Expliquez comment vous préparez votre repas préféré.', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_7'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_7' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Décrivez votre environnement de travail ou d''études idéal.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_9';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Décrivez votre environnement de travail ou d''études idéal.', 1, 'B2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_9'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_9' AND q2.deleted_at IS NULL);
COMMIT;
