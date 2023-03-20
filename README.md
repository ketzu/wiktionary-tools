# wiktionary-tools

Set of scripts I used to work with a wiktionary dump

Yes this is not that helpful, but maybe I'll clean it up, at least I'll find it again here.

## What?

I wanted a set of korean vocabulary with english explanations.

Wiktionary has exactly that, so I looked through the xml data dump of the wikimedia foundation to extract the information I needed.
The resulting python files are contained in this repository, they are, currently, not nice to use and produce only my desired outcome.

## Result files

 * vocab.csv contains the vocabulary with its extracted description
 * templates.csv lists all found template tags starting with 'ko-' and their occurences, as they seemed relevant
 * examples.csv extracts example sentences, especially 'ko-usex' templates

## Usage

 1. process_xml.py scanned the xml file from the data dump and filters it for korean pages, the result is stored as an intermediate data.pkl
 2. process_pkl.py loads this pickle file and extracts examples and parses the sections to some degree
 3. discover_templates.py uses the data.pkl file to discover the template types used
 4. process_templates.py transforms all discovered entries based on (especially) utility.filters 

# Data license

As the data source is [wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Main_Page), all resulting data is obviously [CC-BY-SA](https://creativecommons.org/licenses/by-sa/3.0/).
