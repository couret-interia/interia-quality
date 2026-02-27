# 🧭 InterIA Refactor Assist – AI Tour (v4)

Ce document explique comment utiliser le **mode Refactor Assist**
d’InterIA Quality Pack v4, avec (ou sans) IA externe.

---

## 🇫🇷 1. Vue d’ensemble

Le flux complet se déroule en 5 étapes :

1. **Quality + Plan de refactor**

    ```bash
    make
    ```

    → génère :

    - `quality_report.json`
    - `refactor_plan.json`
    - `refactor_plan.md`

2. **Génération de la requête IA**

    ```bash
    make ai-request
    ```

    → génère :

    - `ai_request.json`
    - `ai_prompt.txt` (optionnel, généré par `make ai-prompt`)

3. **Consultation d’une IA externe**

    - Ouvrir `ai_request.json` (ou `ai_prompt.txt`)
    - Copier/coller dans ChatGPT / Claude / Gemini / Perplexity / ...
    - L’IA va produire un `ai_response.json` au format convenu

4. **Prévisualisation des edits IA**

    ```bash
    make ai-preview
    ```

    → démarre un petit serveur local sur `http://127.0.0.1:8000`
    → ouvre `ai_preview.html` dans le navigateur
    → affiche les edits proposés (fichier, lignes, old/new snippet, rationale)

5. **Application des edits IA**

    ```bash
    make ai-apply
    ```

    → lit `ai_response.json`
    → crée des backups (`.interia-ai-backup`)
    → applique les modifications là où c’est sûr

---

## 🇫🇷 2. Détails des commandes

### `make`

- Lance les checks qualité (plugins v4)
- Construit le plan de refactor :

  - `refactor_plan.json` (version machine)
  - `refactor_plan.md` (version humaine / cosmique)

### `make ai-request`

- Requiert que `refactor_plan.json` existe.
- Construit `ai_request.json` à partir du plan.
- Ce fichier est pensé comme un contrat JSON à envoyer à une IA externe.

### `make ai-preview`

- Démarre un serveur HTTP local sur le port 8000 (sauf s’il tourne déjà)
- Ouvre `ai_preview.html` dans le navigateur
- Affiche les edits contenus dans `ai_response.json`

### `make ai-apply`

- Lit `ai_response.json`
- Crée un backup par fichier modifié (`*.interia-ai-backup`)
- Applique les `new_snippet` aux fichiers cibles (avec des garde-fous)

---

## 🇫🇷 3. Contrat JSON avec l’IA

### Entrée IA – `ai_request.json`

- Contient :

  - `project`
  - `version`
  - `context`
  - `suggestions` (reprend `refactor_plan.json`)
  - `instructions` (ce que l’on attend de l’IA)

### Sortie IA – `ai_response.json`

L’IA doit renvoyer un JSON du type :

```json
{
  "project": "interia_quality_pack_v4",
  "edits": [
    {
      "file": "interia_quality/refactor/python_refactor.py",
      "kind": "python_function_refactor",
      "location": {"start_line": 14, "end_line": 74},
      "old_snippet": "",
      "new_snippet": "def scan_file(path: Path): ...",
      "rationale": "Short docstring added..."
    }
  ]
}
```

---

## 🇬🇧 4. English Summary

**InterIA Refactor Assist v4** introduces an AI-agnostic workflow:

1. `make`
    → quality checks, `refactor_plan.json`, `refactor_plan.md`

2. `make ai-request`
    → build `ai_request.json` from the refactor plan

3. Use any external LLM (ChatGPT / Claude / Gemini)
    → paste `ai_request.json` and ask for a structured `ai_response.json`

4. `make ai-preview`
    → open `ai_preview.html` and browse the proposed edits

5. `make ai-apply`
    → backup + apply edits where safe

The JSON contract is transparent, human-readable, and does not
tie InterIA to a specific AI provider.

---

## 🌌 5. Philosophie

> *“Ce fichier est un miroir des endroits où le projet peut devenir plus clair,
> plus lisible, plus généreux pour le prochain contributeur.”*

L’IA n’est pas un oracle : c’est un collègue.
Le pont IA InterIA n’est pas une boîte noire : c’est un dialogue JSON ↔ JSON.
L’humain garde toujours le dernier mot.
