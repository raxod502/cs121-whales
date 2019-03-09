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
function View(params) {
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

  this.setBoardFEN = fen => {
    board.position(fen);
  };

  this.setStatusText = text => {
    $("#status").text(text);
  };

  this.changeSettings = () => {
    window.location.href = "/";
  };
}
