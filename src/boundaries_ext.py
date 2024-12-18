import geopandas as gpd
import pandas as pd

"""
Region is one of the maps' filters and its definition is usually specific to different organization.
Here, we define the regions based on Winmart's store data.
"""

def read_boundaries(level):
    # Read Vietnam's boundaries
    geojson_url = "https://raw.githubusercontent.com/hgscarlette/vn-demographic/main/VN_Boundaries_"+level+".json"
    gdf = gpd.read_file(geojson_url)

    # Assign WCM's defined regions to each city in Vietnam's boundaries
    gdf = pd.merge(gdf, city_wcm_list, how="left")
    gdf.loc[gdf.city_en=="daknong", ["region"]] = "Central"
    gdf.insert(0, "region", gdf.pop("region"))

    # Save the updated boundaries
    gdf.to_file(r"data\VN_Boundaries_"+level+"_ext.json", driver="GeoJSON")
    return gdf

# Read WCM data
df = pd.read_excel(r"data\Winmart location.xlsx")
df["city_en"] = df.city.apply(lambda x: x.lower().replace(" ","").replace("bariavungtau","baria-vungtau"))
city_wcm_list = df[["region","city_en"]]
city_wcm_list = city_wcm_list.drop_duplicates()

read_boundaries("Ward")
read_boundaries("District")