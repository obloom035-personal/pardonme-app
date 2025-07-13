from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

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
        
        # NOTE: You'll also need to handle the file uploads ('documents[]') and
        # the checkbox ('sending_physical_docs[]') when you implement that logic.

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

        # Save the list of offense dictionaries to the session
        session['section_two'] = offenses

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

@app.route("/section_three")
def section_three():
    # Placeholder for the next section to prevent 404 errors on redirect
    return "<h1>Section 3 - Coming Soon!</h1><p><a href='/section_two'>Go Back</a></p>"

@app.route("/pardon_form", methods=["GET", "POST"])
@app.route("/pardon_form/<int:page>", methods=["GET", "POST"])
def pardon_form(page=1):
    if page < 1 or page > 11:
        return redirect(url_for('pardon_form', page=1))
    
    if request.method == "POST":
        if 'pardon_form_data' not in session:
            session['pardon_form_data'] = {}
        
        page_data = {}
        for key, value in request.form.items():
            if isinstance(value, list):
                page_data[key] = value
            else:
                page_data[key] = value
        
        session['pardon_form_data'][f'page_{page}'] = page_data
        
        if IS_DEVELOPMENT:
            print(f"DEV MODE: Writing pardon form page {page} data...")
            os.makedirs("logs", exist_ok=True)
            with open(f"logs/pardon_form_page_{page}.json", "w") as f:
                json.dump(page_data, f, indent=4)
        
        if page < 11:
            return redirect(url_for('pardon_form', page=page + 1))
        else:
            return redirect(url_for('generate_pardon_pdf'))
    
    current_data = {}
    if 'pardon_form_data' in session and f'page_{page}' in session['pardon_form_data']:
        current_data = session['pardon_form_data'][f'page_{page}']
    
    progress = int((page / 11) * 100)
    return render_template(f"pardon_form_page_{page}.html", 
                         page=page, 
                         progress=progress, 
                         current_data=current_data)

@app.route("/generate_pardon_pdf")
def generate_pardon_pdf():
    if 'pardon_form_data' not in session:
        return redirect(url_for('pardon_form', page=1))
    
    from weasyprint import HTML, CSS
    from flask import make_response
    
    html_content = render_template('pardon_form_pdf.html', 
                                 form_data=session['pardon_form_data'])
    
    pdf = HTML(string=html_content).write_pdf(
        stylesheets=[CSS(filename='static/pardon_form_pdf.css')]
    )
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=wisconsin_pardon_application.pdf'
    
    return response

if __name__ == '__main__':
    # The `debug=True` flag is great for local development.
    # The `IS_DEVELOPMENT` flag we set above will control the JSON logging.
    app.run(debug=True)
