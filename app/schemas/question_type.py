"""
Enum centralizado de tipos de preguntas de examen.

Todos los módulos del sistema deben importar QuestionType desde aquí
en lugar de usar comparaciones con strings directas.
"""

from enum import Enum


class QuestionType(str, Enum):
    """
    Tipos de preguntas soportados por el sistema de evaluación.

    Tipos activos:
        FILL_BLANK      - Rellenar huecos con texto libre
        SINGLE_CHOICE   - Opción múltiple con una respuesta correcta
        ORDERING        - Reordenar elementos en secuencia correcta
        IMAGE           - Pregunta basada en imagen + opción múltiple
        WRITING_TEXT    - Texto libre evaluado con rúbrica DELF
        SPEAKING_RECORD - Grabación de voz (arquitectura preparada)

    Tipos futuros (arquitectura preparada):
        AUDIO           - Comprensión auditiva
        VIDEO           - Comprensión visual

    Valores legacy (compatibilidad hacia atrás):
        mcq             - Alias de SINGLE_CHOICE
        open            - Alias de WRITING_TEXT
        short_answer    - Alias de WRITING_TEXT
        essay           - Alias de WRITING_TEXT
    """

    # ── Tipos activos ────────────────────────────────────────────────────────
    FILL_BLANK = "fill_blank"
    SINGLE_CHOICE = "single_choice"
    ORDERING = "ordering"
    IMAGE = "image"
    WRITING_TEXT = "writing_text"
    SPEAKING_RECORD = "speaking_record"

    # ── Tipos futuros (arquitectura preparada) ───────────────────────────────
    AUDIO = "audio"
    VIDEO = "video"

    # ── Legacy (backward compatibility) ─────────────────────────────────────
    mcq = "mcq"
    short_answer = "short_answer"
    essay = "essay"
    open = "open"

    # ── Helpers ──────────────────────────────────────────────────────────────

    def is_choice_based(self) -> bool:
        """Devuelve True si la pregunta requiere seleccionar entre opciones."""
        return self in {
            QuestionType.SINGLE_CHOICE,
            QuestionType.IMAGE,
            QuestionType.mcq,
        }

    def is_open_text(self) -> bool:
        """Devuelve True si la pregunta requiere respuesta de texto libre."""
        return self in {
            QuestionType.WRITING_TEXT,
            QuestionType.open,
            QuestionType.short_answer,
            QuestionType.essay,
        }

    def is_fill_blank(self) -> bool:
        return self == QuestionType.FILL_BLANK

    def is_ordering(self) -> bool:
        return self == QuestionType.ORDERING

    def is_speaking(self) -> bool:
        return self == QuestionType.SPEAKING_RECORD

    def requires_human_review_by_default(self) -> bool:
        """Devuelve True para tipos que aún no tienen scoring automático."""
        return self in {QuestionType.AUDIO, QuestionType.VIDEO}
