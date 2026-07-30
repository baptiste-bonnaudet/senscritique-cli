# SensCritique CLI

The terminal front-end to SensCritique. It exposes the read-only API surface as
commands, renders results for a human by default, and writes bulk data to file
when asked.

## Language

### Catalogue

**Work**:
Anything SensCritique catalogues and rates: a film, TV show, book, game, comic,
album, or track.
_Avoid_: Product (the API's term), title, item, entry

**Universe**:
The category a work belongs to. One of movie, TV show, book, game, comic, album,
track.
_Avoid_: Type, category, medium, kind

**Title**:
A work's name in French, as senscritique.com displays it.
_Avoid_: Local title, French title, name

**Original Title**:
A work's name in its original language, when it differs from the Title.
_Avoid_: Native title, source title

**Person**:
An entity credited on a work: a director, actor, or author, or a company such as
a label or studio.
_Avoid_: Contact (the API's and library's term), creator, credit, artist

**Franchise**:
A group of works released under one banner, such as a film series.
_Avoid_: Group, saga, collection

**Genre**:
A thematic label a universe uses to subdivide its works.
_Avoid_: Tag, category

**Provider**:
A streaming service on which a work can be watched.
_Avoid_: Platform, service, VOD

### Opinions about works

**Rating**:
A score out of 10 that a user gives a work.
_Avoid_: Score, note, mark

**Review**:
A titled long-form piece of writing about a work.
_Avoid_: Critique, article, post

**Shout**:
A short untitled comment on a work, distinct from a review.
_Avoid_: Comment, note, blurb

**Top Chart**:
SensCritique's own ranking of a universe, such as the Top 111.
_Avoid_: Topchart, leaderboard, ranking, chart

### People and their pages

**User**:
Someone with a SensCritique account, identified by a username.
_Avoid_: Member, profile, account

**Collection**:
The set of works a user has marked, with the rating and status they gave each
one.
_Avoid_: Library, watchlist, diary, log

**List**:
An ordered, user-curated selection of works published on SensCritique.
_Avoid_: Collection, selection, set

**Poll**:
A SensCritique-run vote in which users rank works around a theme.
_Avoid_: Survey, vote, sondage
