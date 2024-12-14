import streamlit as st
import leafmap.foliumap as leafmap

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
# options = list(leafmap.basemaps.keys())
options = ["CartoDB","Google Map","OpenStreetMap","Bus Map","ESRI Street Map","Google Satellite","Google Satellite with POIs","Google Terrain"]
# Strava for health data
# Stadia for nice nature, WaymarkedTrails for hiking, OpenTopoMap for topography
# OpenAIP for aeronautical like airports, heights of buildings/obstacles 

index = options.index("CartoDB")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)


with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    # Map the basemap names to folium tile names
    basemap_tiles = {
        "CartoDB": "CartoDB.Positron", #light basemap
        "Google Map": "ROADMAP",
        "OpenStreetMap": "OpenStreetMap",
        "Bus Map": "OPNVKarte",
        "ESRI Street Map": "Esri.WorldStreetMap", #highlights of main streets
        "Google Satellite": "SATELLITE",
        "Google Satellite with POIs": "HYBRID",
        "Google Terrain": "TERRAIN" #height
    }
    m.add_basemap(basemap_tiles[basemap])
    m.to_streamlit(height=700)
