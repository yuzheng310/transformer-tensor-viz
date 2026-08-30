# Connector routing contract

Read this reference for shared operands, multi-input operators, fan-out, fan-in, collectives, or multi-lane diagrams.

## Why this contract exists

A tensor grid represents a value, not the computation that produced it. When two arrows terminate directly on a result grid, the arrowheads compete with the tensor symbol, shape label, and cells. Hard-coded coordinate endpoints also stop following the object when its geometry changes.

## Connector ledger

Before drawing edges, record these fields for every connector:

| Field | Requirement |
|---|---|
| source | Named node and free anchor |
| target | Named operator, tensor, collective, or junction and free anchor |
| role | primary flow, shared operand, broadcast, fan-in, or collective |
| corridor | Horizontal or vertical whitespace reserved for this route |
| label | Separate node outside the path, or none |

Define all tensor and operator nodes before connectors. Draw connectors in the background layer after the ledger is complete.

## Multi-input operations

- Create an explicit operator node for `matmul`, addition, masking, concat, or another true multi-input computation.
- Each input arrow terminates on a distinct operator port. One output arrow leaves the operator for the result tensor.
- Do not use the result tensor as an implicit operator by pointing two or more input arrows at its face.
- Operation text belongs inside or next to the operator node. Tensor symbols and shapes belong to the tensor, not on a connector path.

For example, draw `Q -> matmul <- K`, followed by `matmul -> score`; draw `P -> matmul <- V`, followed by `matmul -> context`.

## Shared operands and GQA fan-out

Prefer these strategies in order:

1. A named shared-operand bus in a reserved whitespace corridor, branching to named operator ports.
2. Clearly marked visual aliases when a bus would cross primary pipelines. Label aliases as `shared`, `broadcast`, or `same K/V`; they do not imply recomputation or communication.
3. A compact operator label such as `× K_0^T` only when the master K/V matrix is already visible and the dependency remains unambiguous.

Never force a long diagonal arrow through a tensor symbol, formula label, or sibling pipeline merely to keep a single physical copy of the shared operand.

## Ports and waypoints

- Use named anchors for both endpoints: `(q0.east)`, `(dot0.west)`, `(score0.west)`.
- Raw coordinates may define a named waypoint with `\coordinate (route-a) at (...)`; connectors then reference `(route-a)`.
- A waypoint is not a tensor port. It must remain in reserved whitespace.
- Labels above and shape annotations below reserve `north` and `south`; use `east` or `west` unless an explicit port lane was reserved.
- The arrowhead must stop on the target boundary. It must not enter a matrix cell or land on a symbol/shape label.

## Fan-in, collectives, and lane boundaries

- Route each lane's contribution to a named collective node. The collective owns the fan-in; the final tensor receives only the collective's single output.
- Cross a lane boundary orthogonally and only where the boundary has a deliberate gap or where the collective visually owns the crossing.
- Use distinct named waypoints for separate lanes. Do not merge paths accidentally by sharing an unlabeled coordinate.

## Validation

Run:

```bash
python3 scripts/lint_tikz_connectors.py diagram.tex
```

Then inspect both full-size and thumbnail PNGs. Trace every arrow from tail to arrowhead and ask:

- Does the source and target match the computation?
- Is the arrowhead on a named object boundary?
- Does the path cross any tensor, number, tensor symbol, shape label, or unrelated edge?
- Can a reader distinguish data flow from visual grouping without guessing?

Any failed answer blocks delivery.
