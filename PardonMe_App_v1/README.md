# PardonMe - Wisconsin Pardon Application System

A Flask web application that provides a user-friendly interface for completing the official Wisconsin State Pardon Application. The application guides users through a multi-section form process and generates a properly formatted PDF that matches the official Wisconsin pardon application format.

## 🎯 Project Overview

This application streamlines the Wisconsin pardon application process by:
- Breaking down the complex 11-page official form into manageable sections
- Providing a modern, responsive web interface
- Automatically generating a properly formatted PDF that matches the official Wisconsin pardon application
- Maintaining data persistence throughout the application process using session storage
- Including all required elements from the official form including headers, logos, and legal notices

## 📁 Project Structure

```
PardonMe_App_v1/
├── app.py                      # Main Flask application with route handlers
├── pdf_service.py              # PDF generation and form field mapping service
├── examine_pdf_fields.py       # Utility script for PDF field analysis
├── requirements.txt            # Python dependencies
├── PardonApp_Aug2021.pdf       # Official Wisconsin pardon application template
├── pdf_field_names.txt         # Reference file containing PDF form field names
├── .gitignore                  # Git ignore rules
├── static/                     # Static assets
│   ├── logo.png               # Wisconsin state logo
│   ├── styles.css             # Main stylesheet
│   ├── styles_section_*.css   # Section-specific stylesheets
│   └── forms/                 # Form-related static files
├── templates/                  # HTML templates
│   ├── home.html              # Landing page
│   ├── section_*.html         # Multi-part application form sections
│   ├── form_page*.html        # Additional form pages
│   └── application_complete.html # Completion confirmation page
├── uploads/                    # File upload storage directory
├── logs/                      # Application log files
├── __pycache__/               # Python bytecode cache
└── venv/                      # Virtual environment (if present)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd PardonMe_App_v1
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   # For development mode
   set FLASK_ENV=development
   
   # For production, set a secure secret key
   set APP_SECRET_KEY=your-secure-secret-key-here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your web browser and navigate to `http://localhost:5000`

## 💻 Usage Guide

### Application Flow

1. **Home Page** (`/`)
   - Introduction and overview of the pardon application process
   - Clear session data to start fresh

2. **Section 1: Personal Information** (`/section_one`)
   - Basic personal details (name, DOB, contact information)
   - Address information and aliases

3. **Section 2: Criminal History** (`/section_two`)
   - Detailed criminal offense information
   - Court details and case numbers
   - Sentencing information

4. **Section 3: Additional Information** (`/section_three`)
   - Supplementary personal and legal details

5. **Section 4: Employment History** (`/section_four`)
   - Current and previous employment information

6. **Section 5: Character References** (`/section_five`)
   - Personal and professional references

7. **Section 6: Essay Questions** (`/section_six`)
   - Detailed responses to required essay questions
   - Explanation of circumstances and rehabilitation

8. **Section 7: Final Details** (`/section_seven`)
   - Completion of remaining required information
   - Legal acknowledgments

9. **Application Complete** (`/application_complete`)
   - Review and confirmation page
   - PDF generation and download

### PDF Generation

The application automatically maps form data to the official Wisconsin pardon application PDF fields and generates a completed document that includes:
- Official Wisconsin state header and logo
- Properly formatted tables and sections
- All required legal notices and disclaimers
- Signature lines and certification sections

## � Recent Improvements

### PDF Generation System Overhaul (Latest)
- **Library Migration**: Migrated from pypdf to PyMuPDF (fitz) for more reliable PDF form filling
- **Field Coverage Expansion**: Increased mapped fields from ~38 to 65+ fields across all 11 pages
- **Checkbox Support**: Implemented comprehensive checkbox field mapping for yes/no questions
- **Debug Enhancement**: Added detailed debug output showing field mapping status and coverage
- **AcroForm Preservation**: Eliminated PDF corruption issues that occurred with previous pypdf implementation
- **Multi-Page Support**: Proper field updates across all pages without PDF structure corruption

### Key Technical Achievements
- ✅ **Zero PDF corruption**: Generated PDFs maintain proper AcroForm structure
- ✅ **High field coverage**: 65+ fields successfully mapped and populated
- ✅ **Checkbox functionality**: Proper selection of yes/no checkboxes throughout the form
- ✅ **Multi-instance support**: Handles multiple references, employment entries, and offense records
- ✅ **Comprehensive debugging**: Real-time field mapping analysis and success tracking
- ✅ **Data validation**: Robust filtering of empty values and proper field data formatting

### Remaining Development Goals
- [ ] Multi-row/multi-instance field mapping for additional offenses, aliases, and employers
- [ ] Generic checkbox identification and mapping (page 9 checkboxes)
- [ ] Complete field coverage for all 173+ PDF form fields
- [ ] End-to-end testing and validation of generated PDFs

## �🔧 Technical Details

### Core Technologies
- **Flask 3.1.1**: Web framework for Python
- **PyMuPDF (fitz) 1.24.14**: PDF manipulation and form filling (primary library)
- **pypdf 5.6.0**: PDF field analysis and structure examination
- **HTML5/CSS3**: Frontend user interface
- **Session Storage**: Data persistence across form sections

### Key Components

#### `app.py`
- Main Flask application file
- Contains route handlers for all sections
- Manages session data and form processing
- Handles PDF generation requests

#### `pdf_service.py`
- Core PDF processing module
- Maps form data to PDF field names
- Handles PDF template loading and form filling
- Generates final completed PDF documents

#### `examine_pdf_fields.py`
- Utility script for analyzing PDF form fields
- Used during development to identify field names
- Helps maintain accurate field mappings

### Session Management
- User data is stored in Flask sessions throughout the application process
- Sessions are cleared on the home page to ensure fresh starts
- Data persists across all form sections until completion

### CSS Architecture
- Modular CSS approach with section-specific stylesheets
- Main `styles.css` for global styles
- Individual `styles_section_*.css` files for section-specific formatting
- Responsive design principles

## 🛠️ Development Notes

### Environment Configuration
- `IS_DEVELOPMENT` flag controls development-specific features
- Debug mode enabled for local development
- Environment variables for secure production deployment

### Security Considerations
- Secret key should be set via environment variable in production
- File upload security with secure filename handling
- Session management with proper data isolation

### PDF Field Mapping
- **Comprehensive field coverage**: Maps 65+ form fields across all 11 pages of the Wisconsin pardon application
- **Intelligent field mapping**: Session data keys are precisely aligned with actual PDF field names discovered through analysis
- **Multi-type field support**: Handles text fields, checkboxes, and multi-page summary fields
- **Robust checkbox handling**: Maps yes/no session values to proper checkbox field selections
- **PyMuPDF integration**: Uses PyMuPDF (fitz) for reliable form filling without AcroForm corruption
- **Detailed debugging**: Comprehensive debug output shows field mapping status, success rates, and unmapped fields
- **Error prevention**: Filters empty values and validates field data before PDF generation
- **Field categories covered**:
  - Personal information (name, DOB, contact details, addresses)
  - Alias/maiden name fields with date ranges
  - Criminal history details (offenses, courts, sentences)
  - Employment information including phone numbers
  - Character references and contact information
  - Legal status checkboxes (restitution, previous pardons, law enforcement contacts)
  - Educational background and personal growth descriptions
  - Multi-page summary fields for application completion

### Logging
- Application logging configured for development and production
- Log files stored in `/logs` directory
- JSON logging format for structured log analysis

## 📋 Form Sections Breakdown

1. **Personal Information**: Name, DOB, contact details, addresses
2. **Criminal History**: Offense details, court information, sentences
3. **Current Status**: Legal status, supervision details
4. **Employment**: Work history, current employment
5. **References**: Character references and contact information
6. **Essays**: Required narrative responses
7. **Certifications**: Legal acknowledgments and signatures

## 🤝 Contributing

This application is designed to match the official Wisconsin pardon application exactly. Any changes should:
- Maintain compatibility with the official PDF template
- Preserve all required legal notices and formatting
- Test PDF generation thoroughly
- Follow the existing code structure and patterns

## 📝 Legal Notice

This application generates documents for submission to the State of Wisconsin Office of the Governor. Users are responsible for ensuring all information provided is accurate and truthful. The application does not provide legal advice and users should consult with legal counsel as needed.

## 🔗 Official Resources

- [Wisconsin Governor's Office - Pardons](https://govstatus.egov.com/wi-pardons)
- Official Wisconsin Pardon Application Form (included as `PardonApp_Aug2021.pdf`)

---

**Version**: 1.0  
**Last Updated**: July 2025  
**Compatibility**: Wisconsin Pardon Application (August 2021 version)
