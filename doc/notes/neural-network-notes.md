# Neural Network Notes & Research Summary

Last updated 3/9

## ~ Deep Learning ~ Plan 1: Board Classification

Use a convolutional neural network to classify a chess board as either
belonging to a game where white won, or where black won.

## Data

To train a neural net to classify boards, we need to create a 
dataset that contains discrete board positions labeled with who 
ultimately won. 

There are a variety of online chess game databases to choose from, which 
have various pros and cons. We will need to decide where to get our data.
However, regardless of source, most chess data is stored in [pgn] format, which records the 
entire sequence of moves that occurred in a game, rather than explicit 
intermediate board positions. Thus, there are three main steps between
starting out and feeding data to a neural net:
1. Acquire pgn data
1. Convert from pgn to board positions
1. Convert from board positions to a data format that a neural 
 network can understand
 
### Database options

* [Lichess] A very large database of random people on the internet playing
chess games against one another. It's quite large, and allows for single,
easy downloads of large pgn files. However, it consists largely of random
people on the internet, meaning the average skill of the players is fairly 
low (~18% of games with both players above 1500 ELO, 0.9% above 1800, and
effectively none above 1900), many games end in a resign rather than a strict
checkmate, and it involves a number of 'Blitz' or 'Bullet' games (fast chess,
which also results in poorer play).

* [PGNMentor] A website with a bunch of games sorted by opening, players involved
(so you could download all games played by Gary Kasparov, for example), or event
(so you could download all 10-15 games played in the 2018 world championship). This
allows you to access (presumably) very high quality games, by downloading all of the
world championships. However, each event is a separate link, and would require some
automatic downloading script and data collation to be useful.

* [KingBase] A large databse of chess games with the strict cutoff that all ELO is
above 2000. Similarly to LiChess, this involves relatively few links and separate
downloads, which is convenient. The average game quality (as measured by reported 
ELO and lack of being a blitz or bullet game) is much higher (100% above 2000, 99% 
above 2200, 65% above 2300).

I recommend we focus on using KingBase, because it best combines ease of use
with higher-quality games. If we have extra time, it might be fun to explore
the specifics in PGNMentor, either to just scrape for the extra-high-quality
play in certain events, or to see what happens if you train a neural net
exclusively on games played by Kasparov (for example).

### Convert from pgn to board positions
The [python-chess] library provides an easy way to [convert from pgn]
to a Board representation that allows you to implement the moves that
occurred during the game one-by-one, allowing easy access to each
unique board position that occurred during the game.

### Convert to data that a neural net understands
The next question is how to represent a chess board to a neural network.
This is a non-trivial question, and my research seemed to indicate that
there have been many different ways that people have handled this,
including some (generally older) models that relied on features hand-created
by chess experts (ie, add in specific variables to represent certain
relative positions of pieces). Data representation may be something we want
to revist and tweak as we try to improve model performance. However, I found a 
representation that seemed reasonable and straightforward to implement, 
which I detail below.

#### 'Piece-channel' representation
In essence, this treats the chessboard as an 8x8 image. A normal image
can be black and white, with only one channel, or RGB, with three channels
per pixel. This representation treats the chessboard as an 8x8 image with 7
channels, where the channels represent different piece types, with 0 if there 
is no piece of that type, 1 if there is a white piece, and -1 if there is a 
black piece of that type. The current ordering is (pawn, knight, bishop, rook, 
queen, king). The last 8x8 board represents which color will move next, for an 
8x8 array of 1s if white moves next and an 8x8 array of -1s if black moves 
next. 

This representation was drawn from this [chess-evaluation tutorial].

#### Numpy
Keras (which, see below, is the framework I think we should use)
definitely works with numpy arrays, and I haven't seen an alternate
beyond using a pandas dataframe, which is a pretty similar idea. So, we
need to convert the chess board data into numpy arrays that are 7x8x8,
and stack them together into a dataset of nx7x8x8 (with n total board positions)
and another n dataset of the labels. This processing is done in ``data_conversion.py``
in ``file_to_arrays()``. However, it is a somewhat slow process
(ie, ~30 seconds to process 500 games on my laptop), so it would be nice
to not repeat it more than is needed. Originally, we discussed storing this
data in a .csv file, but numpy provides its own functions ``np.save()`` and
``np.load()`` which serve the purpose of saving and loading the numpy arrays
once they have been computed. This is also implemented in ``data_conversion.py``.
To process in every game in a .pgn file, run ``pgn_to_npy(pgn_file, x_file_name, y_file_name)``
with the desired input file, and the names of the files that you would like to
store the x and y data in. The x and y files should use the '.npy' extension.

## Neural Network

### Keras
I think we should use Keras as the neural network library, because it seems
pretty well-known (so there's a lot of internet resources for it). It can
run on top of several other libraries, including TensorFlow and Theano.

To start with we should try a convolutional neural network. In Keras, you
sequentially add layers to the network you're building. We will I believe
be alternating convolutional and pooling layers. The details of how many
layers and what parameters we pass in will need to be figured out, but will
likely largely also be a question of tweaking parameters and setup to get
better performance later.

[This tutorial] seemed like a very helpful place to begin.

[pgn]: https://en.wikipedia.org/wiki/Portable_Game_Notation
[python-chess]: https://python-chess.readthedocs.io/en/latest/
[convert from pgn]: https://python-chess.readthedocs.io/en/latest/pgn.html
[chess-evaluation tutorial]: https://int8.io/chess-position-evaluation-with-convolutional-neural-networks-in-julia/
[This tutorial]: https://adventuresinmachinelearning.com/keras-tutorial-cnn-11-lines/
[Lichess]: https://database.lichess.org/
[PGNMentor]: https://www.pgnmentor.com/files.html
[KingBase]: http://www.kingbase-chess.net/
