# Memory MCP Challenge

**Hackathon INTELO2026** — Serveur MCP de mémoire avec benchmark chiffré tokens/qualité.

> Construisez un serveur MCP qui prouve qu'on peut réduire drastiquement les tokens d'un agent conversationnel **sans le rendre amnésique**.

## Contexte

| Mode | Comportement | Coût tokens |
|------|-------------|-------------|
| **Naïf** | Renvoie tout l'historique à chaque tour | Croissance quadratique |
| **Mémoire MCP** | Stocke, recherche, résume | Quasi plat |

Le benchmark mesure les deux axes : **coût** (tokens/€) et **qualité** (questions pièges).

## Structure

```
memory-mcp-challenge/
├── src/memory_mcp/     # Serveur MCP + 4 outils
├── benchmark/          # Harnais naïf vs mémoire
├── demo/               # Agent de démo (stub)
├── dashboard/          # Visualisation benchmark
├── tests/              # Tests unitaires + intégration
└── .github/workflows/  # CI (lint + tests)
```

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

## Utilisation

### Lancer les tests

```bash
pytest -v
```

### Linter

```bash
ruff check src tests benchmark demo
ruff format src tests benchmark demo
```

### Benchmark

```bash
python -m benchmark.harness
```

### Serveur MCP

```bash
memory-mcp
# ou
python -m memory_mcp.server
```

### Agent de démo

```bash
python demo/agent.py
```

## Les 4 outils MCP

| Outil | Description |
|-------|-------------|
| `memory_store(content, tags)` | Stocke un fragment de mémoire |
| `memory_search(query, top_k)` | Recherche sémantique |
| `memory_summarize(session)` | Résumé compressé de l'historique |
| `memory_stats()` | Tokens consommés |

## CI

Chaque push/PR sur `main` ou `develop` déclenche :
1. **Lint** — `ruff check` + `ruff format --check`
2. **Tests** — `pytest` + smoke benchmark

## Pitch complet

Voir [PITCH.md](PITCH.md) pour le one-pager destiné au jury / proposition de sujet.

## Licence

Projet hackathon INTELO2026 — usage libre dans le cadre de l'événement.
