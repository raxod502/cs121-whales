// board: chessboard.js
// game: chess.js

/*****************************************
 * Turn King's square red while in check *
 *****************************************/

var redSq = "";

// THIS RESETS ALL SQUARES...CHANGE TO ONLY RESET RED SQUARE
var removeRedSquare = function() {
  $("#board .square-55d63").css("background", "");
};

var redSquare = function(square) {
  redSquare = square;
  var squareEl = $("#board .square-" + square);
  var background = "#ff0000";
  squareEl.css("background", background);
};

var findPiece = function(piece) {
  const entries = Object.entries(board.position());
  for (const [sq, pc] of entries) {
    if (pc === piece) {
      return sq;
    }
  }

  return null;
};

/*************************
 * Highlight legal moves *
 *************************/

var removeGreySquares = function() {
  $("#board .square-55d63").css("background", "");
};

var greySquare = function(square) {
  var squareEl = $("#board .square-" + square);

  var background = "#a9a9a9";
  if (squareEl.hasClass("black-3c85d") === true) {
    background = "#696969";
  }

  squareEl.css("background", background);
};

var onMouseoverSquare = function(square, piece) {
  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true
  });

  // exit if there are no moves available for this square
  if (moves.length === 0) return;

  // highlight the square they moused over
  greySquare(square);

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to);
  }
};

var onMouseoutSquare = function(square, piece) {
  removeGreySquares();
};

/*******************
 * AI random moves *
 *******************/

var makeAIMove = function(msg) {
  game.load_pgn(msg.pgn);
  board.position(game.fen());
  updateStatus();
};

/**************
 * User moves *
 **************/
var board,
  game = new Chess(),
  statusEl = $("#status"),
  fenEl = $("#fen"),
  pgnEl = $("#pgn");

// do not pick up pieces if the game is over
// only pick up pieces for the side to move
var onDragStart = function(source, piece, position, orientation) {
  if (
    game.game_over() === true ||
    (game.turn() === "w" && piece.search(/^b/) !== -1) ||
    (game.turn() === "b" && piece.search(/^w/) !== -1)
  ) {
    return false;
  }
};

var onDrop = function(source, target) {
  removeGreySquares();

  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: "q" // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return "snapback";

  updateStatus();
};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
  board.position(game.fen());
};

/****************
 * Update board *
 ****************/
var updateStatus = function() {
  // removeRedSquares();
  var status = "";
  var gameOver = false;

  var moveColor = "White";
  if (game.turn() === "b") {
    moveColor = "Black";
  }

  // checkmate?
  if (game.in_checkmate() === true) {
    status = "Game over, " + moveColor + " is in checkmate.";
    gameOver = true;
    console.log("CHECKMATE");
  }

  // draw?
  else if (game.in_draw() === true) {
    status = "Game over, drawn position";
    gameOver = true;
    console.log("DRAW");
  }

  // game still on
  else {
    status = moveColor + " to move";

    // check?
    if (game.in_check() === true) {
      status += ", " + moveColor + " is in check";
      // Turn King's square red
      // redSquare(findPiece(game.turn() + 'K'));
    }
  }

  statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());

  if (!gameOver && game.turn() !== myColor) {
    var moveRequest = {
      command: "get_move",
      model: model,
      pgn: game.pgn()
    };

    // Eliminate errors with empty PGN, when AI is white on first turn
    if (moveRequest.pgn === "") {
      moveRequest.pgn = "1.";
    }
    sendRequest(moveRequest, function(msg) {
      window.setTimeout(makeAIMove, 500, msg);
    });
  }
};

var cfg = {
  draggable: true,
  position: "start",
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
  onMouseoutSquare: onMouseoutSquare,
  onMouseoverSquare: onMouseoverSquare,
  orientation: "white"
};

/**************
 * UI buttons *
 **************/
var restart = function() {
  board.start();
  game.reset();
  updateStatus();
};

// Thank you, StackOverflow
var save = function(filename, text) {
  var element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text)
  );
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
};

var load = function() {
  // Open file explorer
  $("#uploadPgn").trigger("click");
  var fileReader = new FileReader();
  // Read PGN and update board accordingly
  $("#uploadPgn").on("change", function() {
    var fileReader = new FileReader();
    fileReader.onload = function() {
      var gamePgn = fileReader.result;
      game.load_pgn(gamePgn);
      board.position(game.fen());
      updateStatus();
    };

    fileReader.readAsText($("#uploadPgn").prop("files")[0]);
  });
};

var undo = function() {
  if (game.turn() === myColor) {
    game.undo(); // Undo my move
    game.undo(); // Undo computer's move
    board.position(game.fen());
    updateStatus();
  }
};

var sendRequest = function(request, callBack) {
  $.ajax({
    method: "POST",
    //the url where you want to sent the userName and password to
    url: "/api/v1/http",
    dataType: "json",
    contentType: "application/json",
    //json object to sent to the authentication url
    data: JSON.stringify(request),
    success: function(msg) {
      console.log(msg);
      callBack(msg);
    },
    error: function(msg) {
      console.log(msg);
    }
  });
};

/********
 * Main *
 ********/

var model = sessionStorage.getItem("modelName");
var myColor = sessionStorage.getItem("userColor");
if (myColor === "b") {
  cfg.orientation = "black";
}
board = ChessBoard("board", cfg);
updateStatus();
$("#restartBtn").on("click", restart);
$("#saveBtn").on("click", function() {
  save("saved_game.pgn", game.pgn());
});
$("#loadBtn").on("click", load);
$("#undoBtn").on("click", undo);
