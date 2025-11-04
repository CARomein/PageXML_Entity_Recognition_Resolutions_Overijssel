"""
Entity Tagger for PageXML files
Tags dates (DAT) and persons (PER) in PageXML files
"""
import os
import glob
import re
import sys
import xml.etree.ElementTree as ET
from flair.data import Sentence
from flair.models import SequenceTagger

# Tag names for Transkribus
TAG_NAMES = {
    'PER': 'persoon',
    'DAT': 'datum'
}

def find_collections(base_dir):
    """Find all numbered folders that contain page/ subdirectories with XML files."""
    collections = {}
    
    if not os.path.isdir(base_dir):
        print(f"Error: Directory not found: {base_dir}")
        return collections
    
    # Look for numbered folders
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        
        # Check if it's a directory
        if not os.path.isdir(item_path):
            continue
        
        # Check if it has a page/ subdirectory
        page_dir = os.path.join(item_path, 'page')
        if not os.path.isdir(page_dir):
            continue
        
        # Check if page/ has XML files
        xml_files = glob.glob(os.path.join(page_dir, '*.xml'))
        if xml_files:
            collections[item] = item_path
    
    return collections

def display_and_select_collections(collections):
    """Display collections and let user select which to process."""
    if not collections:
        print("\nNo collections found!")
        print("Expected structure: base_dir/number/page/*.xml")
        return []
    
    collection_list = sorted(collections.keys())
    
    print("\n" + "="*70)
    print("Available Collections:")
    print("="*70)
    
    for i, coll_name in enumerate(collection_list, 1):
        page_dir = os.path.join(collections[coll_name], 'page')
        xml_count = len(glob.glob(os.path.join(page_dir, '*.xml')))
        print(f"{i:3d}. {coll_name:15s} ({xml_count:4d} XML files)")
    
    print("="*70)
    print("\nOptions:")
    print("  - Type 'all' to process all collections")
    print("  - Type 'include' to select specific collections")
    print("  - Type 'exclude' to exclude specific collections")
    
    while True:
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'all':
            print(f"\nSelected: All {len(collection_list)} collections")
            return collection_list
        
        elif choice == 'include':
            print("\nEnter numbers to INCLUDE (space-separated, e.g. 1 3 5):")
            nums = input("Numbers: ").strip()
            
            try:
                indices = [int(x) - 1 for x in nums.split()]
                selected = [collection_list[i] for i in indices if 0 <= i < len(collection_list)]
                
                if not selected:
                    print("No valid selections. Try again.")
                    continue
                
                print(f"\nYou selected {len(selected)} collection(s):")
                for name in selected:
                    page_dir = os.path.join(collections[name], 'page')
                    xml_count = len(glob.glob(os.path.join(page_dir, '*.xml')))
                    print(f"  - {name} ({xml_count} files)")
                
                confirm = input("\nConfirm? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    return selected
                
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid numbers.")
        
        elif choice == 'exclude':
            print("\nEnter numbers to EXCLUDE (space-separated, e.g. 2 4):")
            nums = input("Numbers: ").strip()
            
            try:
                indices = [int(x) - 1 for x in nums.split()]
                excluded = {collection_list[i] for i in indices if 0 <= i < len(collection_list)}
                selected = [name for name in collection_list if name not in excluded]
                
                if not selected:
                    print("All collections excluded. Try again.")
                    continue
                
                print(f"\nYou selected {len(selected)} collection(s):")
                for name in selected:
                    page_dir = os.path.join(collections[name], 'page')
                    xml_count = len(glob.glob(os.path.join(page_dir, '*.xml')))
                    print(f"  - {name} ({xml_count} files)")
                
                confirm = input("\nConfirm? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    return selected
                
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid numbers.")
        
        else:
            print("Invalid option. Type 'all', 'include', or 'exclude'.")

def tag_files(collections, selected_names, model_path, entity_type):
    """Tag all XML files in selected collections."""
    
    print(f"\n{'='*70}")
    print(f"Loading {entity_type} model...")
    print(f"{'='*70}")
    
    tagger = SequenceTagger.load(model_path)
    tag_name = TAG_NAMES[entity_type]
    
    print(f"Model loaded: {entity_type}")
    print(f"Tag name: {tag_name}\n")
    
    total_files_processed = 0
    total_tags_added = 0
    
    for coll_name in selected_names:
        coll_path = collections[coll_name]
        page_dir = os.path.join(coll_path, 'page')
        xml_files = sorted(glob.glob(os.path.join(page_dir, '*.xml')))
        
        print(f"\n{'='*70}")
        print(f"Processing: {coll_name} ({len(xml_files)} files)")
        print(f"{'='*70}")
        
        files_with_tags = 0
        
        for xml_file in xml_files:
            # Parse XML
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Remove namespace for easier processing
            for elem in tree.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}', 1)[1]
                elem.attrib = {k.split('}', 1)[-1]: v for k, v in elem.attrib.items()}
            
            root = tree.getroot()
            text_lines = root.findall('.//TextLine')
            file_tag_count = 0
            
            # Process each text line
            for text_line in text_lines:
                unicode_elem = text_line.find('.//TextEquiv/Unicode')
                
                if unicode_elem is None or unicode_elem.text is None:
                    continue
                
                text = unicode_elem.text
                
                # Run NER model
                sentence = Sentence(text)
                tagger.predict(sentence)
                entities = sentence.get_spans('ner')
                
                if not entities:
                    continue
                
                # Get existing custom attribute
                custom_attr = text_line.attrib.get('custom', '')
                
                # Add tags for each entity
                for entity in entities:
                    offset = entity.start_position
                    length = len(entity.text)
                    tag = f"{tag_name} {{offset:{offset};length:{length};}}"
                    
                    if custom_attr:
                        custom_attr = f"{custom_attr} {tag}"
                    else:
                        custom_attr = tag
                    
                    file_tag_count += 1
                    total_tags_added += 1
                
                # Update the custom attribute if entities were found
                if entities:
                    text_line.set('custom', custom_attr)
            
            # Save modified XML
            if file_tag_count > 0:
                xml_bytes = ET.tostring(root, encoding='UTF-8', method='xml', xml_declaration=True)
                xml_str = xml_bytes.decode('UTF-8')
                
                # Fix XML declaration
                xml_str = re.sub(
                    r"(<\?xml version='1.0' encoding='UTF-8'\?>)",
                    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                    xml_str
                )
                
                # Add namespace if missing
                if 'xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"' not in xml_str:
                    xml_str = re.sub(
                        r'<PcGts',
                        '<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"',
                        xml_str
                    )
                
                # Write back to file
                with open(xml_file, 'w', encoding='UTF-8') as f:
                    f.write(xml_str)
                
                print(f"  ✓ {os.path.basename(xml_file):50s} {file_tag_count:4d} tags")
                files_with_tags += 1
                total_files_processed += 1
        
        print(f"\nCollection {coll_name}: {files_with_tags} files processed")
    
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Total files processed: {total_files_processed}")
    print(f"Total {entity_type} tags added: {total_tags_added}")
    print(f"{'='*70}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python tag_entities.py <base_directory> <entity_type>")
        print("\nExample: python tag_entities.py output_goetgevonden_decisions DAT")
        print("\nEntity types: PER (persons), DAT (dates)")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    entity_type = sys.argv[2].upper()
    
    # Validate entity type
    if entity_type not in ['PER', 'DAT']:
        print(f"Error: Invalid entity type '{entity_type}'")
        print("Valid types: PER, DAT")
        sys.exit(1)
    
    # Check model file
    model_path = f"./models/best-model_{entity_type.lower()}.pt"
    if not os.path.isfile(model_path):
        print(f"Error: Model file not found: {model_path}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"Entity Recognition Tagger")
    print(f"{'='*70}")
    print(f"Base directory: {base_dir}")
    print(f"Entity type: {entity_type}")
    print(f"Model: {model_path}")
    print(f"{'='*70}")
    
    # Find collections
    collections = find_collections(base_dir)
    
    if not collections:
        print("\nNo valid collections found!")
        sys.exit(1)
    
    # Let user select collections
    selected = display_and_select_collections(collections)
    
    if not selected:
        print("\nNo collections selected. Exiting.")
        sys.exit(0)
    
    # Process selected collections
    tag_files(collections, selected, model_path, entity_type)
    
    print("Done!")

if __name__ == "__main__":
    main()
