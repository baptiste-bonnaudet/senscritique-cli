# The CLI owns no state

The SensCritique API is polite-rate-limited to roughly one request every 2.5
seconds, which makes an on-disk response cache the obvious optimization, and a
config file the obvious place to stop retyping a username. We deliberately have
neither: every command hits the live API, and every default comes from
`SENSCRITIQUE_*` environment variables. The CLI reads and writes nothing outside
its own stdout and whatever `-o` names.

## Why

The library it wraps is a pure stateless client by design, with no persistence
and no cache layers. Extending that property through the CLI means there is
exactly one place where SensCritique data lives (SensCritique), no staleness to
reason about, no cache to invalidate or explain, and no divergence between what
the CLI shows and what the site shows. It also keeps every invocation
reproducible: given the same environment, a command's behavior is fully
determined by its arguments.

## Consequences

Repeating a command repeats its cost, and iterating on a large export means
refetching it. This was accepted knowingly. The mitigations are `--all` with
`-o FILE` (fetch once, then work on the file) and `--format json` (pipe into
jq rather than re-querying).

If this is ever revisited, the shape to reach for first is an opt-in
`--cache` flag rather than a cache that is on by default, so that the
stateless behavior remains the documented default.
