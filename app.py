import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

used_fields = ["classe_estimation_ges",
               "latitude",
               "longitude",
               #"nom_methode_dpe",
               "usr_diagnostiqueur_id",
               "numero_dpe",
               "secteur_activite",
               "organisme_certificateur",
               "adresse_organisme_certificateur",
               "geo_adresse",
               #"tv016_departement_id",
               "tv016_departement_departement",
               "commune"]


@st.cache
def load_data():
    return pd.read_excel("dpe-tertiaire.xlsx")

# load data
DPE = load_data()
DPE = DPE[used_fields]

# filter departement
departe = st.sidebar.selectbox('Séléctionnez le département', DPE['tv016_departement_departement'].unique())
sub_DPE = DPE[DPE.tv016_departement_departement == departe]
commune = st.sidebar.selectbox('Séléctionnez la commune', sub_DPE['commune'].unique())
sub_DPE = DPE[DPE.commune == commune].dropna()
st.header('Département sélectionné:', departe)
st.header('Commune sélectionnée:', departe)

st.subheader("DPEs effectués")
st.dataframe(sub_DPE)

# set the map center
m = folium.Map(location=[sub_DPE.latitude.mean(), sub_DPE.longitude.mean()], zoom_start=10)
for index, row in sub_DPE.iterrows():
    # add marker for Liberty Bell
    tooltip = row['geo_adresse']
    folium.Marker(
        [row['latitude'], row['longitude']], popup=row['geo_adresse'], tooltip=tooltip
    ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)
