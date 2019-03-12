"use strict";

/**
 * Params:
 * - boardOrientation
 * - fen
 * - mouseoverEntryHandler
 * - mouseoverExitHandler
 * - dragStartHandler
 * - dragFinishHandler
 * - moveFinishHandler
 * - undoHandler
 * - newGameHandler
 * - changeSettingsHandler
 */
function View() {

  this.getHash = () => {
    return window.location.hash.substr(1);
  };

  this.setHash = hash => {
    window.location.hash = "#" + hash;
  };

  // Caller needs to invoke this method before being able to use most
  // of the functionality. Only methods that need to be used before
  // creating the model are available before init.
  this.init = params => {
    let board = ChessBoard("board", {
      draggable: true,
      position: "start",
      onMouseoverSquare: (square, piece) => {
        params.mouseoverEntryHandler(square);
      },
      onMouseoutSquare: (square, piece) => {
        params.mouseoverExitHandler(square);
      },
      onDragStart: (source, piece, position, orientation) => {
        return params.dragStartHandler(piece);
      },
      onDrop: (fromSquare, toSquare) => {
        if (params.dragFinishHandler(fromSquare, toSquare)) {
          return null;
        } else {
          return "snapback";
        }
      },
      onSnapEnd: () => {
        params.moveFinishHandler();
      },
      orientation: params.boardOrientation === "w" ? "white" : "black"
    });

    $("#undoBtn").on("click", params.undoHandler);
    $("#newGameBtn").on("click", params.newGameHandler);
    $("#changeSettingsBtn").on("click", params.changeSettingsHandler);

    this.highlightSquare = square => {
      const squareEl = $("#board .square-" + square);

      let background;
      if (squareEl.hasClass("black-3c85d")) {
        background = "#696969";
      } else {
        background = "#a9a9a9";
      }

      squareEl.css("background", background);
    };

    this.unhighlightAllSquares = () => {
      $("#board .square-55d63").css("background", "");
    };

    this.setBoardFEN = (fen, params) => {
      board.position(fen, params.animate);
    };

    this.setStatusText = text => {
      $("#status").text(text);
    };

    this.changeSettings = (defaultParameters) => {
      window.location.href = "/#" + encodeHash(defaultParameters);
    };
  };

}
