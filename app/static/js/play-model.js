"use strict";

/**
 * Params:
 * - backendModel
 * - pgn
 * - playerColor
 */
function Model(params) {
  let game = Chess();
  let backendModel = params.backendModel;
  let playerColor = params.playerColor;

  this.getGamePGN = () => {
    return game.pgn();
  };

  this.setGamePGN = pgn => {
    game.load_pgn(pgn);
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
    game.undo();
    game.undo();
  };

  function isPlayerTurn() {
    return game.turn() === playerColor;
  }

  this.doesPlayerOwnPiece = piece => {
    return piece.search(new RegExp(`^${playerColor}`)) !== -1;
  };

  this.canPlayerMove = () => {
    if (game.in_checkmate() || game.in_draw()) {
      return false;
    }

    return isPlayerTurn();
  };

  this.canComputerMove = () => {
    if (game.in_checkmate() || game.in_draw()) {
      return false;
    }

    return !isPlayerTurn();
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
      if (isPlayerTurn()) {
        return "Checkmate! You have lost.";
      } else {
        return "Checkmate! You have won!";
      }
    }

    if (game.in_draw()) {
      return "Draw!";
    }

    if (isPlayerTurn()) {
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

  if (params.pgn !== null) {
    this.setGamePGN(params.pgn);
  }
}
