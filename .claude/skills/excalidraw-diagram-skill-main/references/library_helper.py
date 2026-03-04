"""Fetch and extract items from Excalidraw community libraries.

Usage:
    cd <skill-directory>/references
    uv run python library_helper.py list <source>
    uv run python library_helper.py fetch <source> --item "Name" --x 500 --y 300 --seed-base 300000 --id-prefix "srv"
    uv run python library_helper.py search "keyword"

Libraries are downloaded from the excalidraw-libraries GitHub repo and cached locally.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/excalidraw/excalidraw-libraries/main/libraries/"
)
CACHE_DIR = Path(__file__).parent / "libraries_cache"


# ---------------------------------------------------------------------------
# Download / cache
# ---------------------------------------------------------------------------

def download_library(source: str) -> dict:
    """Download a library file, caching locally. Returns parsed JSON or error dict."""
    cache_path = CACHE_DIR / source
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Cached file has invalid JSON: {e}"}

    url = GITHUB_RAW_BASE + source
    try:
        with urlopen(url, timeout=30) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8")
    except HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code} fetching {url}"}
    except URLError as e:
        return {"success": False, "error": f"Network error fetching {url}: {e.reason}"}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON from {url}: {e}"}

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(raw, encoding="utf-8")
    return data


# ---------------------------------------------------------------------------
# Parse library formats
# ---------------------------------------------------------------------------

def parse_library_items(data: dict) -> list[dict]:
    """Extract items from v1 or v2 library format.

    v2: {"libraryItems": [{"name": str, "elements": [...], ...}, ...]}
    v1: {"library": [[element, ...], ...]}

    Returns list of {"name": str, "elements": list[dict]}.
    """
    items: list[dict] = []

    # v2 format
    if "libraryItems" in data:
        for item in data["libraryItems"]:
            items.append({
                "name": item.get("name", "Unnamed"),
                "elements": item.get("elements", []),
            })
        return items

    # v1 format — unnamed groups
    if "library" in data:
        for i, group in enumerate(data["library"]):
            if isinstance(group, list):
                items.append({"name": f"Item {i + 1}", "elements": group})
        return items

    return items


# ---------------------------------------------------------------------------
# Bounding box & transform
# ---------------------------------------------------------------------------

def compute_bounding_box(elements: list[dict]) -> tuple[float, float, float, float]:
    """Compute (min_x, min_y, max_x, max_y) across elements."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)

        if el.get("type") in ("arrow", "line") and "points" in el:
            for px, py in el["points"]:
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(w))
            max_y = max(max_y, y + abs(h))

    if min_x == float("inf"):
        return (0, 0, 0, 0)

    return (min_x, min_y, max_x, max_y)


def reposition_elements(
    elements: list[dict],
    target_x: float,
    target_y: float,
    seed_base: int,
    id_prefix: str,
) -> list[dict]:
    """Clone elements, reposition to target coordinates, remap IDs/seeds/groups."""
    import copy

    elements = copy.deepcopy(elements)
    min_x, min_y, _, _ = compute_bounding_box(elements)

    dx = target_x - min_x
    dy = target_y - min_y

    # Build ID and groupId remapping tables
    id_map: dict[str, str] = {}
    group_map: dict[str, str] = {}

    for i, el in enumerate(elements):
        old_id = el.get("id", "")
        new_id = f"{id_prefix}_{i}"
        id_map[old_id] = new_id

        for gid in el.get("groupIds", []):
            if gid not in group_map:
                group_map[gid] = f"{id_prefix}_g{len(group_map)}"

    # Apply transforms
    for i, el in enumerate(elements):
        # Position
        el["x"] = el.get("x", 0) + dx
        el["y"] = el.get("y", 0) + dy

        # ID and seed
        el["id"] = id_map.get(el.get("id", ""), f"{id_prefix}_{i}")
        el["seed"] = seed_base + i

        # Group IDs
        el["groupIds"] = [group_map.get(g, g) for g in el.get("groupIds", [])]

        # Remap boundElements references
        if "boundElements" in el and el["boundElements"]:
            el["boundElements"] = [
                {**be, "id": id_map.get(be.get("id", ""), be.get("id", ""))}
                for be in el["boundElements"]
            ]

        # Remap arrow bindings
        for binding_key in ("startBinding", "endBinding"):
            binding = el.get(binding_key)
            if binding and "elementId" in binding:
                binding["elementId"] = id_map.get(
                    binding["elementId"], binding["elementId"]
                )

        # Remap containerId
        if el.get("containerId"):
            el["containerId"] = id_map.get(el["containerId"], el["containerId"])

    return elements


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(source: str) -> dict:
    """List all items in a library."""
    data = download_library(source)
    if isinstance(data, dict) and "success" in data and not data["success"]:
        return data

    items = parse_library_items(data)
    if not items:
        return {"success": False, "error": f"No items found in {source}"}

    lines = [f"Library: {source}", f"Items: {len(items)}", ""]
    for i, item in enumerate(items):
        el_count = len(item["elements"])
        lines.append(f"  {i + 1}. {item['name']} ({el_count} elements)")

    return {"success": True, "output": "\n".join(lines)}


def cmd_fetch(
    source: str,
    item_name: str,
    target_x: float,
    target_y: float,
    seed_base: int,
    id_prefix: str,
) -> dict:
    """Fetch a specific item, reposition, and output JSON."""
    data = download_library(source)
    if isinstance(data, dict) and "success" in data and not data["success"]:
        return data

    items = parse_library_items(data)
    if not items:
        return {"success": False, "error": f"No items found in {source}"}

    # Find item by name (case-insensitive substring match)
    match = None
    for item in items:
        if item_name.lower() in item["name"].lower():
            match = item
            break

    if match is None:
        available = [it["name"] for it in items]
        return {
            "success": False,
            "error": f"Item '{item_name}' not found. Available: {', '.join(available[:20])}",
        }

    elements = reposition_elements(
        match["elements"], target_x, target_y, seed_base, id_prefix
    )

    return {"success": True, "elements": elements, "item_name": match["name"]}


def cmd_search(keyword: str) -> dict:
    """Search item names across all cached libraries."""
    if not CACHE_DIR.exists():
        return {"success": False, "error": "No cached libraries. Fetch a library first."}

    keyword_lower = keyword.lower()
    results: list[str] = []

    for cache_file in sorted(CACHE_DIR.rglob("*.excalidrawlib")):
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        items = parse_library_items(data)
        source = str(cache_file.relative_to(CACHE_DIR))

        for item in items:
            if keyword_lower in item["name"].lower():
                results.append(f"  {item['name']} — {source}")

    if not results:
        return {
            "success": True,
            "output": f"No items matching '{keyword}' in cached libraries.",
        }

    return {
        "success": True,
        "output": f"Found {len(results)} matches for '{keyword}':\n" + "\n".join(results),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and extract Excalidraw community library items"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List items in a library")
    p_list.add_argument("source", help="Library source path (e.g. rohanp/system-design.excalidrawlib)")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Extract and reposition an item")
    p_fetch.add_argument("source", help="Library source path")
    p_fetch.add_argument("--item", required=True, help="Item name (substring match)")
    p_fetch.add_argument("--x", type=float, default=0, help="Target X position")
    p_fetch.add_argument("--y", type=float, default=0, help="Target Y position")
    p_fetch.add_argument("--seed-base", type=int, default=100000, help="Starting seed value")
    p_fetch.add_argument("--id-prefix", default="lib", help="Prefix for element IDs")

    # search
    p_search = sub.add_parser("search", help="Search item names across cached libraries")
    p_search.add_argument("keyword", help="Search keyword")

    args = parser.parse_args()

    if args.command == "list":
        result = cmd_list(args.source)
    elif args.command == "fetch":
        result = cmd_fetch(
            args.source, args.item, args.x, args.y, args.seed_base, args.id_prefix
        )
    elif args.command == "search":
        result = cmd_search(args.keyword)
    else:
        parser.print_help()
        sys.exit(1)

    if not result.get("success", False):
        print(f"ERROR: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    if "output" in result:
        print(result["output"])
    elif "elements" in result:
        print(json.dumps(result["elements"], indent=2))


if __name__ == "__main__":
    main()
