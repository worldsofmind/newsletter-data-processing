# LAB Officer Data Converter

This Streamlit app converts raw data files from the Legal Aid Bureau (LAB) into standardized CSV files for analysis and reporting.

## 🔧 Features

- ✅ Extracts `abbreviation` and `name` from `LO/LE` in case load
- ✅ Removes suffixes like `(LAB)` and `(MLAW)`
- ✅ Standardizes all officer names using case load as the single source of truth
- ✅ Expands each `LO` and `LE` in ratings into their own row
- ✅ Converts headers to lowercase and standard formats

## 📂 Input Files

Upload the following:

1. `case_load.xlsx`  
   - Sheet starting from row 11
   - Must contain `LO/LE` column

2. `namelist.csv`  
   - Columns: `name_self`, `self_type`, `email_address`

3. `ratings.csv`  
   - Columns include: `NAME`, `LO`, `LE`, and rating fields

## 📤 Output Files

The app produces:

- `standardized_case_load.csv`
- `standardized_namelist.csv`
- `standardized_ratings.csv`

## 🚀 How to Deploy

1. Upload the following to a GitHub repo:
   - `lab_converter_app.py`
   - `requirements.txt`
   - `README.md`

2. Deploy on [Streamlit Cloud](https://streamlit.io/cloud):
   - Point to the GitHub repo
   - Set main file to `lab_converter_app.py`

## 📌 Requirements

```
streamlit
pandas
openpyxl
```

## 📝 Author

Generated with ❤️ from DD(OPDA)
