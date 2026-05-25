import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import os
from utils.data_processing import get_class_stats



st.title("📄 Generate Reports")

def create_pdf_report(df, stats):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Student Performance Analytics Report", ln=1, align='C')
    pdf.ln(10)
    
    # Overall Stats
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Class Summary", ln=1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Total Students: {stats.get('total_students', 0)}", ln=1)
    pdf.cell(200, 10, f"Class Average: {stats.get('avg_percentage', 0):.2f}%", ln=1)
    pdf.cell(200, 10, f"Pass Rate: {stats.get('pass_rate', 0):.1f}%", ln=1)
    pdf.ln(10)
    
    # Top 5 Students
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Top 5 Students", ln=1)
    pdf.set_font("Arial", '', 10)
    
    top_5 = df.nlargest(5, "Percentage")
    for index, row in top_5.iterrows():
        pdf.cell(200, 8, f"{row['Name']} ({row['Roll No']}) - {row['Percentage']}% - Grade {row['Grade']}", ln=1)
        
    pdf.ln(10)
    
    # Bottom 5 Students (Risk)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Students Needing Attention", ln=1)
    pdf.set_font("Arial", '', 10)
    
    bottom_5 = df.nsmallest(5, "Percentage")
    for index, row in bottom_5.iterrows():
        pdf.cell(200, 8, f"{row['Name']} ({row['Roll No']}) - {row['Percentage']}% - Grade {row['Grade']}", ln=1)
        
    # Output to file
    pdf_path = "analytics_report.pdf"
    pdf.output(pdf_path)
    return pdf_path

if st.session_state.df is not None:
    df = st.session_state.df
    stats = get_class_stats(df)
    
    st.write("Generate and download comprehensive analytics reports for the entire class or download the processed dataset.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Download Processed Data (CSV)")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_students_data.csv",
            mime="text/csv",
            type="primary"
        )
        
    with col2:
        st.subheader("📑 Generate Analytics Report (PDF)")
        if st.button("Generate PDF Report"):
            with st.spinner("Generating PDF..."):
                pdf_file_path = create_pdf_report(df, stats)
                
                with open(pdf_file_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                    
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name="Class_Analytics_Report.pdf",
                    mime="application/octet-stream",
                    type="primary"
                )
                
else:
    st.info("👈 Please load a dataset from the Dashboard first to generate reports.")
