## Notes on the bug where minimax takes too long and the HTTP request times out

### Minimax length
Some quick tests showed that, with a starting board, minimax takes:
* < 1 sec for max_plies = 1
* ~ 60 sec for max_plies = 2
* 15+ min for max_plies = 3 (I stopped it at around 15m, but it was still thinking)

#### Possible minimax solution for later
We might look into calling minimax iteratively, with increasing depth (ie with depth 1,
then depth 2, etc.), storing the best move we've yet found, until a set amount of time
has passed (at which point it kills the current minimax search and returns the best move
yet found). This would require storing the work that minimax does in each round and
accessing it despite the recursive calls - this [decorator] might help with that. It looks
like running this sort of loop would require either threading or using system signals.

### Gunicorn 
I found a [setting] in gunicorn that might be what we want: ``-t INT`` or ``--timeout INT``
which regulates how many seconds a worker can be silent before it is killed and restarted.
This looks like it is default set to 30, which would definitely cause the 50+ sec minimax to
be killed. We might want to try adding ``-t 75`` to the gunicorn call.

### Server testing
* __run-server-prod__
Doesn't work for me?
* __run-server-dev__
If you select the "material to depth 2" model, it takes ~60 seconds for the computer to 
think, but it does eventually make a move so you can play the game. If gunicorn is the
problem, this result makes sense, because that make command does not appear to use gunicorn.
* __whales.life__
Computer never moves.


[setting]: http://docs.gunicorn.org/en/stable/settings.html
[decorator]: https://docs.python.org/3/library/functools.html#functools.lru_cache
