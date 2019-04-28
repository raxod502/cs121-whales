# Testing
## Dynamic testing

See [here](https://docs.google.com/document/d/1dBsCISVta9HC85s470jur387ijljPglaegBSbq-4jAA/edit?usp=sharing).

## Static testing

Most of the below linter output seems pretty much like garbage.

* Too many return statements is BS
* Hanging indent stuff conflicts with Black
* Missing module docstrings is valid, but we already have PRs to
  address that
* Missing imports are because pylint isn't configured with our
  virtualenv
* It complains about single-letter variables, but I don't super think
  that's a big issue
* Using enumerate is an okay hint, but it really doesn't matter that
  much
* It reports many errors on our vendored code
* Access to protected member is a question for Shannon but I think
  it's a workaround for a bug
* eslint mostly doesn't understand our imports

No use integrating these tools into our build system.

### pylint output

    ************* Module whales.api
    whales/api.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/api.py:10:4: W0107: Unnecessary pass statement (unnecessary-pass)
    whales/api.py:31:0: R0911: Too many return statements (8/6) (too-many-return-statements)

    -----------------------------------
    Your code has been rated at 9.09/10

    ************* Module minimax
    whales/minimax_ab/minimax.py:28:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        board,
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:29:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        max_plies=2,
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:30:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        curr_depth=0,
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:31:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        alpha=float("-inf"),
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:32:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        beta=float("inf"),
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:33:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        eval_fn=eval_material,
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:34:0: C0330: Wrong hanging indentation before block (add 4 spaces).
        starting_player=None,
        ^   | (bad-continuation)
    whales/minimax_ab/minimax.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/minimax_ab/minimax.py:1:0: E0401: Unable to import 'chess' (import-error)
    whales/minimax_ab/minimax.py:3:0: E0401: Unable to import 'numpy' (import-error)
    whales/minimax_ab/minimax.py:18:4: W0612: Unused variable 'black_won' (unused-variable)
    whales/minimax_ab/minimax.py:27:0: R0913: Too many arguments (7/5) (too-many-arguments)
    whales/minimax_ab/minimax.py:27:0: R0914: Too many local variables (17/15) (too-many-locals)
    whales/minimax_ab/minimax.py:62:4: C0103: Variable name "v" doesn't conform to snake_case naming style (invalid-name)
    whales/minimax_ab/minimax.py:66:8: C0103: Variable name "v" doesn't conform to snake_case naming style (invalid-name)
    whales/minimax_ab/minimax.py:68:8: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
    whales/minimax_ab/minimax.py:87:16: C0103: Variable name "v" doesn't conform to snake_case naming style (invalid-name)
    whales/minimax_ab/minimax.py:98:8: C0103: Variable name "v" doesn't conform to snake_case naming style (invalid-name)
    whales/minimax_ab/minimax.py:100:8: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
    whales/minimax_ab/minimax.py:117:16: C0103: Variable name "v" doesn't conform to snake_case naming style (invalid-name)
    whales/minimax_ab/minimax.py:130:0: C0111: Missing function docstring (missing-docstring)
    whales/minimax_ab/minimax.py:133:4: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
    whales/minimax_ab/minimax.py:2:0: W0611: Unused import random (unused-import)
    whales/minimax_ab/minimax.py:2:0: C0411: standard import "import random" should be placed before "import chess" (wrong-import-order)

    -----------------------------------
    Your code has been rated at 4.39/10

    ************* Module whales.models
    whales/models.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/models.py:15:4: W0107: Unnecessary pass statement (unnecessary-pass)

    -----------------------------------
    Your code has been rated at 9.56/10

    ************* Module chess_alpha_data
    whales/neural_net/chess_alpha_data.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:3:0: E0401: Unable to import 'numpy' (import-error)
    whales/neural_net/chess_alpha_data.py:24:0: C0103: Constant name "Winner" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:28:0: C0103: Constant name "pieces_order" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:29:0: C0103: Constant name "castling_order" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:33:0: C0103: Constant name "ind" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:46:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:56:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:59:4: C0102: Black listed name "foo" (blacklisted-name)
    whales/neural_net/chess_alpha_data.py:62:4: C0103: Argument name "a" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:67:4: C0103: Argument name "aa" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:85:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:86:4: C0102: Black listed name "foo" (blacklisted-name)
    whales/neural_net/chess_alpha_data.py:131:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:137:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:143:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:148:12: C0103: Variable name "v" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/chess_alpha_data.py:155:0: C0111: Missing function docstring (missing-docstring)
    whales/neural_net/chess_alpha_data.py:167:0: C0111: Missing function docstring (missing-docstring)

    -----------------------------------
    Your code has been rated at 6.81/10

    ************* Module data_conversion
    whales/neural_net/data_conversion.py:31:6: W0511: TODO: refactor to give max_games a default value as a parameter (fixme)
    whales/neural_net/data_conversion.py:60:6: W0511: TODO: update to match current file_to_arrays (fixme)
    whales/neural_net/data_conversion.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/neural_net/data_conversion.py:6:0: E0401: Unable to import 'chess' (import-error)
    whales/neural_net/data_conversion.py:7:0: E0401: Unable to import 'chess.pgn' (import-error)
    whales/neural_net/data_conversion.py:8:0: E0401: Unable to import 'numpy' (import-error)
    whales/neural_net/data_conversion.py:35:4: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/data_conversion.py:35:7: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/data_conversion.py:61:4: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/data_conversion.py:61:7: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/data_conversion.py:61:11: E1120: No value for argument 'use_chess_alpha' in function call (no-value-for-parameter)
    whales/neural_net/data_conversion.py:70:4: W0612: Unused variable 'x_read' (unused-variable)
    whales/neural_net/data_conversion.py:71:4: W0612: Unused variable 'y_read' (unused-variable)
    whales/neural_net/data_conversion.py:232:4: C0103: Constant name "parser" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/data_conversion.py:257:4: C0103: Constant name "args" doesn't conform to UPPER_CASE naming style (invalid-name)

    -----------------------------------
    Your code has been rated at 6.77/10

    ************* Module interface
    whales/neural_net/interface.py:145:6: W0511: TODO: QUESTION FOR BEN: WHAT DOES MINIMAX WANT? (fixme)
    whales/neural_net/interface.py:187:2: W0511: TODO: check if there is a better way to integrate this list with models.py (fixme)
    whales/neural_net/interface.py:192:2: W0511: TODO: (optional optimization) lazily load neural nets rather than upfront (fixme)
    whales/neural_net/interface.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/neural_net/interface.py:3:0: E0401: Unable to import 'chess' (import-error)
    whales/neural_net/interface.py:4:0: E0401: Unable to import 'numpy' (import-error)
    whales/neural_net/interface.py:5:0: E0401: Unable to import 'keras.models' (import-error)
    whales/neural_net/interface.py:11:21: W0621: Redefining name 'neural_nets' from outer scope (line 195) (redefined-outer-name)
    whales/neural_net/interface.py:30:4: W0621: Redefining name 'neural_nets' from outer scope (line 195) (redefined-outer-name)
    whales/neural_net/interface.py:76:8: C0103: Variable name "l1" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:77:12: C0103: Variable name "n1" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:97:17: C0103: Variable name "l2" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:97:21: C0103: Variable name "n2" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:101:8: C0103: Variable name "l1" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:102:8: C0103: Variable name "l" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:103:12: C0103: Variable name "p" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/interface.py:138:4: W0612: Unused variable 'policy' (unused-variable)
    whales/neural_net/interface.py:169:0: C0103: Constant name "move_labels" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/interface.py:178:12: W0612: Unused variable 'value' (unused-variable)
    whales/neural_net/interface.py:190:0: C0103: Constant name "neural_net_names" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/interface.py:195:0: C0103: Constant name "neural_nets" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/interface.py:199:4: W0212: Access to a protected member _make_predict_function of a client class (protected-access)
    whales/neural_net/interface.py:201:0: C0103: Constant name "neural_net_dict" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/interface.py:202:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
    whales/neural_net/interface.py:207:0: C0103: Constant name "model_predict_func_dict" doesn't conform to UPPER_CASE naming style (invalid-name)

    -----------------------------------
    Your code has been rated at 5.43/10

    ************* Module test_neural_net
    whales/neural_net/test_neural_net.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/neural_net/test_neural_net.py:4:0: E0401: Unable to import 'numpy' (import-error)
    whales/neural_net/test_neural_net.py:36:4: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/test_neural_net.py:37:4: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
    whales/neural_net/test_neural_net.py:67:4: C0103: Constant name "parser" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/neural_net/test_neural_net.py:89:4: C0103: Constant name "args" doesn't conform to UPPER_CASE naming style (invalid-name)

    -----------------------------------
    Your code has been rated at 5.65/10

    ************* Module whales.server
    whales/server.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/server.py:5:0: E0401: Unable to import 'flask' (import-error)
    whales/server.py:6:0: E0401: Unable to import 'flask_talisman' (import-error)
    whales/server.py:10:0: C0103: Constant name "app" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/server.py:64:4: C0103: Constant name "port" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/server.py:67:12: C0103: Constant name "port" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/server.py:69:12: C0103: Constant name "port" doesn't conform to UPPER_CASE naming style (invalid-name)
    whales/server.py:71:8: C0103: Constant name "port" doesn't conform to UPPER_CASE naming style (invalid-name)

    -----------------------------------
    Your code has been rated at 5.00/10

    ************* Module chess
    whales/util/chess.py:50:0: C0305: Trailing newlines (trailing-newlines)
    whales/util/chess.py:1:0: C0111: Missing module docstring (missing-docstring)
    whales/util/chess.py:1:0: E0611: No name 'pgn' in module 'chess' (no-name-in-module)
    whales/util/chess.py:1:0: E0401: Unable to import 'chess.pgn' (import-error)
    whales/util/chess.py:2:0: W0406: Module import itself (import-self)
    whales/util/chess.py:11:4: W0107: Unnecessary pass statement (unnecessary-pass)
    whales/util/chess.py:14:24: E1101: Module 'chess' has no 'pgn' member (no-member)
    whales/util/chess.py:20:4: C0111: Missing method docstring (missing-docstring)
    whales/util/chess.py:20:4: R0201: Method could be a function (no-self-use)
    whales/util/chess.py:14:0: R0903: Too few public methods (1/2) (too-few-public-methods)
    whales/util/chess.py:32:11: E1101: Module 'chess' has no 'pgn' member (no-member)
    whales/util/chess.py:40:11: E1101: Module 'chess' has no 'pgn' member (no-member)
    whales/util/chess.py:49:11: E1101: Module 'chess' has no 'Move' member (no-member)
    whales/util/chess.py:3:0: C0411: standard import "import io" should be placed before "import chess.pgn" (wrong-import-order)

    -------------------------------------
    Your code has been rated at -10.00/10

### eslint output

    /Users/raxod502/files/school/hmc/junior/spring/cs121/cs121-whales/whales/static/js/new-game.js
       8:3   error  '$' is not defined           no-undef
      10:20  error  '$' is not defined           no-undef
      13:27  error  '$' is not defined           no-undef
      14:16  error  'model' is not defined       no-undef
      17:42  error  'encodeHash' is not defined  no-undef
      21:18  error  'decodeHash' is not defined  no-undef
      26:3   error  '$' is not defined           no-undef
      29:1   error  'apiRequest' is not defined  no-undef
      35:5   error  '$' is not defined           no-undef
      37:7   error  '$' is not defined           no-undef
      41:9   error  '$' is not defined           no-undef

    ✖ 11 problems (11 errors, 0 warnings)


    /Users/raxod502/files/school/hmc/junior/spring/cs121/cs121-whales/whales/static/js/play-controller.js
        4:20  error  'View' is not defined                            no-undef
        5:17  error  'Model' is not defined                           no-undef
       28:33  error  'square' is defined but never used               no-unused-vars
       68:33  error  'statusText' is defined but never used           no-unused-vars
       81:16  error  'apiRequest' is not defined                      no-undef
      148:7   error  'controller' is assigned a value but never used  no-unused-vars

    ✖ 6 problems (6 errors, 0 warnings)


    /Users/raxod502/files/school/hmc/junior/spring/cs121/cs121-whales/whales/static/js/play-model.js
       20:12  error  'Chess' is not defined       no-undef
      174:12  error  'encodeHash' is not defined  no-undef
      185:16  error  'Chess' is not defined       no-undef
      190:20  error  'decodeHash' is not defined  no-undef

    ✖ 4 problems (4 errors, 0 warnings)


    /Users/raxod502/files/school/hmc/junior/spring/cs121/cs121-whales/whales/static/js/play-view.js
       17:10  error  'View' is defined but never used         no-unused-vars
       30:17  error  'ChessBoard' is not defined              no-undef
       33:35  error  'piece' is defined but never used        no-unused-vars
       36:34  error  'piece' is defined but never used        no-unused-vars
       39:36  error  'position' is defined but never used     no-unused-vars
       39:46  error  'orientation' is defined but never used  no-unused-vars
       55:5   error  '$' is not defined                       no-undef
       56:5   error  '$' is not defined                       no-undef
       57:5   error  '$' is not defined                       no-undef
       59:5   error  '$' is not defined                       no-undef
       60:5   error  '$' is not defined                       no-undef
       65:5   error  'apiRequest' is not defined              no-undef
       81:24  error  '$' is not defined                       no-undef
       96:7   error  '$' is not defined                       no-undef
      106:24  error  '$' is not defined                       no-undef
      114:7   error  '$' is not defined                       no-undef
      121:7   error  '$' is not defined                       no-undef
      129:7   error  '$' is not defined                       no-undef
      133:37  error  'encodeHash' is not defined              no-undef

    ✖ 19 problems (19 errors, 0 warnings)


    /Users/raxod502/files/school/hmc/junior/spring/cs121/cs121-whales/whales/static/js/util.js
       1:10  error  'apiRequest' is defined but never used  no-unused-vars
       2:10  error  '$' is not defined                      no-undef
      11:12  error  Unexpected console statement            no-console
      15:10  error  'decodeHash' is defined but never used  no-unused-vars
      27:10  error  'encodeHash' is defined but never used  no-unused-vars
      35:1   error  '$' is not defined                      no-undef
      36:3   error  '$' is not defined                      no-undef

    ✖ 7 problems (7 errors, 0 warnings)
