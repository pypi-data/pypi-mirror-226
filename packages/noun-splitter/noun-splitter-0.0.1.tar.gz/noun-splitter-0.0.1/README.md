# SECOS
This repo is a modular python implementation of the SECOS algorithm for decomposing composite nouns.

Based on the SECOS algorithm:

[original python implementation](https://github.com/riedlma/SECOS)

[original paper](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2016-riedletal-naacl.pdf)

However, the training data of the models have been distilled slightly to reduce the size of the models. More information on this can be found in the pretrained-models directory in the github repo. Typically though it involves trimming out words with low frequency counts, words with non-unicode characters etc. 

# Installation

## From Github
`pip install git+https://github.com/mhaugestad/noun-splitter.git -U`

## From Source
```
git clone
cd noun-splitter
pip install -e . -U
```

## From Pip
```
pip install noun-splitter
```

## Installing models:
The module relies on pretrained models to be passed in. These can be downloaded from command line as follows:

`python -m secos download --model de`

The command line tool also takes an optional argument --overwrite. This is to be used if you would like to redownload a model for whatever reason, as follows:

`python -m secos download --model no --overwrite`

Alternatively, you can download models directly from a python script or notebook like this:

```
from secos import Decomposition

Decomposition.download_model('de')
```

Available models and their names are:

| Language  | Model |
| ------------- | ------------- |
| Danish | da |
| German | de |
| English | en |
| Spanish | es |
| Estonian | et |
| Finnish | fi |
| Hungarian | hu |
| Latin | la |
| Latvian | lv |
| Netherland | nl |
| Norway | no |
| Swedish | sv |

# Basic Usage
```
from secos import Decomposition

model = Decomposition.load_model('de')

secos = Decomposition(model)

secos.decompose("Bundesfinanzministerium")

['bundes', 'finanz', 'ministerium']
```

# Evaluation
The evaluation folder in the github repo includes code for the evaluation of the pretrained models.