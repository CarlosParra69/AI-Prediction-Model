"""
Módulo para detectar y reportar sesgos en evaluación.

Implementa checks automáticos de sesgo:
- No usa datos sensibles (edad, género, raza, etc.)
- Calcula métricas agregadas por grupo demográfico si se proporciona
- Reporta desviaciones > threshold (e.g., 10%)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class BiasReport:
    """Reporte de análisis de sesgo."""

    has_demographic_data: bool
    total_samples: int
    groups_analyzed: List[str]
    group_statistics: Dict[str, Dict[str, float]]  # {group: {"mean": x, "std": y, "count": z}}
    suspicious_deviations: List[str]  # Reporta si algún grupo difiere > threshold
    recommendation: str


class BiasChecker:
    """
    Verificador de sesgos en datos de evaluación.
    
    Detecta datos sensibles que no deberían usarse.
    Calcula estadísticas de scoring por grupo demográfico.
    Alerta si hay desviaciones significativas.
    """

    # Palabras clave que indican datos sensibles
    SENSITIVE_KEYWORDS = {
        "age", "edad",
        "gender", "género", "sexo", "male", "female", "hombre", "mujer",
        "race", "raza", "ethnicity", "etnicidad",
        "religion", "religión",
        "disability", "discapacidad",
        "national_origin", "origen_nacional",
        "marital_status", "estado_civil",
        "sexual_orientation", "orientación_sexual",
    }

    def __init__(self, deviation_threshold: float = 0.10):
        """
        Args:
            deviation_threshold: Umbral de desviación permitida (default 10%).
                                Se reporta si algún grupo difiere más de este porcentaje.
        """
        self.deviation_threshold = deviation_threshold

    def check_training_data(
        self,
        samples: List[Dict],
        score_field: str = "score",
        demographic_field: Optional[str] = None,
    ) -> BiasReport:
        """
        Analiza datos de entrenamiento para detectar sesgos.

        Args:
            samples: Lista de samples de entrenamiento.
            score_field: Nombre del campo de score en cada sample.
            demographic_field: Campo que contiene datos demográficos 
                             (e.g., 'demographics' con subkeys 'age', 'gender').

        Returns:
            BiasReport con análisis completo.
        """
        if not samples:
            return BiasReport(
                has_demographic_data=False,
                total_samples=0,
                groups_analyzed=[],
                group_statistics={},
                suspicious_deviations=[],
                recommendation="No hay samples para analizar.",
            )

        # Verifica si hay datos sensibles en los samples
        has_sensitive_data = self._check_for_sensitive_data(samples)

        # Si hay campo demográfico, analiza por grupo
        group_stats = {}
        suspicious = []
        groups_analyzed = []
        
        if demographic_field and any(demographic_field in s for s in samples):
            group_stats, suspicious = self._analyze_by_group(
                samples=samples,
                score_field=score_field,
                demographic_field=demographic_field,
            )
            groups_analyzed = list(group_stats.keys())

        # Construye recomendación
        recommendation = self._build_recommendation(
            has_sensitive_data=has_sensitive_data,
            suspicious=suspicious,
            groups_analyzed=groups_analyzed,
        )

        return BiasReport(
            has_demographic_data=bool(demographic_field and groups_analyzed),
            total_samples=len(samples),
            groups_analyzed=groups_analyzed,
            group_statistics=group_stats,
            suspicious_deviations=suspicious,
            recommendation=recommendation,
        )

    def _check_for_sensitive_data(self, samples: List[Dict]) -> bool:
        """Verifica si hay datos sensibles en los samples."""
        all_text = str(samples).lower()
        return any(keyword in all_text for keyword in self.SENSITIVE_KEYWORDS)

    def _analyze_by_group(
        self,
        samples: List[Dict],
        score_field: str,
        demographic_field: str,
    ) -> tuple[Dict[str, Dict[str, float]], List[str]]:
        """
        Analiza scores agrupados por campo demográfico.

        Returns:
            (group_stats, suspicious_deviations)
        """
        groups: Dict[str, List[float]] = {}

        for sample in samples:
            if demographic_field not in sample:
                continue

            demo = sample[demographic_field]
            # Si es dict, extrae valores; si es string, úsalo como key
            if isinstance(demo, dict):
                for key, value in demo.items():
                    group_key = f"{key}={value}"
                    if group_key not in groups:
                        groups[group_key] = []
                    if score_field in sample:
                        groups[group_key].append(float(sample[score_field]))
            else:
                group_key = str(demo)
                if group_key not in groups:
                    groups[group_key] = []
                if score_field in sample:
                    groups[group_key].append(float(sample[score_field]))

        # Calcula estadísticas por grupo
        group_stats = {}
        for group, scores in groups.items():
            if not scores:
                continue
            
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            std = variance ** 0.5
            
            group_stats[group] = {
                "mean": round(mean, 3),
                "std": round(std, 3),
                "count": len(scores),
            }

        # Identifica desviaciones sospechosas
        suspicious = self._detect_suspicious_deviations(group_stats)

        return group_stats, suspicious

    def _detect_suspicious_deviations(self, group_stats: Dict[str, Dict[str, float]]) -> List[str]:
        """Detecta grupos que se desvían significativamente de la media global."""
        if not group_stats or len(group_stats) < 2:
            return []

        # Media global
        all_means = [g["mean"] for g in group_stats.values()]
        global_mean = sum(all_means) / len(all_means)

        suspicious = []
        for group, stats in group_stats.items():
            deviation = abs(stats["mean"] - global_mean) / (global_mean + 1e-6)
            if deviation > self.deviation_threshold:
                suspicious.append(
                    f"Grupo '{group}': media {stats['mean']:.3f}, "
                    f"desviación {deviation*100:.1f}% (global {global_mean:.3f})"
                )

        return suspicious

    def _build_recommendation(
        self,
        has_sensitive_data: bool,
        suspicious: List[str],
        groups_analyzed: List[str],
    ) -> str:
        """Construye recomendación basada en análisis."""
        parts = []

        if has_sensitive_data:
            parts.append(
                "⚠️ Se detectaron datos sensibles potenciales. "
                "Asegurate de no usar edad, género, raza u otra info demográfica en scoring."
            )

        if suspicious:
            parts.append(
                f"⚠️ Se detectaron posibles sesgos: {', '.join(suspicious)}. "
                "Revisa la calidad y representatividad de tus datos."
            )
        elif groups_analyzed:
            parts.append(
                f"✓ Análisis de {len(groups_analyzed)} grupos demográficos: "
                "no se detectaron desviaciones significativas."
            )

        if not parts:
            parts.append("✓ No se detectaron problemas inmediatos de sesgo.")

        return " ".join(parts)

    def is_data_suitable_for_evaluation(self, sample: Dict) -> bool:
        """
        Verifica si un sample de evaluación es adecuado (no contiene datos sensibles).

        Args:
            sample: Un sample individual de evaluación.

        Returns:
            True si es seguro usar para evaluación, False si contiene datos sensibles.
        """
        all_text = str(sample).lower()
        return not any(keyword in all_text for keyword in self.SENSITIVE_KEYWORDS)
