# Named Entity Recognition for Historical Dutch Resolutions

Automated entity tagging pipeline for early modern Dutch PageXML documents using Republic project NER models trained on 17th-18th century Dutch States General resolutions.

## Overview

This repository contains scripts for tagging named entities in PageXML documents exported from Transkribus. The tagged documents can be re-imported into Transkribus with entity annotations preserved in custom attributes.

### Supported Entity Types

- **PER** (persoon) - Persons
- **LOC** (geonames_locations) - Geographic locations
- **ORG** (organisatie) - Organisations
- **DAT** (datum) - Dates
- **HOE** (capaciteit_hoedanigheid) - Government authorities/capacities
- **COM** (commissie_committee) - Committees/commissions
- **RES** (document) - Resolutions

## Prerequisites

- Windows operating system
- Python 3.8-3.11 (Python 3.12+ is not compatible with the Republic models' installation requirements)
- Republic NER models from [Hugging Face](https://huggingface.co/marijnkoolen)

## Installation and Setup

### 1. Clone or Download Repository

Download this repository to your local machine and navigate to the project directory in Command Prompt.

### 2. Create Virtual Environments

The different NER models have incompatible dependencies, particularly the ORG model which requires gensim whilst the DAT model cannot function when gensim is present. To resolve this conflict, each entity type uses an isolated virtual environment.

Open Command Prompt in the project directory and execute the following commands:

```batch
python -m venv venv_per
python -m venv venv_loc
python -m venv venv_org
python -m venv venv_dat
```

### 3. Install Dependencies

Install the required libraries in each environment. Copy and paste these commands one at a time:

```batch
venv_per\Scripts\activate
pip install flair
deactivate

venv_loc\Scripts\activate
pip install flair
deactivate

venv_org\Scripts\activate
pip install flair gensim
deactivate

venv_dat\Scripts\activate
pip install flair
deactivate
```

Note that the first run will download Flair embeddings (approximately 500MB), which may take several minutes depending on your connection.

### 4. Download NER Models

Download the required `.pt` model files from [marijnkoolen's Hugging Face profile](https://huggingface.co/marijnkoolen) and place them in the `models/` directory within this repository:

- `best-model-per.pt` (persons)
- `best-model-loc.pt` (locations)
- `best-model-org.pt` (organisations)
- `best-model-dat.pt` (dates)
- `best-model-hoe.pt` (authorities)
- `best-model-com.pt` (committees)
- `best-model-res.pt` (resolutions)

### 5. Verify Installation

After completing these steps, your directory structure should resemble:

```
Entity_Recognition_Resolutions\
├── tag_entities_direct.py
├── venv_per\
├── venv_loc\
├── venv_org\
├── venv_dat\
├── run_per_tagger.bat
├── run_loc_tagger.bat
├── run_org_tagger.bat
├── run_dat_tagger.bat
├── models\
│   ├── best-model-per.pt
│   ├── best-model-loc.pt
│   ├── best-model-org.pt
│   └── best-model-dat.pt
├── pagexml\
└── README.md
```

## Usage

Each entity type has a dedicated launcher script to ensure compatibility. To tag documents, execute the appropriate batch file from Command Prompt with your PageXML directory and model path as arguments.

#### Tagging Persons

```batch
run_per_tagger.bat ./pagexml ./models/best-model-per.pt
```

#### Tagging Locations

```batch
run_loc_tagger.bat ./pagexml ./models/best-model-loc.pt
```

#### Tagging Organisations

```batch
run_org_tagger.bat ./pagexml ./models/best-model-org.pt
```

#### Tagging Dates

```batch
run_dat_tagger.bat ./pagexml ./models/best-model-dat.pt
```

Each script will display progress as it processes files and report the total number of entities tagged upon completion.



## Input and Output Format

**Input:** PageXML files exported from Transkribus containing transcribed text.

**Output:** PageXML files with entity annotations embedded in TextLine custom attributes. The format follows Transkribus conventions:

```xml
<TextLine custom="readingOrder {index:0;} persoon {offset:10;length:15;} geonames_locations {offset:30;length:8;}">
```

Tagged files can be re-imported into Transkribus for further annotation, analysis, or export.

## Technical Notes

### Dependency Conflicts

The separate virtual environments exist because different Republic NER models were trained with incompatible embedding configurations. The ORG model requires gensim for word embeddings, whilst the DAT model fails when gensim (or its associated dependencies) are present in the environment. Isolated environments ensure all models function correctly without mutual interference.

### Performance Considerations

- Processing speed: approximately 10-30 seconds per file, depending on text density and line count
- GPU acceleration is not required; models run efficiently on CPU
- First execution in each environment downloads embeddings (one-time operation)
- Memory usage is modest; 8GB RAM is sufficient for typical document batches

## Repository Structure

```
.
├── tag_entities_direct.py          # Direct tagger for all entity types
├── run_per_tagger.bat              # Launcher for PER tagging
├── run_loc_tagger.bat              # Launcher for LOC tagging
├── run_org_tagger.bat              # Launcher for ORG tagging
├── run_dat_tagger.bat              # Launcher for DAT tagging
├── venv_per\                       # Virtual environment for PER
├── venv_loc\                       # Virtual environment for LOC
├── venv_org\                       # Virtual environment for ORG
├── venv_dat\                       # Virtual environment for DAT
└── models\                         # Downloaded .pt model files (not in repository)
├── pagexml\                        # Your PageXML documents (not in repository)

```

## Citation

If you use these scripts for academic work, please cite both this repository as well as the Republic project (Huygens Institute, Amsterdam) from which the NER models originate.

## Acknowledgements

- Republic NER models trained by Marijn Koolen (KNAW Humanities Cluster) and can be found on https://huggingface.co/marijnkoolen 
- Built on the Flair NLP framework
- Developed for the analysis of early modern Dutch *provincial* resolutions of the province of Overijssel.

## Licence

MIT License

## Contact

For questions or issues regarding this repository:
- c.a.romein@utwente.nl
- info@caromein.nl