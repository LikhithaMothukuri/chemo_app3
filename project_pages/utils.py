import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os.path
from project_pages.dataprocessMode import map_data
from project_pages.dataMode import map_dataprocess
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import tensorflow as tf
# from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model


# Load the saved model
# def load_model1(file_path):
#     with open(file_path, 'rb') as f:
#         model = pickle.load(f)
#     return model

# def setup_google_sheets(credentials_file, spreadsheet_name):
#     scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
#              "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
#     client = gspread.authorize(credentials)
#     spreadsheet = client.open(spreadsheet_name)
#     return spreadsheet

def runAndSave(input_df,input_data,savedModel):    
    output_df = map_data(input_df)
    result = savedModel.predict(output_df)
    label = result[0]

    if label == 1:
        st.markdown("<p style='font-size: 20px;'><b>Prediction:</b></p><p style='font-size: 25px; color: red;'>Patient may develop severe hematologic toxicity</p>", unsafe_allow_html=True)

    else:
        st.markdown(f"<p style='font-size: 20px;'><b>Prediction:</b></p><p style='font-size: 25px; color:green;'>No severe hematologic toxicity</p>", unsafe_allow_html=True)
        
    input_data['Tool Predicted Hematological Toxicity'] = label    
    new_input = input_data.copy()
    return new_input
 

def runAndSavemod(input_df,input_data,savedModel,patient_id,gc,sheet_id):
    outputdf = map_dataprocess(input_df)

    result = savedModel.predict(outputdf)
    label = np.argmax(result, axis=1)[0]
    # label = result[0]

    if label == 1:
        st.markdown("<p style='font-size: 20px;'><b>Prediction:</b></p><p style='font-size: 25px; color: red;'>Patient may develop severe hematologic toxicity</p>", unsafe_allow_html=True)

    else:
        st.markdown(f"<p style='font-size: 20px;'><b>Prediction:</b></p><p style='font-size: 25px; color:green;'>No severe hematologic toxicity</p>", unsafe_allow_html=True)
        
    try:
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet('Validation')
        
        # Read existing data from the worksheet
        existing_data = worksheet.get_all_values()
        prev_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
        
        # Add the prediction result to the input_data
        input_data['AHRC IITBBS Tool '] = label
        
        # Update or append the new data in the DataFrame
        if patient_id in prev_df['FILE NO'].values:
            prev_df.loc[prev_df['FILE NO'] == patient_id, 'AHRC IITBBS Tool '] = str(label)
        else:
            prev_df = pd.concat([prev_df, input_data])
        
        # Write the updated DataFrame back to the worksheet
        worksheet.clear()
        set_with_dataframe(worksheet, prev_df)
    except Exception as e:
        st.error(f"An error occurred while saving the result: {e}")

    

    
    
    

    
    




    
