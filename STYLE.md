## Code style

### General Formatting
We use a [pre-commit hook](https://githooks.com/) to automatically run
[Black](https://github.com/ambv/black) and
[Prettier](https://prettier.io/) on all code before it is checked in.
This takes care of most disagreements about style (spacing, import
order, etc.).

No trailing whitespace.

### Python
#### Comments
- Wrap at 72 characters.
- Write in complete sentences, starting with a capital letter.
- Avoid end-of-line comments if possible. In most cases, comments
  should go on the line immediately above the line of code they are
  referring to. If they are explaining a longer block of code, taken
  together, alternative conventions may be used.
- For if-else statements, comments describing the condition go below
  the condition statement and are indented. Example:

      if cond_1:
          # in this case, do x
          code
      else:
          # otherwise, do y
          code

#### Naming Conventions
- `camelCase` for JavaScript (`PascalCase` for classes)
- `snake_case` for Python (`SCREAMING_SNAKE_CASE` for global constants
  and `PascalCase` for classes)
- Use variable names that are as useful as possible

#### Function Conventions
- Functions require good docstrings. This means they need to describe
  the input parameters and output type, how all data is formatted, any
  side effects, etc. When in doubt, include more information.
- Docstrings should be wrapped at 72 characters, like all comments.

Docstrings should have the following format:

    def functionName(x, y):
        """
        Here is the first paragraph. Wrap to 72 columns.

        If you have multiple paragraphs, leave a blank line between
        them. No trailing whitespace!
        """
        code begins

Note that the triple quotes are always on their own lines, and that
there is no empty line between the end of the docstring and the
beginning of the function’s code. Use the imperative tense for
description (e.g., "Return x times 2").

#### Import Conventions
Follow [PEP8](https://www.python.org/dev/peps/pep-0008/#imports).

#### JavaScript

- Always `"use strict"`.
- Use `const` where possible; otherwise `let`. Never use `var`.
- Never use global variables.
