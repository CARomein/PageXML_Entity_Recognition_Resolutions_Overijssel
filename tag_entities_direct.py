"""
Direct Entity Tagger for PageXML using Republic NER models
Tags entities directly in PageXML files with Transkribus-compatible format
Interactive version with folder selection
"""
import os
import glob
import re
import sys
import xml.etree.ElementTree as ET
from flair.data import Sentence
from flair.models import SequenceTagger

# Mapping entity types to Transkribus tag names
TRANSKRIBUS_TAGS = {
    'PER': 'persoon',
    'LOC': 'geonames_locations',
    'ORG': 'organisatie',
    'HOE': 'capaciteit_hoedanigheid',
    'COM': 'commissie_committee',
    'DAT': 'datum',
    'RES': 'document'
}

# Model paths
MODEL_PATHS = {
    'PER': './models/best-model_per.pt',
    'LOC': './models/best-model_loc.pt',
    'ORG': './models/best-model_org.pt',
    'DAT': './models/best-model_dat.pt',
    'HOE': './models/best-model_hoe.pt',
    'COM': './models/best-model_com.pt',
    'RES': './models/best-model_res.pt'
}

def get_available_folders(base_dir='./pagexml'):
    """Get list of numbered folders in pagexml directory."""
    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' not found!")
        return []
    
    folders = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            # Check if folder contains a 'page' subdirectory
            page_dir = os.path.join(item_path, 'page')
            if os.path.isdir(page_dir):
                folders.append(item)
    
    return sorted(folders)

def select_folders():
    """Interactive folder selection."""
    folders = get_available_folders()
    
    if not folders:
        print("No valid folders found in pagexml/ directory.")
        print("Expected structure: pagexml/XXXX/page/*.xml")
        sys.exit(1)
    
    print("\nAvailable folders in pagexml/:")
    for folder in folders:
        print(f"  - {folder}")
    
    print("\nWhich folder(s) would you like to process?")
    print("Enter folder number(s) separated by spaces (e.g., 0001 0036)")
    print("Or type 'all' to process all folders")
    
    while True:
        choice = input("\nYour choice: ").strip()
        
        if choice.lower() == 'all':
            return folders
        
        selected = choice.split()
        invalid = [f for f in selected if f not in folders]
        
        if invalid:
            print(f"Invalid folder(s): {', '.join(invalid)}")
            print(f"Available folders: {', '.join(folders)}")
            continue
        
        if selected:
            return selected
        
        print("Please enter at least one folder number or 'all'")

def tag_pagexml_files(pagexml_dirs, model_path, entity_type):
    """Tags all PageXML files in specified directories with specified entity type."""
    
    print(f"\nLoading {entity_type} model...")
    tagger = SequenceTagger.load(model_path)
    print("Model loaded.\n")
    
    tag_name = TRANSKRIBUS_TAGS.get(entity_type, entity_type.lower())
    total_tags = 0
    total_files = 0
    
    for pagexml_dir in pagexml_dirs:
        full_path = os.path.join('./pagexml', pagexml_dir, 'page')
        
        if not os.path.isdir(full_path):
            print(f"Warning: {full_path} not found, skipping...")
            continue
        
        xml_files = sorted(glob.glob(os.path.join(full_path, '*.xml')))
        
        if not xml_files:
            print(f"No XML files found in {full_path}")
            continue
        
        print(f"\n--- Processing folder {pagexml_dir} ({len(xml_files)} files) ---")
        
        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Remove namespace for easier manipulation
            for elem in tree.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}', 1)[1]
                elem.attrib = {k.split('}', 1)[-1]: v for k, v in elem.attrib.items()}
            
            root = tree.getroot()
            text_lines = root.findall('.//TextLine')
            file_tags = 0
            
            for text_line in text_lines:
                unicode_elem = text_line.find('.//TextEquiv/Unicode')
                if unicode_elem is None or unicode_elem.text is None:
                    continue
                
                text = unicode_elem.text
                sentence = Sentence(text)
                tagger.predict(sentence)
                
                entities = sentence.get_spans('ner')
                if not entities:
                    continue
                
                custom_attr = text_line.attrib.get('custom', '')
                
                for entity in entities:
                    offset = entity.start_position
                    length = len(entity.text)
                    tag = f"{tag_name} {{offset:{offset};length:{length};}}"
                    
                    if custom_attr:
                        custom_attr = f"{custom_attr} {tag}"
                    else:
                        custom_attr = tag
                    
                    file_tags += 1
                    total_tags += 1
                
                if entities:
                    text_line.set('custom', custom_attr)
            
            # Write back with namespace
            xml_bytes = ET.tostring(root, encoding='UTF-8', method='xml', xml_declaration=True)
            xml_str = xml_bytes.decode('UTF-8')
            xml_str = re.sub(r"(<\?xml version='1.0' encoding='UTF-8'\?>)",
                             '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', xml_str)
            
            if 'xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"' not in xml_str:
                xml_str = re.sub(r'<PcGts', '<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"', xml_str)
            
            with open(xml_file, 'w', encoding='UTF-8') as f:
                f.write(xml_str)
            
            if file_tags > 0:
                print(f"  ✓ {os.path.basename(xml_file)}: {file_tags} tags")
                total_files += 1
    
    print(f"\n{'='*50}")
    print(f"Done! Processed {total_files} files")
    print(f"Total {entity_type} tags added: {total_tags}")
    print(f"{'='*50}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tag_entities_direct.py <entity_type>")
        print("\nEntity types: PER, LOC, ORG, HOE, COM, DAT, RES")
        sys.exit(1)
    
    entity_type = sys.argv[1].upper()
    
    if entity_type not in TRANSKRIBUS_TAGS:
        print(f"Error: Invalid entity type: {entity_type}")
        print(f"Valid types: {list(TRANSKRIBUS_TAGS.keys())}")
        sys.exit(1)
    
    model_path = MODEL_PATHS.get(entity_type)
    if not os.path.isfile(model_path):
        print(f"Error: Model file not found: {model_path}")
        sys.exit(1)
    
    # Interactive folder selection
    selected_folders = select_folders()
    
    print(f"\nSelected folders: {', '.join(selected_folders)}")
    
    # Process selected folders
    tag_pagexml_files(selected_folders, model_path, entity_type)