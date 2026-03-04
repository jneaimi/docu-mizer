# Excalidraw JSON Schema

## Element Types

| Type | Use For |
|------|---------|
| `rectangle` | Processes, actions, components |
| `ellipse` | Entry/exit points, external systems, markers |
| `diamond` | Decisions, conditionals |
| `arrow` | Connections between shapes |
| `text` | Labels (inside shapes or free-floating) |
| `line` | Non-arrow connections, structural lines, timelines |
| `frame` | Presentation slides, grouping containers |

## Common Properties

All elements share these:

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (use descriptive strings like `"trigger_rect"`, not numbers) |
| `type` | string | Element type |
| `x`, `y` | number | Position in pixels |
| `width`, `height` | number | Size in pixels |
| `strokeColor` | string | Border color (hex) |
| `backgroundColor` | string | Fill color (hex or "transparent") |
| `fillStyle` | string | "solid", "hachure", "cross-hatch" |
| `strokeWidth` | number | 1, 2, or 4 |
| `strokeStyle` | string | "solid", "dashed", "dotted" |
| `roughness` | number | 0 (smooth), 1 (default), 2 (rough) |
| `opacity` | number | 0-100 |
| `angle` | number | Rotation in radians (0 = no rotation) |
| `seed` | number | Random seed for roughness rendering (see Seed Strategy below) |
| `groupIds` | string[] | Array of group IDs this element belongs to. Empty array `[]` if ungrouped |
| `boundElements` | array\|null | Elements bound to this one (e.g., `[{"id": "text1", "type": "text"}]`). `null` if none |
| `roundness` | object\|null | Corner rounding. Use `{"type": 3}` for rounded corners, `null` for sharp |
| `locked` | boolean | Whether the element is locked from editing |
| `link` | string\|null | URL link attached to the element |
| `isDeleted` | boolean | Soft-delete flag (always `false` for active elements) |

## Text-Specific Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | The display text (readable words only, no formatting codes) |
| `originalText` | string | Same as `text` |
| `fontSize` | number | Size in pixels (16-20 for diagrams, 24+ for presentations) |
| `fontFamily` | number | 1 = hand-drawn (Virgil), 2 = sans-serif (Helvetica), 3 = monospace (Cascadia). Default to 3 for technical diagrams, 2 for presentations |
| `textAlign` | string | "left", "center", "right" |
| `verticalAlign` | string | "top", "middle", "bottom" |
| `containerId` | string\|null | ID of parent shape if text is inside a container. `null` for free-floating text |
| `lineHeight` | number | Line height multiplier. Use `1.25` as default |

## Arrow-Specific Properties

| Property | Type | Description |
|----------|------|-------------|
| `points` | number[][] | Array of [x, y] coordinates relative to element's x,y. Minimum 2 points. Use 3+ for curves |
| `startBinding` | object\|null | Connection to start shape |
| `endBinding` | object\|null | Connection to end shape |
| `startArrowhead` | string\|null | null, "arrow", "bar", "dot", "triangle" |
| `endArrowhead` | string\|null | null, "arrow", "bar", "dot", "triangle" |

## Frame-Specific Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Display label for the frame (e.g., "01 - Title Slide") |

Frames don't use `backgroundColor` or `fillStyle` — they're transparent viewports. Elements whose coordinates fall within a frame's bounds are considered part of that frame.

## Binding Format

```json
{
  "elementId": "shapeId",
  "focus": 0,
  "gap": 2
}
```

- `elementId`: ID of the shape to bind to
- `focus`: Position along the edge (-1 to 1, 0 = center)
- `gap`: Pixel distance between arrow tip and shape edge

## Roundness

Add for rounded corners on rectangles:
```json
"roundness": { "type": 3 }
```

Use `null` or omit for sharp corners.

## Seed Strategy

Seeds control the randomness of hand-drawn rendering. To avoid visual collisions when building diagrams section-by-section:

- **Section 1**: use seeds in range 100000–199999
- **Section 2**: use seeds in range 200000–299999
- **Section N**: use seeds in range N×100000 to (N+1)×100000-1

Each element needs a unique `seed` and `versionNonce` (use two different values from the same range). Seeds only matter visually when `roughness > 0`, but must always be present.
