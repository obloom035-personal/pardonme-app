from flask import Flask, render_template, request, redirect, session, url_for, send_file, make_response
from werkzeug.utils import secure_filename
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io

app = Flask(__name__)
# Using a placeholder for local development. This should be a real secret in production.
app.secret_key = os.environ.get("APP_SECRET_KEY", "dev-placeholder-for-local-use-only")

# This switch enables/disables features for local development vs. production.
# To enable, run in your terminal: `export FLASK_ENV=development` before `python app.py`
IS_DEVELOPMENT = os.environ.get('FLASK_ENV') == 'development' or os.environ.get('FLASK_DEBUG') == '1'

def generate_pardon_pdf(session_data):
    """Generate a comprehensive Wisconsin Pardon Application PDF from session data"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the PDF elements
    Story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.black,
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.spaceAfter = 6
    
    # Title
    Story.append(Paragraph("WISCONSIN PARDON APPLICATION", title_style))
    Story.append(Paragraph("Submitted to the Office of the Governor", styles['Normal']))
    Story.append(Spacer(1, 20))
    
    # Application date
    current_date = datetime.now().strftime("%B %d, %Y")
    Story.append(Paragraph(f"<b>Application Date:</b> {current_date}", normal_style))
    Story.append(Spacer(1, 15))
    
    # Section 1: Personal Information
    if 'section_one' in session_data:
        data = session_data['section_one']
        Story.append(Paragraph("SECTION 1: PERSONAL INFORMATION", heading_style))
        
        personal_data = [
            ['Full Name:', f"{data.get('first_name', '')} {data.get('middle_name', '')} {data.get('last_name', '')}"],
            ['Date of Birth:', data.get('dob', '')],
            ['Social Security Number:', data.get('ssn', '')],
            ['Phone Number:', data.get('home_phone', '')],
            ['Email:', data.get('email', '')],
            ['Current Address:', f"{data.get('home_address', '')} {data.get('home_apartment', '')}"],
            ['Mailing Address:', f"{data.get('mailing_address', '')} {data.get('mailing_apartment', '')}" if data.get('mailing_address') else 'Same as current address'],
            ['Race/Ethnicity:', data.get('ethnicity', '')],
            ['Gender:', data.get('gender', '')],
        ]
        
        table = Table(personal_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        Story.append(table)
        Story.append(Spacer(1, 15))
    
    # Section 2: Criminal History
    if 'section_two' in session_data:
        data = session_data['section_two']
        Story.append(Paragraph("SECTION 2: CRIMINAL HISTORY", heading_style))
        
        for offense in data.get('offenses', []):
            Story.append(Paragraph(f"<b>Crime Committed:</b> {offense.get('crime', '')}", normal_style))
            Story.append(Paragraph(f"<b>Date of Crime:</b> {offense.get('offense_date', '')}", normal_style))
            Story.append(Paragraph(f"<b>County of Conviction:</b> {offense.get('county', '')}", normal_style))
            Story.append(Paragraph(f"<b>Court Case Number:</b> {offense.get('case_number', '')}", normal_style))
            Story.append(Spacer(1, 8))
        
        if data.get('other_crimes'):
            Story.append(Paragraph(f"<b>Other Crimes:</b> {data.get('other_crimes', '')}", normal_style))
        
        Story.append(Paragraph(f"<b>Restitution Status:</b> {data.get('restitution_owed', '')}", normal_style))
        if data.get('restitution_amount'):
            Story.append(Paragraph(f"<b>Restitution Amount:</b> ${data.get('restitution_amount', '')}", normal_style))
        
        Story.append(Paragraph(f"<b>Previous Pardon Applications:</b> {data.get('previous_pardon_applied', '')}", normal_style))
        Story.append(Paragraph(f"<b>Other Law Enforcement Issues:</b> {data.get('other_law_enforcement', '')}", normal_style))
        Story.append(Spacer(1, 15))
    
    # Section 3: Sentence & Incarceration
    if 'section_three' in session_data:
        data = session_data['section_three']
        Story.append(Paragraph("SECTION 3: SENTENCE & INCARCERATION", heading_style))
        
        Story.append(Paragraph(f"<b>Original Sentence:</b> {data.get('sentence_details', '')}", normal_style))
        Story.append(Paragraph(f"<b>Actual Time Served:</b> {data.get('total_time_served', '')}", normal_style))
        Story.append(Paragraph(f"<b>Incarceration Location:</b> {data.get('incarceration_location', '')}", normal_style))
        Story.append(Paragraph(f"<b>Release Date:</b> {data.get('incarceration_end_date', '')}", normal_style))
        Story.append(Paragraph(f"<b>Probation/Parole Status:</b> {data.get('probation_details', '')}", normal_style))
        if data.get('probation_start_date'):
            Story.append(Paragraph(f"<b>Probation Start Date:</b> {data.get('probation_start_date', '')}", normal_style))
        if data.get('probation_end_date'):
            Story.append(Paragraph(f"<b>Probation End Date:</b> {data.get('probation_end_date', '')}", normal_style))
        Story.append(Spacer(1, 15))
    
    # Section 4: Employment & Education
    if 'section_four' in session_data:
        data = session_data['section_four']
        Story.append(Paragraph("SECTION 4: EMPLOYMENT & EDUCATION", heading_style))
        
        Story.append(Paragraph(f"<b>Current Employment Status:</b> {data.get('employment_status', '')}", normal_style))
        if data.get('current_employer'):
            Story.append(Paragraph(f"<b>Current Employer:</b> {data.get('current_employer', '')}", normal_style))
            Story.append(Paragraph(f"<b>Position:</b> {data.get('current_position', '')}", normal_style))
            Story.append(Paragraph(f"<b>Employment Duration:</b> {data.get('employment_duration', '')}", normal_style))
        
        Story.append(Paragraph(f"<b>Education Level:</b> {data.get('education_level', '')}", normal_style))
        if data.get('education_details'):
            Story.append(Paragraph(f"<b>Education Details:</b> {data.get('education_details', '')}", normal_style))
        
        if data.get('vocational_training'):
            Story.append(Paragraph(f"<b>Vocational Training:</b> {data.get('vocational_training', '')}", normal_style))
        Story.append(Spacer(1, 15))
    
    # Section 5: Community Involvement
    if 'section_five' in session_data:
        data = session_data['section_five']
        Story.append(Paragraph("SECTION 5: COMMUNITY INVOLVEMENT", heading_style))
        
        if data.get('volunteer_work'):
            Story.append(Paragraph(f"<b>Volunteer Work:</b> {data.get('volunteer_work', '')}", normal_style))
        if data.get('religious_involvement'):
            Story.append(Paragraph(f"<b>Religious Involvement:</b> {data.get('religious_involvement', '')}", normal_style))
        if data.get('support_groups'):
            Story.append(Paragraph(f"<b>Support Groups:</b> {data.get('support_groups', '')}", normal_style))
        if data.get('counseling_therapy'):
            Story.append(Paragraph(f"<b>Counseling/Therapy:</b> {data.get('counseling_therapy', '')}", normal_style))
        if data.get('mentoring_activities'):
            Story.append(Paragraph(f"<b>Mentoring:</b> {data.get('mentoring_activities', '')}", normal_style))
        if data.get('leadership_roles'):
            Story.append(Paragraph(f"<b>Leadership Roles:</b> {data.get('leadership_roles', '')}", normal_style))
        if data.get('civic_participation'):
            Story.append(Paragraph(f"<b>Civic Participation:</b> {data.get('civic_participation', '')}", normal_style))
        if data.get('future_goals'):
            Story.append(Paragraph(f"<b>Future Goals:</b> {data.get('future_goals', '')}", normal_style))
        Story.append(Spacer(1, 15))
    
    # Section 6: Character References
    if 'section_six' in session_data:
        data = session_data['section_six']
        Story.append(Paragraph("SECTION 6: CHARACTER REFERENCES", heading_style))
        
        for i in range(1, 4):  # References 1-3
            if data.get(f'reference_{i}_name'):
                Story.append(Paragraph(f"<b>Reference {i}:</b>", normal_style))
                Story.append(Paragraph(f"Name: {data.get(f'reference_{i}_name', '')}", normal_style))
                Story.append(Paragraph(f"Relationship: {data.get(f'reference_{i}_relationship', '')}", normal_style))
                Story.append(Paragraph(f"Phone: {data.get(f'reference_{i}_phone', '')}", normal_style))
                Story.append(Paragraph(f"Email: {data.get(f'reference_{i}_email', '')}", normal_style))
                Story.append(Paragraph(f"Years Known: {data.get(f'reference_{i}_years_known', '')}", normal_style))
                Story.append(Spacer(1, 8))
        
        if data.get('additional_references'):
            Story.append(Paragraph(f"<b>Additional References:</b> {data.get('additional_references', '')}", normal_style))
        Story.append(Spacer(1, 15))
    
    # Section 7: Statement & Signature
    if 'section_seven' in session_data:
        data = session_data['section_seven']
        Story.append(PageBreak())  # New page for statements
        Story.append(Paragraph("SECTION 7: PERSONAL STATEMENT & SIGNATURE", heading_style))
        
        if data.get('personal_statement'):
            Story.append(Paragraph("<b>Personal Statement:</b>", normal_style))
            Story.append(Paragraph(data.get('personal_statement', ''), normal_style))
            Story.append(Spacer(1, 10))
        
        if data.get('rehabilitation_efforts'):
            Story.append(Paragraph("<b>Rehabilitation Efforts:</b>", normal_style))
            Story.append(Paragraph(data.get('rehabilitation_efforts', ''), normal_style))
            Story.append(Spacer(1, 10))
        
        if data.get('future_goals'):
            Story.append(Paragraph("<b>Future Goals:</b>", normal_style))
            Story.append(Paragraph(data.get('future_goals', ''), normal_style))
            Story.append(Spacer(1, 10))
        
        if data.get('community_benefit'):
            Story.append(Paragraph("<b>Community Benefit:</b>", normal_style))
            Story.append(Paragraph(data.get('community_benefit', ''), normal_style))
            Story.append(Spacer(1, 10))
        
        if data.get('why_pardon_deserved'):
            Story.append(Paragraph("<b>Why Pardon is Deserved:</b>", normal_style))
            Story.append(Paragraph(data.get('why_pardon_deserved', ''), normal_style))
            Story.append(Spacer(1, 15))
        
        # Signature section
        Story.append(Paragraph("<b>APPLICANT SIGNATURE & VERIFICATION</b>", heading_style))
        Story.append(Paragraph(f"<b>Digital Signature:</b> {data.get('digital_signature', '')}", normal_style))
        Story.append(Paragraph(f"<b>Date:</b> {data.get('signature_date', '')}", normal_style))
        Story.append(Spacer(1, 10))
        
        # Legal acknowledgments
        Story.append(Paragraph("<b>Legal Acknowledgments:</b>", normal_style))
        acknowledgments = [
            "☑ I solemnly swear that the information provided is true and complete.",
            "☑ I understand that false information may result in denial and legal consequences.",
            "☑ I understand that a pardon provides official forgiveness but does not expunge records.",
            "☑ I have thoroughly reviewed my application and confirm accuracy.",
            "☑ I am ready to submit this Wisconsin Pardon Application."
        ]
        for ack in acknowledgments:
            Story.append(Paragraph(ack, normal_style))
    
    # Footer
    Story.append(Spacer(1, 20))
    Story.append(Paragraph("<i>This application was prepared using PardonMe, Inc. - Please ensure compliance with all Wisconsin state requirements.</i>", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
    
    # Build PDF
    doc.build(Story)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

@app.route("/")
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
        
        # Handle file uploads and checkboxes
        uploaded_files = request.files.getlist('documents[]')
        physical_docs_flags = request.form.getlist('sending_physical_docs[]')
        
        # Process uploaded files (save to uploads directory)
        file_paths = []
        for file in uploaded_files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads', filename)
                os.makedirs('uploads', exist_ok=True)
                file.save(file_path)
                file_paths.append(file_path)

        # Handle additional Wisconsin application fields
        other_crimes = request.form.get('other_crimes', '')
        other_crimes_details = request.form.get('other_crimes_details', '')
        restitution_owed = request.form.get('restitution_owed', '')
        restitution_amount = request.form.get('restitution_amount', '')
        restitution_paid = request.form.get('restitution_paid', '')
        previous_pardon_applied = request.form.get('previous_pardon_applied', '')
        previous_pardon_date = request.form.get('previous_pardon_date', '')
        previous_pardon_outcome = request.form.get('previous_pardon_outcome', '')
        other_law_enforcement = request.form.get('other_law_enforcement', '')
        other_law_enforcement_details = request.form.get('other_law_enforcement_details', '')

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
                "uploaded_files": file_paths if i == 0 else [],  # Associate files with first offense for now
                "sending_physical_docs": len(physical_docs_flags) > i
            }
            offenses.append(offense_data)

        # Create comprehensive section_two data including additional fields
        section_two_data = {
            "offenses": offenses,
            "other_crimes": other_crimes,
            "other_crimes_details": other_crimes_details,
            "restitution_owed": restitution_owed,
            "restitution_amount": restitution_amount,
            "restitution_paid": restitution_paid,
            "previous_pardon_applied": previous_pardon_applied,
            "previous_pardon_date": previous_pardon_date,
            "previous_pardon_outcome": previous_pardon_outcome,
            "other_law_enforcement": other_law_enforcement,
            "other_law_enforcement_details": other_law_enforcement_details,
            "uploaded_files": file_paths
        }

        # Save the comprehensive data to the session
        session['section_two'] = section_two_data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_two.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_two.json", "w") as f:
                json.dump(offenses, f, indent=4)

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
        # Handle sentence and incarceration data
        data = {
            "sentence_details": request.form.get("sentence_details", ""),
            "incarceration_location": request.form.get("incarceration_location", ""),
            "incarceration_start_date": request.form.get("incarceration_start_date", ""),
            "incarceration_end_date": request.form.get("incarceration_end_date", ""),
            "total_time_served": request.form.get("total_time_served", ""),
            "probation_details": request.form.get("probation_details", ""),
            "probation_start_date": request.form.get("probation_start_date", ""),
            "probation_end_date": request.form.get("probation_end_date", ""),
            "parole_details": request.form.get("parole_details", ""),
            "parole_start_date": request.form.get("parole_start_date", ""),
            "parole_end_date": request.form.get("parole_end_date", ""),
            "extended_supervision": request.form.get("extended_supervision", ""),
            "supervision_start_date": request.form.get("supervision_start_date", ""),
            "supervision_end_date": request.form.get("supervision_end_date", ""),
            "compliance_status": request.form.get("compliance_status", ""),
            "violations_occurred": request.form.get("violations_occurred", ""),
            "violation_details": request.form.get("violation_details", ""),
            "completion_certificate": request.form.get("completion_certificate", ""),
            "additional_notes": request.form.get("additional_notes", "")
        }

        # Save to session
        session['section_three'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_three.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_three.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for("section_four"))

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
        # Handle employment and education data
        data = {
            "current_employment_status": request.form.get("current_employment_status", ""),
            "current_employer": request.form.get("current_employer", ""),
            "current_job_title": request.form.get("current_job_title", ""),
            "current_start_date": request.form.get("current_start_date", ""),
            "current_salary": request.form.get("current_salary", ""),
            "current_supervisor": request.form.get("current_supervisor", ""),
            "current_supervisor_phone": request.form.get("current_supervisor_phone", ""),
            "employment_history": request.form.get("employment_history", ""),
            "unemployment_periods": request.form.get("unemployment_periods", ""),
            "unemployment_reasons": request.form.get("unemployment_reasons", ""),
            "highest_education": request.form.get("highest_education", ""),
            "education_institution": request.form.get("education_institution", ""),
            "graduation_date": request.form.get("graduation_date", ""),
            "education_since_conviction": request.form.get("education_since_conviction", ""),
            "vocational_training": request.form.get("vocational_training", ""),
            "certifications": request.form.get("certifications", ""),
            "career_goals": request.form.get("career_goals", ""),
            "employment_challenges": request.form.get("employment_challenges", ""),
            "skills_developed": request.form.get("skills_developed", ""),
            "financial_stability": request.form.get("financial_stability", "")
        }

        # Save to session
        session['section_four'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_four.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_four.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for("section_five"))

    # Render Section 4 page for a GET request
    current_section = 4
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)  # 4/7 = 57%
    return render_template("section_four.html", progress=progress, current_section=4)

@app.route("/section_five", methods=["GET", "POST"])
def section_five():
    # Prevent users from skipping ahead to this section
    if 'section_four' not in session:
        return redirect(url_for('section_four'))

    if request.method == "POST":
        # Handle community involvement data
        data = {
            "volunteer_work": request.form.get("volunteer_work", ""),
            "volunteer_organizations": request.form.get("volunteer_organizations", ""),
            "volunteer_hours": request.form.get("volunteer_hours", ""),
            "community_service": request.form.get("community_service", ""),
            "community_service_details": request.form.get("community_service_details", ""),
            "religious_involvement": request.form.get("religious_involvement", ""),
            "religious_details": request.form.get("religious_details", ""),
            "spiritual_growth": request.form.get("spiritual_growth", ""),
            "support_groups": request.form.get("support_groups", ""),
            "support_group_details": request.form.get("support_group_details", ""),
            "counseling_therapy": request.form.get("counseling_therapy", ""),
            "counseling_details": request.form.get("counseling_details", ""),
            "mentoring_others": request.form.get("mentoring_others", ""),
            "mentoring_details": request.form.get("mentoring_details", ""),
            "community_leadership": request.form.get("community_leadership", ""),
            "leadership_details": request.form.get("leadership_details", ""),
            "civic_participation": request.form.get("civic_participation", ""),
            "neighborhood_involvement": request.form.get("neighborhood_involvement", ""),
            "positive_influence": request.form.get("positive_influence", ""),
            "community_impact": request.form.get("community_impact", "")
        }

        # Save to session
        session['section_five'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_five.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_five.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for("section_six"))

    # Render Section 5 page for a GET request
    current_section = 5
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)  # 5/7 = 71%
    return render_template("section_five.html", progress=progress, current_section=5)

@app.route("/section_six", methods=["GET", "POST"])
def section_six():
    # Prevent users from skipping ahead to this section
    if 'section_five' not in session:
        return redirect(url_for('section_five'))

    if request.method == "POST":
        # Handle character references data
        data = {
            "reference_count": request.form.get("reference_count", ""),
            "reference_1_name": request.form.get("reference_1_name", ""),
            "reference_1_relationship": request.form.get("reference_1_relationship", ""),
            "reference_1_phone": request.form.get("reference_1_phone", ""),
            "reference_1_email": request.form.get("reference_1_email", ""),
            "reference_1_address": request.form.get("reference_1_address", ""),
            "reference_1_years_known": request.form.get("reference_1_years_known", ""),
            "reference_1_context": request.form.get("reference_1_context", ""),
            "reference_2_name": request.form.get("reference_2_name", ""),
            "reference_2_relationship": request.form.get("reference_2_relationship", ""),
            "reference_2_phone": request.form.get("reference_2_phone", ""),
            "reference_2_email": request.form.get("reference_2_email", ""),
            "reference_2_address": request.form.get("reference_2_address", ""),
            "reference_2_years_known": request.form.get("reference_2_years_known", ""),
            "reference_2_context": request.form.get("reference_2_context", ""),
            "reference_3_name": request.form.get("reference_3_name", ""),
            "reference_3_relationship": request.form.get("reference_3_relationship", ""),
            "reference_3_phone": request.form.get("reference_3_phone", ""),
            "reference_3_email": request.form.get("reference_3_email", ""),
            "reference_3_address": request.form.get("reference_3_address", ""),
            "reference_3_years_known": request.form.get("reference_3_years_known", ""),
            "reference_3_context": request.form.get("reference_3_context", ""),
            "additional_references": request.form.get("additional_references", ""),
            "reference_letters_included": request.form.get("reference_letters_included", ""),
            "reference_contact_permission": request.form.get("reference_contact_permission", ""),
            "character_statement": request.form.get("character_statement", ""),
            "personal_growth": request.form.get("personal_growth", ""),
            "support_system": request.form.get("support_system", "")
        }

        # Handle file uploads for reference letters
        uploaded_files = []
        if 'reference_letters' in request.files:
            files = request.files.getlist('reference_letters')
            for file in files:
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join('uploads', filename)
                    os.makedirs('uploads', exist_ok=True)
                    file.save(filepath)
                    uploaded_files.append(filename)
        
        data['uploaded_reference_letters'] = uploaded_files

        # Handle checkboxes for reference contact permission
        reference_contact_checkboxes = request.form.getlist('reference_contact_permission[]')
        data['reference_contact_permission_list'] = reference_contact_checkboxes

        # Save to session
        session['section_six'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_six.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_six.json", "w") as f:
                json.dump(data, f, indent=4)

        return redirect(url_for("section_seven"))

    # Render Section 6 page for a GET request
    current_section = 6
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)  # 6/7 = 86%
    return render_template("section_six.html", progress=progress, current_section=6)

@app.route("/section_seven", methods=["GET", "POST"])
def section_seven():
    # Prevent users from skipping ahead to this section
    if 'section_six' not in session:
        return redirect(url_for('section_six'))

    if request.method == "POST":
        # Handle statement and signature data
        data = {
            "personal_statement": request.form.get("personal_statement", ""),
            "rehabilitation_efforts": request.form.get("rehabilitation_efforts", ""),
            "future_goals": request.form.get("future_goals", ""),
            "impact_on_victims": request.form.get("impact_on_victims", ""),
            "community_benefit": request.form.get("community_benefit", ""),
            "lessons_learned": request.form.get("lessons_learned", ""),
            "personal_responsibility": request.form.get("personal_responsibility", ""),
            "why_pardon_deserved": request.form.get("why_pardon_deserved", ""),
            "additional_information": request.form.get("additional_information", ""),
            "oath_acknowledgment": request.form.get("oath_acknowledgment", ""),
            "information_accuracy": request.form.get("information_accuracy", ""),
            "legal_consequences_understanding": request.form.get("legal_consequences_understanding", ""),
            "digital_signature": request.form.get("digital_signature", ""),
            "signature_date": request.form.get("signature_date", ""),
            "application_review_completed": request.form.get("application_review_completed", ""),
            "submit_application": request.form.get("submit_application", "")
        }

        # Handle file uploads for additional supporting documents
        uploaded_files = []
        if 'supporting_documents' in request.files:
            files = request.files.getlist('supporting_documents')
            for file in files:
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    filepath = os.path.join('uploads', filename)
                    os.makedirs('uploads', exist_ok=True)
                    file.save(filepath)
                    uploaded_files.append(filename)
        
        data['uploaded_supporting_documents'] = uploaded_files

        # Save to session
        session['section_seven'] = data

        # If in development mode, write to JSON for debugging
        if IS_DEVELOPMENT:
            print("DEV MODE: Writing to logs/section_seven.json for debugging...")
            os.makedirs("logs", exist_ok=True)
            with open("logs/section_seven.json", "w") as f:
                json.dump(data, f, indent=4)

        # This is the final section - could redirect to a completion page
        return redirect(url_for("application_complete"))

    # Render Section 7 page for a GET request
    current_section = 7
    total_sections = 7
    progress = int(((current_section - 1) / total_sections) * 100)  # 7/7 = 100%
    return render_template("section_seven.html", progress=progress, current_section=7)

@app.route("/application_complete")
def application_complete():
    # Check if all sections are completed
    required_sections = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', 'section_seven']
    completed_sections = [section for section in required_sections if section in session]
    
    if len(completed_sections) != len(required_sections):
        return redirect(url_for('home'))
    
    # Application is complete
    return render_template("application_complete.html", completed_sections=completed_sections)

@app.route("/download_pdf")
def download_pdf():
    # Check if all sections are completed
    required_sections = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', 'section_seven']
    completed_sections = [section for section in required_sections if section in session]
    
    if len(completed_sections) != len(required_sections):
        return redirect(url_for('home'))
    
    try:
        # Generate PDF from session data
        pdf_data = generate_pardon_pdf(session)
        
        # Create response with PDF
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="Wisconsin_Pardon_Application_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        return response
        
    except Exception as e:
        # If PDF generation fails, return error page
        if IS_DEVELOPMENT:
            print(f"PDF Generation Error: {str(e)}")
        return f"<h1>Error generating PDF</h1><p>Unable to generate PDF. Please try again or contact support.</p><p><a href='/application_complete'>Go Back</a></p>", 500

if __name__ == '__main__':
    # The `debug=True` flag is great for local development.
    # The `IS_DEVELOPMENT` flag we set above will control the JSON logging.
    app.run(debug=True)


# This is a test line
# This is also a test line     