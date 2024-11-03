# FairLend
FairLend is a Python application that helps financial institutions identify potential biases in thier lending practices. Using logistic regression, FairLend detects disparities in approval rates based on race, ethnicity, and gender, and generates a detailed PDF report with insights and recommendations.

## Features

- **Bias Analysis**: Detects approval disparities with logistic regression.
- **Automated Reporting**: Uses GPT-3.5 to generate a detailed PDF with findings and suggestions.
- **User-Friendly Interface**: Simple GUI for data upload, analysis, and report download.
- **Data Visualizations**: Includes visuals to highlight approval rates by demographic.

## Technologies Used

- **Python**: Core programming language.
- **scikit-learn** & **statsmodels**: For logistic regression modeling.
- **pandas** & **matplotlib**: For data manipulation and visualization.
- **GPT-3.5**: For generating detailed reports.
- **Tkinter** & **ReportLab**: For creating the GUI and generating PDF reports.

## Prerequisites

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/FairLend.git
   cd FairLend

2. **Set the OpenAI API key**
    ```bash
   export OPENAI_API_KEY="your_openai_api_key"
3. **Run**
    ```bash
   python main.py


