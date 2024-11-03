import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tkinter as tk
from tkinter import filedialog, messagebox, Label
import os
import textwrap
import platform
import subprocess
from src.generate_report import generate_report
from src.logistic_analysis import logistic_analysis

file_path = None
pdf_filename = "mortgage_analysis_report.pdf"

#method to process the uploaded CSV file and generate PDF
def process_data(filepath):
    global pdf_filename
    try:
        
        df = pd.read_csv(filepath)
        analysis = logistic_analysis(df)  
        ai_generated_response = generate_report(analysis)  

        # Mark approvals for graphing
        df['approved'] = df['action_taken'].apply(lambda x: 1 if x == 1 else 0)

        # Start PDF with styled text using ReportLab
        doc = SimpleDocTemplate(pdf_filename, pagesize=LETTER,
                                rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="TitleStyle", parent=styles["Title"], fontSize=18, spaceAfter=12)
        body_style = styles["BodyText"]
        body_style.leading = 14  # line spacing
        header_style = ParagraphStyle(name="HeaderStyle", parent=styles["Heading2"], fontSize=14, spaceAfter=6)

        # Title
        elements.append(Paragraph("Mortgage Data Analysis", title_style))

        # Introductory Text
        intro_text = (
            "A logistic regression analysis shows whether or not there is a statistically significant "
            "difference in categorical variables, like gender, or yes-no outcomes (approved or not approved, "
            "in this instance). The model holds all variables constant, meaning that it isolates the effect "
            "of each predictor (such as race, sex, or income) on the likelihood of mortgage approval. This "
            "allows us to see if certain groups face different approval rates independently of other factors, "
            "which can reveal potential biases or inequities in the lending process."
        )
        elements.append(Paragraph(intro_text, body_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("This report will detail:", body_style))

        # Report sections
        sections = [
            "- Whether there is evidence of discriminatory lending practices based on race, ethnicity, and sex.",
            "- A comparison of the effects of race and sex to highlight which has a stronger impact on approval rates.",
            "- Potential regulatory implications, such as alignment with fair lending practices and the Equal Credit Opportunity Act (ECOA).",
            "- Recommendations for addressing any disparities identified in the analysis, including specific changes to decision-making processes or approval criteria."
        ]

        for content in sections:
            elements.append(Paragraph(content, body_style))
            elements.append(Spacer(1, 12))

        # Add Result Analysis section
        elements.append(Paragraph("Report:", header_style))
        elements.append(Paragraph(ai_generated_response, body_style))
        elements.append(Spacer(1, 12))

        # Add page break before graphs
        elements.append(PageBreak())

        # Define color palette for the graphs
        colors = ['#4B8BBE', '#F7C74A', '#D35B11']

        # Create a figure for the combined graphs stacked vertically
        fig, axes = plt.subplots(3, 1, figsize=(8, 12))

        # Function to wrap labels
        def wrap_labels(labels):
            return ['\n'.join(textwrap.wrap(str(label), width=15)) for label in labels]

        # Plot by Gender
        gender_approval = df.groupby('derived_sex')['approved'].mean().reset_index()
        axes[0].bar(gender_approval['derived_sex'], gender_approval['approved'], color=colors[:2])
        axes[0].set_title('Approval Rates by Gender', fontsize=14)
        axes[0].set_xlabel('Gender', fontsize=12)
        axes[0].set_ylabel('Approval Rate', fontsize=12)
        axes[0].set_ylim(0, 1)
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)
        axes[0].set_xticklabels(wrap_labels(gender_approval['derived_sex']), rotation=45, ha='right', fontsize=10)

        # Plot by Ethnicity
        ethnicity_approval = df.groupby('derived_ethnicity')['approved'].mean().reset_index()
        axes[1].bar(ethnicity_approval['derived_ethnicity'], ethnicity_approval['approved'], color=colors[2])
        axes[1].set_title('Approval Rates by Ethnicity', fontsize=14)
        axes[1].set_xlabel('Ethnicity', fontsize=12)
        axes[1].set_ylabel('Approval Rate', fontsize=12)
        axes[1].set_xticklabels(wrap_labels(ethnicity_approval['derived_ethnicity']), rotation=45, ha='right', fontsize=10)

        #race visualization
        race_approval = df.groupby('derived_race')['approved'].mean().reset_index()
        axes[2].bar(race_approval['derived_race'], race_approval['approved'], color=colors[0])
        axes[2].set_title('Approval Rates by Race', fontsize=14)
        axes[2].set_xlabel('Race', fontsize=12)
        axes[2].set_ylabel('Approval Rate', fontsize=12)
        axes[2].set_xticklabels(wrap_labels(race_approval['derived_race']), rotation=45, ha='right', fontsize=10)

        #save figure as image
        image_filename = "combined_income_graphs.png"
        fig.tight_layout()
        fig.savefig(image_filename, bbox_inches='tight')
        plt.close(fig)

        #adds images to PDF
        elements.append(Paragraph("Approval Rates Analysis", header_style))
        img = Image(image_filename, width=360, height=600)
        img.hAlign = "CENTER"
        elements.append(img)

        #builds the PDF
        doc.build(elements)

        #notifies completion and enable download button
        messagebox.showinfo("Success", f"PDF report '{pdf_filename}' created successfully!")
        download_button.config(state="normal")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI setup
def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        uploaded_file_label.config(text=f"A file has been uploaded! {os.path.basename(file_path)}", fg="green")
        analyze_button.config(state="normal")

def analyze_data():
    if file_path:
        process_data(file_path)
    else:
        messagebox.showwarning("Warning", "Please upload a CSV file first!")


# Create the main application window
root = tk.Tk()
root.title("Bank Data Analysis Tool")
root.geometry("800x600")
root.config(bg="#F5F5DC")

# Title label
title_label = Label(root, text="Bank Data Bias Analysis Tool", font=("Arial", 20, "bold"), bg="#F5F5DC")
title_label.pack(pady=10)

# Subtext label
subtext_label = Label(root, text="Analyze your institution's lending practices for potential bias.",
                      font=("Arial", 12), bg="#F5F5DC")
subtext_label.pack(pady=5)

# Upload button
upload_button = tk.Button(root, text="Upload CSV File", command=upload_file, bg="#D2B48C", fg="black", font=("Arial", 12, "bold"))
upload_button.pack(pady=10)

# Display label for uploaded file
uploaded_file_label = Label(root, text="", font=("Arial", 10), bg="#F5F5DC")
uploaded_file_label.pack(pady=5)

# Analyze button (initially disabled until a file is uploaded)
analyze_button = tk.Button(root, text="Analyze Data", command=analyze_data, bg="#D2B48C", fg="black", font=("Arial", 12, "bold"), state="disabled")
analyze_button.pack(pady=10)

# Download button (initially disabled until analysis is complete)
download_button = tk.Button(root, text="Download PDF Report", command=lambda: os.startfile(pdf_filename), bg="#D2B48C", fg="black", font=("Arial", 12, "bold"), state="disabled")
download_button.pack(pady=10)



# Run the main loop
root.mainloop()