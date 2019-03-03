// board: chessboard.js
// game: chess.js

/*****************************************
 * Turn King's square red while in check * 
 *****************************************/

var redSq = '';
var allSquares = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                  'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
                  'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
                  'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
                  'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
                  'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
                  'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
                  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'];
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
  console.log("remove gray squares");
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
  // removeRedSquares();
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
      // Turn King's square red
      redSquare(findPiece(game.turn() + 'K'));
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
console.log("hello");
var request = {
  "command": "list_models"
}

console.log("hey");

$.ajax
  ({
      type: "POST",
      //the url where you want to sent the userName and password to
      url: '/api/v1/http',
      dataType: 'json',
      contentType: 'application/json',
      //json object to sent to the authentication url
      data: JSON.stringify(request),
      success: function (msg) {
          console.log(msg)
          console.log("SUCCESS!")
      },
      error: function (msg) {
        console.log(msg);
        console.log("ERROR")
      }
  });

  // $.post("/api/v1/http", JSON.stringify(request), function(){
  //   console.log("done");
  // })

board = ChessBoard('board', cfg);
updateStatus();
$('#restartBtn').on('click', restart);
$('#saveBtn').on('click', function() {
  save("saved_game.pgn", game.pgn());
});
$('#loadBtn').on('click', load);
$('#undoBtn').on('click', undo);
