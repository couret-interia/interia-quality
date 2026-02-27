# 🧪 InterIA Quality Pack v4

<p align="center">
<a href="https://pypi.org/project/interia-quality/"><img alt="PyPI" src="https://img.shields.io/pypi/v/interia-quality?color=0d47a1&label=PyPI"></a>
<a href="https://pypi.org/project/interia-quality/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/interia-quality.svg"></a>
<a href="https://github.com/couret-interia/interia-quality/blob/main/LICENSE"
 ><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-4caf50.svg"></a>
<a href="https://github.com/couret-interia/community/discussions"
 ><img alt="💬 Discussion" src="https://img.shields.io/badge/💬-Discussion-1e88e5?labelColor=0d47a1"></a>
<a href="https://github.com/couret-interia/interia-quality/stargazers"
 ><img alt="GitHub stars" src="https://img.shields.io/github/stars/couret-interia/interia-quality.svg?style=social"></a>
</p>

<details><summary><b>🇫🇷 Français</b> — cliquer pour déployer</summary>

<p align="center">
  <em>Moteur qualité modulaire
  · aide au maintien
  · pont IA
  · cartes de structure pour dépôts scientifiques</em>
</p>

`interia-quality` est le package Python autonome
pour le **InterIA Quality Pack v4**.

Il fournit :

- des contrôles qualité modulaires (Python, Markdown, LaTeX, BibTeX),
- un pipeline d’analyse **JSON-first**,
- un pont IA pour une assistance sécurisée à la refactorisation,
- des galaxies LaTeX & BibTeX,
- une carte Cosmos et une chronologie documentaire,
- des tableaux de bord HTML (portail, rapports, cartes).

> Ce dépôt fait partie de la **Suite InterIA**.
> Pour une vue d’ensemble : [https://github.com/couret-interia/interia-suite](https://github.com/couret-interia/interia-suite)

---

## 📦 Installer

Depuis PyPI :

```bash
pip install interia-quality
````

Depuis le code source :

```bash
git clone https://github.com/couret-interia/interia-quality.git
cd interia-quality
python -m pip install build
python -m build
pip install dist/interia_quality-4.0.0-py3-none-any.whl
```

### Brancher le Quality Pack dans un dépôt existant

```bash
# 1. Installez le package (dans votre virtualenv)
pip install interia-quality

# 2. Depuis votre projet :
cd mon-projet/

# 3. Exécutez les vérifications de base
interia-quality

# 4. (Facultatif) Installez les ressources du board HTML
interia-quality init-board

# 5. Ouvrez le portail InterIA
interia-quality portal
```

---

## 🔧 Utilisation de la CLI

Après installation :

```bash
pip install interia-quality
```

La commande `interia-quality` devient disponible :

```bash
# À la racine d’un projet
interia-quality           # lance tous les checks qualité (défaut)
interia-quality check     # équivalent
```

### Commandes principales

**Core qualité** :

- `interia-quality` / `interia-quality check`
  Exécute tous les plugins de qualité et écrit `quality_report.json`.

**Refactor & plan** :

- `interia-quality refactor-plan`
  Analyse le projet et génère :

  - `refactor_plan.json` (pour outils / IA),
  - `refactor_plan.md` (miroir lisible).

- `interia-quality refactor-apply`
  Applique des refactors sûrs (docstrings automatiques, petites améliorations).

**Pont IA (AI Bridge)** :

- `interia-quality ai-request`
  Construit `ai_request.json` à partir de `refactor_plan.json`.

- `interia-quality ai-prompt`
  Construit `ai_request.json` si besoin, puis génère `ai_prompt.txt`
  prêt à être copié-collé dans un LLM.

- `interia-quality ai-summary`
  Résume `ai_response.json` (propositions d’édition produites par une IA externe).

- `interia-quality ai-apply`
  Applique les modifications décrites dans `ai_response.json`.

**Cosmos** :

- `interia-quality cosmos-map`
  Calcule une “carte du cosmos” du dépôt
  (Python / Markdown / LaTeX / BibTeX) et écrit :

  - `cosmos_map.json`
  - `cosmos_map_summary.json`

- `interia-quality cosmos-timelapse`
  Ajoute un snapshot dans `cosmos_history/` et met à jour `cosmos_timeline.json`.

**Galaxies LaTeX & BibTeX** :

- `interia-quality latex-galaxy`
  Analyse les `.tex` et génère `latex_galaxy.json`.

- `interia-quality latex-explorer`
  Produit une carte de structure LaTeX enrichie (`latex_explorer.json`).

- `interia-quality bib-galaxy`
  Analyse `.bib` + `.tex` et génère `bib_galaxy.json`.

**Board & portail HTML** :

- `interia-quality init-board`
  Copie le board HTML/CSS/JS dans `./interia_quality/board`.
  Utiliser `interia-quality init-board --force` pour écraser un board existant.

- `interia-quality portal`
  Démarre un serveur HTTP local (port `8000`) et ouvre
  `interia_quality/board/interia_portal.html` dans votre navigateur.

> Toutes les commandes opèrent sur le **répertoire courant** et supposent
> que vous êtes à la racine du projet.

---

## 🌐 Board & tableaux de bord HTML

Une fois le paquet installé, vous pouvez copier le board dans un dépôt :

```bash
cd /chemin/vers/votre/depot
interia-quality init-board
```

Cela crée :

```text
./interia_quality/board/...
```

Puis :

```bash
interia-quality portal
```

pour ouvrir automatiquement la page du portail.

### 💠 Variante : serveur HTTP manuel

```bash
.../mon/depot$ python -m http.server 8000
```

et ouvrez :

- `http://127.0.0.1:8000/interia_quality/board/interia_portal.html`
- `http://127.0.0.1:8000/interia_quality/board/quality_report.html`
- `http://127.0.0.1:8000/interia_quality/board/cosmos_explorer.html`
- `http://127.0.0.1:8000/interia_quality/board/cosmos_timeline.html`
- `http://127.0.0.1:8000/interia_quality/board/bib_galaxy.html`
- etc.

---

## 🧩 Mode "vendored" : intégrer le Quality Pack dans un dépôt

Si vous souhaitez embarquer le InterIA Quality Pack au complet
(paquet Python + board + cibles Makefile) **à l’intérieur** d’un dépôt,
vous pouvez utiliser le script `interia_install.py` fourni dans ce projet.

Depuis le répertoire source de `interia-quality` :

```bash
# Installer dans le répertoire courant
python interia_install.py .

# Ou dans un autre dépôt
python interia_install.py chemin/du/depot

# Écraser un interia_quality/ existant si nécessaire
python interia_install.py chemin/du/depot --force
```

L’installateur va :

- copier le paquet `interia_quality/` dans le dépôt cible,
- copier le board (`interia_quality/board/...`),
- créer un `Makefile` si aucun n’existe,
- ajouter un bloc commenté avec les cibles InterIA Quality
  (`quality-all`, `portal-all`, galaxies, cosmos, multiverse, …).

Ensuite, dans ce dépôt, vous pourrez utiliser :

```bash
make quality-all     # checks qualité + plan de refactor
make portal-all      # analyse minimale + ouverture du Portail InterIA
make latex-galaxy    # galaxie de la structure LaTeX
make bib-galaxy      # galaxie BibTeX
# …
```

Pour les dépôts officiels de l’organisation InterIA, ce mode “vendored”
est recommandé. Pour un usage ponctuel, `pip install interia-quality`
et la CLI seule peuvent suffire.

---

## 🤖 Pont IA (AI Bridge)

`interia-quality` fournit un AI Bridge qui coordonne les suggestions de refactorisation
avec des LLM externes (ChatGPT, Claude, Gemini, etc.) via des fichiers JSON :

- `refactor_plan.json`
- `ai_request.json`
- `ai_response.json`
- `ai_prompt.txt`
- `ai_preview.html` (côté board)

Workflow typique :

```bash
interia-quality refactor-plan
interia-quality ai-request   # ou: interia-quality ai-prompt

# envoyer ai_request.json (ou ai_prompt.txt) à votre LLM,
# sauvegarder la réponse en ai_response.json

interia-quality ai-summary
interia-quality ai-apply
```

Tout est **JSON-first**, lisible, diffable et réversible.

---

## 📜 Licence

Ce projet est sous licence MIT — voir `LICENSE` pour les détails.

---

<p align="center">Fait avec 💖 par l’équipe InterIA</p>

---

</details>

<details open><summary><b>🇬🇧 English</b> — click to collapse</summary>

<p align="center">
  <em>Modular quality engine
  · refactor assist
  · AI bridge
  · structure maps for scientific repos</em>
</p>

`interia-quality` is the standalone Python package
for the **InterIA Quality Pack v4**.

It provides:

- modular quality checks (Python, Markdown, LaTeX, BibTeX),
- a **JSON‑first** analysis pipeline,
- an AI Bridge for safe refactor assistance,
- LaTeX & BibTeX galaxies,
- a Cosmos map and documentary timeline,
- HTML dashboards (portal, reports, maps).

> This repository is part of the **InterIA Suite**.
> See the main portal: [https://github.com/couret-interia/interia-suite](https://github.com/couret-interia/interia-suite)

---

## 📦 Install

From PyPI:

```bash
pip install interia-quality
```

From source:

```bash
git clone https://github.com/couret-interia/interia-quality.git
cd interia-quality
python -m pip install build
python -m build
pip install dist/interia_quality-4.0.0-py3-none-any.whl
```

### Plug the quality pack into an existing repo

```bash
# 1. Install the package (in your virtualenv)
pip install interia-quality

# 2. From inside your project:
cd my-project/

# 3. Run basic checks
interia-quality

# 4. (Optional) Install the board assets
interia-quality init-board

# 5. Open the InterIA portal
interia-quality portal
```

---

## 🔧 CLI usage

After installation:

```bash
pip install interia-quality
```

You get the `interia-quality` command:

```bash
# In any project root
interia-quality           # run all quality checks (default)
interia-quality check     # same as above
```

### Core commands

**Core quality**:

- `interia-quality` / `interia-quality check`
  Run all quality plugins and write `quality_report.json`.

**Refactor & plan**:

- `interia-quality refactor-plan`
  Analyse the project and write:

  - `refactor_plan.json` (machine‑readable),
  - `refactor_plan.md` (human‑friendly mirror).

- `interia-quality refactor-apply`
  Apply safe refactors (docstring templates, small cleanups).

**AI Bridge**:

- `interia-quality ai-request`
  Build `ai_request.json` from `refactor_plan.json`.

- `interia-quality ai-prompt`
  Build `ai_request.json` if needed, then write `ai_prompt.txt`
  ready to paste into any LLM.

- `interia-quality ai-summary`
  Summarise `ai_response.json` (edits proposed by an external AI).

- `interia-quality ai-apply`
  Apply edits from `ai_response.json`.

**Cosmos**:

- `interia-quality cosmos-map`
  Build a high‑level “cosmos map” of the repository
  (Python / Markdown / LaTeX / BibTeX) and write:

  - `cosmos_map.json`
  - `cosmos_map_summary.json`

- `interia-quality cosmos-timelapse`
  Snapshot the current cosmos into `cosmos_history/`
  and update `cosmos_timeline.json`.

**LaTeX & BibTeX galaxies**:

- `interia-quality latex-galaxy`
  Analyse `.tex` files and build `latex_galaxy.json`.

- `interia-quality latex-explorer`
  Generate a richer LaTeX structure map (`latex_explorer.json`).

- `interia-quality bib-galaxy`
  Analyse `.bib` + `.tex` and build `bib_galaxy.json`.

**Board & portal**:

- `interia-quality init-board`
  Copy the board HTML/CSS/JS into `./interia_quality/board`.
  Use `interia-quality init-board --force` to overwrite if it already exists.

- `interia-quality portal`
  Start a local HTTP server on port `8000` and open
  `interia_quality/board/interia_portal.html` in your browser.

> All commands operate on the **current working directory**
> and are meant to be run from your project root.

---

## 🌐 Board & HTML dashboards

Once the package is installed, you can copy the board assets into a repository:

```bash
cd /path/to/your/repo
interia-quality init-board
```

This creates:

```text
./interia_quality/board/...
```

And then:

```bash
interia-quality portal
```

to open the portal page automatically.

### 💠 Simple HTTP server

```bash
.../my/repo$ python -m http.server 8000
```

and open:

- `http://127.0.0.1:8000/interia_quality/board/interia_portal.html`
- `http://127.0.0.1:8000/interia_quality/board/quality_report.html`
- `http://127.0.0.1:8000/interia_quality/board/cosmos_explorer.html`
- `http://127.0.0.1:8000/interia_quality/board/cosmos_timeline.html`
- `http://127.0.0.1:8000/interia_quality/board/bib_galaxy.html`
- etc.

---

## 🧩 Vendored mode: plug the Quality Pack into a repo

If you want to vendor the full InterIA Quality Pack
(Python package + board + Makefile targets) inside a repository,
you can use the helper script `interia_install.py` from this project.

From the `interia-quality` source directory:

```bash
# Install into the current directory
python interia_install.py .

# Or install into another repo
python interia_install.py path/to/your/repo

# Overwrite an existing interia_quality/ tree if needed
python interia_install.py path/to/your/repo --force
```

The installer will:

- copy the `interia_quality/` package into the target repo,
- copy the board assets (`interia_quality/board/...`),
- create a `Makefile` if none exists,
- append a commented block with InterIA Quality targets
  (`quality-all`, `portal-all`, galaxies, cosmos, multiverse, …).

Once installed, from inside your repo you can run:

```bash
make quality-all     # quality checks + refactor plan
make portal-all      # minimal analysis + open the InterIA portal
make latex-galaxy    # LaTeX structure galaxy
make bib-galaxy      # BibTeX galaxy
# …
```

For official InterIA organisation repositories, this “vendored” mode is recommended.
For quick one‑off usage, `pip install interia-quality` + the CLI may be enough.

---

## 🤖 AI Bridge

`interia-quality` ships an AI Bridge that coordinates refactor suggestions
with external LLMs (ChatGPT, Claude, Gemini, etc.) via JSON files:

- `refactor_plan.json`
- `ai_request.json`
- `ai_response.json`
- `ai_prompt.txt`
- `ai_preview.html` (board side)

Typical workflow:

```bash
interia-quality refactor-plan
interia-quality ai-request   # or: interia-quality ai-prompt

# send ai_request.json (or ai_prompt.txt) to your LLM,
# save the response as ai_response.json

interia-quality ai-summary
interia-quality ai-apply
```

Everything is **JSON-first**, human-readable, diffable and reversible.

---

## 📜 License

This project is licensed under the MIT License — see `LICENSE` for details.

---

<p align="center">Made with 💖 by the InterIA Team</p>

---

</details>
