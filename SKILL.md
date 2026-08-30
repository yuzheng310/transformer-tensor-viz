---
name: transformer-tensor-viz
description: Create or refine consistent, editable diagrams of Transformer tensor and matrix operations, including Q/K/V projection, reshape/view, split or merge heads, permute/transpose, attention matmul, masks, softmax, concat, broadcasting, and reductions. Use when tensor shapes and axis changes must be shown as matrix grids or stacked head slices; do not use for generic software architecture or ordinary charts.
license: GPL-3.0
metadata:
  version: "0.1.0"
  repository: "https://github.com/yuzheng310/transformer-tensor-viz"
  source: "Personal derivative of wdkns/wdkns-skills@tensor-formula-viz"
---

# Transformer Tensor Viz

Create a clean, shape-aware Transformer computation diagram with a stable visual language. The default output is only the computation diagram: no formula zone, no description panel, no title, and no signature.

## Options

Resolve these three options before drawing. Accept natural-language choices such as `有/无`, `on/off`, or `true/false`.

| Option | Default | Effect when enabled |
|---|---|---|
| `formula` | `off` | Add one compact formula zone above the computation. |
| `description` | `off` | Add one compact axes/objects/mechanism panel below the computation. |
| `cell_values` | `off` | Put values inside cells when exact values are supplied; otherwise use symbolic entries only if requested. |

Rules:

- Never add blank space for a disabled zone. Recompute the natural crop after applying the options.
- Never add an author name, handle, watermark, attribution line, logo, or signature unless the user explicitly supplies one for the figure.
- If `cell_values=on` and exact values are supplied, preserve them exactly. When the user explicitly asks for illustrative numbers, use an unmistakably synthetic sequence and identify it as illustrative in the handoff. Otherwise use concise symbolic entries such as $x_{ij}$ when adequate or ask for the data.
- If a request does not mention an option, keep its default.
- When explicit and natural-language choices conflict, read `references/option-contract.md` and apply its resolution order.

## Workflow

1. Reduce the request or code to the primary tensor path. Keep Q/K/V sibling branches together when their structural correspondence is the point.
2. Build a shape ledger: symbol, global shape, visible face axes, stacked or repeated axes, producer, consumer, and transformed/contracted axes.
3. Build a geometry ledger: one physical length per symbolic axis and one bounding box per tensor, full stack, operator, label, and connector.
4. Draw with the visual contract below. Start from `assets/qkv-horizontal-template.tex` for Q/K/V projection and head-splitting diagrams; adapt it rather than redesigning the style.
5. Render to PNG, inspect at full size and thumbnail size, correct violations, then deliver editable TikZ plus PDF and PNG. Export SVG or transparent PNG when the local renderer preserves all fonts.

## Tensor grammar

- Draw a 2D tensor as a matrix grid. Face height represents the first visible matrix axis; face width represents the second.
- Draw a leading head or batch axis as shallow offset sheets or clearly separated panels. The face always represents the last two visible matrix axes.
- When `cell_values=on`, put values only on fully visible faces. If every head or slice must be readable, replace the offset stack with separate aligned panels; never print values on partially occluded back sheets.
- Label operations with their real names: `linear`, `matmul`, `reshape`, `view`, `split heads`, `permute`, `transpose`, `softmax`, `concat`, `broadcast`, or `reduce`.
- Preserve code variable names when code is the source. Show inferred shapes as assumptions, not facts.
- Use entry colors for exact masks, sparsity, or supplied values. Use whole-column or whole-row bands for axis partitions such as heads, channels, or tensor-parallel ranks.
- For `cell_values=off`, use restrained fills or structural color bands without numbers. Do not use random-looking numbers as texture.

## Geometry invariants

- Equal shapes must have identical face dimensions everywhere.
- Draw $a\times a$ as a square. A transpose must physically swap face width and height.
- In $(m\times k)(k\times n)$, both occurrences of $k$ must have the same physical edge length.
- A reshape, flatten, transpose, split, or concat is the only place geometry may change.
- Explicit shards must tile their parent exactly; concat must reverse the split. Use an ellipsis for omitted shards rather than stretching visible shards.
- For $[B,T,d]\rightarrow[B,h,T,d_h]$, encode $d=h d_h$: the projected face uses width $d$, while each output head face uses width $d_h$ and the head axis appears as stack depth.
- Illustrative cell counts may compress real dimensions, but they must preserve equal-shape, square, transpose, contraction, split, and concat relationships.

## Layout invariants

- Default to a left-to-right, wide composition on a white background with a natural crop.
- Use the fewest stages that preserve the computation. Repeated Q/K/V rows must share x coordinates, baselines, tensor sizes, and arrow-label positions.
- Keep separate lanes for stage labels, tensors/operators, connector labels, tensor symbols, and shape labels.
- Connectors sit behind tensors. They may touch only their endpoints and may not cross unrelated tensors or text.
- Keep at least one text-em of whitespace between unrelated bounding boxes. Include all offset sheets in a stack's bounding box.
- When crowded, shorten secondary labels, widen the crop, increase spacing, or move a complete stage—never shrink labels below legible paper size.

## House style

- Inspect `assets/reference-transformer-matrix-style.png` when matching the personal default style. Use it only as a visual calibration reference; never embed it in the result.
- White canvas; no shadows, gradients, decorative cards, or dashboard chrome.
- Matrix cells form a continuous grid with thin blue-gray borders. Use small or zero gaps and only subtle corner rounding.
- Default palette: pastel green `#DDEDD9`, pastel orange `#F6DFC3`, pastel yellow `#F6EDB2`, pastel blue `#D8E6F3`, arrow blue `#82B5D5`, neutral outline `#7892A3`.
- Use low-saturation fills and lightness separation. Keep one role or axis partition visually consistent across all stages.
- Color is semantic, not decorative. Keep pre-partition inputs neutral; once an axis is split, preserve each shard or head color through reshape, permute, stack, concat, and downstream views. In the default three-head template, columns 1--2 are green/head 1, columns 3--4 orange/head 2, and columns 5--6 blue/head 3.
- Use thin blue arrows with open heads and blue dashed vertical separators when stages need separation.
- Use concise sans-serif labels. Put the tensor symbol directly below its block and the shape on the next line in muted text.
- No title by default. When `formula=on`, add at most two compact lines. When `description=on`, use one low-contrast full-width panel with at most three rows: axes, objects, mechanism.

## Rendering and validation

- Prefer editable TikZ with a `standalone` natural crop. For Chinese, use `\usepackage[UTF8,fontset=fandol]{ctex}` unless the user explicitly accepts a system-font dependency.
- Recompute all output shapes independently before delivery.
- Check axis order for every reshape/view/permute/transpose and contracted axes for every matmul/einsum.
- Check all three option states: disabled regions are absent, enabled regions contain the requested content, and the crop has no residual whitespace.
- Inspect the rendered PNG. Reject overlap, tangency, clipping, inconsistent equal-shape geometry, misleading partitions, fabricated cell values, or any unintended signature.

## Invocation examples

```text
$transformer-tensor-viz 画 Q/K/V 投影和多头 reshape；formula=off；description=off；cell_values=off。

$transformer-tensor-viz 画 scaled dot-product attention，显示公式和底部轴说明，但矩阵格子不写数字。

$transformer-tensor-viz 根据给定的 4×4 attention 数值画矩阵；cell_values=on。
```
