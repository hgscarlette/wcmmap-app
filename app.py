import streamlit as st
from streamlit_folium import st_folium
import folium
import leafmap.foliumap as leafmap
import pandas as pd



# Display a map centered in Vietnam

def init_map(center=(33.748997, -84.387985), zoom_start=10, map_type="cartodbpositron"):
    return folium.Map(location=center, zoom_start=zoom_start, tiles=map_type)

def page_filter(df):
    region_list = ['All'] + list(df.region.unique())
    region_list.sort()
    region = st.sidebar.selectbox('Select a region', region_list, 2)
    
    if region == 'All':
        city_list = ['All']
    else:
        city_list = ['All'] + list(df[df.region==region].city.unique())
    city_list.sort()
    city = st.sidebar.selectbox('Select a city', city_list)
    
    if city == 'All':
        concept_list = ['All'] + list(df.concept.unique())
    else:
        concept_list = ['All'] + list(df[(df.region==region) & (df.city==city)].concept.unique())
    concept_list.sort()
    concept = st.sidebar.selectbox('Select a concept', concept_list)
    # concept_index = concept_list.index()

    # Customize the sidebar
    # st.sidebar.title("About")
    # st.sidebar.info("""
    # A guided map for WinCommerce
    
    # Github repository
    # https://github.com/hgscarlette/wcmmap-app
    # """)
    st.sidebar.info(
        """
        This multipage interactive web-app demonstrates multiple use cases.
        Check out [GitHub repository](https://github.com/hgscarlette/wcmmap-app).
        """
    )
    logo = "https://hochiminhexport.com/wp-content/uploads/2024/04/logo-wincommerce-01.png"
    st.sidebar.image(logo)

    return region, city, concept

def main():
    st.set_page_config("WCM Map", "🗺️", layout="wide")
    st.title("Winmart Stores")
    st.caption("Expand the left panel to select a use case")

    # Load data
    df = pd.read_excel(r"data\Winmart location.xlsx")
    region, city, concept = page_filter(df)


    col1, col2 = st.columns([4, 1])
    # options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
    # index = options.index("OpenStreetMap")
    # options = ["ROADMAP","OpenStreetMap","CartoDB.Positron","HYBRID"]
    # index = options.index("ROADMAP")
    options = list(leafmap.basemaps.keys())
    index = options.index("ROADMAP")
    index = options.index("OpenTopoMap")

    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)


    with col1:
        # attribution = "Map data © OpenStreetMap contributors"
        # if "Stamen" in basemap:
        #     attribution = "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
        # elif "CartoDB" in basemap:
        #     attribution = "Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
        
        # # Map the basemap names to folium tile names
        # basemap_tiles = {
        #     "OpenStreetMap": "openstreetmap",
        #     "Stamen Terrain": "Stamen Terrain",
        #     "Stamen Toner": "Stamen Toner",
        #     "Stamen Watercolor": "Stamen Watercolor",
        #     "CartoDB positron": "CartoDB positron",
        #     "CartoDB dark_matter": "CartoDB dark_matter"
        # }
        # base_map = folium.Map(location=[10.7778, 106.6952], zoom_start = 12, tiles=basemap_tiles[basemap], attr=attribution, scrollWheelZoom=False)
        # base_map.add_child(MeasureControl())

        # base_map = init_map(map_type=basemap)
        # st_map = st_folium(
        #                     m, #base_map,
        #                     width=1200,
        #                     height=500,
        #                 )
        
        base_map = leafmap.Map(
            locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        )
        base_map.add_basemap(basemap)
        # base_map.to_streamlit(height=700)
        st.title('Winmart Locations Map')
        st_map = st_folium(
                            base_map,
                            width=1200,
                            height=500,
                        )

        # m = leafmap.Map(
        #     locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
        # )
        # m.add_basemap(basemap)
        # m.to_streamlit(height=700)
        



    # Display the data as a table
    st.title('Winmart Location Data')
    st.write(df)

    # #LOAD DATA
    # wcm_stores_file = r"C:\Users\huongptt5\Documents\Finance insights\WCM Store List.xlsx"
    # wcm_stores = pd.read_excel(wcm_stores_file)
    # wcm_stores = wcm_stores[(wcm_stores['lat'] != 0) & (wcm_stores['REV_30'] + wcm_stores['REV_90'] > 0)]
    # # wcm_stores = gpd.GeoDataFrame(wcm_stores, geometry=gpd.points_from_xy(wcm_stores.long, wcm_stores.lat), crs="EPSG:4326")
    # hcmward_geojson = r"C:\Users\huongptt5\Downloads\Population_Ward_Level.shp"
    # hcmc_boundaries = gpd.read_file(hcmward_geojson)
    # hcmc_boundaries = gpd.GeoDataFrame(hcmc_boundaries, crs=32648)
    # hcmc_boundaries = hcmc_boundaries.to_crs(4326)

    # region = 'South'
    # city = 'Ho Chi Minh'
    # concept = ''
    # last3m = pd.to_datetime('now').normalize() - pd.DateOffset(months=3)
    # # pos_ebitda =

    # # region, city, concept = display_area_filters(wcm_stores)

    # #DISPLAY FILTERS AND MAP
    # display_map(hcmc_boundaries)
    # # ward = display_map(hcmc_boundaries)
    # # st.write(ward)

    # #DISPLAY METRICS
    # st.subheader(f'{city} Store Facts')
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     display_store_facts(wcm_stores,
    #                         'region', region,
    #                         'city', city,
    #                         'concept', concept,
    #                         metric_title = f'No. of {concept} Stores',
    #                         metric = 'count',
    #                         metric_col = 'STORE_ID',
    #                         number_format='{:,}'
    #                         )
    # with col2:
    #     display_store_facts(wcm_stores[wcm_stores['date_open'] >= last3m],
    #                         'region', region,
    #                         'city', city,
    #                         'concept', concept,
    #                         metric_title = f'No. of New {concept} Stores',
    #                         metric = 'count',
    #                         metric_col = 'STORE_ID',
    #                         number_format='{:,}'
    #                         )
    # with col3:
    #     display_store_facts(wcm_stores,
    #                         'region', region,
    #                         'city', city,
    #                         'concept', concept,
    #                         metric_title = 'Total Revenue Last 30D',
    #                         metric = 'sum',
    #                         metric_col = 'REV_30'
    #                         )
        
if __name__ == "__main__":
    main()