PYTHON ?= python3
MAKE_S ?= $(MAKE) -s

.PHONY: portal-all portal-html
.PHONY: quality-all quality-help
.PHONY: quality quality-serve refactor-plan refactor-apply
.PHONY: latex-galaxy latex-galaxy-html latex-explorer latex-explorer-html bib-galaxy bib-galaxy-html
.PHONY: cosmos-map cosmos-map-html
.PHONY: cosmos-timelapse cosmos-timeline cosmos-timeline-html
.PHONY: multiverse-map multiverse-cli
.PHONY: multiverse-3d multiverse-3d-html
.PHONY: multiverse-gravity multiverse-bridges multiverse-thematic-bridges
.PHONY: ai-request ai-summary ai-apply ai-prompt
.PHONY: ai-preview ai-serve ai-stop server-stop

# 🧩 Commande complète : qualité + plan de refactor
quality-all: quality refactor-plan
	@echo "✨ InterIA: quality checks + refactor plan generated."

# 🧩 Aide
quality-help:
	@echo "🧭 InterIA Quality Pack v4 — Commands:"
	@echo "  make quality-all           # Quality + Refactor Plan"
	@echo "  make quality               # Quality only"
	@echo "  make quality-serve         # Open quality_report.html (via local server)"
	@echo '  make multiverse-gravity    # Args: repos="../repo ../repo2 ../repo3" Build a multiverse-level analysis. Nb: Run `make cosmos-map` in repo’s before.'
	@echo '  make multiverse-map        # Args: repos="../repo ../repo2 ../repo3" Build a multiverse-level analysis. Nb: Run `make cosmos-map` in repo’s before.'
	@echo '  make multiverse-cli        # Print ASCII heatmap of the multiverse distance matrix. Nb: Run after `make multiverse-map`.'
	@echo '  make multiverse-3d         # Args: repos="../repo ../repo2 ../repo3" Build a multiverse-level analysis in 3D. Nb: Run `make multiverse-map` in repo’s before.'
	@echo '  make multiverse-3d-html    # Args: repos="../repo ../repo2 ../repo3" Open multiverse_3d.html via local server'
	@echo '  make multiverse-bridges    # Compute thematic resonance and code bridges between repositories. Alias of `multiverse-thematic-bridges`.'
	@echo '                             # Nb: Run like this `make multiverse-map repos="../repo ../repo2 ../repo3" multiverse-bridges`'
	@echo "  make cosmos-map            # Unifies all analysis (PY, MD, TEX, BIB) layers into a single cosmic JSON"
	@echo "  make cosmos-map-html       # Open cosmos_map.html via local server"
	@echo "  make cosmos-timeline       # Builds/updates cosmos_timeline.json (cosmos-timelapse alias)"
	@echo "  make cosmos-timeline-html  # Open cosmos_history preview (cosmos_timeline.html via local server)"
	@echo "  make latex-galaxy          # Build LaTeX Galaxy Map of structure across a repository"
	@echo "  make latex-galaxy-html     # Open LaTeX Galaxy Map preview (latex_galaxy.html via local server)"
	@echo "  make bib-galaxy            # Builds a Galaxy Map of bibliographic references across a LaTeX project"
	@echo "  make bib-galaxy-html       # Open LaTeX Galaxy Map of bibliographic references (bib_galaxy.html via local server)"
	@echo "  make latex-explorer        # Build LaTeX Explorer Galaxy map of structure across a repository"
	@echo "  make latex-explorer-html   # Open LaTeX Galaxy Map preview (latex_explorer.html via local server)"
	@echo "  make refactor-plan         # Build refactor plan"
	@echo "  make refactor-apply        # Apply safe refactors"
	@echo "  make ai-request            # Build ai_request.json"
	@echo "  make ai-prompt             # Build ai_request + open ai_prompt.txt"
	@echo "  make ai-preview            # Open ai_preview.html (via local server)"
	@echo "  make ai-summary            # Summarize the AI response"
	@echo "  make ai-apply              # Apply AI edits"
	@echo "  make ai-serve              # Run Local server"
	@echo "  make portal-all            # Run minimal and Open Portal page (via local server)"
	@echo "  make portal-html           # Open Portal page (via local server)"
	@echo "  make ai-stop               # Stop preview server"
	@echo "  make server-stop           # Force stop server on port 8000"

quality:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.engine
	@echo "💡 Use 'make quality-serve' to open quality_report.html"

portal-all: quality-all cosmos-timelapse latex-galaxy bib-galaxy latex-explorer portal-html

portal-html: ai-serve
	@echo "📡 Open InterIA Portal.."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/interia_portal.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/interia_portal.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/interia_portal.html"
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

# make multiverse-map repos="../repo1 ../repo2 ../repo3" multiverse_bridges
multiverse-thematic-bridges:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.multiverse.thematic_bridges

multiverse-bridges: multiverse-thematic-bridges # Alias

multiverse-3d:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.multiverse.multiverse_3d $(repos)


multiverse-3d-html: multiverse-3d ai-serve
	@echo "🌠 Launching Multiverse 3D Explorer..."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/multiverse_3d.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/multiverse_3d.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/multiverse_3d.html"
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

multiverse-map:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.multiverse.multiverse_map $(repos)

multiverse-gravity: multiverse-map
	@PYTHONPATH=. $(PYTHON) -m interia_quality.multiverse.multiverse_gravity

multiverse-cli:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.multiverse.multiverse_cli

cosmos-map:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.cosmos.cosmos_map

cosmos-map-html: cosmos-map ai-serve
	@echo "🌌 Starting InterIA COSMOS Explorer..."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/cosmos_explorer.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/cosmos_explorer.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/cosmos_explorer.html in your browser."
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

cosmos-timelapse: cosmos-map
	@PYTHONPATH=. $(PYTHON) -m interia_quality.cosmos.cosmos_timelapse
cosmos-timeline: cosmos-timelapse

cosmos-timeline-html: cosmos-timelapse ai-serve
	@echo "🌌 Launching COSMOS TIMELINE viewer..."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/cosmos_timeline.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/cosmos_timeline.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/cosmos_timeline.html"
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

bib-galaxy:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.galaxy.bibtex_galaxy

bib-galaxy-html: bib-galaxy ai-serve
	@echo "🌐 Starting BibTeX Galaxy Explorer..."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/bib_galaxy.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/bib_galaxy.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/bib_galaxy.html in your browser."
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

latex-galaxy:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.doctor.latex_galaxy

latex-galaxy-html: latex-galaxy ai-serve
	@echo "🌌 Starting LaTeX Galaxy preview..."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/doctor_latex_galaxy.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/doctor_latex_galaxy.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/doctor_latex_galaxy.html in your browser."
	@echo "💡 AI preview running at http://127.0.0.1:8000/interia_quality/board/doctor_latex_galaxy.html"
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

latex-explorer: latex-galaxy
	@PYTHONPATH=. $(PYTHON) -m interia_quality.galaxy.latex_explorer

latex-explorer-html: latex-explorer ai-serve
	@echo "📡 Starting LaTeX Galaxy explorer..."
	@xdg-open http://127.0.0.1:8000/interia_quality/board/galaxy_latex_explorer.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/galaxy_latex_explorer.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/galaxy_latex_explorer.html in your browser."
	@echo "💡 AI preview running at http://127.0.0.1:8000/interia_quality/board/galaxy_latex_explorer.html"
	@echo "👉 Use 'make ai-stop' or 'make server-stop' when you're done."

refactor-plan:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.refactor.plan
	@echo "💡 Use 'make ai-prompt' to open 'ai_prompt.txt'."

refactor-apply:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.refactor.apply

ai-request: refactor-plan
	@PYTHONPATH=. $(PYTHON) -m interia_quality.refactor.ai_bridge build

ai-prompt: ai-request
	@PYTHONPATH=. $(PYTHON) -m interia_quality.refactor.ai_bridge prompt
	@xdg-open ai_prompt.txt || open ai_prompt.txt

ai-summary:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.refactor.ai_bridge summary

ai-preview: ai-serve
	@xdg-open http://127.0.0.1:8000/interia_quality/board/ai_preview.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/ai_preview.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/ai_preview.html in your browser."
	@echo "💡 AI preview running at http://127.0.0.1:8000/interia_quality/board/ai_preview.html"
	@echo "👉 Use 'make ai-stop' when you're done."

ai-apply:
	@PYTHONPATH=. $(PYTHON) -m interia_quality.refactor.ai_apply

quality-serve: ai-serve
	@xdg-open http://127.0.0.1:8000/interia_quality/board/quality_report.html 2>/dev/null || \
	 open http://127.0.0.1:8000/interia_quality/board/quality_report.html 2>/dev/null || \
	 echo "ℹ️  Please open http://127.0.0.1:8000/interia_quality/board/quality_report.html in your browser."
	@echo "💡 Quality preview running at http://127.0.0.1:8000/interia_quality/board/quality_report.html"
	@echo "👉 Use 'make ai-stop' when you're done."

ai-serve:
	@pids=$$(lsof -t -i:8000 2>/dev/null); \
	if [ -f .ai_server_pid ] || [ -n "$$pids" ]; then \
	  echo "ℹ️  Server already running on http://127.0.0.1:8000."; \
	else \
	  echo "🌐 Starting local server..."; \
	  PYTHONPATH=. $(PYTHON) -m http.server 8000 > /dev/null 2>&1 & \
	  echo $$! > .ai_server_pid; \
	  sleep 2; \
	  echo "✅ Server running on http://127.0.0.1:8000."; \
	fi

ai-stop:
	@echo "🛑 Stopping local server..."
	@if [ -f .ai_server_pid ]; then \
	  pid=$$(cat .ai_server_pid); \
	  if kill $$pid 2>/dev/null; then \
	    echo "✅ Server (PID $$pid) stopped."; \
	  else \
	    echo "⚠️  The process was already stopped."; \
	    $(MAKE_S) server-stop; \
	  fi; \
	  rm -f .ai_server_pid; \
	else \
	  echo "ℹ️  No .ai_server_pid file found."; \
	  $(MAKE_S) server-stop; \
	fi

server-stop:
	@echo "🛑 Forced stop of port 8000..."
	@pids=$$(lsof -t -i:8000 2>/dev/null); \
	if [ -n "$$pids" ]; then \
	  kill $$pids 2>/dev/null || true; \
	  echo "✅ Stopped processes: $$pids"; \
	else \
	  echo "ℹ️  Port 8000 is already free."; \
	fi