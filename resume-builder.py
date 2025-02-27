import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

def main():
    st.title("Resume Builder Application")
    
    # Initialize session state for storing resume data
    if 'profile_pic' not in st.session_state:
        st.session_state.profile_pic = None
    if 'personal_info' not in st.session_state:
        st.session_state.personal_info = {}
    if 'education' not in st.session_state:
        st.session_state.education = []
    if 'work_experience' not in st.session_state:
        st.session_state.work_experience = []
    if 'skills' not in st.session_state:
        st.session_state.skills = []

    # Sidebar for navigation
    st.sidebar.title("Sections")
    sections = ["Personal Information", "Education", "Work Experience", "Skills"]
    selection = st.sidebar.radio("Go to", sections)

    if selection == "Personal Information":
        show_personal_info()
    elif selection == "Education":
        show_education()
    elif selection == "Work Experience":
        show_work_experience()
    elif selection == "Skills":
        show_skills()

    # Preview button
    if st.button("Preview Resume"):
        preview_resume()

def show_personal_info():
    st.header("Personal Information")
    
    # Add image upload
    if 'profile_pic' not in st.session_state:
        st.session_state.profile_pic = None
        
    uploaded_file = st.file_uploader("Upload Profile Picture", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        st.session_state.profile_pic = uploaded_file.read()
        st.image(st.session_state.profile_pic, width=150)
    elif st.session_state.profile_pic is not None:
        st.image(st.session_state.profile_pic, width=150)
    
    st.session_state.personal_info['full_name'] = st.text_input(
        "Full Name",
        st.session_state.personal_info.get('full_name', '')
    )
    st.session_state.personal_info['email'] = st.text_input(
        "Email",
        st.session_state.personal_info.get('email', '')
    )
    st.session_state.personal_info['phone'] = st.text_input(
        "Phone",
        st.session_state.personal_info.get('phone', '')
    )
    st.session_state.personal_info['linkedin'] = st.text_input(
        "LinkedIn URL",
        st.session_state.personal_info.get('linkedin', '')
    )
    st.session_state.personal_info['summary'] = st.text_area(
        "Professional Summary",
        st.session_state.personal_info.get('summary', '')
    )

def show_education():
    st.header("Education")
    
    if st.button("Add Education"):
        st.session_state.education.append({})
    
    for idx, edu in enumerate(st.session_state.education):
        st.subheader(f"Education #{idx+1}")
        
        edu['degree'] = st.text_input(
            "Degree",
            edu.get('degree', ''),
            key=f"edu_degree_{idx}"
        )
        edu['institution'] = st.text_input(
            "Institution",
            edu.get('institution', ''),
            key=f"edu_institution_{idx}"
        )
        edu['location'] = st.text_input(
            "Location",
            edu.get('location', ''),
            key=f"edu_location_{idx}"
        )
        edu['graduation_year'] = st.text_input(
            "Graduation Year",
            edu.get('graduation_year', ''),
            key=f"edu_grad_year_{idx}"
        )
        
        if st.button(f"Remove Education #{idx+1}"):
            st.session_state.education.pop(idx)
            st.experimental_rerun()

def show_work_experience():
    st.header("Work Experience")
    
    if st.button("Add Work Experience"):
        st.session_state.work_experience.append({})
    
    for idx, exp in enumerate(st.session_state.work_experience):
        st.subheader(f"Experience #{idx+1}")
        
        exp['title'] = st.text_input(
            "Job Title",
            exp.get('title', ''),
            key=f"exp_title_{idx}"
        )
        exp['company'] = st.text_input(
            "Company",
            exp.get('company', ''),
            key=f"exp_company_{idx}"
        )
        exp['location'] = st.text_input(
            "Location",
            exp.get('location', ''),
            key=f"exp_location_{idx}"
        )
        exp['start_date'] = st.text_input(
            "Start Date",
            exp.get('start_date', ''),
            key=f"exp_start_date_{idx}"
        )
        exp['end_date'] = st.text_input(
            "End Date",
            exp.get('end_date', ''),
            key=f"exp_end_date_{idx}"
        )
        exp['description'] = st.text_area(
            "Description",
            exp.get('description', ''),
            key=f"exp_description_{idx}"
        )
        
        if st.button(f"Remove Experience #{idx+1}"):
            st.session_state.work_experience.pop(idx)
            st.experimental_rerun()

def show_skills():
    st.header("Skills")
    
    skills_input = st.text_input(
        "Enter skills (comma-separated)",
        ",".join(st.session_state.skills) if st.session_state.skills else ""
    )
    
    if skills_input:
        st.session_state.skills = [skill.strip() for skill in skills_input.split(",")]
    
    st.write("Current Skills:", st.session_state.skills)

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Add profile picture if it exists
    if st.session_state.profile_pic is not None:
        # Save temporary image file
        temp_img_path = "temp_profile_pic.png"
        with open(temp_img_path, "wb") as f:
            f.write(st.session_state.profile_pic)
        
        # Add image to PDF
        pdf.image(temp_img_path, x=170, y=10, w=30)
        
        # Remove temporary file
        os.remove(temp_img_path)
    
    # Set font
    pdf.set_font("Arial", "B", 16)
    
    # Personal Information (adjusted x position to accommodate image)
    pdf.cell(160, 10, st.session_state.personal_info.get('full_name', ''), ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 5, f"Email: {st.session_state.personal_info.get('email', '')}", ln=True)
    pdf.cell(0, 5, f"Phone: {st.session_state.personal_info.get('phone', '')}", ln=True)
    pdf.cell(0, 5, f"LinkedIn: {st.session_state.personal_info.get('linkedin', '')}", ln=True)
    
    # Summary
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "Professional Summary", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, st.session_state.personal_info.get('summary', ''))
    
    # Education
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "Education", ln=True)
    pdf.set_font("Arial", size=10)
    for edu in st.session_state.education:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, edu.get('degree', ''), ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 5, f"{edu.get('institution', '')}, {edu.get('location', '')}", ln=True)
        pdf.cell(0, 5, f"Graduated: {edu.get('graduation_year', '')}", ln=True)
        pdf.ln(5)
    
    # Work Experience
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "Work Experience", ln=True)
    pdf.set_font("Arial", size=10)
    for exp in st.session_state.work_experience:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 5, exp.get('title', ''), ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 5, f"{exp.get('company', '')}, {exp.get('location', '')}", ln=True)
        pdf.cell(0, 5, f"{exp.get('start_date', '')} - {exp.get('end_date', '')}", ln=True)
        pdf.multi_cell(0, 5, exp.get('description', ''))
        pdf.ln(5)
    
    # Skills
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 5, "Skills", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, ", ".join(st.session_state.skills))
    
    return pdf.output(dest='S').encode('latin-1')

def preview_resume():
    st.header("Resume Preview")
    
    # Display profile picture
    if st.session_state.get('profile_pic') is not None:
        st.image(st.session_state.profile_pic, width=150)
    
    # Display personal information
    st.subheader("Personal Information")
    st.write(f"Name: {st.session_state.personal_info.get('full_name', '')}")
    st.write(f"Email: {st.session_state.personal_info.get('email', '')}")
    st.write(f"Phone: {st.session_state.personal_info.get('phone', '')}")
    st.write(f"LinkedIn: {st.session_state.personal_info.get('linkedin', '')}")
    st.write("Summary:", st.session_state.personal_info.get('summary', ''))
    
    # Display education
    st.subheader("Education")
    for edu in st.session_state.education:
        st.write(f"**{edu.get('degree', '')}**")
        st.write(f"{edu.get('institution', '')}, {edu.get('location', '')}")
        st.write(f"Graduated: {edu.get('graduation_year', '')}")
        st.write("---")
    
    # Display work experience
    st.subheader("Work Experience")
    for exp in st.session_state.work_experience:
        st.write(f"**{exp.get('title', '')}**")
        st.write(f"{exp.get('company', '')}, {exp.get('location', '')}")
        st.write(f"{exp.get('start_date', '')} - {exp.get('end_date', '')}")
        st.write(exp.get('description', ''))
        st.write("---")
    
    # Display skills
    st.subheader("Skills")
    st.write(", ".join(st.session_state.skills))

    # Add download button for PDF
    if st.button("Download PDF"):
        pdf_bytes = create_pdf()
        st.download_button(
            label="Click here to download your resume",
            data=pdf_bytes,
            file_name="resume.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
