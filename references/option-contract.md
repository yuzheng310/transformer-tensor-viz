# Option contract

Use this reference only when a request mixes explicit and implicit presentation choices.

## Resolution order

1. An explicit option assignment wins: `formula=on`, `description=off`, `cell_values=true`.
2. A direct natural-language instruction wins next: “显示公式”, “不要下面的说明”, “矩阵里写数字”.
3. Otherwise use the defaults: all three options are `off`.

## Content boundaries

- `formula` controls only the formula zone inside the figure. Shape labels under tensors remain visible because they are part of the computation diagram.
- `description` controls only the bottom explanatory panel. A concise explanation in the assistant's handoff message is still allowed.
- `cell_values` controls visible cell contents, not cell fill colors or structural masks.
- A formula or description requested outside the figure does not enable its figure option unless the user clearly says it should appear in the image.

## Cell values

- Exact supplied values: render them verbatim with consistent significant digits.
- Symbolic request: use entries such as $x_{ij}$, $q_{ti}$, or $a_{ts}$.
- Illustrative numeric request: visibly identify the values as illustrative in the caption or description, if enabled.
- Missing data with `cell_values=on`: do not fabricate numbers. Use symbols when adequate; otherwise request the matrix values.

## Crop behavior

The three options change layout, not just visibility. Remove disabled nodes before calculating the standalone bounding box. A default figure therefore has neither a top-formula gap nor a bottom-description gap.
