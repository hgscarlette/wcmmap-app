import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
This multipage interactive web-app demonstrates multiple use cases for Location Analyses.

Check out [GitHub repository](https://github.com/hgscarlette/wcmmap-app).
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
st.sidebar.image("https://hochiminhexport.com/wp-content/uploads/2024/04/logo-wincommerce-01.png")
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():

        m = leafmap.Map(center=[40, -100], zoom=4)
        cities = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

        m.add_geojson(regions, layer_name="US Regions")
        m.add_points_from_xy(
            cities,
            x="longitude",
            y="latitude",
            color_column="region",
            icon_names=["gear", "map", "leaf", "globe"],
            spin=True,
            add_legend=True,
        )

m.to_streamlit(height=700)
