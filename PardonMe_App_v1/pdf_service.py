"""
PDF Service Module for Wisconsin Pardon Application
Handles loading, mapping, and filling the official PDF form with user data.
"""

import os
import io
from pypdf import PdfReader, PdfWriter


def load_pdf_template():
    """Load the official Wisconsin pardon application PDF template."""
    template_path = os.path.join(os.path.dirname(__file__), 'PardonApp_Aug2021.pdf')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"PDF template not found at {template_path}")
    return template_path


def create_field_mappings(session_data):
    """
    Create field mappings between session data and PDF form field names.
    Based on the official Wisconsin pardon application PDF fields.
    """
    
    # Helper function to safely get nested session data
    def get_session_value(section, key, default=''):
        return session_data.get(section, {}).get(key, default) or default
    
    # Main field mappings for Wisconsin pardon application
    FIELD_MAPPINGS = {
        # Section 1 - Personal Information
        'Name First Middle LastRow1': f"{get_session_value('section_one', 'first_name')} {get_session_value('section_one', 'middle_name')} {get_session_value('section_one', 'last_name')}".strip(),
        'Date of birth MMDDYYYYRow1': get_session_value('section_one', 'dob'),  
        'Social Security NumberRow1': get_session_value('section_one', 'ssn'),
        'Home addressRow1': get_session_value('section_one', 'home_address'),
        'Mailing addressRow1': get_session_value('section_one', 'mailing_address'),
        'Email addressRow1': get_session_value('section_one', 'email'),
        'Home phone numberRow1': get_session_value('section_one', 'home_phone'),
        'Work phone numberRow1': get_session_value('section_one', 'work_phone'),
        'Cell phone numberRow1': get_session_value('section_one', 'cell_phone'),
        
        # Alias information
        'Maiden name alias or former nameRow1': f"{get_session_value('section_one', 'alias_first_name')} {get_session_value('section_one', 'alias_last_name')}".strip(),
        'Dates usedRow1': get_session_value('section_one', 'alias_dates'),
        
        # Section 2 - Criminal History  
        'CrimeRow1': get_session_value('section_two', 'crime'),
        'Court case numberRow1': get_session_value('section_two', 'case_number'), 
        'SentenceRow1': get_session_value('section_two', 'sentence'),
        'Date of sentencing MMDDYYYYRow1': get_session_value('section_two', 'sentencing_date'),
        'County where conviction occurredRow1': get_session_value('section_two', 'county'),
        
        # Additional criminal history fields
        'CrimeRow1_2': get_session_value('section_two', 'crime_2'),
        'Court case numberRow1_2': get_session_value('section_two', 'case_number_2'),
        'SentenceRow1_2': get_session_value('section_two', 'sentence_2'),
        'Date of sentencing MMDDYYYYRow1_2': get_session_value('section_two', 'sentencing_date_2'),
        'County where conviction occurredRow1_2': get_session_value('section_two', 'county_2'),
        
        'CrimeRow1_3': get_session_value('section_two', 'crime_3'),
        'Court case numberRow1_3': get_session_value('section_two', 'case_number_3'),
        'SentenceRow1_3': get_session_value('section_two', 'sentence_3'),
        'Date of sentencing MMDDYYYYRow1_3': get_session_value('section_two', 'sentencing_date_3'),
        'County where conviction occurredRow1_3': get_session_value('section_two', 'county_3'),
        
        # Section 3 - Sentence & Incarceration
        'Text1': get_session_value('section_three', 'restitution_details'),
        
        # Section 4 - Employment & Education
        'EmployerRow1': get_session_value('section_four', 'employer_1'),
        'Position heldRow1': get_session_value('section_four', 'position_1'),
        'Employer address and phone numberRow1': get_session_value('section_four', 'employer_address_1'),
        'Name of supervisorRow1': get_session_value('section_four', 'supervisor_1'),
        'Dates of employmentRow1': get_session_value('section_four', 'employment_dates_1'),
        
        'EmployerRow2': get_session_value('section_four', 'employer_2'),
        'Position heldRow2': get_session_value('section_four', 'position_2'), 
        'Employer address and phone numberRow2': get_session_value('section_four', 'employer_address_2'),
        'Name of supervisorRow2': get_session_value('section_four', 'supervisor_2'),
        'Dates of employmentRow2': get_session_value('section_four', 'employment_dates_2'),
        
        'EmployerRow3': get_session_value('section_four', 'employer_3'),
        'Position heldRow3': get_session_value('section_four', 'position_3'),
        'Employer address and phone numberRow3': get_session_value('section_four', 'employer_address_3'), 
        'Name of supervisorRow3': get_session_value('section_four', 'supervisor_3'),
        'Dates of employmentRow3': get_session_value('section_four', 'employment_dates_3'),
        
        'EmployerRow4': get_session_value('section_four', 'employer_4'),
        'Position heldRow4': get_session_value('section_four', 'position_4'),
        'Employer address and phone numberRow4': get_session_value('section_four', 'employer_address_4'),
        'Name of supervisorRow4': get_session_value('section_four', 'supervisor_4'),
        'Dates of employmentRow4': get_session_value('section_four', 'employment_dates_4'),
        
        'EmployerRow5': get_session_value('section_four', 'employer_5'),
        'Position heldRow5': get_session_value('section_four', 'position_5'),
        'Employer address and phone numberRow5': get_session_value('section_four', 'employer_address_5'),
        'Name of supervisorRow5': get_session_value('section_four', 'supervisor_5'),
        'Dates of employmentRow5': get_session_value('section_four', 'employment_dates_5'),
        
        'EmployerRow6': get_session_value('section_four', 'employer_6'),
        'Position heldRow6': get_session_value('section_four', 'position_6'),
        'Employer address and phone numberRow6': get_session_value('section_four', 'employer_address_6'),
        'Name of supervisorRow6': get_session_value('section_four', 'supervisor_6'),
        'Dates of employmentRow6': get_session_value('section_four', 'employment_dates_6'),
        
        # Education
        '13List the highest grade you completed or degree you received': get_session_value('section_four', 'education_level'),
        
        # Section 5 - Community Involvement  
        'Describe any education you have received since conviction': get_session_value('section_five', 'education_since_conviction'),
        'If you served in the military provide the details of your service': get_session_value('section_five', 'military_service'),
        'Describe any community service activities or volunteer work you have participated in since conviction': get_session_value('section_five', 'community_service'),
        'Describe any treatment or counseling you have participated in since conviction': get_session_value('section_five', 'treatment_counseling'),
        'Describe any other steps or actions that you have not mentioned so far': get_session_value('section_five', 'other_steps'),
        
        # Section 6 - Character References (basic fields)
        'Reference 1 NameRow1': get_session_value('section_six', 'reference_1_name'),
        'Reference 1 AddressRow1': get_session_value('section_six', 'reference_1_address'),
        'Reference 1 Phone NumberRow1': get_session_value('section_six', 'reference_1_phone'),
        
        'Reference 2 NameRow1': get_session_value('section_six', 'reference_2_name'),
        'Reference 2 AddressRow1': get_session_value('section_six', 'reference_2_address'),
        'Reference 2 Phone NumberRow1': get_session_value('section_six', 'reference_2_phone'),
        
        'Reference 3 NameRow1': get_session_value('section_six', 'reference_3_name'),
        'Reference 3 AddressRow1': get_session_value('section_six', 'reference_3_address'),
        'Reference 3 Phone NumberRow1': get_session_value('section_six', 'reference_3_phone'),
        
        # Section 7 - Statement & Signature
        'Applicant SignatureRow1': get_session_value('section_seven', 'signature'),
        'DateRow1': get_session_value('section_seven', 'signature_date'),
    }
    
    # Return only non-empty field mappings
    return {field: value for field, value in FIELD_MAPPINGS.items() if value and value.strip()}


def fill_pdf_form(template_path, field_mappings):
    """
    Fill the PDF form fields with mapped data and return PDF bytes.
    """
    try:
        # Read the PDF template
        reader = PdfReader(template_path)
        writer = PdfWriter()
        
        # Process each page
        for page_num, page in enumerate(reader.pages):
            # Get form fields for this page
            if reader.trailer.get("/AcroForm"):
                # Fill form fields with mapped data
                writer.add_page(page)
                
        # Update form field values
        if writer.get_form() and field_mappings:
            for field_name, field_value in field_mappings.items():
                try:
                    writer.update_page_form_field_values(
                        writer.pages[0], {field_name: str(field_value)[:500]}  # Limit field length
                    )
                except Exception as e:
                    print(f"Warning: Could not fill field '{field_name}': {e}")
                    continue
        
        # Write to bytes buffer
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer.getvalue()
        
    except Exception as e:
        raise Exception(f"Error filling PDF form: {str(e)}")


def generate_completed_pdf(session_data):
    """
    Main function to generate a completed PDF from session data.
    """
    try:
        # Load PDF template
        template_path = load_pdf_template()
        
        # Create field mappings from session data
        field_mappings = create_field_mappings(session_data)
        
        # Fill PDF form and return bytes
        pdf_bytes = fill_pdf_form(template_path, field_mappings)
        
        return pdf_bytes
        
    except Exception as e:
        raise Exception(f"Error generating completed PDF: {str(e)}")
