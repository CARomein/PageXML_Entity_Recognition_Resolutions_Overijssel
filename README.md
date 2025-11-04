# Named Entity Recognition for Historical Dutch Resolutions

Automated entity tagging pipeline for early modern Dutch PageXML documents using Republic project NER models trained on 17th-18th century Dutch States General resolutions.

## Features

- **Pre-trained models**: Uses Republic NER models specifically trained on historical Dutch administrative texts
- **Multiple entity types**: Supports persons (PER) and dates (DAT) with extensible architecture
- **Transkribus integration**: Direct import/export workflow with Transkribus PageXML format
- **Collection-based processing**: Automatically discovers and processes entire Transkribus export collections
- **Interactive selection**: Choose specific collections to process through an interactive interface
- **Batch processing**: Process multiple collections efficiently
- **Isolated environments**: Handles dependency conflicts through separate virtual environments
- **Preserves structure**: Maintains existing annotations, reading order, and XML structure

## Overview

This repository contains scripts for tagging named entities in PageXML documents exported from Transkribus. The script is designed to work with Transkribus export structures (numbered folders containing `page/` subdirectories with XML files). Tagged documents can be re-imported into Transkribus with entity annotations preserved in custom attributes, enabling further annotation, searching, and analysis of historical entities.

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
pip install -r requirements.txt
deactivate

venv_dat\Scripts\activate
pip install -r requirements.txt
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
├── tag_entities.py               # Main tagging script
├── run_per.bat                   # Launcher for PER tagging
├── run_dat.bat                   # Launcher for DAT tagging
├── requirements.txt              # Python dependencies
├── venv_per\                     # Virtual environment for PER
├── venv_dat\                     # Virtual environment for DAT
├── models\                       # Downloaded model files
│   ├── best-model_per.pt
│   └── best-model_dat.pt
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore patterns
```

## Usage

### Expected Directory Structure

The script expects PageXML documents in a Transkribus export structure:

```
base_directory\
├── 12345\                        # Collection number
│   └── page\
│       ├── 001.xml
│       ├── 002.xml
│       └── ...
├── 12346\                        # Another collection
│   └── page\
│       ├── 001.xml
│       └── ...
└── ...
```

The script will automatically discover all numbered folders containing `page/` subdirectories with XML files.

### Basic Workflow

1. Export collections from Transkribus to a base directory
2. Run the appropriate entity tagging script
3. Select collections to process through the interactive interface
4. Review tagged output
5. Import collections back into Transkribus

### Tagging Persons (PER)

Double-click `run_per.bat` or run it from the command line. The script will prompt for the base directory:

```batch
run_per.bat
```

Example interaction:
```
========================================
  Person Tagger (PER)
========================================

Enter directory to process: C:\transkribus_exports\resolutions

Activating environment...

======================================================================
Entity Recognition Tagger
======================================================================
Base directory: C:\transkribus_exports\resolutions
Entity type: PER
Model: ./models/best-model_per.pt
======================================================================

======================================================================
Available Collections:
======================================================================
  1. 12345           ( 142 XML files)
  2. 12346           (  89 XML files)
  3. 12347           ( 201 XML files)
======================================================================

Options:
  - Type 'all' to process all collections
  - Type 'include' to select specific collections
  - Type 'exclude' to exclude specific collections

Your choice: include

Enter numbers to INCLUDE (space-separated, e.g. 1 3 5):
Numbers: 1 3

You selected 2 collection(s):
  - 12345 (142 files)
  - 12347 (201 files)

Confirm? (yes/no): yes

======================================================================
Loading PER model...
======================================================================
Model loaded: PER
Tag name: persoon

======================================================================
Processing: 12345 (142 files)
======================================================================
  ✓ 001.xml                                              12 tags
  ✓ 002.xml                                               8 tags
  ...

Collection 12345: 142 files processed

======================================================================
Processing: 12347 (201 files)
======================================================================
  ✓ 001.xml                                              15 tags
  ...

======================================================================
SUMMARY
======================================================================
Total files processed: 343
Total PER tags added: 2847
======================================================================

Done!
```

### Tagging Dates (DAT)

Double-click `run_dat.bat` or run it from the command line:

```batch
run_dat.bat
```

The interaction pattern is identical to the PER tagger, but processes date entities instead.

### Processing Multiple Entity Types

To tag multiple entity types, run each script sequentially. Each script preserves existing tags, so running multiple scripts adds cumulative annotations:

```batch
run_per.bat
run_dat.bat
```

### Interactive Selection Options

The script provides three selection modes:

1. **All collections**: Processes every collection found in the base directory
2. **Include specific collections**: Select collections by number (space-separated)
3. **Exclude specific collections**: Process all except specified collections

This flexibility allows for efficient batch processing of large archives or selective processing of specific collections.

### Progress Monitoring

The script displays detailed progress information:
- Collection being processed
- Files processed with tag counts
- Summary statistics per collection
- Total files and tags across all collections

Files without any detected entities are not displayed, keeping the output focused on actual results.

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
<TextLine id="line_1" custom="datum {offset:10;length:17;} persoon {offset:37;length:8;}">
  <Coords points="100,200 500,200 500,250 100,250"/>
  <TextEquiv>
    <Unicode>Op heden den 15 january 1650 compareerde Jan Smit</Unicode>
  </TextEquiv>
</TextLine>
```

The format follows Transkribus conventions for custom attributes:
- `offset`: Character position where entity begins (0-indexed)
- `length`: Number of characters in the entity

Multiple entities on the same line are separated by spaces in the custom attribute.

Tagged files are modified in place and can be directly re-imported into Transkribus for further annotation, analysis, or export.

## Transkribus Integration

### Configuring Entity Types in Transkribus

**Important:** Before importing tagged PageXML files, ensure the entity type names are configured in your Transkribus collection:

1. Open your collection in Transkribus
2. Navigate to Collection → Tags
3. Add custom tags matching your entity types:
   - `persoon` (for PER entities)
   - `datum` (for DAT entities)
4. Assign colours for visualisation
5. Save configuration

Without this configuration, tagged entities will not be visible in the Transkribus interface.

### Workflow: Export → Tag → Import

1. **Export from Transkribus:**
   - Select collections to export
   - Choose PageXML format
   - Export maintains numbered folder structure

2. **Tag with this tool:**
   - Run appropriate launcher scripts
   - Select collections to process
   - Verify output in console

3. **Import back to Transkribus:**
   - Import entire collection folders
   - Verify entity tags appear correctly
   - Continue annotation or analysis

### Cumulative Tagging

The scripts preserve existing custom attributes, allowing cumulative tagging:
- Tag persons first with `run_per.bat`
- Then tag dates with `run_dat.bat`
- Both entity types appear in the final PageXML

This approach enables flexible workflows and iterative refinement.

## Troubleshooting

### Directory not found

**Problem:** "ERROR: Directory not found"

**Solutions:**
- Verify the directory path is correct
- Use absolute paths if relative paths do not work
- Ensure the directory contains numbered folders with `page/` subdirectories
- Check for trailing backslashes (automatically handled by the scripts)

### No collections found

**Problem:** "No collections found! Expected structure: base_dir/number/page/*.xml"

**Solutions:**
- Verify the directory structure matches Transkribus export format
- Ensure numbered folders contain `page/` subdirectories
- Check that `page/` folders contain `.xml` files
- Verify folder names are numbers (not text labels)

### Model not found error

**Problem:** "Error: Model file not found: ./models/best-model_per.pt"

**Solutions:**
- Verify the `.pt` file exists in the `models/` directory
- Check the filename exactly matches (case-sensitive)
- Ensure the file downloaded completely (should be several hundred MB)
- Create the `models/` directory if it does not exist

### Import error: No module named 'flair'

**Problem:** Flair not installed in the virtual environment

**Solutions:**
- Ensure you ran `pip install -r requirements.txt` in the correct environment
- Verify you created both virtual environments
- Reinstall: `pip install flair`
- Check Python version compatibility (3.8-3.11)

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
- Process collections in batches if necessary

### No entities found

**Problem:** Script completes but reports 0 files processed

**Solutions:**
- Verify the model file is correct for the entity type
- Check that TextLine elements contain text (Unicode elements)
- Ensure text is in Dutch (models trained on Dutch)
- Try a different collection to verify the model works
- Check that the text is historical Dutch (modern Dutch may have lower recall)
- Verify XML files are well-formed

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
  - Number of entities per file

### Typical Processing Times

- Small collection (100 pages): ~15-30 minutes
- Medium collection (500 pages): ~1-2 hours
- Large collection (1000 pages): ~2-5 hours

These estimates assume subsequent runs (embeddings already downloaded).

### System Requirements

- **RAM**: 8GB recommended (4GB minimum)
- **Storage**: ~2GB for models and embeddings
- **CPU**: Standard processor sufficient (GPU not required)
- **OS**: Windows (scripts use `.bat` format)

### Optimisation Tips

- Process collections in batches rather than all at once
- Close unnecessary applications to free RAM
- Use SSD storage for faster file I/O
- After initial embedding download, processing is much faster
- Select specific collections to process rather than entire archives

## Limitations

- **Language**: Models trained specifically on historical Dutch; performance on other languages or modern Dutch may vary
- **Time period**: Optimised for 17th-18th century texts; earlier or later periods may have reduced accuracy
- **Text type**: Best suited for administrative/legal documents similar to States General resolutions
- **Entity types**: Currently limited to PER and DAT; other types require additional models
- **ATR quality**: Poor transcription quality affects entity recognition accuracy
- **Windows-specific**: Launcher scripts use Windows batch format (Unix adaptation required)
- **Python version**: Limited to Python 3.8-3.11 due to dependency requirements
- **No GPU support**: Models run on CPU only (sufficient for typical use cases)
- **In-place modification**: Original PageXML files are modified directly (backup recommended)

## Best Practices

1. **Backup originals**: Keep untagged PageXML copies before processing (files are modified in place)
2. **Test on sample first**: Process a small collection before running on entire archive
3. **Verify quality**: Manually review a representative sample of tagged entities
4. **Sequential processing**: Run entity types one at a time, not simultaneously
5. **Monitor output**: Check console output for errors or unexpected results
6. **Configure Transkribus first**: Set up entity tags in collection before importing
7. **Document decisions**: Keep notes on false positives/negatives for future reference
8. **Update models**: Check for updated Republic models periodically
9. **Batch processing**: Use the interactive selection to process related collections together

## Technical Details

### Dependency Conflicts

The separate virtual environments exist because different Republic NER models were trained with incompatible embedding configurations. Isolated environments ensure all models function correctly without mutual interference.

Specific conflicts:
- Different Flair versions required
- Incompatible embedding types
- Conflicting PyTorch dependencies

### Collection Discovery

The script automatically discovers collections by:
1. Scanning the base directory for subdirectories
2. Checking each subdirectory for a `page/` folder
3. Verifying the `page/` folder contains XML files
4. Presenting all valid collections for selection

This approach handles various Transkribus export configurations and allows for flexible archive organisation.

### File Processing

The script:
- Processes XML files sequentially within each collection
- Preserves all existing XML structure and attributes
- Adds custom attributes to TextLine elements
- Maintains namespace declarations
- Handles multiple entities per line
- Skips files with no detected entities (for cleaner output)

### Custom Attribute Format

Transkribus custom attributes follow strict formatting:
```
key {param1:value1;param2:value2;}
```

No spaces around colons or semicolons. Multiple attributes separated by spaces:
```
readingOrder {index:0;} persoon {offset:10;length:8;} datum {offset:0;length:9;}
```

The script preserves existing custom attributes and appends new entity tags.

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
- Parallel processing for faster throughput
- GUI interface
- Integration with Transkribus API
- Support for Python 3.12+
- Dry-run mode (preview without modification)
- Detailed entity reports (CSV export)

## Contributing

Contributions are welcome. Areas for improvement:
- Additional entity type models
- Cross-platform launcher scripts
- Performance optimisation
- Documentation improvements
- Test suite development
- Error handling enhancements

## Citation

If you use these scripts or models for academic work, please cite:

**This repository:**
```
Entity Recognition Resolutions Overijssel (2025)
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

- **v2.0.0** (2025-01): Major architectural revision
  - Collection-based processing with automatic discovery
  - Interactive collection selection (all/include/exclude)
  - Simplified command-line interface (no model path required)
  - In-place modification of PageXML files
  - Improved progress reporting
  - Cleaner output (skips files without entities)

- **v1.0.0** (2025-01): Initial release
  - PER and DAT entity recognition
  - Transkribus integration
  - Batch processing support
