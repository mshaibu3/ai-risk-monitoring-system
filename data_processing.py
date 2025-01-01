import pandas as pd

def load_and_clean_data(file_path):
    data = pd.read_csv(file_path)
    data.fillna(data.mean(), inplace=True)
    features = ['Age', 'Biomarker_A', 'Biomarker_B', 'Symptoms_Severity']
    target = 'Outcome'
    X = data[features]
    y = data[target]
    return X, y
