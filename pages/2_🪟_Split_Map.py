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

st.title("Split-panel Map")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        m.split_map(
            # left_layer="ESA WorldCover 2020 S2 FCC", right_layer="ESA WorldCover 2020"
            left_layer="ROADMAP", right_layer="HYBRID"
        )
        # m.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
        # m.add_legend(title="ESA Land Cover", builtin_legend="USDA/NASS/CDL")

m.to_streamlit(height=700)
