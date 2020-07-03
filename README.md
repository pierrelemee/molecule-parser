![test](https://github.com/pierrelemee/molecule-parser/workflows/test/badge.svg)

# molecule-parser

Python library to flatten a molecule formula into an atoms dictionary

## Installation & run

`molecule-parser` is designed for Python 3.7.

Installation and executions are performed upon `pipenv`:

```bash
pipenv install
pipenv run python main.py
``` 


## Usage

The main script `main.py` accepts as many arguments as formulas to be parsed.
 
In addition, you can specify two options:
- `--stdin` (or `-i`): parse each line from standard input as a unique formula
- `--json` (or `-json`): encode all the flattened formulas into an unique JSON payload

Examples:

```bash
$ pipenv run python main.py 'O((CN2)3K)4'
{'O': 1, 'K': 4, 'C': 12, 'N': 24}
# Parse formulas from formulas.txt file and encode as JSON 
$ cat formulas.txt | pipenv run python main.py --stdin -j
[
    {
        "C": 12,
        "K": 4,
        "N": 24,
        "O": 1
    },
    {
        "H": 2,
        "Mg": 1,
        "O": 2
    }
]
```
