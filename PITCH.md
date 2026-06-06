# Memory MCP Challenge — One-pager

## Le problème

Un agent conversationnel qui renvoie **tout l'historique** à chaque tour voit ses coûts exploser de façon **quadratique** (40 tours ≈ 40× plus cher qu'au tour 1). Compresser aveuglément fait économiser des tokens… mais rend l'agent **amnésique**.

## La mission

Construire un **serveur MCP de mémoire** qui prouve, chiffres à l'appui, qu'on peut **réduire drastiquement les tokens tout en gardant la qualité** sur des conversations longues (30–50 tours).

## Livrables attendus

| Composant | Description |
|-----------|-------------|
| **Serveur MCP** | 4 outils : `memory_store`, `memory_search`, `memory_summarize`, `memory_stats` |
| **Agent de démo** | Assistant (support client ou code) tenant une conversation longue |
| **Benchmark** | Même conversation ×2 : mode naïf vs mode mémoire |
| **Dashboard** | Visualisation côte à côte tokens + score qualité |

## Les deux axes de mesure (critères de succès)

### Axe coût
- Tokens totaux sur toute la conversation
- Coût estimé en €
- **Cible indicative** : −70 à −85 % vs mode naïf sur 40 tours (à mesurer, pas à promettre)

### Axe qualité
- ~10 questions « pièges » dont la réponse dépend d'infos données plus tôt
- Score : X/10 réussies dans chaque mode
- **Succès** : économie significative **ET** qualité maintenue (≥ 80 % des pièges)

## Découpage équipe (3 personnes)

1. **Serveur MCP + outils** — exposition des 4 tools, intégration SDK MCP
2. **Retrieval & compression** — embeddings, index vectoriel, résumé intelligent
3. **Agent + benchmark + dashboard** — démo live, harnais de mesure, visualisation

## Stack suggérée (24–48h)

- Python 3.11+, SDK MCP officiel
- SQLite + index vectoriel léger (sqlite-vec, Chroma…)
- Embeddings : modèle local ou API
- Dashboard : page web simple lisant `memory_stats()`

## Démo jury (money shot)

1. Lancer la conversation longue en live
2. Montrer les compteurs : rouge (naïf) qui grimpe, vert (mémoire) qui stagne
3. Graphe final + encadré « économie : X tokens = Y € »
4. Poser une question piège → l'agent répond juste via `memory_search`

## CI / qualité code

Ce dépôt inclut une **CI GitHub Actions** qui doit passer :
- `ruff check` + `ruff format --check`
- `pytest` (tests unitaires + smoke benchmark)

Les PR qui cassent la CI ne sont pas mergées.

## Getting started

```bash
git clone https://github.com/INTELO2026/memory-mcp-challenge.git
cd memory-mcp-challenge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -v
python -m benchmark.harness
```

## Ce qui est déjà fait (squelette)

- [x] Structure projet + CI
- [x] 4 outils MCP stubés et fonctionnels
- [x] Stockage SQLite + recherche basique
- [x] Harnais benchmark naïf vs mémoire
- [x] Questions pièges + tests
- [x] Dashboard HTML (à brancher)

## Ce que vous devez améliorer

- [ ] Vrais embeddings (remplacer le bag-of-words)
- [ ] Résumé LLM dans `memory_summarize`
- [ ] Agent de démo connecté au serveur MCP
- [ ] Dashboard live branché sur les résultats
- [ ] Mesures réelles sur 40+ tours
