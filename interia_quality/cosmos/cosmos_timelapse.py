"""
cosmos_timelapse.py — InterIA COSMOS TIMELAPSE v1

Records snapshots of the Cosmos Map over time:

- saves timestamped copies in cosmos_history/
- builds/updates cosmos_timeline.json
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

def load_json(path: Path):
    """Return JSON from path"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def record_snapshot():
    """Records snapshots of the Cosmos Map JSON over time"""
    cosmos_path = Path("cosmos_map.json")
    summary_path = Path("cosmos_map_summary.json")

    if not cosmos_path.exists():
        print("❌ cosmos_map.json not found — run `make cosmos-map` first.")
        return 1

    cosmos = load_json(cosmos_path)
    summary = load_json(summary_path)

    # Create history directory
    hist_dir = Path("cosmos_history")
    hist_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snap_path = hist_dir / f"{timestamp}.json"

    snap = {
        "timestamp": timestamp,
        "cosmos": cosmos,
        "summary": summary,
    }

    snap_path.write_text(json.dumps(snap, indent=2), encoding="utf-8")
    print(f"📦 Snapshot saved: {snap_path}")

    # Update global timeline
    timeline_path = Path("cosmos_timeline.json")
    timeline = load_json(timeline_path) or []

    timeline.append(snap)

    timeline_path.write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    print(f"🧭 Timeline updated: cosmos_timeline.json")

    return 0


def main():
    """Main function — InterIA COSMOS TIMELAPSE"""
    return record_snapshot()

if __name__ == "__main__":
    import sys
    sys.exit(main())
