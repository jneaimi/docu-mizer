# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

docu-mizer is a Claude Code skill for generating Excalidraw diagrams and presentations. The skill lives at `.claude/skills/excalidraw-diagram-skill-main/` and teaches the agent to create diagrams that "argue visually" — shapes mirror concepts, colors encode meaning, and evidence artifacts (real code, JSON, API names) replace generic placeholders.

## Setup & Rendering

```bash
# First-time setup
cd .claude/skills/excalidraw-diagram-skill-main/references
uv sync
uv run playwright install chromium

# Render a diagram to PNG
uv run python render_excalidraw.py <path-to-file.excalidraw> [--output path.png] [--scale 2] [--width 1920]

# Render each presentation slide as a separate PNG
uv run python render_excalidraw.py <path-to-file.excalidraw> --slides
```

Requires Python 3.11+ and uv package manager.

### Library Helper (community icons)

```bash
cd .claude/skills/excalidraw-diagram-skill-main/references

# List items in a library
uv run python library_helper.py list rohanp/system-design.excalidrawlib

# Extract an item repositioned to target coordinates
uv run python library_helper.py fetch "dwelle/network-topology-icons.excalidrawlib" \
  --item "Server" --x 500 --y 300 --seed-base 300000 --id-prefix "srv"

# Search across cached libraries
uv run python library_helper.py search "firewall"
```

## Architecture

**Skill system** — SKILL.md (623 lines) is the core methodology file the agent reads. It defines the full workflow: depth assessment → concept mapping → pattern selection → section-by-section JSON building → render-validate loop.

**Rendering pipeline** — `render_excalidraw.py` loads `.excalidraw` JSON into headless Chromium via Playwright, calls Excalidraw's `exportToSvg`, and screenshots the result to PNG. The `render()` function returns `{"success": bool, "path": str, "error": str}` for agent-friendly error handling.

**Reference files** in `references/`:
- `color-palette.md` — Semantic color system (shape fills/strokes, text hierarchy, evidence artifacts). Single source of truth for all colors.
- `element-templates.md` — Copy-paste JSON templates for each element type (rectangle, ellipse, diamond, arrow, text, line, frame).
- `json-schema.md` — Complete Excalidraw JSON property reference with binding formats, roundness config, and seed strategy.
- `render_template.html` — Browser page that imports `@excalidraw/excalidraw@0.18.0` from esm.sh and exposes `window.renderDiagram()`.
- `library_helper.py` — Downloads Excalidraw community library icons on demand, caches locally, extracts/repositions specific items for insertion into diagrams.
- `library-catalog.md` — Curated catalog of ~50 community libraries by category (cloud, system design, networking, DevOps, UX, etc.).

## Key Conventions

- **Seed namespacing**: Each diagram section uses a dedicated seed range (100000–199999, 200000–299999, etc.) to avoid collisions when building JSON incrementally.
- **`<skill-directory>` variable**: All paths in SKILL.md use `<skill-directory>` instead of hardcoded paths. At runtime this resolves to the skill's installation directory.
- **Output location**: Generated `.excalidraw` files go in the user's working directory or alongside source material, not inside the skill directory.
- **Presentation mode**: Frames (1920×1080) act as slides. Horizontal layout with 180px gaps between frames.
- **Font families**: 1=Virgil (hand-drawn), 2=Helvetica (clean), 3=Cascadia (code). Default is 1.
- **Quality checklist**: Tiered system in SKILL.md — Must-Pass (7 items), Should-Pass (10), Advisory (7), Presentation-specific (4).

## File Types

- `.excalidraw` — JSON diagram files (Excalidraw format, `"type": "excalidraw"`)
- `.png` — Rendered diagram outputs (gitignored)
