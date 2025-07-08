import streamlit as st
import base64
from constant import *

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
        
local_css("style/style.css")

st.sidebar.markdown(info['Photo'],unsafe_allow_html=True)

st.title("📝 Resume")

st.write("[Click here if it's blocked by your browser](https://www.linkedin.com/in/sarthak-jain-sahab/overlay/1751823058172/single-media-viewer?type=DOCUMENT&profileId=ACoAAEbLYOYBUghInB1ZrgBWgxrjHm8t2JlhSDY&lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3B4kkfGFJtQMCmwVA7IDfniw%3D%3D)")

with open("images/resume_new.pdf","rb") as f:
      base64_pdf = base64.b64encode(f.read()).decode('utf-8')
      pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000mm" height="1000mm" type="application/pdf"></iframe>'
      st.markdown(pdf_display, unsafe_allow_html=True)
  
