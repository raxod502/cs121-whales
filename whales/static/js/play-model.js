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

  this.undoLastMove = () => {
    // Undo both your move and the computer's move.
    // If computer turn, only undo one move (the players)
    if (this.isPlayerTurn()) {
      game.undo();
    }
    game.undo();
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
