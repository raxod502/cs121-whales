// board: chessboard.js
// game: chess.js

/*************************
 * Highlight legal moves * 
 *************************/
var removeGreySquares = function() {
  $('#board .square-55d63').css('background', '');
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

var makeRandomMove = function() {
  var possibleMoves = game.moves();
  var randomIndex = Math.floor(Math.random() * possibleMoves.length);
  game.move(possibleMoves[randomIndex]);
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
  window.setTimeout(makeRandomMove, 500);
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
  var status = '';

  var moveColor = 'White';
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // checkmate?
  if (game.in_checkmate() === true) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
  }

  // draw?
  else if (game.in_draw() === true) {
    status = 'Game over, drawn position';
  }

  // game still on
  else {
    status = moveColor + ' to move';

    // check?
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
    }
  }

  statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());
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
  game.undo(); // Undo my move
  game.undo(); // Undo computer's move
  board.position(game.fen());
  updateStatus();
}

/********
 * Main * 
 ********/
board = ChessBoard('board', cfg);
updateStatus();
$('#restartBtn').on('click', restart);
$('#saveBtn').on('click', function() {
  save("saved_game.pgn", game.pgn());
});
$('#loadBtn').on('click', load);
$('#undoBtn').on('click', undo);
