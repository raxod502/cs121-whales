We will have a frontend and backend which need to communicate over a
well-defined API that allows for playing chess. This does not touch
any of the HTML, CSS, or JS on the frontend; that can be taken care of
by a static file server in our web framework.

The responsibilities of the API may look something like this:

* Have a standard format in which a game state can be communicated.
* Keep track of ongoing games and the users playing them.
* Validate user moves to prevent cheating.
* Allow the frontend to request to play against a specific backend
  model.
* Request statistics on a particular backend model.
* Modify statistics on a backend model.
* Persist game across sessions.
* Determine winner of game.

Important questions:

* Which functionality should live on the backend and which on the
  frontend?
  * Move validation: needs to be implemented on both frontend (for
    responsiveness) and backend.
  * Determination of winner: optionally could be implemented on
    frontend for responsiveness; probably should be implemented on
    backend
  * Computer moves: only backend
  * Keep track of game state: state will need to be mutated by both
    frontend and backend; needs to be kept track of canonically by
    backend in order to prevent cheating but does not necessarily need
    to be kept track of by frontend
* Do we want to support undoing moves? This might inform our decision
  about whether to send game states or moves.

The API can be designed in isolation from the data format. Both a REST
API and a Websocket API can use the same specification.

JSON is a simple and universally accepted data transfer format and as
such I believe it is the best choice for our API.

Possible chess notations
<https://en.wikipedia.org/wiki/Chess_notation>:

* PGN <https://en.wikipedia.org/wiki/Portable_Game_Notation> records a
  sequence of chess moves. It is a derivative of AN
  <https://en.wikipedia.org/wiki/Algebraic_notation_%28chess%29>
  designed for use with computer systems. This is the most likely of
  the available options to be supported by libraries.
* FEN <https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation>
  records a single game state. It is the most standard format for
  doing this, and is included as part of the PGN standard (albeit only
  for recording the starting game state, if it is nonstandard).

It would be a good idea to verify that popular chess libraries for
Python and JavaScript support these formats, since both the frontend
and backend will need to be able to parse the format used in our API.

Chess libraries:

* Python, process games and moves:
  <https://python-chess.readthedocs.io/en/latest/>
  * supports FEN for initializing/exporting game state
  * supports algebraic notation for moving pieces
  * supports undoing moves
  * can generate ASCII chessboard
  * supports getting/setting EPD
  * can read/write PGN
* JavaScript, process games and moves:
  <https://github.com/jhlywa/chess.js/>
  * supports FEN for initializing/exporting game state
  * can generate 2D array of game state or ASCII chessboard
  * supports PGN for loading/exporting game history
  * supports algebraic notation for moving pieces
* JavaScript, render chessboard on frontend:
  <https://chessboardjs.com>
  * supports FEN, key-value mapping for getting/setting game state
  * supports algebraic notation for moving pieces
  * easy to integrate with chess.js for checking win conditions and
    validating moves
  * great documentation!

Note also that chess rules are a lot more complicated than you
probably think! Insufficient material, threefold repetition, etc. Best
to rely exclusively on libraries to implement these rules.

Example PGN:

    [Event "F/S Return Match"]
    [Site "Belgrade, Serbia JUG"]
    [Date "1992.11.04"]
    [Round "29"]
    [White "Fischer, Robert J."]
    [Black "Spassky, Boris V."]
    [Result "1/2-1/2"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 {This opening is called the Ruy Lopez.}
    4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7
    11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5
    Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6
    23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5
    hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5
    35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6
    Nf2 42. g4 Bd3 43. Re6 1/2-1/2

Example FEN:

    rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2

Wikipedia claims "FEN does not represent sufficient information to
decide whether a draw by threefold repetition may be legally claimed
or a draw offer may be accepted; for that, a different format such as
Extended Position Description is needed." EPD doesn't seem either
popular or well-documented. See
<http://portablegamenotation.com/EPD.html> but it seems not worth
pursuing.

---

Important API questions:

* Should we try to prevent the user from cheating?
* Should we keep track of the entire game history?
  * Save entire history
    * Advantage: allows us to undo moves and display history
    * Disadvantage: potentially involves more data transfer via API
  * Save only current state
    * Advantage: minimal data transfer and storage
    * Disadvantage: we cannot implement all official chess rules
      (threefold repetition) without history
* How should moves be communicated between the frontend and backend?
  * Send the move in AN
    * Advantage: very minimal data transfer
    * Disadvantage: both frontend and backend need to keep track of
      the game state (or history)
    * Disadvantage: if server is restarted, we cannot continue the
      game
  * Send the game state in FEN
    * Advantage: only moderate data transfer
    * Advantage: neither frontend nor backend needs to keep track of
      the game state
      * Counter: if we don't keep track of the history, we can't
        implement all chess rules
    * Disadvantage: backend cannot keep the frontend from cheating
  * Send the game history in PGN
    * Advantage: simplest way to communicate all relevant information
    * Disadvantage: checking for cheating is a little tricky,
      requiring a diff of two PGNs
    * Disadvantage: larger data transfer
      * Counter: with additional code complexity, we could send only
        AN normally, with fallback to PGN on server restart (avoid
        premature optimization)
  * Send both FEN and PGN
  * Send both FEN and AN
* What transfer format should the API use?
  * HTTP
  * WebSocket

... this is not finished; I used it to generate ideas and explore the
design space.
