"use strict";

function Controller() {
  const view = new View();
  const model = Model.fromHash(view.getHash());
  let redSquare = ""; //for use in checkmate
  let apiReq;

  function mouseoverEntryHandler(square) {
    /**
     *take a square, highlight the possible moved from that square
     */
    if (!model.canPlayerMove()) return;

    const moves = model.getAllowedMoves(square);

    if (moves.length === 0) return;

    // Highlight the square the user moused over, if there is a
    // movable piece there (and square is not red).
    if (square !== redSquare) {
      view.highlightSquare(square);
    }

    // Highlight the squares it can move to.
    for (let move of moves) {
      view.highlightSquare(move.to);
    }
  }

  function mouseoverExitHandler(square) {
    /**
     *Unhighlight squares when the mouse moves off of square
     */
    redSquare !== ""
      ? view.unhighlightAllNonredSquares(redSquare)
      : view.unhighlightAllSquares();
  }

  function dragStartHandler(piece) {
    /**
     * Handle start of drag movement.
     * Return True if piece belongs to player, and the player can move.
     */
    return model.canPlayerMove() && model.doesPlayerOwnPiece(piece);
  }

  function dragFinishHandler(fromSquare, toSquare) {
    /**
     *Handle end of drag by unhiglighting squares, and calling tryMakeMove
     */
    redSquare !== ""
      ? view.unhighlightAllNonredSquares(redSquare)
      : view.unhighlightAllSquares();
    return model.tryMakingMove(fromSquare, toSquare);
  }

  function updateViewWithMove(params) {
    /**
     *Update game FEN and status with move
     *Takes boolean 'animate' as param
     *e.x. updateViewWithMove({ animate: true });
     */
    view.setBoardFEN(model.getGameFEN(), { animate: params.animate });
    let text = model.getGameStatus();
    maybeUpdateRedSquare(text);
    view.setStatusText(text);
    updatePrevMoveOutline();
    view.setHash(model.toHash());
  }

  function updatePrevMoveOutline() {
    /**
     *Update the black square denoting the previous move.
     */
    view.unoutlineAllSquares();
    if (model.isPlayerTurn()) {
      let fromAndToSquares = model.getLastMoveSquares();
      if (fromAndToSquares === null) {
        return;
      }
      view.outlineSquare(fromAndToSquares.from);
      view.outlineSquare(fromAndToSquares.to);
    }
  }

  function maybeUpdateRedSquare(statusText) {
    /**
     *Check to see if red square needs updating, and if so, update it.
     */
    if (redSquare !== "") {
      //if there currently are no red qsuares
      view.unhighlightAllSquares();
      redSquare = "";
    } else if (model.inCheck()) {
      //if the model is in check
      redSquare = model.getSquareOfKing(model.getTurnColor());
      view.highlightSquare(redSquare, true);
    }
  }

  function tryMakeComputerMove() {
    /**
     *Attempt to make computer move
     */
    if (model.canComputerMove()) {
      apiReq = apiRequest(
        {
          command: "get_move",
          model: model.getBackendModel(),
          pgn: model.getGamePGN()
        },
        response => {
          // TODO: better error handling.
          model.setGamePGN(response.pgn);
          updateViewWithMove({ animate: true });
        }
      );
    }
  }

  function moveFinishHandler() {
    /**
     *Finish making player move, initiate computers move.
     */
    updateViewWithMove({ animate: true });
    tryMakeComputerMove();
  }

  function undoHandler() {
    /**
     * Allows for the api return to be ignored.
     * Use .abort() method to cancel api request
     */
    if (!model.isPlayerTurn()) {
      if (apiReq && apiReq.readyState != 4) {
        // readyState 4 means the request is already done
        apiReq.abort();
      }
    }

    model.undoLastMove();
    updateViewWithMove({ animate: true });
  }

  function newGameHandler() {
    /**
     * Start a new game
     * Triggered by button
     */
    model.setGamePGN(null);
    updateViewWithMove({ animate: false });
    tryMakeComputerMove();
  }

  function changeSettingsHandler() {
    /**
     * Handle button push of change settings
     */
    view.changeSettings({
      playerColor: model.getPlayerColor(),
      backendModel: model.getBackendModel()
    });
  }

  view.init({
    /**
     *Initialize functions. Update the board to initial state
     */
    boardOrientation: model.getPlayerColor(),
    fen: model.getGameFEN(),
    mouseoverEntryHandler,
    mouseoverExitHandler,
    dragStartHandler,
    dragFinishHandler,
    moveFinishHandler,
    undoHandler,
    newGameHandler,
    changeSettingsHandler,
    backendModel: model.getBackendModel()
  });
  updateViewWithMove({ animate: false });
  tryMakeComputerMove();
}

// Kick everything off.
const controller = new Controller();
