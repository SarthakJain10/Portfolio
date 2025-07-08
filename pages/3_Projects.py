import streamlit as st
from constant import *

st.set_page_config(layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style/style.css")

# Sidebar profile photo
st.sidebar.markdown(info['Photo'], unsafe_allow_html=True)

# Page title
st.title("💼 Projects")


# Display projects in a grid
for i in range(0, len(projects), 2):
    cols = st.columns(2)
    for idx, col in enumerate(cols):
        if i + idx < len(projects):
            project = projects[i + idx]
            with col:
                st.image(project["image"], use_container_width=True)
                st.subheader(project["title"])
                st.write(project["description"])
                if project["github"]:
                    st.markdown(f"[🔗 GitHub]({project['github']})", unsafe_allow_html=True)
                if project["demo"]:
                    st.markdown(f"[🚀 Live Demo]({project['demo']})", unsafe_allow_html=True)
