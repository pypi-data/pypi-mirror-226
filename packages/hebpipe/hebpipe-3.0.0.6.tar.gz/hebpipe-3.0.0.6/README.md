# HebPipe Hebrew NLP Pipeline

A simple NLP pipeline for Hebrew text in UTF-8 encoding, using standard components. Basic features:

  * Performs end to end processing, optionally skipping steps as needed:
    * whitespace tokenization
    * morphological segmentation
    * POS tagging
    * morphological tagging
    * dependency parsing
    * named and non-named entity type recognition (**experimental**)
    * coreference resolution (**experimental**)
  * Does not alter the input string (text reconstructible from, and alignable to output)
  * Compatible with Python 2.7/3.5+, Linux, Windows and OSX

Note that entity recognition and coreference are still in beta and offer rudimentary accuracy.

To cite this tool in academic papers please refer to this paper:

Zeldes, Amir, Nick Howell, Noam Ordan and Yifat Ben Moshe (2022) [A Second Wave of UD Hebrew Treebanking and Cross-Domain Parsing](https://arxiv.org/abs/2210.07873). In: *Proceedings of EMNLP 2022*. Abu Dhabi, UAE.


```
@InProceedings{ZeldesHowellOrdanBenMoshe2022,
  author    = {Amir Zeldes and Nick Howell and Noam Ordan and Yifat Ben Moshe},
  booktitle = {Proceedings of {EMNLP} 2022},
  title     = {A SecondWave of UD Hebrew Treebanking and Cross-Domain Parsing},
  pages     = {4331--4344},
  year      = {2022},
  address   = {Abu Dhabi, UAE},
}
```

## Installation

Either install from PyPI using pip:

`pip install hebpipe`

And run as a module:

`python -m hebpipe example_in.txt`

Or install manually: 

  * Clone this repository into the directory that the script should run in (git clone https://github.com/amir-zeldes/HebPipe)
  * In that directory, install the dependencies under **Requirements**, e.g. by running `python setup.py install` or `pip install -r requirements.txt`
  
Models can be downloaded automatically by the script on its first run.
  
## Requirements

### Python libraries

The NLP pipeline will run on Python 2.7+ or Python 3.5+ (2.6 and lower are not supported). Required libraries:

```
requests
transformers==3.5.1
torch==1.6.0
xgboost==0.81
rftokenizer
numpy
scipy
depedit
pandas
joblib
xmltodict
diaparser==1.1.2
flair==0.6.1
stanza
conllu
```

You should be able to install these manually via pip if necessary (i.e. `pip install rftokenizer` etc.).

Note that some older versions of Python + Windows do not install numpy correctly from pip, in which case you can download compiled binaries for your version of Python + Windows here: https://www.lfd.uci.edu/~gohlke/pythonlibs/, then run for example:

`pip install c:\some_directory\numpy‑1.15.0+mkl‑cp27‑cp27m‑win_amd64.whl`


### Model files

Model files are too large to include in the standard GitHub repository. The software will offer to download them automatically. The latest models can also be downloaded manually at https://gucorpling.org/amir/download/heb_models_v3/. 

## Command line usage

```
usage: python heb_pipe.py [OPTIONS] files

positional arguments:
  files                 File name or pattern of files to process (e.g. *.txt)

optional arguments:
  -h, --help            show this help message and exit

standard module options:
  -w, --whitespace      Perform white-space based tokenization of large word
                        forms
  -t, --tokenize        Tokenize large word forms into smaller morphological
                        segments
  -p, --posmorph        Do POS tagging and Morphological Tagging
  -l, --lemma           Do lemmatization
  -d, --dependencies    Parse with dependency parser
  -e, --entities        Add entity spans and types
  -c, --coref           Add coreference annotations
  -s SENT, --sent SENT  XML tag to split sentences, e.g. sent for <sent ..> or none for no splitting (otherwise automatic sentence splitting)
  -o {pipes,conllu,sgml}, --out {pipes,conllu,sgml}
                        Output CoNLL format, SGML or just tokenize with pipes

less common options:
  -q, --quiet           Suppress verbose messages
  -x EXTENSION, --extension EXTENSION
                        Extension for output files (default: .conllu)
  --cpu                 Use CPU instead of GPU (slower)
  --disable_lex         Do not use lexicon during lemmatization
  --dirout DIROUT       Optional output directory (default: this dir)
  --punct_sentencer     Only use punctuation (.?!) to split sentences (deprecated but faster)
  --from_pipes          Input contains subtoken segmentation with the pipe character (no automatic tokenization is performed)
  --version             Print version number and quit
```

### Example usage

Whitespace tokenize, tokenize morphemes, add pos, lemma, morph, dep parse with automatic sentence splitting, 
entity recognition and coref for one text file, output in default conllu format:
> python heb_pipe.py -wtpldec example_in.txt        

OR specify no processing options (automatically assumes you want all steps)
> python heb_pipe.py example_in.txt        

Just tokenize a file using pipes:
> python heb_pipe.py -wt -o pipes example_in.txt     

Pos tag, lemmatize, add morphology and parse a pre-tokenized file, splitting sentences by existing <sent> tags:
> python heb_pipe.py -pld -s sent example_in.txt  

Add full analyses to a whole directory of *.txt files, output to a specified directory:    
> python heb_pipe.py -wtpldec --dirout /home/heb/out/ *.txt

Parse a tagged TT SGML file into CoNLL tabular format for treebanking, use existing tag <sent> to recognize sentence borders:
> python heb_pipe.py -d -s sent example_in.tt

## Input formats

The pipeline accepts the following kinds of input:

  * Plain text, with normal Hebrew whitespace behavior. Newlines are assumed to indicate a sentence break, but longer paragraphs will receive automatic sentence splitting too.
  * Gold super-tokenized: if whitespace tokenization is already done, you can leave out `-w`. The system expect one super-token per line in this case (e.g. <bbyt> is on one line)
  * Gold tokenized: if gold morphological segmentation is already done, you can input one gold token per line.
  * Pipes: if morphological segmentation is already done, you can also input one super-token per line with sub-tokens separated by pipes - use `--from_pipes` for this option (allows running the segmenter, outputting pipes for manual correction, then continuing NLP processing from pipes)
  * XML sentence tags in input: use -s TAGNAME to indicate an XML tag providing gold sentence boundaries.
