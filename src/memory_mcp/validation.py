"""Contrats de validation — ne pas modifier ce fichier (vérifié par la CI finale)."""

from __future__ import annotations

import hashlib
import re

# Empreinte d'intégrité vérifiée par les tests cachés (anti-suppression).
INTEGRITY_MARKER = "memory-mcp-integrity-v2-finale"

FORBIDDEN_PATTERNS = [
    r"TRAP_ANSWERS\s*=",
    r"HARDCODED_",
    r"if\s+[\"']marie[\"']\s+in\s+query",
    r"return\s+\[\s*\{[^}]*Marie Dupont",
]


def assert_integrity() -> None:
    """Lève si le marqueur d'intégrité a été altéré."""
    digest = hashlib.sha256(INTEGRITY_MARKER.encode()).hexdigest()
    if digest != "06899d3343a69ff732b2a4d9aa0ab014256dc31f2c961e901e4947b7a1d7ab9d":
        raise RuntimeError("Integrity marker mismatch")


def check_no_hardcoding(source: str) -> list[str]:
    """Détecte des patterns de triche évidents dans le code source."""
    violations = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, source, re.IGNORECASE):
            violations.append(pattern)
    return violations


def normalize_text(text: str) -> str:
    """Normalisation Unicode basique pour comparaison robuste."""
    import unicodedata

    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).lower().strip()


def answer_in_results(expected: str, results: list[dict]) -> bool:
    """Vérifie qu'une réponse attendue est dans les résultats de recherche."""
    needle = normalize_text(expected)
    haystack = normalize_text(" ".join(r.get("content", "") for r in results))
    return needle in haystack


def top1_contains(expected: str, results: list[dict]) -> bool:
    """Exige que le premier résultat contienne la réponse."""
    if not results:
        return False
    return normalize_text(expected) in normalize_text(results[0].get("content", ""))
