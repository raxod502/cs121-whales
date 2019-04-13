"use strict";

function Controller() {
  const view = new View();
  const model = Model.fromHash(view.getHash());
  let redSquare = "";
  let ignoreAPICount = 0;

  function mouseoverEntryHandler(square) {
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
    redSquare !== ""
      ? view.unhighlightAllNonredSquares(redSquare)
      : view.unhighlightAllSquares();
  }

  function dragStartHandler(piece) {
    return model.canPlayerMove() && model.doesPlayerOwnPiece(piece);
  }

  function dragFinishHandler(fromSquare, toSquare) {
    redSquare !== ""
      ? view.unhighlightAllNonredSquares(redSquare)
      : view.unhighlightAllSquares();
    return model.tryMakingMove(fromSquare, toSquare);
  }

  function updateViewWithMove(params) {
    view.setBoardFEN(model.getGameFEN(), { animate: params.animate });
    let text = model.getGameStatus();
    maybeUpdateRedSquare(text);
    view.setStatusText(text);
    updatePrevMoveOutline();
    view.setHash(model.toHash());
  }

  function updatePrevMoveOutline() {
    // May need to remove previous outlines even if it is the
    // player's turn (e.g., for undo and restart)
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
    // In check last turn
    if (redSquare !== "") {
      view.unhighlightAllSquares();
      redSquare = "";
    } else if (model.inCheck()) {
      redSquare = model.getSquareOfKing(model.getTurnColor());
      view.highlightSquare(redSquare, true);
    }
  }

  function tryMakeComputerMove() {
    if (model.canComputerMove()) {
      apiRequest(
        {
          command: "get_move",
          model: model.getBackendModel(),
          pgn: model.getGamePGN()
        },
        response => {
          // TODO: better error handling.
          if (ignoreAPICount == 0) {
            model.setGamePGN(response.pgn);
            updateViewWithMove({ animate: true });
          } else {
            ignoreAPICount--;
          }
        }
      );
    }
  }

  function moveFinishHandler() {
    updateViewWithMove({ animate: true });
    tryMakeComputerMove();
  }

  function undoHandler() {
    // This method allows for the api return to be ignored.
    // if it is the computers turn, allow the player move to be undone,
    // and ignore the computer's move

    if (!model.isPlayerTurn()) {
      ignoreAPICount++;
    }

    model.undoLastMove();
    updateViewWithMove({ animate: true });
  }

  function newGameHandler() {
    model.setGamePGN(null);
    updateViewWithMove({ animate: false });
    tryMakeComputerMove();
  }

  function changeSettingsHandler() {
    view.changeSettings({
      playerColor: model.getPlayerColor(),
      backendModel: model.getBackendModel()
    });
  }

  view.init({
    boardOrientation: model.getPlayerColor(),
    fen: model.getGameFEN(),
    mouseoverEntryHandler,
    mouseoverExitHandler,
    dragStartHandler,
    dragFinishHandler,
    moveFinishHandler,
    undoHandler,
    newGameHandler,
    changeSettingsHandler
  });
  updateViewWithMove({ animate: false });
  tryMakeComputerMove();
}

// Kick everything off.
const controller = new Controller();
