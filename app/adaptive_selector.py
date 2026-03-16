"""
Módulo para seleccionar preguntas adaptativas basadas en desempeño.

Implementa un algoritmo adaptativo simple pero robusto:
- Comienza en dificultad 3
- Sube dificultad si score reciente >= 0.8
- Baja dificultad si score reciente <= 0.4
- Mantiene ability_estimate como media móvil de scores
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AbilityState:
    """Estado de habilidad del candidato durante examen adaptativo."""

    current_difficulty: int  # 1-5
    ability_estimate: float  # Media móvil de scores (0-1)
    last_score: float  # Score de la última pregunta (0-1)
    questions_answered: int  # Contador de preguntas contestadas
    recent_scores: list[float]  # Últimos N scores para análisis


class AdaptiveSelector:
    """
    Selector adaptativo de preguntas.
    
    Implementa un algoritmo simple:
    - Comienza en dificultad 3
    - Ajusta basado en últimos scores
    - Computa ability_estimate para mapeo a nivel DELF
    """

    def __init__(
        self,
        start_difficulty: int = 3,
        threshold_high: float = 0.75,
        threshold_low: float = 0.45,
        window_size: int = 3,
    ):
        """
        Args:
            start_difficulty: Dificultad inicial (1-5). Default: 3 (medio).
            threshold_high: Si score >= threshold_high, subir dificultad.
            threshold_low: Si score <= threshold_low, bajar dificultad.
            window_size: Número de scores recientes a mantener.
        """
        self.start_difficulty = start_difficulty
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        self.window_size = window_size

    def initialize_state(self) -> AbilityState:
        """Inicializa el estado de habilidad para un examen."""
        return AbilityState(
            current_difficulty=self.start_difficulty,
            ability_estimate=0.5,  # Asunción neutral
            last_score=0.5,
            questions_answered=0,
            recent_scores=[],
        )

    def update_state(
        self,
        state: AbilityState,
        current_score: float,
    ) -> AbilityState:
        """
        Actualiza el estado de habilidad basado en respuesta actual.

        Args:
            state: Estado actual de habilidad.
            current_score: Score de la pregunta recién contestada (0-1).

        Returns:
            Nuevo estado de habilidad con dificultad ajustada y ability_estimate actualizado.
        """
        # Añade el score a la ventana de scores recientes
        recent = state.recent_scores + [current_score]
        if len(recent) > self.window_size:
            recent = recent[-self.window_size :]

        # Actualiza ability_estimate como media de scores recientes
        ability_estimate = sum(recent) / len(recent) if recent else state.ability_estimate

        # Lógica adaptativa: ajusta dificultad basada en último score
        new_difficulty = state.current_difficulty
        if current_score >= self.threshold_high:
            new_difficulty = min(5, state.current_difficulty + 1)
        elif current_score <= self.threshold_low:
            new_difficulty = max(1, state.current_difficulty - 1)

        return AbilityState(
            current_difficulty=new_difficulty,
            ability_estimate=ability_estimate,
            last_score=current_score,
            questions_answered=state.questions_answered + 1,
            recent_scores=recent,
        )

    def recommend_next_question(
        self,
        state: AbilityState,
        topic: Optional[str] = None,
    ) -> dict:
        """
        Recomienda siguiente pregunta basada en estado actual.

        Args:
            state: Estado actual de habilidad.
            topic: Tema opcional (si hay temas disponibles a rotar).

        Returns:
            Dict con 'difficulty', 'topic' (si aplica), y 'reason'.
        """
        return {
            "difficulty": state.current_difficulty,
            "topic": topic,
            "reason": self._build_reason(state),
        }

    def _build_reason(self, state: AbilityState) -> str:
        """Construye explicación de la recomendación."""
        if state.questions_answered == 0:
            return "Pregunta inicial, dificultad media."

        if state.last_score >= self.threshold_high:
            return f"Desempeño alto ({state.last_score:.2f}), aumentando dificultad."
        elif state.last_score <= self.threshold_low:
            return f"Desempeño bajo ({state.last_score:.2f}), reduciendo dificultad."
        else:
            return f"Desempeño moderado ({state.last_score:.2f}), manteniendo dificultad."

    def estimate_delf_level(self, ability_estimate: float) -> str:
        """
        Mapea ability_estimate (0-1) a nivel DELF.

        Args:
            ability_estimate: Media de scores (0-1).

        Returns:
            Nivel DELF estimado (A1-, A1, A1+, ..., B2+).
        """
        # Umbrales calibrados para el rango real de scoring del sistema (0.35–0.95).
        # El open_response_scorer produce scores entre ~0.35 (texto muy corto con errores
        # graves) y ~0.93 (escritura B2 fluida). Los umbrales están ajustados para que
        # el level_score compuesto (writing×0.8 + overall×0.2) produzca etiquetas DELF
        # coherentes con la calidad lingüística observada en los exámenes de referencia.
        thresholds = [
            (0.35, "A1-"),
            (0.42, "A1"),
            (0.47, "A1+"),
            (0.52, "A2-"),
            (0.66, "A2"),
            (0.684, "A2+"),
            (0.72, "B1-"),
            (0.77, "B1"),
            (0.83, "B1+"),
            (0.88, "B2-"),
            (0.93, "B2"),
        ]

        for threshold, level in thresholds:
            if ability_estimate <= threshold:
                return level

        return "B2+"

    def get_state_summary(self, state: AbilityState) -> dict:
        """Retorna resumen del estado actual."""
        return {
            "questions_answered": state.questions_answered,
            "current_difficulty": state.current_difficulty,
            "ability_estimate": round(state.ability_estimate, 3),
            "last_score": round(state.last_score, 3),
            "estimated_level": self.estimate_delf_level(state.ability_estimate),
            "recent_scores": [round(s, 3) for s in state.recent_scores],
        }
