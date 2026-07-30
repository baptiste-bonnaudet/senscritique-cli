# senscritique-cli design

The decisions behind this CLI, recorded during design so that later readers do
not have to reconstruct them. Domain vocabulary lives in [CONTEXT.md](../CONTEXT.md);
the one decision that warranted its own record is [ADR 0001](adr/0001-the-cli-owns-no-state.md).

## What this is

A complete, human-first terminal front-end to SensCritique, equally usable as a
data-export tool. It wraps the `senscritique` Python library and exposes
essentially every read-only operation the library offers, rendering results for a
human by default and writing machine formats on request.

It is not a tracker, not a sync tool, and not a personal collection manager.
Those belong to other consumers of the same library.

## Scope and coverage

Every library operation gets a command, wired in a single pass rather than
released group by group. Paginated operations do not get a second `_all` command:
they get an `--all` flag.

The CLI supports the three universes the library maps today (`movie`, `tv-show`,
`book`). The other four (game, comic, album, track) are deferred in the library's
own roadmap; the CLI does not anticipate them or maintain a parallel mapping, and
they appear here automatically when the library grows.

## Command surface

Operations are grouped under domain nouns, one level deep. Each group's help
stays short and the top-level help fits on a screen.

| Command | Library method |
| --- | --- |
| `search <query>` | `search` |
| `search users <query>` | `search_users` |
| `search lists <query>` | `search_lists` |
| `search polls <query>` | `search_polls` |
| `search people <query>` | `search_contacts` |
| `search suggest <keywords>` | `autocomplete` |
| `work details <id\|url>` | `work_details` |
| `work reviews <id\|url>` | `work_reviews` |
| `work shouts <id\|url>` | `work_shouts` |
| `work review <url\|id>` | `review` |
| `user profile <username>` | `user_profile` |
| `user collection <username>` | `collection` |
| `list show <id\|url>` | `list_details` |
| `list items <id\|url>` | `list_items` |
| `poll show <id\|url>` | `poll` |
| `poll works <id\|url>` | `poll_works` |
| `poll browse` | `polls` |
| `poll top` | `top_polls` |
| `person show <id\|url>` | `contact` |
| `person works <id\|url>` | `contact_products` |
| `top chart <universe>` | `topchart` |
| `top ten <universe>` | `top10_list` |
| `browse genres <universe>` | `genres` |
| `browse genre <universe> <genre-id>` | `genre_products` |
| `browse release <universe>` | `products_by_release` |
| `browse month <year> <month>` | `products_by_month` |
| `browse day <year> <month> <day>` | `products_by_day` |
| `browse franchise <franchise-id>` | `group_products` |
| `browse providers` | `providers` |
| `browse streaming <universe>` | `streaming_explorer` |
| `discover <universe>` | `discover_products` |

Three placements are worth explaining:

- **`work review`** rather than a standalone `review` group, because one
  operation does not justify a top-level noun.
- **`top ten`** rather than `list top10`, so both site rankings are discoverable
  from `top --help`. This forced `top` to become a group, which is why the Top
  111 is `top chart <universe>` and not the shorter `top <universe>`: a Click
  group parses its first positional as a subcommand name, so the two cannot
  coexist.
- **`discover`** stays at the top level rather than under `browse`, because it is
  the entry point people reach for most casually.

## Naming

The command is `senscritique`, with `sc` installed as a second console script for
interactive use. The distribution is `senscritique-cli` and the import package is
`senscritique_cli`, since the library already owns the plain `senscritique` name
on PyPI.

The CLI says **person** where the library says `contact`. The library's name is
faithful to the GraphQL API and stays internal; the user-facing layer gets the
human word. Help text is explicit that a person may be a company or label, which
is what the API's `contact` actually covers. This sets the precedent: the CLI may
rename any API-derived term, and [CONTEXT.md](../CONTEXT.md) records the mapping.

Universes are spelled in kebab-case (`tv-show`, not the API's `tvShow`) and
translated at the boundary. There is no built-in default; `SENSCRITIQUE_UNIVERSE`
supplies one when set.

## Output

`--format` (`-f`) takes `table`, `json`, `ndjson`, or `csv`, and `-o` writes to a
file. Exporting is therefore the same command as reading, with different flags,
rather than a parallel `export` command group duplicating every argument.

The default is always `table`. Only its **rendering** adapts to context: a Rich
table with borders, color and truncation when stdout is a TTY, plain
tab-separated columns with none of that when it is not. The data format never
changes based on invisible context, so a command written interactively behaves
identically in a pipeline or under cron.

Each format has a defined shape:

- **table** shows a curated column set per model, chosen for readability. Works
  show the French title and the original title as separate columns rather than
  collapsing them via the library's `display_title`.
- **json** and **ndjson** are the Pydantic model dumped faithfully: nesting
  intact, snake_case, nothing dropped or renamed.
- **csv** flattens with dotted keys (`stats.rating`) and joins simple lists with
  a separator. Deeply nested collections such as cast are omitted, which `--help`
  states.

## Pagination and long runs

Paginated commands return about 20 items by default. `--limit N` takes more,
`--all` takes everything. The cheap behavior is the default and the expensive one
is always explicitly requested, which matters when a 1030-item collection costs
roughly 45 minutes under the rate limiter.

`--all` does not ask for confirmation, since typing it is already the
confirmation. It prints an item count and estimate, then a progress bar, on
stderr, and only when stderr is a TTY. stdout carries data and nothing else, so
piping is always clean.

## Failure

Errors print a short human sentence to stderr and exit with a code identifying
the class of failure:

| Code | Meaning |
| --- | --- |
| 0 | success |
| 2 | usage error (Typer's default) |
| 3 | not found |
| 4 | rate limited |
| 5 | transport failure |
| 6 | unexpected API shape |

Under `--format json` the error is additionally emitted as a JSON object on
stderr, so pipelines get structured failures rather than prose. The codes are a
documented contract and should not be reshuffled casually.

Bulk reads are lenient, as in the library: malformed items are skipped, and the
CLI reports the count on stderr while still exiting 0, so an export never
silently loses rows. `--strict` maps to the library's `strict=True` and turns any
skip into exit 6, which is the mode to use in CI and drift canaries.

## Logging

The library's structured logs are suppressed below WARNING by default. `-v` shows
INFO as short human lines, `-vv` adds DEBUG including request timing and retries,
and `--log-json` emits the library's JSON records untouched for piping into a log
tool. Whenever logs are enabled the progress bar is disabled, so the two never
fight over stderr.

## Implementation notes

- **Typer**, so commands are annotated functions, `StrEnum` options become
  validated choices automatically, and the noun groups map onto sub-apps. Shell
  completion comes with it.
- **`SensCritiqueSync`**, not the async client. The rate limiter serializes
  requests anyway, so an async CLI would add complexity and buy nothing.
- **Ids and URLs only.** No command resolves a title to a work. Resolution would
  cost an extra rate-limited request and risk operating on the wrong work
  silently; `search` exists for that and the two-step workflow is explicit.
- **No state.** See [ADR 0001](adr/0001-the-cli-owns-no-state.md). No cache and no
  config file: defaults come from `SENSCRITIQUE_*` environment variables
  (`SENSCRITIQUE_USER`, `SENSCRITIQUE_UNIVERSE`, `SENSCRITIQUE_RATE_LIMIT`), and
  flags override them.
- **UI in English**, while the data stays exactly as SensCritique returns it. No
  translation and no timezone conversion of the library's Paris calendar dates.

## Testing

Unit tests invoke real commands through Typer's `CliRunner` against a stubbed
`SensCritique` returning model objects, and assert rendered table, CSV and JSON
output against snapshots. The suite is offline and fast, and a failure points at
CLI code rather than at the library's transport or parsing, which are covered
next door.

A separate `tests/integration` suite marked `integration` hits the live API and
stays out of default CI, mirroring the library's arrangement.

## Relationship to the library

The CLI depends on `senscritique>=0.1` from PyPI. Locally, `[tool.uv.sources]`
overrides that with an editable path to the sibling checkout, so library changes
are picked up without a release.

This means **the library must be published to PyPI before the CLI can be
released**, though not before it can be built.

The CLI does not work around library gaps. Missing universes, unmapped fields and
auth-gated operations are the library's to fix, and the CLI simply exposes what
exists.
