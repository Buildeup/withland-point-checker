import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

def load_data_from_gsheet():
    """
    Streamlit Cloud secrets를 활용해 Google Sheet에서 데이터를 가져오는 함수
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials_info = {
        "type": st.secrets["gsheets"]["type"],
        "project_id": st.secrets["gsheets"]["project_id"],
        "private_key_id": st.secrets["gsheets"]["private_key_id"],
        "private_key": st.secrets["gsheets"]["private_key"].replace("\\n", "\n"),  # 반드시 복원
        "client_email": st.secrets["gsheets"]["client_email"],
        "client_id": st.secrets["gsheets"]["client_id"],
        "auth_uri": st.secrets["gsheets"]["auth_uri"],
        "token_uri": st.secrets["gsheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gsheets"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gsheets"]["client_x509_cert_url"]
    }

    creds = Credentials.from_service_account_info(credentials_info, scopes=scope)
    client = gspread.authorize(creds)

    spreadsheet_id = "1SIks7Eef4ZHP6q7GHF-yZY7GtFID7TPuoUfL9tPgYUY"
    sheet_name = "시트1"
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df