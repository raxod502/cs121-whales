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
 * - backendModel
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
    let disableGame = false;

    let board = ChessBoard("board", {
      draggable: true,
      position: "start",
      onMouseoverSquare: (square, piece) => {
        if (disableGame) return;
        params.mouseoverEntryHandler(square);
      },
      onMouseoutSquare: (square, piece) => {
        params.mouseoverExitHandler(square);
      },
      onDragStart: (source, piece, position, orientation) => {
        if (disableGame) return false;
        return params.dragStartHandler(piece);
      },
      onDrop: (fromSquare, toSquare) => {
        console.log("Drop " + toSquare);
        if (disableGame) return "snapback";
        if (params.dragFinishHandler(fromSquare, toSquare)) {
          return null;
        } else {
          return "snapback";
        }
      },
      onSnapEnd: () => {
        if (disableGame) return;
        params.moveFinishHandler();
      },
      orientation: params.boardOrientation === "w" ? "white" : "black"
    });

    $("#undoBtn").on("click", params.undoHandler);
    $("#newGameBtn").on("click", params.newGameHandler);
    $("#changeSettingsBtn").on("click", params.changeSettingsHandler);

    $(window).resize(board.resize);
    $("#board").on("touchmove", e => {
      e.preventDefault();
    });

    this.highlightSquare = (square, red = false) => {
      const squareEl = $("#board .square-" + square);

      let background;
      if (red) {
        background = "red";
      } else if (squareEl.hasClass("black-3c85d")) {
        background = "#696969";
      } else {
        background = "#a9a9a9";
      }

      squareEl.css("background", background);
    };

    this.unhighlightAllSquares = () => {
      $("#board .square-55d63").css("background", "");
    };

    this.unhighlightAllNonredSquares = redSquare => {
      let square;
      let squareEl;
      for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
          square = String.fromCharCode(97 + col) + (-row + 8).toString();
          if (square !== redSquare) {
            squareEl = $("#board .square-" + square);
            squareEl.css("background", "");
          }
        }
      }
    };

    this.outlineSquare = square => {
      $("#board .square-" + square).css(
        "box-shadow",
        "0 0 0 3px lightblue inset"
      );
    };

    this.unoutlineAllSquares = () => {
      $("#board .square-55d63").css("box-shadow", "");
    };

    this.selectPawnPromotion = (callback, fromSquare, toSquare) => {
      $("#ppPopup").show();
      $(".ppBtn").click(function(e) {
        $("#ppPopup").hide();
        callback(fromSquare, toSquare, this.id);
      });
    };

    this.setBoardFEN = (fen, params) => {
      board.position(fen, params.animate);
    };

    this.setStatusText = text => {
      $("#status").text(text);
    };

    this.changeSettings = defaultParameters => {
      window.location.href = "/#" + encodeHash(defaultParameters);
    };

    this.crashAndBurn = message => {
      disableGame = true;
      alert(friendlyErrorMessage(message));
    };

    // Display the opponent difficulty.
    apiListModels(respModels => {
      const models = respModels;
      for (const model of models) {
        if (params.backendModel === model.internalName) {
          document.getElementById("opponent").innerText =
            "Opponent: " + model.displayName;
        }
      }
    }, this.crashAndBurn);
  };
}
