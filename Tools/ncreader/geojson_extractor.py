import os
import zipfile
from pathlib import Path

def extract_all_zip_files():
    """Extract all zip files to one folder"""
    
    # Define paths
    output_folder = Path('Extracted_Files')
    
    # Create output directory
    output_folder.mkdir(exist_ok=True)
    
    # Get all zip files in the GeoJson folder
    zip_files = list(Path('GeoJson').glob('*.zip'))
    
    if not zip_files:
        print("No zip files found in the 'GeoJson' folder!")
        return
    
    print(f"Found {len(zip_files)} zip files to extract...")
    
    for zip_file in zip_files:
        print(f"Processing {zip_file.name}")
        
        try:
            # Extract the zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Extract all contents to the output folder
                zip_ref.extractall(output_folder)
                
            print(f"  ✓ Successfully extracted {zip_file.name}")
            
        except zipfile.BadZipFile:
            print(f"  ✗ Error: '{zip_file}' is not a valid zip file")
        except Exception as e:
            print(f"  ✗ Error extracting {zip_file}: {str(e)}")
    
    print(f"\nExtraction complete! All files extracted to '{output_folder}' folder.")
    
    # Count extracted files
    extracted_files = list(output_folder.rglob('*'))
    file_count = len([f for f in extracted_files if f.is_file()])
    print(f"Total files extracted: {file_count}")

def main():
    """Main function to run the extraction process"""
    print("GeoJSON File Extractor")
    print("=" * 30)
    
    extract_all_zip_files()

if __name__ == "__main__":
    main() 