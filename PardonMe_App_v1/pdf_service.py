"""
PDF Service Module for Wisconsin Pardon Application
Handles loading, mapping, and filling the official PDF form with user data.
"""

import os
import io
import fitz  # PyMuPDF
from pypdf import PdfReader  # Keep for field analysis only


def load_pdf_template():
    """Load the official Wisconsin pardon application PDF template."""
    template_path = os.path.join(os.path.dirname(__file__), 'PardonApp_Aug2021.pdf')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"PDF template not found at {template_path}")
    return template_path


def create_field_mappings(session_data):
    """
    Create exact field mappings from session data to PDF form field names.
    Based on actual PDF field names discovered through debugging.
    """
    print("\n=== CREATING FIELD MAPPINGS ===")
    
    # Extract nested session data
    section_one = session_data.get('section_one', {})
    section_two = session_data.get('section_two', {})
    section_three = session_data.get('section_three', {})
    section_four = session_data.get('section_four', {})
    section_five = session_data.get('section_five', {})
    section_six = session_data.get('section_six', {})
    section_seven = session_data.get('section_seven', {})
    
    # Get first offense data
    offenses = section_two.get('offenses', [])
    first_offense = offenses[0] if offenses else {}
    
    # Get first reference data
    references = section_six.get('references', [])
    first_reference = references[0] if references else {}
    
    # Build comprehensive field mappings
    field_mappings = {
        # === SECTION ONE: Personal Information ===
        'Name First Middle LastRow1': f"{section_one.get('first_name', '')} {section_one.get('middle_name', '')} {section_one.get('last_name', '')}".strip(),
        'Date of birth MMDDYYYYRow1': section_one.get('dob', ''),
        'Email addressRow1': section_one.get('email', ''),
        'Home phoneRow1': section_one.get('home_phone', ''),
        'Work phoneRow1': section_one.get('work_phone', ''),
        'Cell phoneRow1': section_one.get('cell_phone', ''),
        'Place of birth City StateRow1': section_one.get('birth_place', ''),
        'Gender optionalRow1': section_one.get('gender', ''),
        'Social Security NumberRow1': section_one.get('ssn', ''),
        'Race or Ethnicity optionalRow1': section_one.get('ethnicity', ''),
        'Home addressRow1': f"{section_one.get('home_address', '')} {section_one.get('home_apartment', '')}".strip(),
        'Mailing addressRow1': f"{section_one.get('mailing_address', '')} {section_one.get('mailing_apartment', '')}".strip(),
        
        # === ALIAS/MAIDEN NAME FIELDS ===
        'Maidenaliasformer namesRow1': section_one.get('alias_names', ''),
        'Dates used MMYY  MMYYRow1': section_one.get('alias_dates', ''),
        'Maidenaliasformer namesRow2': '',  # No additional aliases in session data
        'Dates used MMYY  MMYYRow2': '',
        'Maidenaliasformer namesRow3': '',
        'Dates used MMYY  MMYYRow3': '',
        
        # === SECTION TWO: Criminal History - First Offense ===
        'CrimeRow1': first_offense.get('crime', ''),
        'Court case numberRow1': first_offense.get('case_number', ''),
        'County of convictionRow1': first_offense.get('county', ''),
        'Date of offenseRow1': first_offense.get('offense_date', ''),
        'Sentencing dateRow1': first_offense.get('sentencing_date', ''),
        'Sentence received confinement and supervisionRow1': first_offense.get('sentence_received', ''),
        'Date you completed your sentenceRow1': first_offense.get('sentence_completed', ''),
        'District attorneys who oversaw your convictionRow1': first_offense.get('district_attorney', ''),
        'Judges who presided over your convictionRow1': first_offense.get('judge', ''),
        
        # === CHECKBOX FIELDS FOR YES/NO QUESTIONS ===
        # Physical documents checkbox
        'I have attached certified copies of these three court documents Yes': 'yes' if section_two.get('physical_docs_flags') else '',
        'No': 'yes' if not section_two.get('physical_docs_flags') else '',
        
        # Other crimes/convictions
        'from other places such as from other states or federal convictions Yes': 'yes' if section_two.get('other_crimes') == 'yes' else '',
        'No_2': 'yes' if section_two.get('other_crimes') == 'no' else '',
        
        # Restitution
        '5 Were you ordered to pay restitution for any of your crimes Yes': 'yes' if section_two.get('restitution_ordered') == 'yes' else '',
        'No_3': 'yes' if section_two.get('restitution_ordered') == 'no' else '',
        'If yes have you paid the full amount ordered Yes': 'yes' if section_two.get('restitution_paid') == 'yes' else '',
        'No_4': 'yes' if section_two.get('restitution_paid') == 'no' else '',
        
        # Previous pardon
        '6 Have you ever applied for pardon before Yes': 'yes' if section_two.get('previous_pardon') == 'yes' else '',
        'No_5': 'yes' if section_two.get('previous_pardon') == 'no' else '',
        'If yes please provide the date of the request MMYYYY': section_two.get('previous_pardon_date', ''),
        'hearing andor receipt of formal denial': section_two.get('previous_pardon_details', ''),
        
        # Other law enforcement contacts
        'where you have been the subject of criminal investigations Yes': 'yes' if section_two.get('other_law_enforcement') == 'yes' else '',
        'No_6': 'yes' if section_two.get('other_law_enforcement') == 'no' else '',
        'the circumstances which led to the contacts Attach additional pages if necessary': section_two.get('other_law_enforcement_details', ''),
        
        # Restraining orders
        '8 Has anyone ever gotten a restraining order or order of protection against you Yes': '',  # No data in session
        'No_7': 'yes',  # Default to No since no restraining order data
        'If yes explain what happened and when Attach additional pages if necessary': '',
        
        # === SECTION THREE: Supervision/Incarceration Details ===
        'pages if necessary': section_three.get('sentence_details', ''),
        'supervisor': section_three.get('supervision_officer', ''),
        'additional pages if necessary': section_three.get('programs_completed', ''),
        'additional pages if necessary_2': section_three.get('treatment_programs', ''),
        
        # === SECTION FOUR: Employment Information ===
        'EmployerRow1': section_four.get('employer_name', ''),
        'Position heldRow1': section_four.get('job_title', ''),
        'employment': section_four.get('employment_start', ''),
        'number': section_four.get('work_phone', ''),  # Employer phone
        'Employment phoneRow1': section_four.get('employment_phone', ''),  # Employment phone
        'No_9': 'yes' if section_four.get('current_employment') in ['unemployed', 'retired'] else '',
        
        # === SECTION SEVEN: Education and Personal Growth ===
        '13List the highest grade you completed or degree you received': section_four.get('education_level', ''),
        'Describe any education you have received since conviction': section_four.get('education_since_conviction', ''),
        'If you served in the military, provide the details of your service': '',  # No military data in session
        'Describe any community service, activities, or volunteer work you have participated in since conviction': section_five.get('community_service', ''),
        'Describe any treatment or counseling you have participated in since conviction': section_five.get('counseling_participation', ''),
        'Describe any other steps or actions that you have not mentioned so far': section_five.get('personal_growth', ''),
        
        # === EMPLOYMENT STATUS CHECKBOX (Page 8) ===
        'convictions Yes': 'yes' if section_four.get('current_employment') == 'employed_full_time' else '',
        'No_8': 'yes' if section_four.get('current_employment') in ['unemployed', 'retired'] else '',
        
        # === SECTION SIX: References ===
        'Reference 1 NameRow1': first_reference.get('name', ''),
        'Reference 1 AddressRow1': first_reference.get('address', ''),
        'Reference 1 Phone NumberRow1': first_reference.get('phone', ''),
        
        # === PAGE 10: Summary Information ===
        'Applicant nameRow1': f"{section_one.get('first_name', '')} {section_one.get('middle_name', '')} {section_one.get('last_name', '')}".strip(),
        'Date of birth MMDDYYYYRow1_2': section_one.get('dob', ''),
        'Mailing addressRow1_2': f"{section_one.get('mailing_address', '')} {section_one.get('mailing_apartment', '')}".strip(),
        'Phone number and email addressRow1': f"{section_one.get('cell_phone', '')} {section_one.get('email', '')}".strip(),
        'CrimeRow1_5': first_offense.get('crime', ''),
        'Court case numberRow1_5': first_offense.get('case_number', ''),
        'CountyRow1': first_offense.get('county', ''),
        'SentenceRow1': first_offense.get('sentence_received', ''),
        'Sentencing date MMDDYYYYRow1': first_offense.get('sentencing_date', ''),
        
        # === PAGE 11: Additional Summary Fields ===
        'Applicant nameRow1_2': f"{section_one.get('first_name', '')} {section_one.get('middle_name', '')} {section_one.get('last_name', '')}".strip(),
        'Date of birth MMDDYYYYRow1_3': section_one.get('dob', ''),
        'Mailing addressRow1_3': f"{section_one.get('mailing_address', '')} {section_one.get('mailing_apartment', '')}".strip(),
        'Phone number and email addressRow1_2': f"{section_one.get('cell_phone', '')} {section_one.get('email', '')}".strip(),
        'CrimeRow1_6': first_offense.get('crime', ''),
        'Court case numberRow1_6': first_offense.get('case_number', ''),
        'SentenceRow1_2': first_offense.get('sentence_received', ''),
        'Sentencing date MMDDYYYYRow1_2': first_offense.get('sentencing_date', ''),
    }
    
    # Filter out empty values
    non_empty_mappings = {k: v for k, v in field_mappings.items() if v and str(v).strip()}
    
    print(f"Created {len(non_empty_mappings)} non-empty field mappings out of {len(field_mappings)} total attempted")
    print("Generated {} field mappings:".format(len(non_empty_mappings)))
    for key, value in non_empty_mappings.items():
        print(f"  '{key}' -> '{value}'")
    
    return non_empty_mappings


def fill_pdf_form(template_path, field_mappings):
    """
    Fill the PDF form using PyMuPDF (fitz) for reliable form handling.
    """
    try:
        print("\n=== FILLING PDF FORM WITH PYMUPDF ===")
        
        # Open the PDF with PyMuPDF
        doc = fitz.open(template_path)
        print(f"PDF opened successfully. Pages: {doc.page_count}")
        
        # Track successful field updates
        fields_updated = 0
        fields_failed = 0
        
        # Iterate through all pages and widgets (form fields)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            widgets = list(page.widgets())  # Convert generator to list
            
            if widgets:
                print(f"\nPage {page_num + 1}: Found {len(widgets)} form fields")
                
                # First pass: Show ALL field names for discovery
                print(f"  🔍 ALL FIELD NAMES ON PAGE {page_num + 1}:")
                for widget in widgets:
                    field_name = widget.field_name
                    field_type = widget.field_type_string
                    mapped = "✅ MAPPED" if field_name in field_mappings else "❌ UNMAPPED"
                    print(f"    - '{field_name}' ({field_type}) - {mapped}")
                
                print(f"  📝 UPDATING MAPPED FIELDS:")
                # Second pass: Update mapped fields
                for widget in widgets:
                    field_name = widget.field_name
                    if field_name in field_mappings:
                        field_value = field_mappings[field_name]
                        try:
                            # Handle different field types
                            if widget.field_type_string in ['CheckBox', 'Button']:
                                # For checkboxes, try different checkbox values
                                if str(field_value).lower() in ['yes', 'true', '1', 'on']:
                                    widget.field_value = True
                                else:
                                    widget.field_value = False
                            else:
                                # Regular text fields
                                widget.field_value = str(field_value)
                            
                            widget.update()
                            fields_updated += 1
                            print(f"    ✅ Updated '{field_name}' ({widget.field_type_string}) -> '{field_value}'")
                        except Exception as widget_error:
                            fields_failed += 1
                            print(f"    ❌ Failed to update '{field_name}': {widget_error}")
        
        print(f"\n📊 SUMMARY: {fields_updated} fields updated, {fields_failed} failed")
        
        # Save to bytes
        pdf_bytes = doc.tobytes()
        doc.close()
        
        print("✅ PDF form filled successfully with PyMuPDF")
        return pdf_bytes
        
    except Exception as e:
        print(f"ERROR in fill_pdf_form: {e}")
        raise


def generate_completed_pdf(session_data):
    """Generate a completed Wisconsin pardon application PDF."""
    try:
        print("\n=== PDF GENERATION DEBUG ===")
        print(f"Session data received: {session_data}")
        print(f"Session data type: {type(session_data)}")
        print(f"Session keys: {list(session_data.keys())}")
        
        # Print detailed session data for debugging
        for section_key, section_data in session_data.items():
            if isinstance(section_data, dict):
                print(f"\n{section_key.upper()} DATA:")
                for key, value in section_data.items():
                    print(f"  {key}: {value}")
        
        # Load PDF template
        template_path = load_pdf_template()
        print(f"\nPDF template path: {template_path}")
        
        # Create field mappings
        field_mappings = create_field_mappings(session_data)
        
        # Fill the PDF form using PyMuPDF
        pdf_bytes = fill_pdf_form(template_path, field_mappings)
        
        print("✅ PDF generation completed successfully")
        return pdf_bytes
        
    except Exception as e:
        print(f"ERROR in generate_completed_pdf: {e}")
        raise Exception(f"Error generating PDF: {str(e)}")
