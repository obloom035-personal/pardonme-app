from flask import Flask, render_template, request, redirect, session, url_for, make_response, send_file, jsonify
from werkzeug.utils import secure_filename
import json
import os
import io
from datetime import datetime
import pdf_service
from field_help_texts import get_help_text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available. Install with 'pip install openai' for AI features.")

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

@app.route("/application_complete")
def application_complete():
    required_sections = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', 'section_seven']
    for section in required_sections:
        if section not in session:
            return redirect(url_for('home'))
    
    return render_template("application_complete.html")

@app.route("/generate_pdf")
def generate_pdf():
    # Validate all sections are complete
    required_sections = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', 'section_seven']
    for section in required_sections:
        if section not in session:
            return redirect(url_for('section_one'))
    
    try:
        # Generate PDF using pdf_service
        pdf_bytes = pdf_service.generate_completed_pdf(session)
        
        # Return as downloadable file
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name='completed_pardon_application.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        # Handle PDF generation errors gracefully
        return f"Error generating PDF: {str(e)}", 500

# AI Integration Routes

@app.route('/get_field_help/<field_name>', methods=['GET'])
def get_field_help(field_name):
    """
    Get help text for a specific field name.
    Returns JSON with help text content for tooltips.
    """
    try:
        help_text = get_help_text(field_name)
        return jsonify({
            'success': True,
            'field_name': field_name,
            'help_text': help_text
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error retrieving help text: {str(e)}'
        }), 500

@app.route('/ai_help', methods=['POST'])
def ai_help():
    """
    AI Legal Assistant endpoint.
    Receives user input and session context, returns AI feedback and improved version.
    """
    if not OPENAI_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'AI features are not available. OpenAI library not installed.'
        }), 503
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        user_input = data.get('user_input', '').strip()
        field_name = data.get('field_name', '')
        
        # Validate input
        if not user_input or len(user_input) < 10:
            return jsonify({
                'success': False,
                'error': 'Please provide more detailed input (at least 10 characters)'
            }), 400
        
        if not field_name:
            return jsonify({
                'success': False,
                'error': 'Field name is required'
            }), 400
        
        # Get session context (sanitized for AI)
        session_context = {}
        for key, value in session.items():
            # Only include relevant form data, exclude sensitive information
            if isinstance(value, (str, int, float)) and not key.startswith('_'):
                if len(str(value)) < 200:  # Limit context size
                    session_context[key] = value
        
        # Set up OpenAI API key
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if not openai_api_key:
            return jsonify({
                'success': False,
                'error': 'AI service temporarily unavailable - API key not configured'
            }), 503
        
        # Configure OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Create AI prompt
        prompt = f"""You are an AI legal assistant helping someone complete a Wisconsin pardon application.

Field being completed: {field_name}
User's current response: "{user_input}"

Session context (other information they've provided):
{json.dumps(session_context, indent=2)}

Please provide:
1. Constructive feedback on their current response
2. An improved/rewritten version that would be more effective

Focus on:
- Demonstrating rehabilitation and personal growth
- Showing accountability and remorse
- Highlighting positive contributions to society
- Using appropriate tone for legal documents
- Being specific and detailed where helpful

Respond in JSON format:
{{
    "feedback": "Your constructive feedback here",
    "improved_version": "Your improved/rewritten version here"
}}"""
        
        # Make API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant specializing in Wisconsin pardon applications. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse AI response
        ai_response_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON response from AI
        try:
            ai_data = json.loads(ai_response_text)
            feedback = ai_data.get('feedback', 'No feedback provided')
            improved_version = ai_data.get('improved_version', user_input)
        except json.JSONDecodeError:
            # Fallback if AI doesn't return valid JSON
            feedback = "I've reviewed your response. Consider being more specific about your actions, showing accountability, and highlighting positive changes you've made."
            improved_version = user_input
        
        return jsonify({
            'success': True,
            'field_name': field_name,
            'original_input': user_input,
            'feedback': feedback,
            'improved_version': improved_version
        })
        
    except openai.APIError as e:
        return jsonify({
            'success': False,
            'error': f'AI service error: {str(e)}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # The `debug=True` flag is great for local development.
    # The `IS_DEVELOPMENT` flag we set above will control the JSON logging.
    app.run(debug=True)
