# API specification
## Summary

The frontend and backend communicate over a single WebSocket API
endpoint at `/api/v1`. The format is JSON. No authentication or
session management is required, and the API is stateless.

## Conventions

Key names are camelCase because this makes API responses much easier
to process in JavaScript. Model names are snake\_case because they
refer to specific features of the backend, which is written in Python,
and will not be used as variable names in JavaScript.

Game states are passed in [PGN] format.

## Examples
### Request list of chess models

Request:

    {
      "command": "list_models"
    }

Response:

    {
      "error": null,
      "models": [
        {
          "internalName": "resnet34-depth8",
          "displayName": "resnet34 to depth 8",
          "description": "Make moves using minimax tree to depth 8 with resnet34 convolutional neural net as evaluation function."
        }
      ]
    }

### Request a move

Request:

    {
      "command": "get_move",
      "model": "resnet34-depth8",
      "pgn": "1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 *"
    }

Response:

    {
      "error": null,
      "pgn": "1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7# *"
    }

### Error handling
#### Invalid command

Request:

    {
      "command": "invalid_command"
    }

Response:

    {
      "error": "unknown command 'invalid_command'"
    }

#### Invalid PGN

Request:

    {
      "command": "get_move",
      "model": "resnet34-depth8",
      "pgn": "not actual pgn"
    }

Response:

    {
      "error": "invalid pgn 'not actual pgn'",
    }

[pgn]: https://en.wikipedia.org/wiki/Portable_Game_Notation
