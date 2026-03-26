-- Generado por scripts/generate_bank_seeds.py (no editar a mano; volver a ejecutar el script).
-- FILL_BLANK: interaction drag_drop_fill_blank + allow_manual_input para UI híbrida.

BEGIN;
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'WRITING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'WRITING_TEXT',
  prompt = 'Racontez une expérience de voyage mémorable.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'B1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_11';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'WRITING_TEXT', 'Racontez une expérience de voyage mémorable.', 1, 'B1', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_11'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'WRITING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_11' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Nous ___ allés au marché hier matin.',
  options_json = '{"elements": ["sommes", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "sommes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_13';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Nous ___ allés au marché hier matin.', 1, 'A2', '{"elements": ["sommes", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "sommes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}', true, 'q_fr_13'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_13' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Mon chat dort toujours ___ le canapé.',
  options_json = '{"elements": ["sur", "dans", "sous", "suis"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "sur", "score": 1.0}, {"text": "dans", "score": 1.0}, {"text": "sous", "score": 1.0}, {"text": "suis", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_14';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Mon chat dort toujours ___ le canapé.', 1, 'A1', '{"elements": ["sur", "dans", "sous", "suis"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "sur", "score": 1.0}, {"text": "dans", "score": 1.0}, {"text": "sous", "score": 1.0}, {"text": "suis", "score": 0.15}]}', true, 'q_fr_14'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_14' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Elle a ___ un excellent résultat à son examen de français.',
  options_json = '{"elements": ["obtenu", "eu", "reçu", "suis"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "obtenu", "score": 1.0}, {"text": "eu", "score": 1.0}, {"text": "reçu", "score": 1.0}, {"text": "suis", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_15';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Elle a ___ un excellent résultat à son examen de français.', 1, 'A2', '{"elements": ["obtenu", "eu", "reçu", "suis"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "obtenu", "score": 1.0}, {"text": "eu", "score": 1.0}, {"text": "reçu", "score": 1.0}, {"text": "suis", "score": 0.15}]}', true, 'q_fr_15'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_15' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'ORDERING',
  prompt = 'Remettez ces étapes dans l''ordre correct pour préparer des pâtes.',
  options_json = '{"elements": ["Égoutter les pâtes.", "Faire bouillir l''eau.", "Servir dans une assiette.", "Saler l''eau.", "Ajouter les pâtes."], "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_16';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'ORDERING', 'Remettez ces étapes dans l''ordre correct pour préparer des pâtes.', 1, 'A2', '{"elements": ["Égoutter les pâtes.", "Faire bouillir l''eau.", "Servir dans une assiette.", "Saler l''eau.", "Ajouter les pâtes."], "image_description": null}'::jsonb, NULL, true, 'q_fr_16'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_16' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'ORDERING',
  prompt = 'Remettez ces moments de la journée dans l''ordre chronologique.',
  options_json = '{"elements": ["Le dîner", "Le petit-déjeuner", "Le déjeuner", "Le goûter"], "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_17';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'ORDERING', 'Remettez ces moments de la journée dans l''ordre chronologique.', 1, 'A1', '{"elements": ["Le dîner", "Le petit-déjeuner", "Le déjeuner", "Le goûter"], "image_description": null}'::jsonb, NULL, true, 'q_fr_17'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_17' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Que font les personnes sur l''image?',
  options_json = '{"elements": null, "image_description": "Un groupe d''étudiants en train d''étudier ensemble dans une bibliothèque universitaire."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_1';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Que font les personnes sur l''image?', 1, 'A1', '{"elements": null, "image_description": "Un groupe d''étudiants en train d''étudier ensemble dans une bibliothèque universitaire."}'::jsonb, NULL, true, 'q_img_1'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_1' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Décrivez ce que vous voyez sur l''image.',
  options_json = '{"elements": null, "image_description": "Une jeune femme travaillant sur un ordinateur portable dans un café, avec une tasse de café sur la table."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_2';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Décrivez ce que vous voyez sur l''image.', 1, 'A2', '{"elements": null, "image_description": "Une jeune femme travaillant sur un ordinateur portable dans un café, avec une tasse de café sur la table."}'::jsonb, NULL, true, 'q_img_2'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_2' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Quel lieu représente cette image?',
  options_json = '{"elements": null, "image_description": "Une gare SNCF avec des voyageurs attendant sur le quai, un panneau affichant les horaires des trains."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_3';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Quel lieu représente cette image?', 1, 'A1', '{"elements": null, "image_description": "Une gare SNCF avec des voyageurs attendant sur le quai, un panneau affichant les horaires des trains."}'::jsonb, NULL, true, 'q_img_3'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_3' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'SPEAKING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'SPEAKING_RECORD',
  prompt = 'Présentez-vous en quelques phrases : votre prénom, votre âge, votre profession et un loisir que vous aimez.',
  options_json = '{"elements": null, "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_18';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'SPEAKING_RECORD', 'Présentez-vous en quelques phrases : votre prénom, votre âge, votre profession et un loisir que vous aimez.', 1, 'A2', '{"elements": null, "image_description": null}'::jsonb, NULL, true, 'q_fr_18'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'SPEAKING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_18' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Je ___ très content aujourd''hui.',
  options_json = '{"elements": ["suis", "es", "est", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "suis", "score": 1.0}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}, {"text": "sommes", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_19';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Je ___ très content aujourd''hui.', 1, 'A1', '{"elements": ["suis", "es", "est", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "suis", "score": 1.0}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}, {"text": "sommes", "score": 0.15}]}', true, 'q_fr_19'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_19' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Tu ___ en retard pour le cours.',
  options_json = '{"elements": ["es", "suis", "est", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "es", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "est", "score": 0.15}, {"text": "sommes", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_20';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Tu ___ en retard pour le cours.', 1, 'A1', '{"elements": ["es", "suis", "est", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "es", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "est", "score": 0.15}, {"text": "sommes", "score": 0.15}]}', true, 'q_fr_20'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_20' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Il ___ malade depuis deux jours.',
  options_json = '{"elements": ["est", "suis", "es", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "est", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "sommes", "score": 0.15}]}',
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_21';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Il ___ malade depuis deux jours.', 1, 'A1', '{"elements": ["est", "suis", "es", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "est", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "sommes", "score": 0.15}]}', true, 'q_fr_21'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_21' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Nous ___ très fatigués après le voyage.',
  options_json = '{"elements": ["sommes", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "sommes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_22';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Nous ___ très fatigués après le voyage.', 1, 'A2', '{"elements": ["sommes", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "sommes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}', true, 'q_fr_22'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_22' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Vous ___ prêts pour l''examen de français.',
  options_json = '{"elements": ["êtes", "etes", "suis", "es"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "êtes", "score": 1.0}, {"text": "etes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_23';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Vous ___ prêts pour l''examen de français.', 1, 'A2', '{"elements": ["êtes", "etes", "suis", "es"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "êtes", "score": 1.0}, {"text": "etes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}]}', true, 'q_fr_23'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_23' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Elles ___ toujours en avance au travail.',
  options_json = '{"elements": ["sont", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "sont", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_24';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Elles ___ toujours en avance au travail.', 1, 'A2', '{"elements": ["sont", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "sont", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}', true, 'q_fr_24'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_24' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Hier je ___ allé au cinéma avec mes amis.',
  options_json = '{"elements": ["suis", "es", "est", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "suis", "score": 1.0}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}, {"text": "sommes", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_25';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Hier je ___ allé au cinéma avec mes amis.', 1, 'A2', '{"elements": ["suis", "es", "est", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "suis", "score": 1.0}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}, {"text": "sommes", "score": 0.15}]}', true, 'q_fr_25'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_25' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Nous ___ arrivés très tard à la maison.',
  options_json = '{"elements": ["sommes", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "sommes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_26';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Nous ___ arrivés très tard à la maison.', 1, 'A2', '{"elements": ["sommes", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "sommes", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}', true, 'q_fr_26'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_26' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Ils ___ partis en vacances la semaine dernière.',
  options_json = '{"elements": ["sont", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "sont", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_27';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Ils ___ partis en vacances la semaine dernière.', 1, 'A2', '{"elements": ["sont", "suis", "es", "est"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "sont", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "est", "score": 0.15}]}', true, 'q_fr_27'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_27' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'FILL_BLANK',
  prompt = 'Ma sœur ___ née en 2005.',
  options_json = '{"elements": ["est", "suis", "es", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb,
  correct_answer_json = '{"blank_index": 0, "candidates": [{"text": "est", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "sommes", "score": 0.15}]}',
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_28';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'FILL_BLANK', 'Ma sœur ___ née en 2005.', 1, 'A2', '{"elements": ["est", "suis", "es", "sommes"], "image_description": null, "interaction": "drag_drop_fill_blank", "allow_manual_input": true}'::jsonb, '{"blank_index": 0, "candidates": [{"text": "est", "score": 1.0}, {"text": "suis", "score": 0.15}, {"text": "es", "score": 0.15}, {"text": "sommes", "score": 0.15}]}', true, 'q_fr_28'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_28' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Que fait la personne sur l''image?',
  options_json = '{"elements": null, "image_description": "Un homme cuisinant dans une cuisine moderne, en train de couper des légumes sur une planche."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_4';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Que fait la personne sur l''image?', 1, 'A1', '{"elements": null, "image_description": "Un homme cuisinant dans une cuisine moderne, en train de couper des légumes sur une planche."}'::jsonb, NULL, true, 'q_img_4'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_4' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'IMAGE',
  prompt = 'Où se trouve cette scène?',
  options_json = '{"elements": null, "image_description": "Des personnes assises à une terrasse de café en plein air, avec des parasols et des tables."}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A2',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_img_5';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'IMAGE', 'Où se trouve cette scène?', 1, 'A2', '{"elements": null, "image_description": "Des personnes assises à une terrasse de café en plein air, avec des parasols et des tables."}'::jsonb, NULL, true, 'q_img_5'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_img_5' AND q2.deleted_at IS NULL);
UPDATE pie_pt_questions q SET
  section_id = (SELECT s2.id FROM pie_pt_exam_sections s2 JOIN pie_pt_exams e2 ON e2.id = s2.exam_id
    WHERE e2.id = '00000000-0000-0000-0000-000000000302'::uuid AND s2.type = 'READING' AND s2.deleted_at IS NULL LIMIT 1),
  type = 'ORDERING',
  prompt = 'Remettez les étapes du matin dans l''ordre logique.',
  options_json = '{"elements": ["Se lever.", "Prendre le petit-déjeuner.", "Se laver.", "S''habiller."], "image_description": null}'::jsonb,
  correct_answer_json = NULL,
  difficulty_level = 'A1',
  is_active = true, deleted_at = NULL
WHERE q.external_code = 'q_fr_30';
INSERT INTO pie_pt_questions (section_id, type, prompt, weight, difficulty_level, options_json, correct_answer_json, is_active, external_code)
SELECT s.id, 'ORDERING', 'Remettez les étapes du matin dans l''ordre logique.', 1, 'A1', '{"elements": ["Se lever.", "Prendre le petit-déjeuner.", "Se laver.", "S''habiller."], "image_description": null}'::jsonb, NULL, true, 'q_fr_30'
FROM pie_pt_exam_sections s JOIN pie_pt_exams e ON e.id = s.exam_id
WHERE e.id = '00000000-0000-0000-0000-000000000302'::uuid AND s.type = 'READING' AND s.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM pie_pt_questions q2 WHERE q2.external_code = 'q_fr_30' AND q2.deleted_at IS NULL);
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_lang_03') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Elle travaille dans un bureau chaque jour.', 1, true FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_03' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Elle travailler dans un bureau chaque jour.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_03' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Elle travaillant dans un bureau chaque jour.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_03' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Elle travailles dans un bureau chaque jour.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_03' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_lang_06') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'ai', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_06' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'avais', 2, true FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_06' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'aurai', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_06' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'ayant', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_06' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_lang_08') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'à', 1, true FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_08' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'de', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_08' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'dans', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_08' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'pour', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_08' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_lang_10') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'sommes allés', 1, true FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_10' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'avons allé', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_10' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'allions', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_10' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'sommes allées', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_10' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_lang_12') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'difficile', 1, true FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_12' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'rapide', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_12' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'court', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_12' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'nouveau', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_lang_12' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_4') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'petit', 1, true FROM pie_pt_questions q WHERE q.external_code = 'q_fr_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'long', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'haut', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'épais', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_4' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_16') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Égoutter les pâtes.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Faire bouillir l''eau.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Servir dans une assiette.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Saler l''eau.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_16' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Ajouter les pâtes.', 5, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_16' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_17') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Le dîner', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_17' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Le petit-déjeuner', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_17' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Le déjeuner', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_17' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Le goûter', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_17' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_1') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Ils étudient.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_1' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Ils mangent.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_1' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Ils jouent au football.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_1' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Ils regardent un film.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_1' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_2') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Une femme dans un café avec son ordinateur.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_2' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Une femme dans une bibliothèque.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_2' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Une femme en train de cuisiner.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_2' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Une femme qui fait du sport.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_2' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_3') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Une gare.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Un aéroport.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Une station de métro.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_3' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Un supermarché.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_3' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_4') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Il cuisine.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Il lit un livre.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Il fait du sport.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_4' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Il travaille à l''ordinateur.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_4' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_5') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'À la terrasse d''un café.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_5' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Dans une salle de classe.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_5' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Au supermarché.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_5' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'À la plage.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_img_5' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_30') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Se lever.', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_30' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Prendre le petit-déjeuner.', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_30' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Se laver.', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_30' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'S''habiller.', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_30' LIMIT 1;
DELETE FROM pie_pt_question_options WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_fr_18') AND deleted_at IS NULL;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option A', 1, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_18' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option B', 2, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_18' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option C', 3, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_18' LIMIT 1;
INSERT INTO pie_pt_question_options (question_id, option_text, display_order, is_correct)
SELECT q.id, 'Option D', 4, false FROM pie_pt_questions q WHERE q.external_code = 'q_fr_18' LIMIT 1;

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
SELECT 'seed-fr-q_img_1-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-fr-q_img_1-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_1') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_1'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-fr-q_img_1-img'
WHERE q.external_code = 'q_img_1';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-fr-q_img_2-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-fr-q_img_2-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_2') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_2'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-fr-q_img_2-img'
WHERE q.external_code = 'q_img_2';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-fr-q_img_3-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-fr-q_img_3-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_3') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_3'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-fr-q_img_3-img'
WHERE q.external_code = 'q_img_3';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-fr-q_img_4-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-fr-q_img_4-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_4') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_4'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-fr-q_img_4-img'
WHERE q.external_code = 'q_img_4';

INSERT INTO pie_pt_media_files (storage_key, kind, mime_type, size_bytes, sha256)
SELECT 'seed-fr-q_img_5-img', 'IMAGE', 'image/jpeg', 1, NULL::text
WHERE NOT EXISTS (SELECT 1 FROM pie_pt_media_files mf WHERE mf.storage_key = 'seed-fr-q_img_5-img' AND mf.deleted_at IS NULL);
DELETE FROM pie_pt_question_media WHERE question_id IN (SELECT id FROM pie_pt_questions WHERE external_code = 'q_img_5') AND kind = 'IMAGE' AND deleted_at IS NULL;
INSERT INTO pie_pt_question_media (question_id, kind, media_file_id, external_url)
SELECT q.id, 'IMAGE', mf.id, 'https://example.invalid/q_img_5'
FROM pie_pt_questions q
JOIN pie_pt_media_files mf ON mf.storage_key = 'seed-fr-q_img_5-img'
WHERE q.external_code = 'q_img_5';
COMMIT;
