// board: chessboard.js
// game: chess.js

var model = '';
var myColor = 'w'

/*****************************************
 * Turn King's square red while in check *
 *****************************************/

var redSq = '';
var allSquares = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                  'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                  'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                  'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                  'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                  'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                  'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                  'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'];

// CHANGE THIS FUNCTION TO ONLY RESET RED SQUARES ???
// LOOP THROUGH A1 THRU H8 AND USE squareEl EXAMPLE
// Check bg color and reset if not red
// alert(myDiv.style.backgroundColor);
var removeRedSquare = function() {
  $('#board .square-55d63').css('background', '');
  // const squares = Object.keys(board.position());
  // for (const sq of allSquares) {
  //   if (sq === redSq) {
  //     $('#board .square-' + sq).css('background', '');
  //     break;
  //   }
  // }
  console.log("remove red square");
  // redSq = '';
};

var redSquare = function(square) {
  redSquare = square;
  var squareEl = $('#board .square-' + square);
  var background = '#ff0000';
  squareEl.css('background', background);
};

var findPiece = function(piece) {
  const entries = Object.entries(board.position());
  for (const [sq, pc] of entries) {
    if (pc === piece) {
      return sq;
    }
  }

  return null;
}

/*************************
 * Highlight legal moves *
 *************************/

// CHANGE THIS FUNCTION TO ONLY RESET GREY SQUARES ???
var removeGreySquares = function() {
  $('#board .square-55d63').css('background', '');
  // console.log('red' + redSq);
  // for (const sq of allSquares) {
  //   if (sq !== redSq) {
  //     console.log(sq);
  //     $('#board .square-' + sq).css('background', '');
  //   }
  // }
  // console.log("remove gray squares");
};

var greySquare = function(square) {
  var squareEl = $('#board .square-' + square);

  var background = '#a9a9a9';
  if (squareEl.hasClass('black-3c85d') === true) {
    background = '#696969';
  }

  squareEl.css('background', background);
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

  console.log(msg);
  game.load_pgn(msg.pgn);
  board.position(game.fen());
  updateStatus();
};

/**************
 * User moves *
 **************/
var board,
    game = new Chess(),
    statusEl = $('#status'),
    fenEl = $('#fen'),
    pgnEl = $('#pgn');

// do not pick up pieces if the game is over
// only pick up pieces for the side to move
var onDragStart = function(source, piece, position, orientation) {
  if (game.game_over() === true ||
      (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

var onDrop = function(source, target) {
  removeGreySquares();

  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return 'snapback';

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
  var status = '';
  var gameOver = false;

  var moveColor = 'White';
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // checkmate?
  if (game.in_checkmate() === true) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
    gameOver = true;
    console.log("CHECKMATE");
  }

  // draw?
  else if (game.in_draw() === true) {
    status = 'Game over, drawn position';
    gameOver = true;
    console.log("DRAW");
  }

  // game still on
  else {
    status = moveColor + ' to move';

    // check?
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
      // Turn King's square red
      // redSquare(findPiece(game.turn() + 'K'));
    }
  }

  statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());

  if (!gameOver && game.turn() !== myColor) {
    var moveRequest = {
      "command": "get_move",
      "model": model,
      "pgn": game.pgn()
    }

    sendRequest(moveRequest, function(msg) {
      window.setTimeout(makeAIMove, 500, msg);
    });
  }
};

var cfg = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
  onMouseoutSquare: onMouseoutSquare,
  onMouseoverSquare: onMouseoverSquare
};

/**************
 * UI buttons *
 **************/
var restart = function() {
  board.start();
  game.reset();
  updateStatus();
}

// Thank you, StackOverflow
var save = function(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}

var load = function() {
  // Open file explorer
  $('#uploadPgn').trigger('click');
  var fileReader = new FileReader();
  // Read PGN and update board accordingly
  $('#uploadPgn').on('change', function () {
    var fileReader = new FileReader();
    fileReader.onload = function () {
      var gamePgn = fileReader.result;
      game.load_pgn(gamePgn);
      board.position(game.fen());
      updateStatus();
    };

    fileReader.readAsText($('#uploadPgn').prop('files')[0]);
  });
}

var undo = function() {
  if (game.turn() === myColor) {
    game.undo(); // Undo my move
    game.undo(); // Undo computer's move
    board.position(game.fen());
    updateStatus();
  }
}

var sendRequest = function(request, callBack) {
  $.ajax({
    method: 'GET',
    //the url where you want to sent the userName and password to
    url: '/api/v1/http',
    dataType: 'json',
    contentType: 'application/json',
    //json object to sent to the authentication url
    data: JSON.stringify(request),
    success: function(msg) {
      callBack(msg);
    },
    error: function (msg) {
      console.log(msg);
    }
  });
}

var onModelRequestComplete = function(msg) {
  model = msg.models[0].internalName; // RANDOM FOR NOW !!!
  console.log(model);
  board = ChessBoard('board', cfg);
  updateStatus();
  $('#restartBtn').on('click', restart);
  $('#saveBtn').on('click', function() {
    save("saved_game.pgn", game.pgn());
  });
  $('#loadBtn').on('click', load);
  $('#undoBtn').on('click', undo);
}

/********
 * Main *
 ********/

var modelRequest = {
  "command": "list_models"
}

sendRequest(modelRequest, onModelRequestComplete);
