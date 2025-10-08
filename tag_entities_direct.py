"""
Direct Entity Tagger for PageXML using Republic NER models
Tags entities directly in PageXML files with Transkribus-compatible format
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

def tag_pagexml_files(pagexml_dir, model_path, entity_type):
    """Tags all PageXML files in directory with specified entity type."""
    
    print(f"Loading {entity_type} model...")
    tagger = SequenceTagger.load(model_path)
    print("Model loaded.\n")
    
    xml_files = sorted(glob.glob(os.path.join(pagexml_dir, '*.xml')))
    print(f"Processing {len(xml_files)} files...\n")
    
    tag_name = TRANSKRIBUS_TAGS.get(entity_type, entity_type.lower())
    total_tags = 0
    
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
            print(f"✓ {os.path.basename(xml_file)}: {file_tags} tags")
    
    print(f"\nDone! Total {entity_type} tags added: {total_tags}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python tag_entities_direct.py <pagexml_dir> <model_path> <entity_type>")
        print("\nExample:")
        print("  python tag_entities_direct.py ./pagexml ./models/best-model-per.pt PER")
        print("\nEntity types: PER, LOC, ORG, HOE, COM, DAT, RES")
        sys.exit(1)
    
    pagexml_dir = sys.argv[1]
    model_path = sys.argv[2]
    entity_type = sys.argv[3].upper()
    
    if entity_type not in TRANSKRIBUS_TAGS:
        print(f"Error: Invalid entity type: {entity_type}")
        print(f"Valid types: {list(TRANSKRIBUS_TAGS.keys())}")
        sys.exit(1)
    
    if not os.path.isdir(pagexml_dir):
        print(f"Error: Directory not found: {pagexml_dir}")
        sys.exit(1)
    
    if not os.path.isfile(model_path):
        print(f"Error: Model file not found: {model_path}")
        sys.exit(1)
    
    tag_pagexml_files(pagexml_dir, model_path, entity_type)