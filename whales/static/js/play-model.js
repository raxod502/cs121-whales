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
    /**
     * Return the game PGN.
     */
    return game.pgn();
  };

  this.setGamePGN = pgn => {
    /**
     * Set the game PGN.
     */
    game = Chess();
    if (pgn !== null) {
      game.load_pgn(pgn);
    }
  };

  this.getGameFEN = () => {
    /**
     * Return the game FEN.
     */
    return game.fen();
  };

  this.getAllowedMoves = fromSquare => {
    /**
     * Return a list of allowed moves.
     */
    return game.moves({
      square: fromSquare,
      verbose: true
    });
  };

  this.getLastMoveSquares = () => {
    /**
     * Return start and end squares of previous move.
     */
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
    /**
     * Undo the last move of the player, and the computer move,
     * if appropriate.
     */

    if (this.isPlayerTurn()) {
      // Undo player and computer move.
      game.undo();
    }
    // Undo only your move if it is the computers turn.
    game.undo();
  };

  this.getSquareOfKing = color => {
    /**
     * Returns square which king is located in.
     */
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
    // Shouldn't reach this.
    return null;
  };

  this.getPlayerColor = () => {
    /**
     * Return player color.
     * RETURNS: 'b' or 'w'.
     */
    return playerColor;
  };

  this.isPlayerTurn = () => {
    /**
     * Return true is player turn, else false.
     */
    return game.turn() === playerColor;
  };

  this.doesPlayerOwnPiece = piece => {
    /**
     * Return true if player owns piece, false else.
     */
    return piece.search(new RegExp(`^${playerColor}`)) !== -1;
  };

  this.canPlayerMove = () => {
    /**
     * Return true if player can move, false else.
     */
    if (game.in_checkmate() || game.in_draw()) {
      return false;
    }

    return this.isPlayerTurn();
  };

  this.canComputerMove = () => {
    /**
     * Return true if computer can move, false else.
     */
    if (game.in_checkmate() || game.in_draw()) {
      return false;
    }

    return !this.isPlayerTurn();
  };

  this.hasPlayerMoved = () => {
    /**
     * Return true if player has moved, else false.
     */
    if (playerColor === "w") {
      return game.history().length >= 1;
    } else {
      return game.history().length >= 2;
    }
  };

  this.tryMakingMove = (fromSquare, toSquare, promotePiece) => {
    /**
     * Try making a move from fromSquare to toSquare.
     */
    let move = game.move({
      from: fromSquare,
      to: toSquare,
      promotion: promotePiece === null ? "q" : promotePiece
    });

    if (move === null) {
      return { isValid: false, isPromotion: false };
    }

    if (promotePiece === null && move.flags.includes("p")) {
      game.undo();
      return { isValid: false, isPromotion: true };
    }

    return { isValid: true, isPromotion: false };
  };

  this.getGameStatus = () => {
    /**
     * Return text indicating game status.
     */
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
    /**
     * Return the color of the player who is next to move.
     */
    return game.turn();
  };

  this.putPiece = (piece, square) => {
    /**
     * Put a piece on the specified square.
     * NOTE: This updates the FEN, but not the PGN.
     */
    return game.put(piece, square);
  };

  this.removePiece = square => {
    /**
     * Remove the piece on the specified square.
     * NOTE: This updates the FEN, but not the PGN.
     */
    return game.remove(square);
  };

  this.inCheck = () => {
    /**
     * Return true if game in check, false else.
     */
    return game.in_check();
  };

  this.setBackendModel = newBackendModel => {
    /**
     * Set new back end model.
     */
    backendModel = newBackendModel;
  };

  this.getBackendModel = () => {
    /**
     * Return name of backend model.
     */
    return backendModel;
  };

  this.toHash = () => {
    /**
     * Encode hash of current game state.
     */
    return encodeHash({
      playerColor,
      backendModel,
      pgn: this.getGamePGN()
    });
  };

  this.setGamePGN(params.pgn);
}

Model.checkPGN = pgn => {
  /**
   * Validate the PGN. Return Boolean.
   * NOTE: Calls load_pgn, uses the response to determine validity.
   */
  const game = Chess();
  return game.load_pgn(pgn);
};

Model.fromHash = hash => {
  /**
   * Decode hash data, load into game state.
   */
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
