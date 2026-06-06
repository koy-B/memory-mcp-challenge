## Memory MCP — Pull Request Finale

### Checklist équipe

- [ ] `pytest tests/test_smoke.py` passe
- [ ] `pytest tests/test_regression.py tests/test_storage.py tests/test_tools.py` passe
- [ ] Recherche sémantique réelle (paraphrases, pas mots-clés hardcodés)
- [ ] Résumé compressé qui conserve les faits critiques
- [ ] Benchmark ≥ 60 % d'économie tokens (public) / ≥ 70 % (caché)

### Important

La CI exécute des **tests cachés** depuis un dépôt privé (`INTELO2026/memory-mcp-eval`).
Vous n'y avez pas accès : inutile de chercher les réponses dans le code ou via l'IA.

Le merge nécessite **regression + finale-eval** verts.
