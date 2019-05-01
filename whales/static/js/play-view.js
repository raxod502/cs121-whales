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
 * - promoteHandler
 */
function View() {
  let storeFromSquare;
  let storeToSquare;

  this.getHash = () => {
    /**
     * Return the hash of the current game state.
     */
    return window.location.hash.substr(1);
  };

  this.setHash = hash => {
    /**
     * Set the hash of the current game state.
     */
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
        if (disableGame) return "snapback";
        let move = params.dragFinishHandler(fromSquare, toSquare);
        if (move == "promote") {
          this.openPromoteWindow();
          storeFromSquare = fromSquare;
          storeToSquare = toSquare;
          return null;
        } else if (move) {
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
      /**
       * Highlight given square.
       * Take optional parameter 'red', turns highlightesd square red.
       */
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
      /**
       * Unhighlight all squares.
       */
      $("#board .square-55d63").css("background", "");
    };

    this.unhighlightAllNonredSquares = redSquare => {
      /**
       * Unhighlight all non-red squares.
       */
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
      /**
       * Create an outline around a square.
       */
      $("#board .square-" + square).css(
        "box-shadow",
        "0 0 0 3px lightblue inset"
      );
    };

    this.unoutlineAllSquares = () => {
      /**
       * Remove the outline from all squares.
       */
      $("#board .square-55d63").css("box-shadow", "");
    };

    this.setBoardFEN = (fen, params) => {
      /**
       * Set board FEN.
       * Takes option, animate = true/false.
       */
      board.position(fen, params.animate);
    };

    this.setStatusText = text => {
      /**
       * Set the text displayed at the bottom of the screen.
       */
      $("#status").text(text);
    };

    this.changeSettings = defaultParameters => {
      /**
       * Take the settings from the change settings box and encode them.
       */
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

    this.passPromoteChoice = () => {
      /**
       * Return promotion selection from dropdown.
       */
      return $(promoteDropdown).val();
    };

    this.openPromoteWindow = () => {
      /**
       * Open promotion window
       */
      modal.style.display = "block";
    };

    const promoteDropdown = "#select-promote";

    // Get the modal
    let modal = document.getElementById("promotePopup");

    //get the 'promote' button
    let go = document.getElementsByClassName("promoteBtn");

    promoteBtn.onclick = function() {
      /**
       * When promotion button is clicked, hide the modal window,
       * call promoteHandler.
       */
      modal.style.display = "none";
      params.promoteHandler(storeFromSquare, storeToSquare);
    };
  };
}
