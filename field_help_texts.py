# Field Help Texts Configuration
# This file contains all help text content for form field tooltips
# Used by the /get_field_help/<field_name> endpoint

FIELD_HELP_TEXTS = {
    # Section 2: Criminal History
    "previous_pardon_details": "If you have previously applied for a pardon in Wisconsin or any other state, provide details including when you applied, the outcome, and any relevant case numbers. If this is your first pardon application, simply write 'None' or 'This is my first pardon application.'",
    
    "other_law_enforcement_details": "Describe any interactions with law enforcement that did not result in charges or convictions. This includes arrests without prosecution, citations, traffic violations, or any other police encounters. Be honest and complete - background checks will reveal these interactions.",
    
    "other_crimes_details": "Provide information about any restraining orders, protective orders, or injunctions that have been issued against you. Include the date, jurisdiction, and current status. If none apply, write 'None.'",
    
    # Section 3: Grounds for Pardon
    "sentence_details": "Provide a detailed explanation of the crime(s) for which you are seeking a pardon. Include what happened, your role, and why you committed the offense. Take responsibility and show understanding of the impact. This is your opportunity to provide context and demonstrate accountability.",
    
    # Section 4: Employment & Education
    "education_since_conviction": "List any education, training, or skill development you have completed since your conviction. Include formal education (GED, college courses), vocational training, certifications, workshops, or self-improvement programs. Show how you've invested in personal growth and development.",
    
    # Section 5: Community Involvement
    "volunteer_work": "Describe your military service if applicable, including branch, years served, type of discharge, and any honors or commendations received. Military service demonstrates commitment to serving your country and can be a strong factor in pardon consideration.",
    
    "community_service": "Detail your volunteer work and community service activities. Include organization names, dates, hours contributed, and the type of work performed. Show ongoing commitment to giving back to your community and helping others.",
    
    "counseling_participation": "Describe any counseling, therapy, treatment programs, or support groups you have participated in. Include substance abuse treatment, anger management, mental health counseling, or other programs that address issues related to your offense. Show commitment to addressing underlying problems.",
    
    # Additional rehabilitation fields for Section 5
    "rehabilitation_steps": "Describe other steps you have taken toward rehabilitation and personal improvement. This might include lifestyle changes, new relationships, career development, spiritual growth, or other positive changes in your life since your conviction.",
    
    # Section 6: References (if needed)
    "reference_relationship": "Describe how you know this reference and for how long. Explain their role in your life and why they are qualified to speak to your character and rehabilitation.",
    
    # Section 7: Essays and Final Information
    "rehabilitation_demonstration": "Explain how you have demonstrated rehabilitation and positive change since your conviction. Provide specific examples of how you have grown as a person, contributed to society, and shown that you pose no risk to public safety.",
    
    "pardon_reasons": "Explain why you are seeking a pardon and how it would benefit you. Be specific about opportunities that are currently blocked by your conviction (employment, housing, professional licensing, etc.) and how a pardon would help you continue contributing positively to society.",
    
    # General form fields
    "current_address": "Provide your complete current residential address including street address, city, state, and ZIP code. This must be your actual residence where you can be reached.",
    
    "phone_number": "Provide a reliable phone number where you can be reached during business hours. Include area code.",
    
    "email_address": "Provide a current email address that you check regularly. This will be used for official correspondence regarding your application.",
    
    "employer_name": "Provide the full legal name of your current employer. If self-employed, write 'Self-employed' and include your business name if applicable.",
    
    "employer_address": "Provide the complete business address of your employer including street address, city, state, and ZIP code.",
    
    "job_title": "Provide your official job title or position. Be specific about your role and responsibilities.",
    
    "employment_start_date": "Provide the date you started your current employment in MM/DD/YYYY format.",
    
    "supervisor_name": "Provide the name of your direct supervisor or manager who can verify your employment.",
    
    "work_phone": "Provide the main phone number for your workplace where your employment can be verified.",
    
    # Court and legal information
    "court_name": "Provide the full name of the court where you were convicted. Include the county and state if not in Wisconsin.",
    
    "case_number": "Provide the complete case number from your conviction. This can usually be found on court documents or judgments.",
    
    "conviction_date": "Provide the exact date of your conviction in MM/DD/YYYY format. This is the date you were found guilty or pled guilty, not the sentencing date.",
    
    "sentence_imposed": "Describe the complete sentence that was imposed, including prison time, probation, fines, restitution, and any other conditions. Be specific about the length and terms.",
    
    "sentence_completion_date": "Provide the date you completed all aspects of your sentence including prison time, probation, parole, and payment of all fines and restitution.",
    
    # Personal information
    "date_of_birth": "Provide your date of birth in MM/DD/YYYY format. This must match your official identification documents.",
    
    "social_security": "Provide your complete Social Security number. This is required for background check purposes and will be kept confidential.",
    
    "drivers_license": "Provide your current driver's license number and the state that issued it. If you don't have a driver's license, provide your state ID number.",
    
    # Default help text for unmapped fields
    "default": "Please provide accurate and complete information for this field. Be honest and thorough in your response."
}

def get_help_text(field_name):
    """
    Get help text for a specific field name.
    Returns default help text if field is not found.
    """
    return FIELD_HELP_TEXTS.get(field_name, FIELD_HELP_TEXTS["default"])
