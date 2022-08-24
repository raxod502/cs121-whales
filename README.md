# W.H.A.L.E.S.

Chess AI web application using minimax and deep learning on backend.

## Backend
### Backend setup

Install the following dependencies:

* [Git](https://git-scm.com/)
* [Git LFS](https://git-lfs.github.com/)
* [Python 3](https://www.python.org/)
* [Poetry](https://python-poetry.org/)

Clone this repository:

    $ git clone https://github.com/raxod502/cs121-whales.git
    $ cd cs121-whales

Run the server:

    $ make run-server-dev

Code is live-reloaded. To test in production mode using a real WSGI
server:

    $ make run-server-prod-test

In either case, the backend is now running on `localhost:5000`, or
whichever port is printed on the command line.

### Backend usage

Install [HTTPie](https://httpie.org/). On macOS, that looks like this:

    $ brew install httpie

This makes it easy to test HTTP requests.

    $ http GET localhost:5000/not-found
    $ http GET localhost:5000/api/v1 command=unknown_command
    $ http GET localhost:5000/api/v1 command=list_models
    $ http GET localhost:5000/api/v1 command=get_move model=random pgn="1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 *"

## General tips
### Developing documentation

Install [Grip](https://github.com/joeyespo/grip). On macOS, that looks
like this:

    $ brew install grip

Then you can render the README locally, so you can correct formatting
errors before pushing to GitHub:

    $ grip

Or you can render another Markdown document:

    $ grip doc/api-spec.md

Typically the server runs on `localhost:6419` if that port is
available.

### Vendored files

We vendor a forked version of `chessboard.js` from
[here](https://github.com/raxod502/chessboardjs/blob/whales/src/chessboard.js),
minified [online](https://javascript-minifier.com/).
