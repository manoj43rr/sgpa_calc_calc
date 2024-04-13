import streamlit as st
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class SGPA_Calculator:
    def __init__(self):
        self.subjects_sem1 = [
            ("18MAT11", 4), ("18CHE12", 4), ("18CPS13", 3), ("18ELN14", 3),
            ("18ME15", 3), ("18CHEL16", 1), ("18CPL17", 1), ("18EGH18", 1)
        ]
        self.subjects_sem2 = [
            ("18MAT21", 4), ("18PHY22", 4), ("18ELE23", 3), ("18CIV24", 3),
            ("18EGDL25", 3), ("18PHYL26", 1), ("18ELEL27", 1), ("18EGH28", 1)
        ]
        self.subjects_sem3 = [
            ("18MAT31", 3), ("18CS32", 4), ("18CS33", 3), ("18CS34", 3),
            ("18CS35", 3), ("18CS36", 3), ("18CSL37", 2), ("18CSL38", 2), ("18CPC39", 1)
        ]
        self.subjects_sem4 = [
            ("18MAT41", 3), ("18CS42", 4), ("18CS43", 3), ("18CS44", 3),
            ("18CS45", 3), ("18CS46", 3), ("18CSL47", 2), ("18CSL48", 2), ("18CPC49", 1)
        ]
        self.subjects_sem5 = [
            ("18CS51", 3), ("18AI52", 4), ("18CS53", 4), ("18CS54", 3),
            ("18AI55", 3), ("18AD56", 3), ("18AIL57", 2), ("18CSL58", 2), ("18CIV59", 1)
        ]
        self.subjects_sem6 = [
            ("18AI61", 4), ("18AD62", 4), ("18AI63", 4), ("18ME653", 3),
            ("18AI643", 3), ("18AIL66", 2), ("18ADL67", 2), ("18ADMP68", 2)
        ]
        self.subjects_sem7 = [
            ("18ME751", 3), ("18AI731", 3), ("18AI71", 4), ("18AD72", 4),
            ("18AI744", 3), ("18ADL76", 1), ("18ADP77", 2)
        ]
        self.subjects_sem8 = [
            ("18AD81", 3), ("18AI822", 3), ("18ADP83", 8), ("18ADS84", 1), ("18ADI85", 3)
        ]

    def save_pdf(self, data, sgpa):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Define custom styles
        style_heading = styles["Heading1"]
        style_body = ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontSize=12,
            leading=14,
            spaceAfter=12
        )

        elements = []

        # Add title
        title = Paragraph("<b>SGPA Calculation Report</b>", style_heading)
        elements.append(title)

        # Add table to PDF
        table_data = [["Subject Name", "Subject Credits", "Grade Points", "Credits Earned"]] + data[1:]
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)

        # Add SGPA to PDF
        sgpa_text = f"<b>SGPA:</b> {sgpa:.2f}"
        sgpa_paragraph = Paragraph(sgpa_text, style_body)
        elements.append(sgpa_paragraph)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    def get_binary_file_downloader_html(self, bin_data, file_label='File'):
        bin_str = base64.b64encode(bin_data.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="grade_table.pdf">{file_label}</a>'
        return href

    def calculate_grade_points(self, marks):
        if marks >= 90:
            return 10
        elif 80 <= marks <= 89:
            return 9
        elif 70 <= marks <= 79:
            return 8
        elif 60 <= marks <= 69:
            return 7
        elif 50 <= marks <= 59:
            return 6
        elif 45 <= marks <= 49:
            return 5
        elif 40 <= marks <= 44:
            return 4
        else:
            return 0

    def calculate_sgpa_and_generate_table(self, subjects):
        total_credits = sum(credit for _, credit in subjects)
        subject_marks = {}
        subject_grade_points = {}

        for subject, credits in subjects:
            subject_marks[subject] = st.number_input(f"{subject} Marks:", min_value=0, max_value=100, step=1, key=subject, format="%d")
            subject_grade_points[subject] = self.calculate_grade_points(subject_marks[subject])

        data = [["Subject Name", "Subject Credits", "Grade Points", "Credits Earned"]]
        total_credits_earned = 0

        for subject, credits in subjects:
            credit_earned = subject_grade_points[subject] * credits
            data.append([subject, credits, subject_grade_points[subject], credit_earned])
            total_credits_earned += credit_earned

        sgpa = total_credits_earned / total_credits

        return data, sgpa

class CGPA_Calculator:
    def _init_(self):
        self.sem_credits = [(1, 20), (2, 20), (3, 24), (4, 24), (5, 25), (6, 24), (7, 20), (8, 18)]

    def calculate_cgpa(self, n_sem, sem_credits_earned):
        total_credits = sum(credit for _, credit in sem_credits_earned[:n_sem])
        total_final_credits_earned = sum(sem_credits_earned[i][1] for i in range(n_sem))
        cgpa = total_final_credits_earned / total_credits
        return cgpa

def main():
    
    st.title("CGPA and SGPA Calculator")

    option = st.radio("Choose Calculator:", ["SGPA Calculator for all Semesters", "CGPA Calculator"])

    if option == "SGPA Calculator for all Semesters":
        sgpa_calc = SGPA_Calculator()
        semester_selection = st.selectbox("Select Semester:", ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8"])

        if semester_selection == "Semester 1":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem1)
        elif semester_selection == "Semester 2":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem2)
        elif semester_selection == "Semester 3":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem3)
        elif semester_selection == "Semester 4":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem4)
        elif semester_selection == "Semester 5":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem5)
        elif semester_selection == "Semester 6":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem6)
        elif semester_selection == "Semester 7":
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem7)
        else:  # Semester 8
            data, sgpa = sgpa_calc.calculate_sgpa_and_generate_table(sgpa_calc.subjects_sem8)

        st.write("<div class='container'>", unsafe_allow_html=True)
        st.write("<h1>Enter marks for the following subjects:</h1>", unsafe_allow_html=True)
        st.table(data)
        st.info('⚠ Note: Total credits earned refer to the sum of credits obtained in all semesters. You\'ll need this value to calculate the CGPA.')

        st.write(f"<h2>Total Credits Earned: {sum([row[3] for row in data[1:]])}</h2>", unsafe_allow_html=True)

        if st.button("Calculate SGPA", key="calculate", help="Calculate SGPA"):
            st.write("<div class='result-container'>", unsafe_allow_html=True)
            st.write(f"<h2>SGPA: {sgpa:.2f}</h2>", unsafe_allow_html=True)
            st.write("</div>", unsafe_allow_html=True)

            pdf_buffer = sgpa_calc.save_pdf(data, sgpa)
            st.markdown(sgpa_calc.get_binary_file_downloader_html(pdf_buffer, "Table as PDF"), unsafe_allow_html=True)
            st.balloons()
        st.write("</div>", unsafe_allow_html=True)

    elif option == "CGPA Calculator":
        cgpa_calc = CGPA_Calculator()
        num_semesters = len(cgpa_calc.sem_credits)

        num_sem_input = st.slider("Enter the number of semesters you want to calculate CGPA for:", min_value=1, max_value=num_semesters, value=1, step=1)

        sem_credits_earned = []
        for i in range(num_sem_input):
            sem_num = st.number_input(f"Enter credits earned for Semester {i+1}:", min_value=0, max_value=300, step=1)
            sem_credits_earned.append((i+1, sem_num))

        if st.button("Calculate CGPA"):
            total_credits = sum(credit for _, credit in cgpa_calc.sem_credits[:num_sem_input])
            total_final_credits_earned = sum(credit for _, credit in sem_credits_earned)
            cgpa = total_final_credits_earned / total_credits
            st.title(f"CGPA for {num_sem_input} semesters: {cgpa:.2f}")
            st.balloons()      



if __name__ == "__main__":
    main()
