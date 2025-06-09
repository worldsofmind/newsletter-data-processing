import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="LAB File Converter", layout="wide")
st.title("LAB Officer Data Converter")

st.markdown("This tool converts raw case load, namelist, and ratings files into standardized, clean CSV files.")

# --- File Upload ---
case_file = st.file_uploader("Upload Case Load (.xlsx)", type=["xlsx"])
namelist_file = st.file_uploader("Upload Namelist (.csv)", type=["csv"])
ratings_file = st.file_uploader("Upload Ratings (.csv)", type=["csv"])

# --- Processing Functions ---

def process_case_load(uploaded_file):
    df = pd.read_excel(uploaded_file, header=10)
    df['name'] = (
        df['LO/LE']
        .str.replace(r'\s*\((LAB|MLAW)\)', '', regex=True)
        .str.replace(r'\s*\([^)]*\)$', '', regex=True)
        .str.strip()
    )
    df['abbreviation'] = df['LO/LE'].str.extract(r'\(([^()]+)\)\s*$', expand=False)
    df.columns = df.columns.str.lower()
    return df

def process_namelist(uploaded_file, name_map):
    df = pd.read_csv(uploaded_file, encoding='cp1252')
    df = df.rename(columns={'name_self': 'abbreviation', 'self_type': 'function'})
    df['name'] = df['abbreviation'].map(name_map)
    df.columns = df.columns.str.lower()
    return df

def process_ratings(uploaded_file, name_map):
    df = pd.read_csv(uploaded_file, encoding='cp1252')
    df = df.rename(columns=lambda x: 'applicant' if x.strip().lower() == 'name' else x)

    records = []
    for _, row in df.iterrows():
        for role in ['LO', 'LE']:
            abbr = row.get(role)
            if pd.notna(abbr) and str(abbr).strip():
                new_row = row.to_dict()
                new_row['type'] = role
                new_row['abbreviation'] = abbr
                records.append(new_row)

    df_expanded = pd.DataFrame(records).drop(columns=['LO', 'LE'], errors='ignore')
    df_expanded.columns = df_expanded.columns.str.lower()
    df_expanded['name'] = df_expanded['abbreviation'].map(name_map)
    return df_expanded

# --- Run Processing ---
if st.button("Convert Files"):
    if not (case_file and namelist_file and ratings_file):
        st.error("Please upload all three files.")
    else:
        with st.spinner("Processing files..."):
            case_df = process_case_load(case_file)
            name_map = case_df.set_index('abbreviation')['name'].dropna().to_dict()
            namelist_df = process_namelist(namelist_file, name_map)
            ratings_df = process_ratings(ratings_file, name_map)

        st.success("Files successfully converted!")

        st.download_button("Download Processed Case Load", case_df.to_csv(index=False).encode('utf-8'), "standardized_case_load.csv", "text/csv")
        st.download_button("Download Processed NameList", namelist_df.to_csv(index=False).encode('utf-8'), "standardized_namelist.csv", "text/csv")
        st.download_button("Download Processed Ratings", ratings_df.to_csv(index=False).encode('utf-8'), "standardized_ratings.csv", "text/csv")

        st.subheader("Preview")
        st.write("Case Load", case_df.head())
        st.write("NameList", namelist_df.head())
        st.write("Ratings", ratings_df.head())
