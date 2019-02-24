Proposed API design and rationale:

* Use WebSockets
  * Faster than HTTP
  * Can communicate the same information as HTTP
* Frontend and backend send back and forth full PGN at each move
  * Could be useful for the backend to have access to game history
  * Not that much more data transfer (avoid premature optimization)
  * Data transfer can be optimized by letting the backend keep track
    of in-progress games, and sending only AN if the current game is
    remembered (else fall back to PGN)
  * We can undo moves easily and display game history
  * Allows us to support official chess rules that require inspecting
    history, without maintaining game state
* No persistent game state maintained; do not try to detect cheating,
  but do validate PGN
  * Allowing games to be continued through a server restart becomes
    much more difficult if we want to keep track of which games are in
    progress
  * User accounts, scoring, statistics are out of scope for this
    project
    * This API design still works with these features if we implement
      the AN optimization
  * Validating PGN is important not only for detecting cheating, but
    also in making our code more predictable (we do not know that the
    different libraries handle nonstandard PGN or illegal moves in the
    same way)
