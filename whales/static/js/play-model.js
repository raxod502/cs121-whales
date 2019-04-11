"use strict";

/**
 * Params:
 * - backendModel
 * - pgn
 * - playerColor
 */
function Model(params) {
  // Initialized down below using this.setGamePgn().
  let game;
  let backendModel = params.backendModel;
  let playerColor = params.playerColor;

  this.getGamePGN = () => {
    return game.pgn();
  };

  this.setGamePGN = pgn => {
    game = Chess();
    if (pgn !== null) {
      game.load_pgn(pgn);
    }
  };

  this.getGameFEN = () => {
    return game.fen();
  };

  this.getAllowedMoves = fromSquare => {
    return game.moves({
      square: fromSquare,
      verbose: true
    });
  };

  // Returns start and end squares of previous move
  this.getLastMoveSquares = () => {
    let history = game.history({ verbose: true });
    if (history.length == 0) {
      return null;
    }
    let lastMove = history[history.length - 1];
    return { from: lastMove.from, to: lastMove.to };
  };

  // Note: I re-added this line so that the user can undo while the
  // computer is thinking. To make sure that the user's move doesn't redo,
  // it checks whether the pending api should be ignored in controller.

  this.undoLastMove = () => {
    // Dont undo the first move if computer is white
    if (!this.hasPlayerMoved() && playerColor == "b") {
      return;
    }
    //undo player and computer move
    if (this.isPlayerTurn()) {
      game.undo();
    }
    //undo only your move if it is the computers turn
    game.undo();
  };

  this.getSquareOfKing = color => {
    let square;
    let piece;
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        square = String.fromCharCode(97 + col) + (-row + 8).toString();
        piece = game.get(square);
        if (piece && piece.type === "k" && piece.color === color) {
          return square;
        }
      }
    }
    // Shouldn't reach this
    return null;
  };

  this.getPlayerColor = () => {
    return playerColor;
  };

  this.isPlayerTurn = () => {
    return game.turn() === playerColor;
  };

  this.doesPlayerOwnPiece = piece => {
    return piece.search(new RegExp(`^${playerColor}`)) !== -1;
  };

  this.canPlayerMove = () => {
    if (game.in_checkmate() || game.in_draw()) {
      return false;
    }

    return this.isPlayerTurn();
  };

  this.canComputerMove = () => {
    if (game.in_checkmate() || game.in_draw()) {
      return false;
    }

    return !this.isPlayerTurn();
  };

  this.hasPlayerMoved = () => {
    if (playerColor === "white") {
      return game.history().length >= 1;
    } else {
      return game.history().length >= 2;
    }
  };

  this.tryMakingMove = (fromSquare, toSquare) => {
    // We ought to be able to check if a move is legal without
    // actually making it. I can't figure out how to do this, though.
    // Do we really have to make it and then undo it?
    return (
      game.move({
        from: fromSquare,
        to: toSquare,
        promotion: "q"
      }) !== null
    );
  };

  this.getGameStatus = () => {
    if (game.in_checkmate()) {
      if (this.isPlayerTurn()) {
        return "Checkmate! You have lost.";
      } else {
        return "Checkmate! You have won!";
      }
    }

    if (game.in_draw()) {
      return "Draw!";
    }

    if (this.isPlayerTurn()) {
      if (game.in_check()) {
        return "Check! Your move.";
      } else {
        return "Your move!";
      }
    } else {
      if (game.in_check()) {
        return "Check! The computer is thinking...";
      } else {
        return "The computer is thinking...";
      }
    }
  };

  this.getTurnColor = () => {
    return game.turn();
  };

  this.inCheck = () => {
    return game.in_check();
  };

  this.setBackendModel = newBackendModel => {
    backendModel = newBackendModel;
  };

  this.getBackendModel = () => {
    return backendModel;
  };

  this.toHash = () => {
    return encodeHash({
      playerColor,
      backendModel,
      pgn: this.getGamePGN()
    });
  };

  this.setGamePGN(params.pgn);
}

Model.checkPGN = pgn => {
  const game = Chess();
  return game.load_pgn(pgn);
};

Model.fromHash = hash => {
  const hashData = decodeHash(hash);

  let playerColor;
  if (hashData.playerColor === "w" || hashData.playerColor === "b") {
    playerColor = hashData.playerColor;
  } else {
    playerColor = "w";
  }

  let backendModel;
  if (hashData.backendModel) {
    backendModel = hashData.backendModel;
  } else {
    backendModel = "random";
  }

  let pgn;
  if (hashData.pgn && Model.checkPGN(hashData.pgn)) {
    pgn = hashData.pgn;
  } else {
    pgn = null;
  }

  return new Model({
    playerColor,
    backendModel,
    pgn
  });
};
