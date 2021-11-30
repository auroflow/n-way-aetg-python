# n-way-aetg-python

This is a naïve implementation of the AETG algorithm [(link)](https://ieeexplore.ieee.org/document/605761), which generates test cases that cover pair-wise or n-way combinations of the test parameters.

## Install dependencies

Built on Python 3.10.

```bash
$ python -m venv env

> env\Scripts\activate  # Windows
$ . env/bin/activate    # Linux / macOS

(env) $ pip install -r requirements.txt
```

## Usage

```bash
(venv) $ python main.py --help
usage: main.py [-h] [-s SOURCE] [-d DESTINATION] [-n DIMENSION]

options:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        path to the CSV source file
  -d DESTINATION, --destination DESTINATION
                        path to destination folder
  -n DIMENSION, --dimension DIMENSION
                        dimension of coverage required
(venv) $ python main.py --source jd.csv --destination output.xlsx --dimension 3
13364 combinations to cover.
100%|█████████████████████████████████| 13364/13364 [00:29<00:00, 407.96it/s, 2069 cases generated]
Done.
```

If arguments are not provided, the program will try to read input from `input.csv`, generate a test plan with pair-wise coverage, and output to `output.xlsx`.

Two sample data files:

- `index.csv` (Longce Testing Platform)
- `jd.csv` (JD's searching page)

