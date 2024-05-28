import sys

import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from pygwalker.api.streamlit import StreamlitRenderer
from streamlit_folium import st_folium

from db import MySQLExecutor


st.set_page_config(page_title="Encar Data Analysis App", page_icon=None, layout="wide")
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

st.sidebar.write("****A) Select Data Loader****")

ft = st.sidebar.selectbox("Data from: ", ["mysql", "Excel", "csv"])
if ft != "mysql":
    uploaded_file = st.sidebar.file_uploader("*Upload file here*")
else:
    uploaded_file = None

db = None

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
                global db
                db = MySQLExecutor(database_name, user, db_passwd, host, int(port))
                res = db.read(table_name, 0)
                data = pd.DataFrame(res)
                data.set_index("index", inplace=True, drop=True)
                faq_data = db.read("faq", 0)
                faq_data = pd.DataFrame(faq_data)
                faq_data.set_index("index", inplace=True, drop=True)
            except Exception as e:
                warn = "build dataset('$ python build_dataset.py') or check your db password"
                st.warning(f"{warn}", icon="⚠️")
                st.stop()

        return data, faq_data

    data, faq_data = load_data(file_path, ft, sh, h)
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
        st.write("###### Data shape :", data.shape)

    st.sidebar.write("****C) Click to Visualize****")
    vis_select = st.sidebar.button("Visualize")

    if vis_select:

        st.write("### 3. Visual Insights ")
        StreamlitRenderer(data).explorer()

with tab2:
    # TODO map visualization
    st.write("### 4. Map")

    m = folium.Map(location=[37.56693229959581, 126.97852771817074], zoom_start=7)

    region_coords = {
        "서울": [37.540705, 126.956764],
        "경기": [37.567167, 127.190292],
        "인천": [37.469221, 126.573234],
        "대전": [36.321655, 127.378953],
        "세종": [36.5040736, 127.2494855],
        "충남": [36.557229, 126.779757],
        "충북": [36.628503, 127.929344],
        "강원": [37.555837, 128.209315],
        "부산": [35.198362, 129.053922],
        "대구": [35.798838, 128.583052],
        "울산": [35.519301, 129.239078],
        "경남": [35.259787, 128.664734],
        "경북": [36.248647, 128.664734],
        "광주": [35.126033, 126.831302],
        "전남": [34.819400, 126.893113],
        "전북": [35.716705, 127.144185],
        "제주": [33.364805, 126.542671],
    }

    region_counts = data["지역"].value_counts()

    # 마커 클러스터 생성
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)

    # 각 지역에 등장 횟수 마커 추가
    for region, count in region_counts.items():
        if region in region_coords:
            folium.Marker(
                location=region_coords[region],
                popup=f"{region}: {count}대",
                tooltip=f"{region}: {count}대",
                icon=folium.Icon(color="blue"),
            ).add_to(marker_cluster)
    # st_folium(m, width=700, height=500)

    # html로 맵 저장해서 뿌려주기
    m.save("map.html")
    st.components.v1.html(open("map.html", "r").read(), height=500)


with tab3:
    st.write("### FAQ")
    st.dataframe(faq_data)
