# Johns Hopkins University - Whiting Engineering

## Prediction of Protein Secondary Structure using Machine Learning
Final Project - Algorithms for Structural Bioinformatics (605.751)

## Development Environment
Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and activate it.
Then install or update the dependencies by running:
```bash
pip install -r requirements.txt
```

## Run `pred-sec-struc`

`pred-sec-struc` is a command line application. To generate a model for an amino acid sequence
input its [PDB](https://www.rcsb.org/) ID as an input like so:
```bash
python pred-sec-struc.py -g <PDBID>
```
where `<PDBID>` could be `1MOA` for myoglobin. Run the same command with the `-h` flag for more
information on the syntax.

## Tests
To run all test open a terminal and run:
```bash
python -m unittest
```




