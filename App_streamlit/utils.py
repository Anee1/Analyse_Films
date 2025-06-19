import streamlit as st
import pandas as pd 
from pathlib import Path



OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

@st.cache_data
def load_parquet_data(file_name):

    file_path = OUTPUT_DIR / file_name
    return pd.read_parquet(file_path)
