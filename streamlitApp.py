import pandas as pd
import streamlit as st
# from streamlit_gsheets import GSheetsConnection
from project_pages.specific_options import specific_options
from project_pages.patient_id import patient_id
# from project_pages.utils import load_model1
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
from tensorflow.keras.models import load_model



st.set_page_config(layout="wide")

savedModel = load_model('model.h5')


def get_gspread_service_account():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"],scopes = scope)
    gc = gspread.authorize(credentials)
    return gc

def write_to_google_sheets(df, spreadsheet_id, worksheet_name):
    gc = get_gspread_service_account()
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)
    
    # Read existing data from the worksheet
    existing_data = worksheet.get_all_values()
    
    # If there is existing data, convert it to a DataFrame
    if existing_data:
        existing_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
    else:
        # If no existing data, create an empty DataFrame with the same columns as df
        existing_df = pd.DataFrame(columns=df.columns)
    
    # Concatenate existing data with the new DataFrame
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    
    # Clear the existing content in the worksheet
    worksheet.clear()
    
    # Write the combined DataFrame to the worksheet
    set_with_dataframe(worksheet, combined_df)


def read_google_sheets(spreadsheet_id, worksheet_name):
    gc = get_gspread_service_account()
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)
    
    # Read existing data from the worksheet
    existing_data = worksheet.get_all_values()
    return existing_data


sheet_id = st.secrets["spreadsheet"]["sheet_id"]

# Add the logo image
logo_url = "logo.png" 

def main():

    st.image(logo_url, width=450)
    st.title("Predicting Severe Chemotherapy Related Toxicities")

    button_style = """
    <style>
    .stButton button {
        width: 450px;
        height: 45px;
        background-color: #11A2D7;
        color: white;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,0.5,2])

    if 'button1' not in st.session_state:
        st.session_state['button1'] = False
    if 'button2' not in st.session_state:
        st.session_state['button2'] = False

    with col1:
        if st.button("Enter Patient File Number"):
            st.session_state['button1'] = True
            st.session_state['button2'] = False

    with col2:
        st.markdown("<p style='font-size: 22px;'>OR</p>", unsafe_allow_html=True)

    with col3:
        if st.button("Enter Specific Parameters"):
            st.session_state['button1'] = False
            st.session_state['button2'] = True

    if st.session_state['button1']:
        ex_data = read_google_sheets(sheet_id,"Validation")
        gc = get_gspread_service_account()
        patient_id(savedModel,ex_data,gc,sheet_id)
    
    if st.session_state['button2']:
        # data_append = specific_options(savedModel)
        write_to_google_sheets(specific_options(savedModel),sheet_id,"SpecificOptions")    
  

if __name__ == "__main__":
    main()