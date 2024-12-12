import pandas as pd
import numpy as np

# Define the function to map data as given
def map_data(df):
    # Helper function for range-based mapping
    def map_ranges(value, ranges, default):
        try:
            value = float(value)
            if 0 < value < ranges[0]:
                return 1
            elif value <= ranges[1]:
                return 2
            elif value > ranges[1]:
                return 3
        except (ValueError, TypeError):
            return default

    # Apply the mappings
    df['Age'] = df['Age'].apply(lambda x: 1 if float(x) <= 60 else 2 if float(x) > 60 else 1)
    df['Gender'] = df['Gender'].apply(lambda x: 2 if str(x) == '-1' else 1 if x.lower() == 'male' else 2)
    df['Place of Habitation'] = df['Place of Habitation'].apply(lambda x: 2 if str(x) == '-1' else 1 if x.lower() == 'urban' else 2)
    df['Annual Income'] = df['Annual Income'].apply(lambda x: 1 if str(x) == '-1' else 1 if x.lower() == 'bpl' else 2)
    df['Smoking Status'] = df['Smoking Status'].apply(lambda x: 0 if str(x) == '-1' else 1 if x.lower() == 'smoker' else 0)
    df['Alcohol'] = df['Alcohol'].apply(lambda x: 0 if str(x) == '-1' else 1 if x.lower() == 'alcoholic' else 0)
    df['Tobacco Chewing Status'] = df['Tobacco Chewing Status'].apply(lambda x: 0 if str(x) == '-1' else 1 if x.lower() == 'yes' else 0)
    df['Comorbidities'] = df['Comorbidities'].apply(lambda x: 0 if str(x) == '-1' else 1 if x.lower() == 'yes' else 0)
    df['ECOG PS'] = df['ECOG PS'].apply(lambda x: 2 if pd.notna(x) and float(x) in [3, 4] else 1 if pd.notna(x) and float(x) in [0, 1, 2] else 1)
    df['BMI'] = df['BMI'].apply(lambda x: 1 if str(x) == '-1' else {'normal': 1, 'underweight': 2, 'overweight/obese': 3}[x.lower()])
    df['Bipedal Edema'] = df['Bipedal Edema'].apply(lambda x: 0 if str(x) == '-1' else 1 if x.lower() == 'yes' else 0)
    df['Site of Primary Cancer'] = df['Site of Primary Cancer'].apply(lambda x: 2 if str(x) == '-1' else 1 if x.lower() == 'hematological' else 2)
    df['Stage'] = df['Stage'].apply(lambda x: 2 if str(x) == '-1' else {'early (stage 1 &2)': 1, 'stage 3': 2, 'stage 4': 3}[x.lower()])
    df['Chemotherapy Protocol'] = df['Chemotherapy Protocol'].apply(lambda x: 2 if str(x) == '-1' else {'single agent': 1, 'doublet': 2, 'triplet': 3,'multiagent': 4}[x.lower()])
    df['Cycle Number'] = df['Cycle Number'].apply(lambda x: 2 if float(x) == '-1' else 1 if float(x) != 1 else 2)
    df['Dosing of Chemotherapy'] = df['Dosing of Chemotherapy'].apply(lambda x: 1 if str(x) == '-1' else 1 if x.lower() == 'standard' else 2)
    df['Use of Prophylactic Growth Factors'] = df['Use of Prophylactic Growth Factors'].apply(lambda x: 0 if str(x) == '-1' else 1 if x.lower() == 'yes' else 0)

    # Apply range-based mappings with updated default values
    df['Haemoglobin'] = df['Haemoglobin'].apply(lambda x: map_ranges(x, (13, 17), default=1))
    df['WBC'] = df['WBC'].apply(lambda x: map_ranges(x, (4000, 11000), default=2))
    df['Absolute Lymphocytes'] = df['Absolute Lymphocytes'].apply(lambda x: map_ranges(x, (800, 4400), default=2))
    df['Absolute Neutrophil Count'] = df['Absolute Neutrophil Count'].apply(lambda x: map_ranges(x, (1600, 8800), default=2))
    df['Neutrophil to Lymphocyte ratio'] = df['Neutrophil to Lymphocyte ratio'].apply(lambda x: map_ranges(x, (2, 2), default=1))
    df['Total Platelet count'] = df['Total Platelet count'].apply(lambda x: map_ranges(x, (150, 450), default=2))
    df['Serum Albumin'] = df['Serum Albumin'].apply(lambda x: map_ranges(x, (3.5, 5.2), default=2))
    df['Serum Creatinine'] = df['Serum Creatinine'].apply(lambda x: map_ranges(x, (0.7, 1.3), default=2))
    df['Eosinophils'] = df['Eosinophils'].apply(lambda x: map_ranges(x, (1, 6), default=2))
    df['Basophils'] = df['Basophils'].apply(lambda x: map_ranges(x, (2, 2), default=1))
    df['Monocytes'] = df['Monocytes'].apply(lambda x: map_ranges(x, (2, 10), default=2))

    return df


