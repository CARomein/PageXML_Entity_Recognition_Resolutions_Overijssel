# Named Entity Recognition for Historical Dutch Resolutions

Automated entity tagging pipeline for early modern Dutch PageXML documents using Republic project NER models trained on 17th-18th century Dutch States General resolutions.

## Features

- **Pre-trained models**: Uses Republic NER models specifically trained on historical Dutch administrative texts
- **Multiple entity types**: Supports persons (PER) and dates (DAT) with extensible architecture
- **Transkribus integration**: Direct import/export workflow with Transkribus PageXML format
- **Batch processing**: Process entire collections efficiently
- **Isolated environments**: Handles dependency conflicts through separate virtual environments
- **Confidence tracking**: Reports entity recognition confidence levels
- **Preserves structure**: Maintains existing annotations and reading order

## Overview

This repository contains scripts for tagging named entities in PageXML documents exported from Transkribus. The tagged documents can be re-imported into Transkribus with entity annotations preserved in custom attributes, enabling further annotation, searching, and analysis of historical entities.

### Supported Entity Types

- **PER** (persoon) - Persons: names of individuals, titles, and roles
- **DAT** (datum) - Dates: temporal expressions in various historical formats

The modular architecture allows for future expansion to additional entity types such as organisations (ORG) and geographical locations (LOC).

## Prerequisites

- Windows operating system (scripts use `.bat` launchers; for Unix systems, adaptation is required)
- Python 3.8-3.11 (Python 3.12+ is not compatible with the Republic models' installation requirements)
- Sufficient disk space (~2GB for models and embeddings)
- Internet connection for initial setup (downloading models and embeddings)

## Installation and Setup

### 1. Clone or Download Repository

Clone this repository or download as ZIP and extract to your local machine:

```bash
git clone https://github.com/CARomein/Entity_Recognition_Resolutions.git
cd Entity_Recognition_Resolutions
```

### 2. Create Virtual Environments

The different NER models have incompatible dependencies. The DAT model requires specific Flair configurations that conflict with other models' requirements. To resolve this, each entity type uses an isolated virtual environment.

Open Command Prompt in the project directory and execute the following commands:

```batch
python -m venv venv_per
python -m venv venv_dat
```

**Why separate environments?**
- The Republic NER models were trained with different embedding configurations
- Dependency conflicts prevent simultaneous installation in a single environment
- Isolated environments ensure all models function correctly without mutual interference

### 3. Install Dependencies

Install the required libraries in each environment. Execute these commands one at a time:

```batch
venv_per\Scripts\activate
pip install flair
deactivate

venv_dat\Scripts\activate
pip install flair
deactivate
```

**Note:** The first run will download Flair embeddings (approximately 500MB), which may take several minutes depending on your connection speed. This is a one-time operation.

### 4. Download NER Models

Download the required `.pt` model files from [marijnkoolen's Hugging Face profile](https://huggingface.co/marijnkoolen) and place them in the `models/` directory within this repository:

**Required models:**
- [`best-model_per.pt`](https://huggingface.co/marijnkoolen/flair-hipe2022-ner-dutch-per-ritter/tree/main) - Persons model
- [`best-model_dat.pt`](https://huggingface.co/marijnkoolen/flair-hipe2022-ner-dutch-dat-ritter/tree/main) - Dates model

Create the `models/` directory if it does not exist:

```batch
mkdir models
```

Then place the downloaded `.pt` files in this directory.

### 5. Verify Installation

After completing these steps, your directory structure should resemble:

```
Entity_Recognition_Resolutions\
├── tag_entities_direct.py       # Main tagging script
├── run_per_tagger.bat            # Launcher for PER tagging
├── run_dat_tagger.bat            # Launcher for DAT tagging
├── venv_per\                     # Virtual environment for PER
├── venv_dat\                     # Virtual environment for DAT
├── models\                       # Downloaded model files
│   ├── best-model_per.pt
│   └── best-model_dat.pt
├── pagexml\                      # Your PageXML documents
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore patterns
```

## Usage

### Basic Workflow

Each entity type has a dedicated launcher script to ensure compatibility. The general workflow is:

1. Export PageXML from Transkribus
2. Run entity tagging script(s)
3. Review tagged output
4. Import back into Transkribus

### Tagging Persons (PER)

```batch
run_per_tagger.bat ./pagexml ./models/best-model_per.pt
```

This processes all PageXML files in the `./pagexml` directory and adds person entity tags.

### Tagging Dates (DAT)

```batch
run_dat_tagger.bat ./pagexml ./models/best-model_dat.pt
```

This processes all PageXML files in the `./pagexml` directory and adds date entity tags.

### Processing Multiple Entity Types

To tag multiple entity types, run each script sequentially:

```batch
run_per_tagger.bat ./pagexml ./models/best-model_per.pt
run_dat_tagger.bat ./pagexml ./models/best-model_dat.pt
```

Each script preserves existing tags, so running multiple scripts adds cumulative annotations.

### Command-Line Arguments

```
run_[entity]_tagger.bat [pagexml_directory] [model_path]
```

**Arguments:**
- `pagexml_directory`: Path to folder containing PageXML files (processes recursively)
- `model_path`: Path to the `.pt` model file for the entity type

### Progress Monitoring

Each script displays progress information:
- File currently being processed
- Number of entities found per file
- Total entities tagged
- Processing time per file

Example output:
```
Processing: pagexml/0018/page/0001.xml
Found 12 PER entities
Processing: pagexml/0018/page/0002.xml
Found 8 PER entities
...
Total: 156 PER entities tagged across 42 files
```

## Input and Output Format

### Input Format

PageXML files exported from Transkribus containing transcribed text. The script processes TextLine elements:

```xml
<TextLine id="line_1">
  <Coords points="100,200 500,200 500,250 100,250"/>
  <TextEquiv>
    <Unicode>Op heden den 15 january 1650 compareerde Jan Smit</Unicode>
  </TextEquiv>
</TextLine>
```

### Output Format

PageXML files with entity annotations embedded in TextLine custom attributes:

```xml
<TextLine id="line_1" custom="persoon {offset:37;length:8;continued:false;}">
  <Coords points="100,200 500,200 500,250 100,250"/>
  <TextEquiv>
    <Unicode>Op heden den 15 january 1650 compareerde Jan Smit</Unicode>
  </TextEquiv>
</TextLine>
```

The format follows Transkribus conventions for custom attributes:
- `offset`: Character position where entity begins (0-indexed)
- `length`: Number of characters in the entity
- `continued`: Whether the entity continues on the next line

Tagged files can be directly re-imported into Transkribus for further annotation, analysis, or export.

## Transkribus Integration

### Configuring Entity Types in Transkribus

**Important:** Before importing tagged PageXML files, ensure the entity type names are configured in your Transkribus collection:

1. Open your collection in Transkribus
2. Navigate to Collection → Tags
3. Add custom tags matching your entity types:
   - `persoon` (for PER entities)
   - `datum` (for DAT entities)
4. Assign colours for visualisation

### Workflow with Transkribus

1. **Export from Transkribus:**
   - Select your collection or documents
   - Export as PageXML
   - Save to `pagexml/` directory

2. **Run NER tagging:**
   ```batch
   run_per_tagger.bat ./pagexml ./models/best-model_per.pt
   run_dat_tagger.bat ./pagexml ./models/best-model_dat.pt
   ```

3. **Review output:**
   - Check console output for statistics
   - Examine sample files to verify tagging quality

4. **Configure Transkribus:**
   - Ensure `persoon` and `datum` tags exist in collection settings
   - Assign appropriate colours

5. **Import to Transkribus:**
   - Import the tagged PageXML files
   - Verify entities display correctly in the interface
   - Tags should appear highlighted according to your colour scheme

6. **Quality control:**
   - Manually review a sample of tagged entities
   - Correct false positives/negatives as needed
   - Use Transkribus search to find all instances of specific entity types

## How It Works

### NER Pipeline

1. **Text extraction**: Reads Unicode text from PageXML TextLine elements
2. **Entity recognition**: Applies Flair NER model to identify entities
3. **Offset calculation**: Determines character positions for each entity
4. **Attribute insertion**: Adds entity information to custom attributes
5. **XML preservation**: Maintains all existing structure and metadata

### Model Architecture

The Republic NER models use:
- **Flair framework**: Contextual string embeddings
- **Training data**: 17th-18th century Dutch States General resolutions
- **Architecture**: BiLSTM-CRF sequence labelling
- **Embeddings**: Historical Dutch language models

### Entity Boundary Detection

The models identify entity boundaries using:
- Contextual information from surrounding text
- Historical naming conventions
- Document structure patterns
- Linguistic features specific to early modern Dutch

## Troubleshooting

### Model not found error

**Problem:** "FileNotFoundError: [Errno 2] No such file or directory: './models/best-model_per.pt'"

**Solutions:**
- Verify the `.pt` file exists in the `models/` directory
- Check the filename exactly matches (case-sensitive)
- Ensure the file downloaded completely (should be several hundred MB)
- Provide the full path if relative path does not work

### Import error: No module named 'flair'

**Problem:** Flair not installed in the virtual environment

**Solutions:**
- Ensure you activated the correct virtual environment
- Reinstall Flair: `pip install flair`
- Verify you are using Python 3.8-3.11 (not 3.12+)

### Python version incompatibility

**Problem:** "This version of Flair requires Python 3.8-3.11"

**Solutions:**
- Check your Python version: `python --version`
- Install Python 3.11 if necessary
- Create virtual environments with correct Python version
- Use `py -3.11 -m venv venv_per` to specify version

### Slow processing speed

**Problem:** Script takes very long to process files

**Solutions:**
- First run downloads embeddings (~500MB) - this is normal and one-time only
- Subsequent runs should be faster (10-30 seconds per file)
- Large files with many TextLines naturally take longer
- Close other applications to free up RAM

### No entities found

**Problem:** Script completes but reports 0 entities tagged

**Solutions:**
- Verify the model file is correct for the entity type
- Check that TextLine elements contain text (Unicode elements)
- Ensure text is in Dutch (models trained on Dutch)
- Try a different document to verify the model works
- Check that the text is historical Dutch (modern Dutch may have lower recall)

### Encoding errors

**Problem:** UnicodeDecodeError or similar encoding issues

**Solutions:**
- Ensure PageXML files are UTF-8 encoded
- Re-export from Transkribus if necessary
- Check for corrupted XML files
- Verify namespace declarations are correct

### Custom attributes not visible in Transkribus

**Problem:** Imported files do not show entity tags in Transkribus interface

**Solutions:**
- Configure entity types in Collection → Tags with exact names (`persoon`, `datum`)
- Re-import the documents after configuring tags
- Verify the custom attribute format matches Transkribus conventions
- Check that the XML structure was preserved correctly

## Performance

### Processing Speed

- **Typical speed**: 10-30 seconds per PageXML file
- **Factors affecting speed:**
  - Number of TextLines per file
  - Text density (characters per line)
  - First run (downloads embeddings)
  - System specifications

### Typical Processing Times

- Single document (10 pages): ~2-5 minutes
- Small collection (100 pages): ~15-30 minutes
- Large collection (1000 pages): ~2-5 hours

### System Requirements

- **RAM**: 8GB recommended (4GB minimum)
- **Storage**: ~2GB for models and embeddings
- **CPU**: Standard processor sufficient (GPU not required)
- **OS**: Windows (scripts use `.bat` format)

### Optimisation Tips

- Process documents in batches of 100-200 files
- Close unnecessary applications to free RAM
- Use SSD storage for faster file I/O
- After initial embedding download, processing is much faster

## Limitations

- **Language**: Models trained specifically on historical Dutch; performance on other languages or modern Dutch may vary
- **Time period**: Optimised for 17th-18th century texts; earlier or later periods may have reduced accuracy
- **Text type**: Best suited for administrative/legal documents similar to States General resolutions
- **Entity types**: Currently limited to PER and DAT; other types require additional models
- **ATR quality**: Poor transcription quality affects entity recognition accuracy
- **Windows-specific**: Launcher scripts use Windows batch format (Unix adaptation required)
- **Python version**: Limited to Python 3.8-3.11 due to dependency requirements
- **No GPU support**: Models run on CPU only (sufficient for typical use cases)

## Best Practices

1. **Test on sample first**: Process a small subset before running on entire collection
2. **Verify quality**: Manually review a representative sample of tagged entities
3. **Backup originals**: Keep untagged PageXML copies before processing
4. **Sequential processing**: Run entity types one at a time, not simultaneously
5. **Monitor output**: Check console output for errors or unexpected results
6. **Configure Transkribus first**: Set up entity tags in collection before importing
7. **Document decisions**: Keep notes on false positives/negatives for future reference
8. **Update models**: Check for updated Republic models periodically

## Technical Details

### Dependency Conflicts

The separate virtual environments exist because different Republic NER models were trained with incompatible embedding configurations. Isolated environments ensure all models function correctly without mutual interference.

Specific conflicts:
- Different Flair versions required
- Incompatible embedding types
- Conflicting PyTorch dependencies

### File Processing

The script:
- Recursively searches for `.xml` files in the specified directory
- Preserves folder structure in output
- Maintains XML formatting and namespace declarations
- Handles Transkribus export structure (`[archief]/page/*.xml`)

### Custom Attribute Format

Transkribus custom attributes follow strict formatting:
```
key {param1:value1;param2:value2;}
```

No spaces around colons or semicolons. Multiple attributes separated by spaces:
```
readingOrder {index:0;} persoon {offset:10;length:8;}
```

## Related Tools

This tool is part of a suite for working with PageXML annotations:

- **Tag Transfer Tool**: Transfer entity tags between old and new PageXML versions
  - Repository: [Transfer_Tags_To_New_PageXML](https://github.com/CARomein/Transfer_Tags_To_New_PageXML)
- **Label Normalisation Tool**: Normalise structural region labels across collections
  - Repository: [PageXML_regionname_normalisation](https://github.com/CARomein/PageXML_regionname_normalisation)

## Future Enhancements

Potential improvements:
- Additional entity types (ORG, LOC)
- Unix/Linux launcher scripts
- Confidence threshold configuration
- GUI interface
- Integration with Transkribus API
- Support for Python 3.12+

## Contributing

Contributions are welcome. Areas for improvement:
- Additional entity type models
- Cross-platform launcher scripts
- Performance optimisation
- Documentation improvements
- Test suite development

## Citation

If you use these scripts or models for academic work, please cite:

**This repository:**
```
Entity Recoginition Resolutions Overijssel (2025)
Developed as part of the HAICu Project
https://github.com/CARomein/Entity_Recognition_Resolutions
```

**Republic NER models:**
```
Koolen, M., van Veen, T., & Brouwer, M. (2022)
Republic NER Models for Historical Dutch
Huygens Institute, KNAW Humanities Cluster
https://huggingface.co/marijnkoolen
```

## License

MIT License - See LICENSE file for details.

## Acknowledgements

This tool was developed within the context of the [HAICu project](https://haicu.science) on the Resoluties van de Staten van Overijssel (Resolutions of the States of Overijssel), funded by the Dutch Research Council/Nederlandse Organisatie voor Wetenschappelijk Onderzoek/Nationale Wetenschapsagenda [NWA.1518.22.105].

Development was assisted by Claude (Anthropic) for code implementation and documentation.

**Special thanks to:**
- Marijn Koolen (KNAW Humanities Cluster) for developing and sharing the Republic NER models
- The Republic project (Huygens Institute, Amsterdam) for pioneering NER on historical Dutch texts
- The Flair NLP framework team for the underlying technology

## Version History

- **v1.0.0** (2025-01): Initial release
  - PER and DAT entity recognition
  - Transkribus integration
  - Batch processing support