-- Generado por scripts/generate_bank_seeds.py (no editar a mano; volver a ejecutar el script).
-- FILL_BLANK: interaction drag_drop_fill_blank + allow_manual_input para UI híbrida.

BEGIN;
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'They ___ in this city since 2020.',
  options_json = '{"elements": ["have lived", "have been living", "''ve lived", "''ve been living"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "have lived", "score": 1.0}, {"text": "have been living", "score": 1.0}, {"text": "''ve lived", "score": 1.0}, {"text": "''ve been living", "score": 1.0}]}',
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_13';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'They ___ in this city since 2020.', 1, 'B1', '{"elements": ["have lived", "have been living", "''ve lived", "''ve been living"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "have lived", "score": 1.0}, {"text": "have been living", "score": 1.0}, {"text": "''ve lived", "score": 1.0}, {"text": "''ve been living", "score": 1.0}]}', true, 'q_en_13'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_13' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'This email ___ sent to all students yesterday.',
  options_json = '{"elements": ["was", "were", "is", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "was", "score": 1.0}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}, {"text": "are", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_14';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'This email ___ sent to all students yesterday.', 1, 'A2', '{"elements": ["was", "were", "is", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "was", "score": 1.0}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}, {"text": "are", "score": 0.15}]}', true, 'q_en_14'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_14' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'At the airport, the officer asked: "Could you ___ me your passport, please?"',
  options_json = '{"elements": ["show", "hand", "was", "were"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "show", "score": 1.0}, {"text": "hand", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_15';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'At the airport, the officer asked: "Could you ___ me your passport, please?"', 1, 'A2', '{"elements": ["show", "hand", "was", "were"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "show", "score": 1.0}, {"text": "hand", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}]}', true, 'q_en_15'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_15' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'ORDERING',
  prompt = 'Put these steps in a logical order for writing a short formal email in English.',
  options_json = '{"elements": ["State clearly why you are writing.", "Use an appropriate greeting (e.g. Dear Mr Smith,).", "Sign off politely (e.g. Best regards,).", "Write a clear subject line."], "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_16';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'ORDERING', 'Put these steps in a logical order for writing a short formal email in English.', 1, 'A2', '{"elements": ["State clearly why you are writing.", "Use an appropriate greeting (e.g. Dear Mr Smith,).", "Sign off politely (e.g. Best regards,).", "Write a clear subject line."], "image_description": null}'::jsonb, NULL, true, 'q_en_16'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_16' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'ORDERING',
  prompt = 'Order these parts of the day from earliest to latest.',
  options_json = '{"elements": ["dinner", "breakfast", "lunch", "mid-afternoon snack"], "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_17';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'ORDERING', 'Order these parts of the day from earliest to latest.', 1, 'A1', '{"elements": ["dinner", "breakfast", "lunch", "mid-afternoon snack"], "image_description": null}'::jsonb, NULL, true, 'q_en_17'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_17' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'What are the people in the image doing?',
  options_json = '{"elements": null, "image_description": "A group of students studying together with books and laptops in a university library."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_en_1';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'What are the people in the image doing?', 1, 'A1', '{"elements": null, "image_description": "A group of students studying together with books and laptops in a university library."}'::jsonb, NULL, true, 'q_img_en_1'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_en_1' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Which option best describes what you see?',
  options_json = '{"elements": null, "image_description": "A person working on a laptop at a small table in a café, with a cup of coffee nearby."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_en_2';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Which option best describes what you see?', 1, 'A2', '{"elements": null, "image_description": "A person working on a laptop at a small table in a café, with a cup of coffee nearby."}'::jsonb, NULL, true, 'q_img_en_2'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_en_2' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Where is this scene most likely taking place?',
  options_json = '{"elements": null, "image_description": "A teacher pointing at a whiteboard with grammar notes while learners sit at desks with notebooks."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_en_3';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Where is this scene most likely taking place?', 1, 'A1', '{"elements": null, "image_description": "A teacher pointing at a whiteboard with grammar notes while learners sit at desks with notebooks."}'::jsonb, NULL, true, 'q_img_en_3'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_en_3' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'SPEAKING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SPEAKING_RECORD',
  prompt = 'Introduce yourself in a few sentences: your name, where you are from, your job or studies, and one thing you like doing in English class or when you practise English.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_18';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SPEAKING_RECORD', 'Introduce yourself in a few sentences: your name, where you are from, your job or studies, and one thing you like doing in English class or when you practise English.', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_18'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'SPEAKING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_18' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Give a balanced view: what are two advantages and two disadvantages of learning English mainly through apps and short videos? Use connectors such as however, on the other hand, and therefore where appropriate.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'C2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_19';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Give a balanced view: what are two advantages and two disadvantages of learning English mainly through apps and short videos? Use connectors such as however, on the other hand, and therefore where appropriate.', 1, 'C2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_19'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_19' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'I ___ very happy with my progress this month.',
  options_json = '{"elements": ["am", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "am", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_20';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'I ___ very happy with my progress this month.', 1, 'A1', '{"elements": ["am", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "am", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}', true, 'q_en_20'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_20' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'She ___ a doctor; she works at the local clinic.',
  options_json = '{"elements": ["is", "was", "were", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "is", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "are", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_21';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'She ___ a doctor; she works at the local clinic.', 1, 'A1', '{"elements": ["is", "was", "were", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "is", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "are", "score": 0.15}]}', true, 'q_en_21'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_21' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'We ___ ready to start the listening exercise.',
  options_json = '{"elements": ["are", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "are", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_22';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'We ___ ready to start the listening exercise.', 1, 'A1', '{"elements": ["are", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "are", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}', true, 'q_en_22'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_22' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Last year they ___ complete beginners; now they are intermediate.',
  options_json = '{"elements": ["were", "was", "is", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "were", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "is", "score": 0.15}, {"text": "are", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_23';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Last year they ___ complete beginners; now they are intermediate.', 1, 'A2', '{"elements": ["were", "was", "is", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "were", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "is", "score": 0.15}, {"text": "are", "score": 0.15}]}', true, 'q_en_23'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_23' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'He ___ finished the online module before the deadline.',
  options_json = '{"elements": ["has", "''s", "was", "were"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "has", "score": 1.0}, {"text": "''s", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_24';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'He ___ finished the online module before the deadline.', 1, 'A2', '{"elements": ["has", "''s", "was", "were"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "has", "score": 1.0}, {"text": "''s", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}]}', true, 'q_en_24'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_24' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = '___ you ever spoken English outside the classroom?',
  options_json = '{"elements": ["Have", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "Have", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_25';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', '___ you ever spoken English outside the classroom?', 1, 'A2', '{"elements": ["Have", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "Have", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}', true, 'q_en_25'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_25' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'If the sentence starts with "There", complete: There ___ many ways to practise listening.',
  options_json = '{"elements": ["are", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "are", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_26';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'If the sentence starts with "There", complete: There ___ many ways to practise listening.', 1, 'A2', '{"elements": ["are", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "are", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}', true, 'q_en_26'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_26' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'She suggested that we ___ the new vocabulary in sentences.',
  options_json = '{"elements": ["use", "should use", "was", "were"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "use", "score": 1.0}, {"text": "should use", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}]}',
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_27';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'She suggested that we ___ the new vocabulary in sentences.', 1, 'B1', '{"elements": ["use", "should use", "was", "were"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "use", "score": 1.0}, {"text": "should use", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}]}', true, 'q_en_27'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_27' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'The article ___ published on the school blog last Friday.',
  options_json = '{"elements": ["was", "were", "is", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "was", "score": 1.0}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}, {"text": "are", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_28';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'The article ___ published on the school blog last Friday.', 1, 'A2', '{"elements": ["was", "were", "is", "are"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "was", "score": 1.0}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}, {"text": "are", "score": 0.15}]}', true, 'q_en_28'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_28' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Could I have ___ umbrella? It is starting to rain. (one umbrella, first mention)',
  options_json = '{"elements": ["an", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "an", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_29';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Could I have ___ umbrella? It is starting to rain. (one umbrella, first mention)', 1, 'A2', '{"elements": ["an", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "an", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}', true, 'q_en_29'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_29' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Turn left ___ the corner and you will see the language centre.',
  options_json = '{"elements": ["at", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "at", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_30';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Turn left ___ the corner and you will see the language centre.', 1, 'A2', '{"elements": ["at", "was", "were", "is"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "at", "score": 1.0}, {"text": "was", "score": 0.15}, {"text": "were", "score": 0.15}, {"text": "is", "score": 0.15}]}', true, 'q_en_30'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_30' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Which question is formed correctly?',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_31';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Which question is formed correctly?', 1, 'A1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_31'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_31' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SINGLE_CHOICE',
  prompt = 'Choose the correct comparative: "This exercise is ___ than the one we did yesterday."',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_32';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SINGLE_CHOICE', 'Choose the correct comparative: "This exercise is ___ than the one we did yesterday."', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_32'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_32' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'ORDERING',
  prompt = 'Put these classroom instructions in a sensible order for starting a pairwork activity.',
  options_json = '{"elements": ["Compare your answers with your partner.", "Read the questions silently.", "Work alone for three minutes.", "Listen to the example on the audio."], "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_33';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'ORDERING', 'Put these classroom instructions in a sensible order for starting a pairwork activity.', 1, 'A2', '{"elements": ["Compare your answers with your partner.", "Read the questions silently.", "Work alone for three minutes.", "Listen to the example on the audio."], "image_description": null}'::jsonb, NULL, true, 'q_en_33'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_33' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'What is the person doing in the image?',
  options_json = '{"elements": null, "image_description": "A person wearing headphones and typing on a keyboard, with a language-learning website visible on the screen."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_en_4';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'What is the person doing in the image?', 1, 'A1', '{"elements": null, "image_description": "A person wearing headphones and typing on a keyboard, with a language-learning website visible on the screen."}'::jsonb, NULL, true, 'q_img_en_4'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_en_4' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'What does this scene show?',
  options_json = '{"elements": null, "image_description": "Two people face to face, gesturing, with speech bubbles suggesting a conversation in a quiet corner of a bookshop."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_en_5';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'What does this scene show?', 1, 'A2', '{"elements": null, "image_description": "Two people face to face, gesturing, with speech bubbles suggesting a conversation in a quiet corner of a bookshop."}'::jsonb, NULL, true, 'q_img_en_5'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_en_5' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000301'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'You arrived late to your English lesson. Write a very short note (to your teacher) apologising and giving one brief reason.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_en_34';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'You arrived late to your English lesson. Write a very short note (to your teacher) apologising and giving one brief reason.', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_en_34'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000301'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_en_34' AND q2.deleted_at IS NULL);
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_3') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'She work in an office every day.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'She works in an office every day.', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'She working in an office every day.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_3' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_4') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'easy', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'hard', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'quick', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'short', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_4' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_6') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'on', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_6' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'at', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_6' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'in', 3, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_6' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'for', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_6' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_8') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'study', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_8' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'studied', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_8' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'studying', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_8' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'am studying', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_8' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_10') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'have', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_10' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'had', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_10' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'will have', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_10' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'having', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_10' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_12') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'do a mistake', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_12' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'make a mistake', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_12' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'make homework', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_12' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'do a break', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_12' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_16') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'State clearly why you are writing.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Use an appropriate greeting (e.g. Dear Mr Smith,).', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Sign off politely (e.g. Best regards,).', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Write a clear subject line.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_16' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_17') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'dinner', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_17' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'breakfast', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_17' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'lunch', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_17' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'mid-afternoon snack', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_17' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_1') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'They are studying.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_1' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'They are cooking.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_1' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'They are playing football.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_1' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'They are watching a film.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_1' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_2') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Someone working on a laptop in a café.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_2' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Someone reading in a hospital.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_2' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Someone swimming in a pool.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_2' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Someone driving a bus.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_2' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_3') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'In a language classroom.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'In a restaurant kitchen.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'On a sports field.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'At a concert hall.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_3' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_31') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Where you live?', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_31' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Where do you live?', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_31' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Where does you live?', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_31' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Where living you?', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_31' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_32') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'more easy', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_32' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'easier', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_en_32' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'more easier', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_32' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'easyer', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_32' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_33') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Compare your answers with your partner.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_33' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Read the questions silently.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_33' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Work alone for three minutes.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_33' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Listen to the example on the audio.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_33' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_4') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Doing an online English exercise.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Cooking dinner.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Playing tennis.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Painting a wall.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_4' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_5') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'A conversation between two people.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_5' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'A swimming lesson.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_5' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'A car repair.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_5' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'A weather forecast on TV.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_en_5' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_en_18') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option A', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_18' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option B', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_18' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option C', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_18' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option D', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_en_18' LIMIT 1;

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


INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-en-q_img_en_1-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-en-q_img_en_1-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_1') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_en_1'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-en-q_img_en_1-img'
WHERE q.external_code = 'q_img_en_1';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-en-q_img_en_2-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-en-q_img_en_2-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_2') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_en_2'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-en-q_img_en_2-img'
WHERE q.external_code = 'q_img_en_2';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-en-q_img_en_3-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-en-q_img_en_3-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_3') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_en_3'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-en-q_img_en_3-img'
WHERE q.external_code = 'q_img_en_3';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-en-q_img_en_4-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-en-q_img_en_4-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_4') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_en_4'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-en-q_img_en_4-img'
WHERE q.external_code = 'q_img_en_4';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-en-q_img_en_5-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-en-q_img_en_5-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_en_5') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_en_5'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-en-q_img_en_5-img'
WHERE q.external_code = 'q_img_en_5';
COMMIT;
