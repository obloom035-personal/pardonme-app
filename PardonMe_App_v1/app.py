from flask import Flask, render_template, request, redirect, session, url_for, make_response
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import json
import os
import io
from datetime import datetime

app = Flask(__name__)
# Using a placeholder for local development. This should be a real secret in production.
app.secret_key = os.environ.get("APP_SECRET_KEY", "dev-placeholder-for-local-use-only")

# This switch enables/disables features for local development vs. production.
# To enable, run in your terminal: `export FLASK_ENV=development` before `python app.py`
IS_DEVELOPMENT = os.environ.get('FLASK_ENV') == 'development'


@app.route('/')
def home():
    session.clear()  # Clear session to start fresh
    return render_template('home.html')

@app.route("/section_one", methods=["GET", "POST"])
def section_one():
    if request.method == "POST":
        # Get form data from Section 1
        data = {
            "first_name": request.form.get("first_name"),
            "middle_name": request.form.get("middle_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "work_phone": request.form.get("work_phone"),
            "birth_place": request.form.get("birth_place"),
            "ssn": request.form.get("ssn"),
            "home_address": request.form.get("home_address"),
            "home_apartment": request.form.get("home_apartment"),
            "alias_names": request.form.get("alias_names"),
            "dob": request.form.get("dob"),
            "home_phone": request.form.get("home_phone"),
            "cell_phone": request.form.get("cell_phone"),
            "gender": request.form.get("gender"),
            "ethnicity": request.form.get("ethnicity"),
            "mailing_address": request.form.get("mailing_address"),
            "mailing_apartment": request.form.get("mailing_apartment"),
            "alias_dates": request.form.get("alias_dates"),
        }

        # Save to session (primary storage)
        session['section_one'] = data

        # If in development mode, also write to a JSON file for easy debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_one.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_one.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for('section_two'))

    # Render Section 1 page for a GET request
    current_section = 1
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_one.html", progress=progress)

@app.route("/section_two", methods=["GET", "POST"])
def section_two():
    # Prevent users from skipping ahead to this section
    if 'section_one' not in session:
        return redirect(url_for('section_one'))

    if request.method == "POST":
        # The form fields have '[]' in their names, e.g., name="crime[]"
        # request.form.getlist() will collect all of them into Python lists.
        crimes = request.form.getlist('crime[]')
        case_numbers = request.form.getlist('case_number[]')
        counties = request.form.getlist('county[]')
        offense_dates = request.form.getlist('offense_date[]')
        sentencing_dates = request.form.getlist('sentencing_date[]')
        sentences_received = request.form.getlist('sentence_received[]')
        sentences_completed = request.form.getlist('sentence_completed[]')
        district_attorneys = request.form.getlist('district_attorney[]')
        judges = request.form.getlist('judge[]')
        
        uploaded_files = request.files.getlist('documents[]')
        physical_docs_flags = request.form.getlist('sending_physical_docs[]')
        
        file_paths = []
        for file in uploaded_files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads', filename)
                os.makedirs('uploads', exist_ok=True)
                file.save(file_path)
                file_paths.append(file_path)

        offenses = []
        # We loop through the number of crimes submitted to build a dictionary for each offense
        for i in range(len(crimes)):
            offense_data = {
                "crime": crimes[i],
                "case_number": case_numbers[i],
                "county": counties[i],
                "offense_date": offense_dates[i],
                "sentencing_date": sentencing_dates[i],
                "sentence_received": sentences_received[i],
                "sentence_completed": sentences_completed[i],
                "district_attorney": district_attorneys[i],
                "judge": judges[i],
            }
            offenses.append(offense_data)

        section_two_data = {
            "offenses": offenses,
            "uploaded_files": file_paths,
            "physical_docs_flags": physical_docs_flags,
            "other_crimes": request.form.get('other_crimes', ''),
            "other_crimes_details": request.form.get('other_crimes_details', ''),
            "restitution_ordered": request.form.get('restitution_ordered', ''),
            "restitution_paid": request.form.get('restitution_paid', ''),
            "restitution_proof": request.form.get('restitution_proof', ''),
            "previous_pardon": request.form.get('previous_pardon', ''),
            "previous_pardon_date": request.form.get('previous_pardon_date', ''),
            "previous_pardon_details": request.form.get('previous_pardon_details', ''),
            "other_law_enforcement": request.form.get('other_law_enforcement', ''),
            "other_law_enforcement_details": request.form.get('other_law_enforcement_details', '')
        }

        # Save the complete section two data to the session
        session['section_two'] = section_two_data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_two.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_two.json", "w") as f:
                json.dump(section_two_data, f, indent=4)

        return redirect(url_for("section_three"))

    # Render Section 2 page for a GET request
    current_section = 2
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_two.html", progress=progress, current_section=2)

@app.route("/section_three", methods=["GET", "POST"])
def section_three():
    # Prevent users from skipping ahead to this section
    if 'section_two' not in session:
        return redirect(url_for('section_two'))

    if request.method == "POST":
        # Get form data from Section 3
        data = {
            "sentence_details": request.form.get("sentence_details"),
            "incarceration_location": request.form.get("incarceration_location"),
            "incarceration_start": request.form.get("incarceration_start"),
            "incarceration_end": request.form.get("incarceration_end"),
            "supervision_type": request.form.get("supervision_type"),
            "supervision_start": request.form.get("supervision_start"),
            "supervision_end": request.form.get("supervision_end"),
            "supervision_officer": request.form.get("supervision_officer"),
            "compliance_issues": request.form.get("compliance_issues"),
            "compliance_details": request.form.get("compliance_details"),
            "programs_completed": request.form.get("programs_completed"),
            "treatment_programs": request.form.get("treatment_programs")
        }

        # Save to session
        session['section_three'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_three.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_three.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for('section_four'))

    # Render Section 3 page for a GET request
    current_section = 3
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_three.html", progress=progress, current_section=3)

@app.route("/section_four", methods=["GET", "POST"])
def section_four():
    # Prevent users from skipping ahead to this section
    if 'section_three' not in session:
        return redirect(url_for('section_three'))

    if request.method == "POST":
        # Get form data from Section 4
        data = {
            "current_employment": request.form.get("current_employment"),
            "employer_name": request.form.get("employer_name"),
            "job_title": request.form.get("job_title"),
            "employment_start": request.form.get("employment_start"),
            "employment_income": request.form.get("employment_income"),
            "employment_history": request.form.get("employment_history"),
            "education_level": request.form.get("education_level"),
            "education_since_conviction": request.form.get("education_since_conviction"),
            "vocational_training": request.form.get("vocational_training"),
            "certifications": request.form.get("certifications"),
            "career_goals": request.form.get("career_goals"),
            "financial_stability": request.form.get("financial_stability")
        }

        # Save to session
        session['section_four'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_four.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_four.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for('section_five'))

    # Render Section 4 page for a GET request
    current_section = 4
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_four.html", progress=progress, current_section=4)

@app.route("/section_five", methods=["GET", "POST"])
def section_five():
    # Prevent users from skipping ahead to this section
    if 'section_four' not in session:
        return redirect(url_for('section_four'))

    if request.method == "POST":
        # Get form data from Section 5
        data = {
            "volunteer_work": request.form.get("volunteer_work"),
            "community_service": request.form.get("community_service"),
            "religious_involvement": request.form.get("religious_involvement"),
            "support_groups": request.form.get("support_groups"),
            "counseling_participation": request.form.get("counseling_participation"),
            "mentoring_roles": request.form.get("mentoring_roles"),
            "community_leadership": request.form.get("community_leadership"),
            "charitable_activities": request.form.get("charitable_activities"),
            "civic_participation": request.form.get("civic_participation"),
            "personal_growth": request.form.get("personal_growth")
        }

        # Save to session
        session['section_five'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_five.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_five.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for('section_six'))

    # Render Section 5 page for a GET request
    current_section = 5
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_five.html", progress=progress, current_section=5)

@app.route("/section_six", methods=["GET", "POST"])
def section_six():
    # Prevent users from skipping ahead to this section
    if 'section_five' not in session:
        return redirect(url_for('section_five'))

    if request.method == "POST":
        reference_names = request.form.getlist('reference_name[]')
        reference_relationships = request.form.getlist('reference_relationship[]')
        reference_phones = request.form.getlist('reference_phone[]')
        reference_emails = request.form.getlist('reference_email[]')
        reference_addresses = request.form.getlist('reference_address[]')
        reference_years_known = request.form.getlist('reference_years_known[]')

        uploaded_letters = request.files.getlist('reference_letters[]')
        letter_paths = []
        for file in uploaded_letters:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads', 'references', filename)
                os.makedirs('uploads/references', exist_ok=True)
                file.save(file_path)
                letter_paths.append(file_path)

        references = []
        for i in range(len(reference_names)):
            if reference_names[i]:  # Only add if name is provided
                reference_data = {
                    "name": reference_names[i],
                    "relationship": reference_relationships[i] if i < len(reference_relationships) else "",
                    "phone": reference_phones[i] if i < len(reference_phones) else "",
                    "email": reference_emails[i] if i < len(reference_emails) else "",
                    "address": reference_addresses[i] if i < len(reference_addresses) else "",
                    "years_known": reference_years_known[i] if i < len(reference_years_known) else ""
                }
                references.append(reference_data)

        data = {
            "references": references,
            "reference_letters": letter_paths,
            "additional_references": request.form.get("additional_references", "")
        }

        # Save to session
        session['section_six'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_six.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_six.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for('section_seven'))

    # Render Section 6 page for a GET request
    current_section = 6
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_six.html", progress=progress, current_section=6)

@app.route("/section_seven", methods=["GET", "POST"])
def section_seven():
    # Prevent users from skipping ahead to this section
    if 'section_six' not in session:
        return redirect(url_for('section_six'))

    if request.method == "POST":
        # Get form data from Section 7
        data = {
            "personal_statement": request.form.get("personal_statement"),
            "why_pardon": request.form.get("why_pardon"),
            "life_changes": request.form.get("life_changes"),
            "future_goals": request.form.get("future_goals"),
            "remorse_statement": request.form.get("remorse_statement"),
            "signature": request.form.get("signature"),
            "signature_date": request.form.get("signature_date"),
            "application_complete": request.form.get("application_complete") == "on"
        }

        # Save to session
        session['section_seven'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_seven.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_seven.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for('application_complete'))

    # Render Section 7 page for a GET request
    current_section = 7
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)
    return render_template("section_seven.html", progress=progress, current_section=7)

def safe_str(value):
    """Helper function to safely convert any value to a string, handling None values."""
    if value is None:
        return ""
    return str(value)

@app.route("/test_pdf")
def test_pdf():
    """Test route to generate PDF with sample data"""
    # Populate session with sample data for testing
    session['section_one'] = {
        'first_name': 'John',
        'middle_name': 'Michael',
        'last_name': 'Smith',
        'dob': '01/15/1985',
        'ssn': '123-45-6789',
        'mailing_address': '123 Main Street, Madison, WI 53703',
        'home_phone': '(608) 555-0123',
        'email': 'john.smith@email.com',
        'alias_used': 'yes',
        'alias_first_name': 'Johnny',
        'alias_last_name': 'Smith'
    }
    
    session['section_two'] = {
        'crime': 'Burglary',
        'case_number': '2018CF001234',
        'sentence': '3 years probation, $5000 fine',
        'sentencing_date': '03/15/2018',
        'county': 'Dane County',
        'other_convictions': 'no',
        'pending_charges': 'no',
        'other_interactions': 'Arrested for DUI in 2010, charges dropped'
    }
    
    session['section_three'] = {
        'notice_sent': 'yes'
    }
    
    session['section_four'] = {
        'employer_1': 'ABC Construction',
        'position_1': 'Site Supervisor',
        'start_date_1': '06/2019',
        'end_date_1': 'Present',
        'employer_2': 'Local Hardware Store',
        'position_2': 'Sales Associate',
        'start_date_2': '01/2019',
        'end_date_2': '05/2019',
        'education_level': 'High School Diploma',
        'education_since_conviction': 'Completed construction management certificate program at Madison College in 2020'
    }
    
    session['section_five'] = {
        'volunteer_work': 'Volunteer at local food bank every Saturday for the past 2 years. Help serve meals and organize donations.',
        'counseling_participation': 'Completed anger management counseling program in 2019. Attended weekly sessions for 6 months.',
        'personal_growth': 'Started attending church regularly, joined a support group for people with criminal backgrounds, and mentor young people in my neighborhood.'
    }
    
    session['section_seven'] = {
        'personal_statement': 'I made a serious mistake when I was younger and broke into a house when I was struggling with addiction. I take full responsibility for my actions and the harm I caused to the victim and community. Since then, I have worked hard to turn my life around.',
        'why_pardon': 'I am seeking a pardon to remove barriers to employment and housing. My criminal record has prevented me from advancing in my career and finding stable housing for my family.',
        'life_changes': 'I have been sober for 5 years, completed my probation successfully, paid all restitution, and have been steadily employed. I am now a contributing member of my community.',
        'signature': 'John M. Smith',
        'signature_date': '07/12/2025'
    }
    
    # Now generate the PDF with this sample data
    return generate_pdf()

@app.route("/generate_pdf")
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=12, alignment=1, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Normal'], fontSize=12, spaceAfter=6, alignment=1)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=12, spaceAfter=6, fontName='Helvetica-Bold')
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, fontName='Helvetica')
    small_style = ParagraphStyle('SmallText', parent=styles['Normal'], fontSize=8, fontName='Helvetica')
    question_style = ParagraphStyle('QuestionStyle', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', spaceAfter=6)
    answer_style = ParagraphStyle('AnswerStyle', parent=styles['Normal'], fontSize=10, fontName='Helvetica', leftIndent=20, spaceAfter=12)
    
    story = []
    
    # PAGE 1 - Header and Instructions
    story.append(Paragraph("Tony Evers", title_style))
    story.append(Paragraph("Office of the Governor • State of Wisconsin", subtitle_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("State of Wisconsin Pardon Application", title_style))
    story.append(Spacer(1, 18))
    
    # Notice section (more detailed)
    notice_text = (
        "<b>Notice:</b> This application and any materials submitted in support of it may be used for purposes "
        "other than consideration for a pardon. Further, the application and materials are subject to public "
        "disclosure under Wisconsin's Public Records Law, which means they may be released to members "
        "of the public if requested. Wis. Stat. §§ 19.31-19.39."
    )
    story.append(Paragraph(notice_text, normal_style))
    story.append(Spacer(1, 18))
    
    # Eligibility section (expanded)
    story.append(Paragraph("<b>Eligibility:</b> You are eligible for a pardon only if <b>all</b> of the following conditions apply to you:", normal_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("1. You are seeking a pardon for a Wisconsin felony conviction.", normal_style))
    story.append(Paragraph("2. It has been <i>at least</i> five (5) years since you finished any criminal sentence. This means you:", normal_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;a. Completed all confinement; and", normal_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;b. Completed all supervised release (e.g., probation, parole, or extended supervision).", normal_style))
    story.append(Paragraph("3. You do not have any pending criminal cases or charges in any jurisdiction.", normal_style))
    story.append(Paragraph("4. You are not currently required to register as a sex offender.", normal_style))
    story.append(Spacer(1, 18))
    
    # Instructions section
    instructions_text = (
        "<b>Instructions:</b><br/>"
        "• Please type or print legibly.<br/>"
        "• Answer all questions completely. If a question does not apply to you, write 'N/A'.<br/>"
        "• Attach additional pages if you need more space for any answer.<br/>"
        "• You must submit this application and all supporting documents to the Governor's office.<br/>"
        "• Do not leave any question blank."
    )
    story.append(Paragraph(instructions_text, normal_style))
    story.append(Spacer(1, 24))
    
    # Page break after instructions
    story.append(PageBreak())
    
    # PAGE 2 - Section 1: Personal Information (Expanded)
    story.append(Paragraph("<b>Section 1: Personal Information</b>", heading_style))
    story.append(Paragraph("1. Provide the following personal information:", normal_style))
    story.append(Spacer(1, 12))
    
    section_one = session.get('section_one', {})
    
    # Expanded personal information table (more detailed)
    personal_data = [
        ['Name (First Middle Last)', 'Date of birth (MM/DD/YYYY)'],
        [safe_str(f"{section_one.get('first_name', '')} {section_one.get('middle_name', '')} {section_one.get('last_name', '')}").strip(), safe_str(section_one.get('dob'))],
        ['Email address', 'Home phone'],
        [safe_str(section_one.get('email')), safe_str(section_one.get('home_phone'))],
        ['Work phone', 'Cell phone'],
        [safe_str(section_one.get('work_phone')), safe_str(section_one.get('cell_phone'))],
        ['Place of birth (City, State)', 'Gender (optional)'],
        [safe_str(section_one.get('birth_place')), safe_str(section_one.get('gender'))],
        ['Social Security Number', 'Race or Ethnicity (optional)'],
        [safe_str(section_one.get('ssn')), safe_str(section_one.get('ethnicity'))],
        ['Home address (Street, City, State, ZIP)', ''],
        [safe_str(section_one.get('home_address')), ''],
        ['Mailing address (if different from home address)', ''],
        [safe_str(section_one.get('mailing_address')), '']
    ]
    
    personal_table = Table(personal_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=[0.4*inch]*len(personal_data))
    personal_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 2), (1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 4), (1, 4), colors.lightgrey),
        ('BACKGROUND', (0, 6), (1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 8), (1, 8), colors.lightgrey),
        ('BACKGROUND', (0, 10), (1, 10), colors.lightgrey),
        ('BACKGROUND', (0, 12), (1, 12), colors.lightgrey),
        ('SPAN', (0, 10), (1, 10)),
        ('SPAN', (0, 11), (1, 11)),
        ('SPAN', (0, 12), (1, 12)),
        ('SPAN', (0, 13), (1, 13)),
    ]))
    story.append(personal_table)
    story.append(Spacer(1, 18))
    
    # Alias information section (expanded)
    story.append(Paragraph("2. Have you ever used or been known by any other name(s)? (Check one)", normal_style))
    story.append(Spacer(1, 6))
    
    alias_used = section_one.get('alias_used', '').lower()
    if alias_used == 'yes':
        story.append(Paragraph("☑ Yes    ☐ No", normal_style))
    else:
        story.append(Paragraph("☐ Yes    ☑ No", normal_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("If yes, complete the table below:", normal_style))
    story.append(Spacer(1, 6))
    
    alias_data = [
        ['Maiden/alias/former name(s)', 'Dates used (MM/YYYY - MM/YYYY)'],
        [safe_str(section_one.get('alias_first_name', '') + ' ' + section_one.get('alias_last_name', '')).strip(), safe_str(section_one.get('alias_dates'))],
        ['', ''],
        ['', '']
    ]
    
    alias_table = Table(alias_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=[0.4*inch, 0.6*inch, 0.6*inch, 0.6*inch])
    alias_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
    ]))
    story.append(alias_table)
    story.append(Spacer(1, 24))
    
    # Page break before criminal history
    story.append(PageBreak())
    
    # PAGE 3 - Section 2: Criminal History (Expanded)
    story.append(Paragraph("<b>Section 2: Criminal History</b>", heading_style))
    story.append(Paragraph("2. Complete the following for each case you are seeking a pardon for (attach additional sheets for multiple crimes):", normal_style))
    story.append(Spacer(1, 12))
    
    section_two = session.get('section_two', {})
    
    # Criminal history table matching official format (expanded)
    criminal_data = [
        ['Crime/Charge', 'Case number'],
        [safe_str(section_two.get('crime')), safe_str(section_two.get('case_number'))],
        ['Court (include county)', 'Sentencing date (MM/DD/YYYY)'],
        [safe_str(section_two.get('court')), safe_str(section_two.get('sentencing_date'))],
        ['Sentencing judge', 'Sentence imposed'],
        [safe_str(section_two.get('judge')), safe_str(section_two.get('sentence'))],
        ['Start of sentence (MM/DD/YYYY)', 'End of sentence (MM/DD/YYYY)'],
        [safe_str(section_two.get('sentence_start')), safe_str(section_two.get('sentence_end'))],
        ['Type of supervision after release', 'Supervising agent/officer name'],
        [safe_str(section_two.get('supervision_type')), safe_str(section_two.get('agent_name'))],
        ['Start of supervision (MM/DD/YYYY)', 'End of supervision (MM/DD/YYYY)'],
        [safe_str(section_two.get('supervision_start')), safe_str(section_two.get('supervision_end'))]
    ]
    
    criminal_table = Table(criminal_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=[0.4*inch]*len(criminal_data))
    criminal_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 2), (1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 4), (1, 4), colors.lightgrey),
        ('BACKGROUND', (0, 6), (1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 8), (1, 8), colors.lightgrey),
        ('BACKGROUND', (0, 10), (1, 10), colors.lightgrey),
    ]))
    story.append(criminal_table)
    story.append(Spacer(1, 18))
    
    # Additional crimes section
    story.append(Paragraph("3. Are you seeking a pardon for additional crimes? (Check one)", normal_style))
    story.append(Spacer(1, 6))
    additional_crimes = section_two.get('additional_crimes', '')
    if additional_crimes.lower() == 'yes':
        story.append(Paragraph("☑ Yes (attach additional sheets)    ☐ No", normal_style))
    else:
        story.append(Paragraph("☐ Yes (attach additional sheets)    ☑ No", normal_style))
    story.append(Spacer(1, 18))
    
    # Criminal record questions
    story.append(Paragraph("4. Do you have any other criminal convictions (including juvenile adjudications) not covered above? (Check one)", normal_style))
    story.append(Spacer(1, 6))
    other_records = section_two.get('other_records', '')
    if other_records.lower() == 'yes':
        story.append(Paragraph("☑ Yes    ☐ No", normal_style))
    else:
        story.append(Paragraph("☐ Yes    ☑ No", normal_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("If yes, explain:", normal_style))
    story.append(Spacer(1, 6))
    
    # Text box for other records explanation
    other_records_data = [['', '', ''], ['', '', ''], ['', '', '']]
    other_records_table = Table(other_records_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch], rowHeights=[0.5*inch, 0.5*inch, 0.5*inch])
    other_records_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (2, 1)),
        ('SPAN', (0, 2), (2, 2)),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    if other_records.lower() == 'yes':
        other_records_table = Table([[safe_str(section_two.get('other_records_explanation', ''))], [''], ['']], colWidths=[7.5*inch], rowHeights=[0.5*inch, 0.5*inch, 0.5*inch])
        other_records_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
    story.append(other_records_table)
    story.append(Spacer(1, 24))
    
    # Page break before next section
    story.append(PageBreak())
    
    # PAGE 4 - Section 3: Employment History
    story.append(Paragraph("<b>Section 3: Employment History</b>", heading_style))
    story.append(Paragraph("5. List your employment history for the past 10 years (start with most recent):", normal_style))
    story.append(Spacer(1, 12))
    
    section_three = session.get('section_three', {})
    
    # Employment history table
    employment_data = [
        ['Employer name and address', 'Position/Job title', 'Start date (MM/YYYY)', 'End date (MM/YYYY)'],
        [safe_str(section_three.get('employer_1_name', '') + '\n' + section_three.get('employer_1_address', '')), safe_str(section_three.get('position_1')), safe_str(section_three.get('start_date_1')), safe_str(section_three.get('end_date_1'))],
        [safe_str(section_three.get('employer_2_name', '') + '\n' + section_three.get('employer_2_address', '')), safe_str(section_three.get('position_2')), safe_str(section_three.get('start_date_2')), safe_str(section_three.get('end_date_2'))],
        [safe_str(section_three.get('employer_3_name', '') + '\n' + section_three.get('employer_3_address', '')), safe_str(section_three.get('position_3')), safe_str(section_three.get('start_date_3')), safe_str(section_three.get('end_date_3'))],
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', '']
    ]
    
    employment_table = Table(employment_data, colWidths=[2.5*inch, 2*inch, 1.5*inch, 1.5*inch], rowHeights=[0.6*inch]*len(employment_data))
    employment_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (3, 0), colors.lightgrey),
    ]))
    story.append(employment_table)
    story.append(Spacer(1, 18))
    
    # Current employment status
    story.append(Paragraph("6. What is your current employment status? (Check one)", normal_style))
    story.append(Spacer(1, 6))
    
    employment_status = section_three.get('employment_status', '')
    status_options = {
        'employed_full': '☑ Employed full-time',
        'employed_part': '☐ Employed part-time', 
        'self_employed': '☐ Self-employed',
        'unemployed': '☐ Unemployed',
        'retired': '☐ Retired',
        'disabled': '☐ Disabled',
        'student': '☐ Student'
    }
    
    for key, option in status_options.items():
        if employment_status == key:
            option = option.replace('☐', '☑')
        story.append(Paragraph(option, normal_style))
    
    story.append(Spacer(1, 18))
    
    # Page break before education section
    story.append(PageBreak())
    
    # PAGE 5 - Section 4: Education
    story.append(Paragraph("<b>Section 4: Education</b>", heading_style))
    story.append(Paragraph("7. What is the highest grade you completed in school?", normal_style))
    story.append(Spacer(1, 6))
    
    section_four = session.get('section_four', {})
    
    # Education level checkboxes
    education_level = section_four.get('education_level', '')
    education_options = [
        ('elementary', 'Elementary school'),
        ('middle', 'Middle school/Junior high'),
        ('some_high', 'Some high school'),
        ('high_school', 'High school diploma/GED'),
        ('some_college', 'Some college'),
        ('associates', "Associate's degree"),
        ('bachelors', "Bachelor's degree"),
        ('masters', "Master's degree"),
        ('doctorate', 'Doctorate/Professional degree')
    ]
    
    for key, option in education_options:
        if education_level == key:
            story.append(Paragraph(f"☑ {option}", normal_style))
        else:
            story.append(Paragraph(f"☐ {option}", normal_style))
    
    story.append(Spacer(1, 18))
    
    # Post-conviction education
    story.append(Paragraph("8. Have you received any education, training, or certificates after your conviction? (Check one)", normal_style))
    story.append(Spacer(1, 6))
    
    post_education = section_four.get('post_education', '')
    if post_education.lower() == 'yes':
        story.append(Paragraph("☑ Yes    ☐ No", normal_style))
    else:
        story.append(Paragraph("☐ Yes    ☑ No", normal_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("If yes, describe:", normal_style))
    story.append(Spacer(1, 6))
    
    # Text box for post-conviction education
    post_edu_table = Table([[safe_str(section_four.get('post_education_details', ''))], [''], ['']], colWidths=[7.5*inch], rowHeights=[0.6*inch, 0.6*inch, 0.6*inch])
    post_edu_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(post_edu_table)
    story.append(Spacer(1, 24))
    
    # Page break before community service
    story.append(PageBreak())
    
    # PAGE 6 - Section 5: Community Service and Personal Growth
    story.append(Paragraph("<b>Section 5: Community Service and Personal Growth</b>", heading_style))
    story.append(Paragraph("9. Describe any volunteer work, community service, or other activities you have participated in since your conviction:", normal_style))
    story.append(Spacer(1, 12))
    
    section_five = session.get('section_five', {})
    
    # Community service text box
    community_service_table = Table([[safe_str(section_five.get('community_service', ''))], [''], [''], ['']], colWidths=[7.5*inch], rowHeights=[0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    community_service_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(community_service_table)
    story.append(Spacer(1, 18))
    
    # Counseling/treatment question
    story.append(Paragraph("10. Have you received any counseling, treatment, or participated in any programs since your conviction? (Check one)", normal_style))
    story.append(Spacer(1, 6))
    
    counseling = section_five.get('counseling', '')
    if counseling.lower() == 'yes':
        story.append(Paragraph("☑ Yes    ☐ No", normal_style))
    else:
        story.append(Paragraph("☐ Yes    ☑ No", normal_style))
    
    story.append(Spacer(1, 6))
    story.append(Paragraph("If yes, describe:", normal_style))
    story.append(Spacer(1, 6))
    
    # Counseling details text box
    counseling_table = Table([[safe_str(section_five.get('counseling_details', ''))], [''], ['']], colWidths=[7.5*inch], rowHeights=[0.6*inch, 0.6*inch, 0.6*inch])
    counseling_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(counseling_table)
    story.append(Spacer(1, 24))
    
    # Page break before essay questions
    story.append(PageBreak())
    
    # PAGE 7 - Section 6: Grounds for a Pardon (Essay Questions)
    story.append(Paragraph("<b>Section 6: Grounds for a Pardon</b>", heading_style))
    story.append(Paragraph("Please answer ALL questions in this section completely. Use additional pages if necessary.", normal_style))
    story.append(Spacer(1, 12))
    
    section_seven = session.get('section_seven', {})
    
    # Question 11: Crime description
    story.append(Paragraph("11. In your own words, describe in detail the crime(s) for which you are seeking a pardon. Include the circumstances that led to the crime and your role in it:", question_style))
    story.append(Spacer(1, 6))
    
    crime_description_table = Table([[safe_str(section_seven.get('personal_statement', ''))], [''], [''], [''], ['']], colWidths=[7.5*inch], rowHeights=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    crime_description_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(crime_description_table)
    story.append(Spacer(1, 18))
    
    # Page break before next question
    story.append(PageBreak())
    
    # PAGE 8 - Continued Essay Questions
    # Question 12: Why do you want a pardon?
    story.append(Paragraph("12. Why do you want or need a pardon? Be specific about how your conviction has affected your life and why a pardon would help you:", question_style))
    story.append(Spacer(1, 6))
    
    why_pardon_table = Table([[safe_str(section_seven.get('why_pardon', ''))], [''], [''], [''], ['']], colWidths=[7.5*inch], rowHeights=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    why_pardon_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(why_pardon_table)
    story.append(Spacer(1, 24))
    
    # Page break before next question
    story.append(PageBreak())
    
    # PAGE 9 - Continued Essay Questions
    # Question 13: How have you changed?
    story.append(Paragraph("13. How have you changed since your conviction? Describe the steps you have taken toward rehabilitation and how you have demonstrated that you will not commit crimes in the future:", question_style))
    story.append(Spacer(1, 6))
    
    life_changes_table = Table([[safe_str(section_seven.get('life_changes', ''))], [''], [''], [''], ['']], colWidths=[7.5*inch], rowHeights=[1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    life_changes_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    story.append(life_changes_table)
    story.append(Spacer(1, 24))
    
    # Page break before authorization section
    story.append(PageBreak())
    
    # PAGE 10 - Section 7: Notice of Pardon Application
    story.append(Paragraph("<b>Section 7: Notice of Pardon Application</b>", heading_style))
    story.append(Paragraph("You are required to send a copy of the Notice of Pardon Application to the sentencing judge and the district attorney who prosecuted your case.", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("14. I have sent the required Notice of Pardon Application to: (Check all that apply)", normal_style))
    story.append(Spacer(1, 6))
    
    section_three = session.get('section_three', {})
    notice_judge = section_three.get('notice_judge', '')
    notice_da = section_three.get('notice_da', '')
    
    if notice_judge.lower() == 'yes':
        story.append(Paragraph("☑ Sentencing judge", normal_style))
    else:
        story.append(Paragraph("☐ Sentencing judge", normal_style))
        
    if notice_da.lower() == 'yes':
        story.append(Paragraph("☑ District attorney who prosecuted my case", normal_style))
    else:
        story.append(Paragraph("☐ District attorney who prosecuted my case", normal_style))
    
    story.append(Spacer(1, 18))
    
    # Section 8: Background Check Authorization
    story.append(Paragraph("<b>Section 8: Background Check Authorization</b>", heading_style))
    bg_auth_text = (
        "By signing this application, I authorize the State of Wisconsin to conduct a background investigation, "
        "including a criminal history records check, to determine my fitness to receive a pardon. I understand "
        "that the investigation may include contact with employers, schools, law enforcement agencies, courts, "
        "and other persons and organizations with information relevant to my fitness to receive a pardon."
    )
    story.append(Paragraph(bg_auth_text, normal_style))
    story.append(Spacer(1, 18))
    
    # Section 9: Certification
    story.append(Paragraph("<b>Section 9: Certification</b>", heading_style))
    certification_text = (
        "I certify that I have read and understand this application and that the information I have provided "
        "is true and complete to the best of my knowledge. I understand that any false statements may be "
        "grounds for denial of this application or revocation of any pardon that may be granted. I understand "
        "that I must notify the Governor's office immediately if any of the information in this application changes."
    )
    story.append(Paragraph(certification_text, normal_style))
    story.append(Spacer(1, 18))
    
    # Signature lines with proper formatting
    sig_data = [
        ['Applicant signature', 'Date (MM/DD/YYYY)'],
        ['', ''],
        ['Print full name', 'Email address'],
        ['', '']
    ]
    
    sig_table = Table(sig_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=[0.4*inch, 0.8*inch, 0.4*inch, 0.8*inch])
    sig_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 2), (1, 2), colors.lightgrey),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 24))
    
    # Notary section
    story.append(Paragraph("<b>For Notary Public Use Only:</b>", heading_style))
    story.append(Spacer(1, 6))
    
    notary_text = (
        "State of Wisconsin, County of ________________<br/><br/>"
        "Sworn to (or affirmed) and subscribed before me on ________________ by the above-named applicant.<br/><br/>"
        "Signature of Notary Public: _________________________________<br/><br/>"
        "My commission expires: _______________"
    )
    story.append(Paragraph(notary_text, normal_style))
    
    # Page break for Notice to District Attorney
    story.append(PageBreak())
    
    # Notice to District Attorney of Pardon Application Page
    story.append(Paragraph("Notice to District Attorney of Pardon Application", title_style))
    story.append(Spacer(1, 12))
    
    # Instructions for District Attorney notice
    da_instructions = (
        "<b>TO THE APPLICANT:</b> Fill out the information below. Mail this form to <b>each</b> district attorney's office "
        "that oversaw your conviction. <b>Do not submit this form with your pardon application.</b> It is <b>strongly "
        "encouraged</b> that you provide the district attorney's office a copy of your application materials or a "
        "cover letter explaining why you are seeking a pardon."
    )
    story.append(Paragraph(da_instructions, normal_style))
    story.append(Spacer(1, 12))
    
    # DA Notice table
    da_table_data = [
        ['Applicant name', 'Date of birth (MM/DD/YYYY)'],
        [safe_str(f"{section_one.get('first_name', '')} {section_one.get('middle_name', '')} {section_one.get('last_name', '')}").strip(), safe_str(section_one.get('dob'))],
        ['Mailing address', 'Phone number and email address'],
        [safe_str(section_one.get('mailing_address')), safe_str(f"{section_one.get('home_phone', '')} {section_one.get('email', '')}")]
    ]
    
    da_table = Table(da_table_data, colWidths=[3.7*inch, 3.7*inch], rowHeights=[0.3*inch, 0.7*inch, 0.3*inch, 0.7*inch])
    da_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 2), (1, 2), colors.lightgrey),
    ]))
    story.append(da_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("I am seeking a pardon for the following crime(s):", normal_style))
    story.append(Spacer(1, 6))
    
    # Crime details table for DA notice
    crime_table_data = [
        ['Crime', 'Court case number', 'Sentence', 'Sentencing date (MM/DD/YYYY)'],
        [safe_str(section_two.get('crime')), safe_str(section_two.get('case_number')), safe_str(section_two.get('sentence')), safe_str(section_two.get('sentencing_date'))],
        ['', '', '', ''],
        ['', '', '', ''],
        ['', '', '', '']
    ]
    
    crime_table = Table(crime_table_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch, 1.8*inch])
    crime_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (3, 0), colors.lightgrey),
    ]))
    story.append(crime_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Pardon applicant: do not fill out anything beyond this point.</b>", normal_style))
    story.append(Spacer(1, 12))
    
    # DA response section
    da_response_text = (
        "<b>TO THE DISTRICT ATTORNEY:</b> The Governor and the Governor's Pardon Advisory Board request "
        "your opinion on whether the above-named applicant should be granted a pardon. Your support or "
        "opposition to a pardon will be given significant weight by the Governor and the Board. If you have "
        "questions, please email GOVPardons@wisconsin.gov. Thank you for your assistance."
    )
    story.append(Paragraph(da_response_text, normal_style))
    story.append(Spacer(1, 12))
    
    # DA comments table
    da_comments_data = [
        ["DA's or ADA's comments (Support / Oppose / No Opinion)"],
        [""]
    ]
    da_comments_table = Table(da_comments_data, colWidths=[7.4*inch], rowHeights=[0.3*inch, 2*inch])
    da_comments_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
    ]))
    story.append(da_comments_table)
    story.append(Spacer(1, 12))
    
    # DA signature table
    da_sig_data = [
        ["DA's/ADA's name (print)", "DA's/ADA's signature", "Date"],
        ["", "", ""]
    ]
    da_sig_table = Table(da_sig_data, colWidths=[2.4*inch, 2.5*inch, 2.5*inch], rowHeights=[0.3*inch, 0.5*inch])
    da_sig_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (2, 0), colors.lightgrey),
    ]))
    story.append(da_sig_table)
    story.append(Spacer(1, 12))
    
    # Final instructions
    final_instructions = (
        "Please send the completed original form to Office of the Governor, Attn: Pardon Advisory Board, P.O. "
        "Box 7863, Madison, WI 53707 <i>or</i> GOVPardons@wisconsin.gov, and a copy to the applicant at the "
        "mailing address or email address listed above."
    )
    story.append(Paragraph(final_instructions, normal_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Page 11", small_style))
    
    doc.build(story)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    buffer.close()
    
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Wisconsin_Pardon_Application_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response

@app.route("/application_complete")
def application_complete():
    required_sections = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', 'section_seven']
    for section in required_sections:
        if section not in session:
            return redirect(url_for('home'))
    
    return render_template("application_complete.html")

if __name__ == '__main__':
    # The `debug=True` flag is great for local development.
    # The `IS_DEVELOPMENT` flag we set above will control the JSON logging.
    app.run(debug=True)
