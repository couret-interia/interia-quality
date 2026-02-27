#!/usr/bin/env python3
"""
cli.py — InterIA Quality Pack v4 CLI

This module exposes the `interia-quality` command via pyproject.toml.

Usage examples:
    interia-quality
    interia-quality refactor-plan
    interia-quality ai-request
    interia-quality cosmos-map
    interia-quality init-board
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from typing import Union

import importlib.resources as resources

def _run_quality_engine() -> int:
    """Run the main quality engine (equivalent to `make quality`)."""
    from . import engine
    return engine.main()


def _run_refactor_plan() -> int:
    """Build the refactor plan (refactor_plan.json + .md)."""
    from .refactor import plan
    return plan.main()


def _run_refactor_apply() -> int:
    """Apply safe refactors from refactor_plan.json."""
    from .refactor import apply
    return apply.main()


def _run_ai_request() -> int:
    """Build ai_request.json from refactor_plan.json."""
    from .refactor import ai_bridge
    return ai_bridge.main_build()


def _run_ai_prompt() -> int:
    """Build ai_prompt.txt from ai_request.json (and refactor plan if needed)."""
    from .refactor import ai_bridge
    return ai_bridge.main_prompt()


def _run_ai_summary() -> int:
    """Summarize ai_response.json."""
    from .refactor import ai_bridge
    return ai_bridge.main_summary()


def _run_ai_apply() -> int:
    """Apply AI edits from ai_response.json."""
    from .refactor import ai_apply
    return ai_apply.main()


def _run_cosmos_map() -> int:
    """Build cosmos_map.json and cosmos_map_summary.json."""
    from .cosmos import cosmos_map
    return cosmos_map.main()


def _run_cosmos_timelapse() -> int:
    """Record a snapshot into cosmos_history and update cosmos_timeline.json."""
    from .cosmos import cosmos_timelapse
    return cosmos_timelapse.main()


def _run_latex_explorer() -> int:
    """Build LaTeX Explorer galaxy from all .tex files."""
    from .galaxy import latex_explorer
    return latex_explorer.main()


def _run_latex_galaxy() -> int:
    """Build LaTeX galaxy (latex_galaxy.json) from all .tex files."""
    from .doctor import latex_galaxy
    return latex_galaxy.main()


def _run_bib_galaxy() -> int:
    """Build BibTeX galaxy (bib_galaxy.json) from all .bib + .tex files."""
    from .galaxy import bibtex_galaxy
    return bibtex_galaxy.main()

import http.server
import socketserver
import threading
import webbrowser
import time
import re
from contextlib import suppress
from urllib.parse import parse_qs
# https://stackoverflow.com/a/71025791 (https://stackoverflow.com/questions/71024723/is-there-a-python-function-equivalent-to-the-ob-start-and-ob-get-clean-in-ph)
from io import StringIO


class _PortalRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for the InterIA portal.

    Returns 404 for /favicon.ico to avoid noisy log entries.
    """
    # https://www.homedutech.com/faq/python/how-to-set-a-header-with-python39s-simplehttpserver.html
    def end_headers(self):
        """Add CORS in response header."""
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


    def flush_headers(self):
        """Add missing charset UTF-8 in 'Content-type' response header."""
        j = -1;
        for i in self._headers_buffer:
            j += 1
            if i.startswith(b'Content-type:') and not i.endswith(b'UTF-8\r\n'): # Add encode
                i = i.replace(b'\r\n', b'; charset=UTF-8\r\n')
                self._headers_buffer[j] = i
                break
        super().flush_headers()


    def do_GET(self):  # type: ignore[override]
        """Handle GET requests, run some commands, ignoring /favicon.ico."""
        output = ''
        # Has query (idea: why not a function)
        if self.path != re.sub('[?&]', '', self.path):
            tpath, _, query = self.path.partition('?')
            if query != None:
                gets = parse_qs(query)
                if 'run' in gets:
                    r = gets.get('run')[0] # unhashable type: 'list'
                    # In python howto get `print` result in cli like `ob_start` in php
                    # Create a string buffer
                    buffer = StringIO()
                    # Redirect stdout to the buffer
                    sys.stdout = buffer
                    globals()['run_command'](r, [])
                    # Reset stdout to default
                    sys.stdout = sys.__stdout__
                    # Get the output from the buffer
                    output = buffer.getvalue()
                    # Close the buffer
                    buffer.close()

                    # if tpath.endswith('ai_preview.html'):
                        # todo:
                        # howto call action, howto edit json (idea ai_responses.json like: edits[x].ok = 1/0 (str???) All at begining
                        # when apply by web(idea cardx click apply this snippet) / cli / make

        if output: # output buffer
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(output)))
            super().end_headers() # basic
            self.wfile.write(output.strip().encode('utf-8')) # need binary
            print(f"👇 Try ⚙f web portal to run in CLI: {r}")
            print(output) # Show buffer in CLI

        # Idea for get is served by cli
        elif self.path == "/webcli.html":
            self.send_response(http.HTTPStatus.OK)
            self.end_headers()
        elif self.path == "/favicon.ico":
            self.send_response(404)
            self.end_headers()
        else:
            try:
                super().do_GET()
            except BrokenPipeError as e:
                # print(f'⚠️  {e}')
                pass


def _start_portal_server(port: int) -> socketserver.TCPServer:
    """Create the HTTP server that serves the current directory."""
    return socketserver.TCPServer(("127.0.0.1", port), _PortalRequestHandler)


def _open_portal_url(url: str) -> None:
    """Open the portal URL in the default browser with a fallback message."""
    try:
        webbrowser.open(url)
    except Exception:
        print(f"ℹ️  Please open {url} in your browser.")


def _run_server_loop(httpd: socketserver.TCPServer) -> None:
    """Run the HTTP server in a background daemon thread."""

    def serve() -> None:
        """Run the HTTP server until it is stopped.

        Any exception raised by the underlying server loop is suppressed so that
        the CLI does not crash on transient server errors.
        """
        with suppress(Exception):
            httpd.serve_forever()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()


def _wait_for_server_shutdown(httpd: socketserver.TCPServer) -> None:
    """Block until Ctrl+C is pressed, then shut down the server."""
    print("👉 Press Ctrl+C in this terminal to stop the server.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping server...")
        httpd.shutdown()
        httpd.server_close()


def _run_portal() -> int:
    """
    Start a local HTTP server and open the InterIA board portal.

    - Serves the current directory on http://127.0.0.1:8000
    - Opens interia_quality/board/interia_portal.html in the default browser
    - Runs until Ctrl+C
    """
    port = 8000
    root = Path.cwd()
    portal_path = root / "interia_quality" / "board" / "interia_portal.html"
    url = f"http://127.0.0.1:{port}/interia_quality/board/interia_portal.html"

    if not portal_path.exists():
        print("❌ interia_quality/board/interia_portal.html not found.")
        print("   Run `interia-quality init-board` in this repository first.")
        return 1

    try:
        httpd = _start_portal_server(port)
    except OSError:
        print(f"ℹ️  Port {port} already in use. Assuming a server is running.")
        print(f"   Try opening: {url}")
        _open_portal_url(url)
        return 0

    _run_server_loop(httpd)

    print(f"🌐 Local server started on http://127.0.0.1:{port}")
    print(f"📡 Opening portal: {url}")
    _open_portal_url(url)

    _wait_for_server_shutdown(httpd)
    return 0


def _copy_board_tree() -> int:
    """
    Copy the installed `interia_quality/board` into the current repository.

    Target layout:
        ./interia_quality/board/...

    This is useful when the package was installed via pip and we want the
    HTML/CSS/JS locally in a repo.

    If force=True and the target directory already exists, it will be removed first.
    """
    target_root = Path.cwd() / "interia_quality" / "board"

    if target_root.exists():
        if not force:
            print(f"⚠️  Target directory already exists: {target_root}")
            print("    Aborting for safety. Use `init-board --force` to overwrite.")
            return 1
        else:
            print(f"🧹 Removing existing board directory: {target_root}")
            import shutil
            shutil.rmtree(target_root)

    # Get the 'board' directory from the installed package
    try:
        board_root = resources.files("interia_quality") / "board"
    except Exception as e:
        print(f"❌ Unable to locate 'interia_quality/board' in the installed package: {e}")
        return 1

    if not board_root.is_dir():
        print("❌ 'interia_quality/board' is not a directory in the installed package.")
        return 1

    def copy_traversable(src, dst: Path) -> None:
        """Recursively copy a Traversable tree into a local filesystem directory."""
        dst.mkdir(parents=True, exist_ok=True)
        for entry in src.iterdir():
            if entry.is_dir():
                copy_traversable(entry, dst / entry.name)
            else:
                (dst / entry.name).write_bytes(entry.read_bytes())

    print(f"📁 Copying board assets into {target_root}")
    copy_traversable(board_root, target_root)
    print("✅ Board copied. You can now open files under interia_quality/board/ in this repo.")
    return 0


def print_help() -> int:
    """Print CLI help."""
    prog = Path(sys.argv[0]).name
    print("InterIA Quality Pack v4 — CLI")
    print(f"Usage: {prog} [command]")
    print("")
    print("Core commands (CLI):")
    print("  (no command)        Run quality engine (default)")
    print("  check               Run quality engine")
    print("  refactor-plan       Build refactor plan")
    print("  refactor-apply      Apply safe refactors")
    print("  ai-request          Build ai_request.json from refactor_plan.json")
    print("  ai-prompt           Build ai_prompt.txt (LLM-ready prompt)")
    print("  ai-summary          Summarize ai_response.json")
    print("  ai-apply            Apply AI edits")
    print("  cosmos-map          Build cosmos_map.json + summary")
    print("  cosmos-timelapse    Append a snapshot to cosmos_history + timeline")
    print("  latex-galaxy        Build LaTeX galaxy")
    print("  latex-explorer      Build LaTeX Explorer galaxy")
    print("  bib-galaxy          Build BibTeX galaxy")
    print("  init-board          Copy board HTML/CSS/JS into ./interia_quality/board")
    print("                      (use `init-board --force` to overwrite)")
    print("  portal              Start a local server and open the InterIA Portal")
    print("")
    print("Advanced features (via Makefile in the full pack):")
    print("  multiverse-*        Multiverse mapping, gravity, bridges, 3D explorer")
    print("  *-html              Serve local HTTP and open board visualisations")
    print("  portal-*            Portal launcher (board HTML entry point)")
    print("")
    print("The CLI acts on the current working directory.")
    return 0


def run_command(cmd: str, extra_args: list[str]) -> int:
    """
    Execute the corresponding function for the given command.
    """
    commands = {
        "-h": print_help,
        "--help": print_help,
        "help": print_help,
        "check": _run_quality_engine,
        "quality": _run_quality_engine,
        "refactor-plan": _run_refactor_plan,
        "refactor-apply": _run_refactor_apply,
        "ai-request": _run_ai_request,
        "ai-prompt": _run_ai_prompt,
        "ai-summary": _run_ai_summary,
        "ai-apply": _run_ai_apply,
        "cosmos-map": _run_cosmos_map,
        "cosmos-timelapse": _run_cosmos_timelapse,
        "latex-galaxy": _run_latex_galaxy,
        "bib-galaxy": _run_bib_galaxy,
        "latex-explorer": _run_latex_explorer,
        "portal": _run_portal,
    }

    # Special handling for init-board (supports --force)
    if cmd == "init-board":
        force = "--force" in extra_args or "-f" in extra_args
        return _copy_board_tree(force=force)

    func = commands.get(cmd)

    if func:
        return func()

    print(f"❌ Unknown command: {cmd!r}")
    print("Use `interia-quality --help` for available commands.")
    return 1


def main() -> int:
    """Entry point for the `interia-quality` script."""
    args = sys.argv[1:]

    # no args → run quality engine
    if not args:
        return _run_quality_engine()

    cmd = args[0]
    extra = args[1:]
    return run_command(cmd, extra)

if __name__ == "__main__":
    raise SystemExit(main())
