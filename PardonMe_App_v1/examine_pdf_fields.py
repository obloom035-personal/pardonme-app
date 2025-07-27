#!/usr/bin/env python3
"""
Script to examine the fillable fields in the official Wisconsin pardon application PDF
"""
import PyPDF2
import sys

def examine_pdf_fields(pdf_path):
    """Examine and list all fillable fields in a PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            print(f"PDF: {pdf_path}")
            print(f"Number of pages: {len(pdf_reader.pages)}")
            print("-" * 50)
            
            # Check if PDF has form fields
            if pdf_reader.get_form_text_fields():
                print("Found fillable form fields:")
                print("-" * 50)
                
                fields = pdf_reader.get_form_text_fields()
                field_list = list(fields.keys())
                field_list.sort()  # Sort alphabetically for easier review
                
                for i, field_name in enumerate(field_list, 1):
                    field_value = fields[field_name]
                    print(f"{i:3d}. {field_name}")
                    if field_value:
                        print(f"     Default: {field_value}")
                
                print("-" * 50)
                print(f"Total fields found: {len(fields)}")
                
                # Also save to a text file for easier reference
                with open('pdf_field_names.txt', 'w') as f:
                    f.write("Wisconsin Pardon Application PDF Field Names\n")
                    f.write("=" * 50 + "\n\n")
                    for i, field_name in enumerate(field_list, 1):
                        field_value = fields[field_name]
                        f.write(f"{i:3d}. {field_name}\n")
                        if field_value:
                            f.write(f"     Default: {field_value}\n")
                    f.write(f"\nTotal fields: {len(fields)}\n")
                print("Field names also saved to 'pdf_field_names.txt'")
            else:
                print("No fillable form fields found in this PDF")
                
                # Try alternative method to check for annotations
                print("Checking for annotations on each page...")
                for page_num, page in enumerate(pdf_reader.pages):
                    if '/Annots' in page:
                        print(f"Page {page_num + 1} has annotations")
                    else:
                        print(f"Page {page_num + 1} has no annotations")
                        
    except Exception as e:
        print(f"Error examining PDF: {e}")

if __name__ == "__main__":
    pdf_path = "PardonApp_Aug2021.pdf"
    examine_pdf_fields(pdf_path)
