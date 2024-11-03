import pandas as pd
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm

def logistic_analysis(df):
    #This method shows if certain groups face different approval rates independent of other factors, 
    #which can reveal potential biases or inequities in the lending process.
    
    data_simple = df[['derived_ethnicity', 'derived_race', 'derived_sex', 'action_taken', 'income']]
    le_ethnicity = LabelEncoder()
    le_race = LabelEncoder()
    le_sex = LabelEncoder()
    #quantifies the categorical variables
    data_simple['derived_ethnicity'] = le_ethnicity.fit_transform(data_simple['derived_ethnicity'])
    data_simple['derived_race'] = le_race.fit_transform(data_simple['derived_race'])
    data_simple['derived_sex'] = le_sex.fit_transform(data_simple['derived_sex'])

    #define the features and target for logistic regression
    X_simple = data_simple[['derived_ethnicity', 'derived_race', 'derived_sex', 'income']]
    y_simple = data_simple['action_taken'].apply(lambda x: 1 if x == 1 else 0)

    #drops any rows with missing values in features or target
    X_simple = X_simple.dropna()
    y_simple = y_simple.loc[X_simple.index]

    #adds a constant for the intercept
    X_simple = sm.add_constant(X_simple)

    #fits the logistic regression model
    logit_model_simple = sm.Logit(y_simple, X_simple)
    result_simple = logit_model_simple.fit()

    #outputs the analysis
    summary_df = result_simple.summary2().tables[1]  # Extract the coefficient table as a DataFrame

    #creates a dictionary of the analysis
    report_data = {
    "Intercept": {
        "coefficient": summary_df.loc["const", "Coef."],
        "p_value": summary_df.loc["const", "P>|z|"]
    },
    "Ethnicity": {
        "coefficient": summary_df.loc["derived_ethnicity", "Coef."],
        "p_value": summary_df.loc["derived_ethnicity", "P>|z|"]
    },
    "Race": {
        "coefficient": summary_df.loc["derived_race", "Coef."],
        "p_value": summary_df.loc["derived_race", "P>|z|"]
    },
    "Sex": {
        "coefficient": summary_df.loc["derived_sex", "Coef."],
        "p_value": summary_df.loc["derived_sex", "P>|z|"]
    },
    "Income": {
        "coefficient": summary_df.loc["income", "Coef."],
        "p_value": summary_df.loc["income", "P>|z|"]
    }
    }
    #outputs the data into a structured text format, to be used by an LLM
    return "\n".join([f"{key}: {value}" for key, value in report_data.items()])

