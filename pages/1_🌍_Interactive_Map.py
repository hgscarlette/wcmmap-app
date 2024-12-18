import streamlit as st
import leafmap.foliumap as leafmap
import folium
import geopandas as gpd
import pandas as pd

markdown = """
This multipage interactive web-app demonstrates multiple use cases for Location Analyses.

Check out [GitHub repository](https://github.com/hgscarlette/wcmmap-app).
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
st.sidebar.image("logo\logo_WinCommerce.jpg")
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")


### SUPPORTING FUNCTIONS
def page_filter(df):
    region_list = ['All'] + list(df.region.unique())
    region_list.sort()
    region = st.selectbox('Region', region_list)
    
    if region == 'All':
        city_list = ['All']
    else:
        city_list = ['All'] + list(df[df.region==region].city.unique())
    city_list.sort()
    city = st.selectbox('City', city_list)
    
    if city == 'All':
        concept_list = ['All'] + list(df.concept.unique())
    else:
        concept_list = ['All'] + list(df[(df.region==region) & (df.city==city)].concept.unique())
    concept_list.sort()
    concept = st.selectbox('Concept', concept_list)
    return region, city, concept

def get_representative_loc(gdf, admin_level):
    gdf_admin = gdf[[admin_level,"geometry"]].dissolve(by=admin_level, as_index=False)
    gdf_admin[admin_level+"_centroid"] = gdf_admin.representative_point()
    gdf = pd.merge(gdf, gdf_admin[[admin_level,admin_level+"_centroid"]], how="inner")
    return gdf

def make_marker(gdf, layer_name, bubble_size, tooltip_cols, tooltip_aliases, popup_cols, popup_aliases):
    marker = folium.GeoJson(
        gdf,
        name=layer_name,
        marker=folium.Circle(
            radius=4, 
            fill_color='orange', 
            fill_opacity=0.5, 
            color="black", 
            weight=0.1
        ),
        style_function=lambda x: {
            "fillColor": x['properties']['color'],
            "radius": (x['properties'][bubble_size])/50000000+50,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_cols,
            aliases=tooltip_aliases,
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=popup_cols,
            aliases=popup_aliases,
            localize=True
        ),
        highlight_function=lambda x: {"fillOpacity": 0.8},
        zoom_on_click=True,
    )
    return marker

### MAIN PAGE
st.title("Interactive Map")

# Load WCM data
df = pd.read_csv(r"data\WCM stores_ext.csv", encoding="utf8")

# Load GeoJSON of Vietnam's boundaries (Ward level)
geojson_file = r"data\VN_Boundaries_Ward_ext.json"
gdf = gpd.read_file(geojson_file, encoding="utf8")

# Load population data
df_pop = pd.read_csv(r"data\VN_Population_ward.csv", encoding="utf8")
df_household = pd.read_csv(r"data\VN_HouseholdPop_ward.csv", encoding="utf8")

# Content
col1, col2, col3 = st.columns([1, 4, 2])

options = ["CartoDB","Google Map","OpenStreetMap","Bus Map","ESRI Street Map","Google Satellite","Google Satellite with POIs","Google Terrain"]
# options = list(leafmap.basemaps.keys())
# ESA Land Cover Type for land cover, OpenWeatherMap for weather, OpenSeaMap for sea, OpenRailwayMap for trains
# Strava for health data
# Stadia for nice nature, WaymarkedTrails for hiking, OpenTopoMap for topography
# OpenAIP for aeronautical like airports, heights of buildings/obstacles

index = 1

with col1:
    # Set up filters
    region, city, concept = page_filter(df)
    basemap = st.selectbox("Basemap", options, index)
    st.caption("*Updated by Oct 2024")

    # Submit & Reset filters buttons
    button_cols = st.columns(2)
    with button_cols[0]:
        st.button("Reset", use_container_width=True)
    with button_cols[1]:
        submit_button = st.button("Submit", type="primary", use_container_width=True)

    # Save filters
    # st.session_state.region = region
    # st.session_state.city = city
    # st.session_state.concept = concept

with col2:
    if submit_button:
        if region != "All" and city == "All":
            gdf = gdf[gdf.region==region]
            # Get reagion's representative point for the map's center
            gdf = get_representative_loc(gdf, "region")
            map_center = (gdf.region_centroid.values[0].y, gdf.region_centroid.values[0].x)
            map_zoom = 10
            # Update gdf for the booundary layer
            gdf_map = gdf.loc[:, gdf.columns != "region_centroid"]
            df_map = df[df.region==region]
        else:
            city_en = city.lower().replace(" ","").replace("bariavungtau","baria-vungtau")
            gdf = gdf[gdf.city_en==city_en]
            # Get reagion's representative point for the map's center
            gdf = get_representative_loc(gdf, "city")
            map_center = (gdf.city_centroid.values[0].y, gdf.city_centroid.values[0].x)
            map_zoom = 13
            # Update gdf for the booundary layer
            gdf_map = gdf.loc[:, gdf.columns != "city_centroid"]
            df_map = df[(df.region==region) & (df.city==city)]

        m = leafmap.Map(
            locate_control=True, draw_control=False, attribution_control=True, #latlon_control=True, #draw_export=True, #minimap_control=True,
            center=map_center, zoom=map_zoom, height="700px"
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

        # Add ward boundaries
        m.add_geojson(
            gdf_map,
            layer_name="Administrative",
            style={"fillOpacity": 0.7},
            # fill_colors=["green"],
            # column="POP_EST",
            # scheme="Quantiles",
            # cmap="Blues",
            # legend_title="Population",
        )

        # m.add_circle_markers_from_xy(
        #     data=df_map,
        #     layer_name="WCM Store",
        #     x="long",
        #     y="lat",
        #     # color_column="region",
        #     # icon_names=["gear", "map", "leaf", "globe"],
        #     spin=True,
        #     add_legend=True,
        # )

        # Add to page
        m.to_streamlit(height=700)
    else:
        map_default = leafmap.Map(
            locate_control=True, draw_control=False, attribution_control=True,
            center=(16.088850817930474, 107.82173235396314), zoom=6, height="700px"
        )
        map_default.to_streamlit(height=700)

with col3:
    st.subheader(f"Region: {region}")

