import pandas as pd

def keep_columns(df, columns_to_keep):
    #Removes all columns except the columns in columns_to_keep
    return df[columns_to_keep]
    

def exclude_entries_by_value(df, feature, value):
    #Removes rows from a DataFrame where the specified feature matches a given value.

    #Parameters:
    #- df (pd.DataFrame): The DataFrame to filter.
    #- feature (str): The name of the feature (column) to check.
    #- value: The value to remove rows for.

    
    return df[df[feature] != value]


def include_entries_by_value(df, feature, value):
    #Removes rows from a DataFrame unless the specified feature matches a given value
    return df[df[feature] == value]

def remove_na(df):
    #removes entries with blank, or null values
    return df.dropna()