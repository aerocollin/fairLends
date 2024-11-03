from openai import OpenAI
import os
def generate_report(structured_data):
    #prompt for llm to generate report
    prompt = f"""
    The following data represents the results of a logistic regression analysis on mortgage approval decisions.
    Each variable shows the coefficient and p-value in relation to the probability of approval:

    {structured_data}

    Please provide a detailed report assessing:
    1. Whether there is evidence of discriminatory lending practices based on race, ethnicity, and sex. Additionally, provide details on the methodology.
    2. A comparison of the effects of race and sex to highlight which has a stronger impact on approval rates.
    3. Potential regulatory implications, such as alignment with fair lending practices and the Equal Credit Opportunity Act (ECOA).
    4. Recommendations for addressing any disparities identified in the analysis, including specific changes to decision-making processes or approval criteria.
    Do not do anything beyond the 4 points. Additionally, use the exact values you are given to back up your claims. Also, do not list out the paragraphs.
    """
    #creates a client for API use
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    #generates the report
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    )
    #outputs the report
    return response.choices[0].message.content