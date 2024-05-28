import sys

import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

from db import MySQLExecutor


st.set_page_config(page_title="Encar Data Analysis App", page_icon=None, layout="wide")
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

st.sidebar.write("****A) Select Data Loader****")

ft = st.sidebar.selectbox("Data from: ", ["mysql", "Excel", "csv"])
if ft != "mysql":
    uploaded_file = st.sidebar.file_uploader("*Upload file here*")
else:
    uploaded_file = None

if uploaded_file is not None or ft == "mysql":
    file_path = uploaded_file

    if ft == "Excel":
        try:
            sh = st.sidebar.selectbox(
                "*Which sheet name in the file should be read?*",
                pd.ExcelFile(file_path, "openpyxl").sheet_names,
            )
            h = st.sidebar.number_input(
                "*Which row contains the column names?*", 0, 100
            )
        except:
            st.info("File is not recognised as an Excel file")
            sys.exit()

    elif ft == "csv":
        try:
            sh = None
            h = None
        except:
            st.info("File is not recognised as a csv file.")
            sys.exit()

    elif ft == "mysql":
        database_name = st.sidebar.text_input("Database: ", "encar")
        user = st.sidebar.text_input("USER: ", "root")
        host = st.sidebar.text_input("HOST: ", "127.0.0.1")
        port = st.sidebar.text_input("PORT: ", "3306")
        table_name = st.sidebar.text_input("TABLE: ", "info")

        db_passwd = None
        db_passwd = st.sidebar.text_input("Enter DB password: ", "", type="password")
        while db_passwd is None:
            continue
        try:
            sh = None
            h = None
        except Exception as e:
            st.info(f"{e}")
            raise Exception from e

    @st.cache_data(experimental_allow_widgets=True)
    def load_data(file_path, ft, sh, h):

        if ft == "Excel":
            try:
                data = pd.read_excel(
                    file_path, header=h, sheet_name=sh, engine="openpyxl"
                )
            except:
                st.info("File is not recognised as an Excel file.")
                sys.exit()

        elif ft == "csv":
            try:
                data = pd.read_csv(file_path)
            except:
                st.info("File is not recognised as a csv file.")
                sys.exit()

        elif ft == "mysql":
            try:
                db = MySQLExecutor(database_name, user, db_passwd, host, int(port))
                res = db.read(table_name, 0)
                data = pd.DataFrame(res)
                data.set_index("index", inplace=True, drop=True)
            except Exception as e:
                st.warning("[check your db password.]", icon="⚠️")
                st.stop()

        return data

    data = load_data(file_path, ft, sh, h)
with tab1:

    st.write("### 1. Dataset Preview ")

    try:
        st.dataframe(data, use_container_width=True)

    except:
        st.info(
            "The file wasn't read properly. Please ensure that the input parameters are correctly defined."
        )
        sys.exit()
    st.write("### 2. High-Level Overview ")

    st.sidebar.write(
        "**B) What would you like to know about the data?**",
    )
    selected = st.sidebar.radio(
        "",
        [
            "Data Dimensions",
            "Field Descriptions",
            "Summary Statistics",
            "Value Counts of Fields",
        ],
    )

    if selected == "Field Descriptions":
        fd = (
            data.dtypes.reset_index()
            .rename(columns={"index": "Field Name", 0: "Field Type"})
            .sort_values(by="Field Type", ascending=False)
            .reset_index(drop=True)
        )
        st.dataframe(fd, use_container_width=True)

    elif selected == "Summary Statistics":
        ss = pd.DataFrame(data.describe(include="all").round(2).fillna(""))
        st.dataframe(ss, use_container_width=True)

    elif selected == "Value Counts of Fields":
        sub_selected = st.sidebar.radio(
            "*Which field should be investigated?*",
            data.select_dtypes("object").columns,
        )
        vc = (
            data[sub_selected]
            .value_counts()
            .reset_index()
            .rename(columns={"count": "Count"})
            .reset_index(drop=True)
        )
        st.dataframe(vc, use_container_width=True)

    else:
        st.write("###### The data has the dimensions :", data.shape)

    # vis_select = st.sidebar.checkbox(
    #     "**C) Is visualisation required for this dataset?**"
    # )
    st.sidebar.write("****C) Click Visualize****")
    vis_select = st.sidebar.button("Visualize")

    if vis_select:

        st.write("### 3. Visual Insights ")
        StreamlitRenderer(data).explorer()

with tab2:
    # TODO map visualization
    st.write("### 4. Map")

with tab3:
    st.write("### FAQ")
