import streamlit as st
import requests
import pandas as pd
import pythonwhois
import dns.resolver
import dns.reversename
import regex as re 
from streamlit_option_menu import option_menu
from  streamlit_lottie import  st_lottie
from look_up import lookup
from osint import OSINTTool
from ipdr import iprecord
from logfile import CybersecurityLogAnalyzer


def progress_bar(progress):
    st.progress(progress)
st.set_page_config(page_title="IP Tools and OSINT", page_icon="🔍", layout="wide")
def localcss(filename):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
localcss("style.css")
pg_bg_img = f"""
<style>
[data-testid="stApp"] {{
background-image: url("https://i.imgur.com/bg2bhqC.png");
background-size: cover;
background-repeat: no-repeat;
background-attachment: local;
background-position: top left;
}}
[data-testid="stHeader"]{{
background-color: rgba(0,0,0,0);
}}

[data-testid="stSidebar"]{{
background-color: rgba(255,255,243,50);
background-image : url("https://i.imgur.com/bg2bhqC.png");  #[img]https://i.imgur.com/bg2bhqC.png[/img]
}}

</style>
"""

st.markdown(pg_bg_img, unsafe_allow_html=True)
c1,c2 = st.sidebar.columns(2)
with c1:
    st.markdown("""
                        <style>
                        .st-emotion-cache-1v0mbdj > img{
                        border-radius: 50%;
                            }
                        </style>
            
                        """, unsafe_allow_html=True)

    st.image("ggplogo2.png")

with c2:
    st.empty()
     


# Sidebar for navigation
st.sidebar.title("Gurugram Police Project")

tool_option = st.sidebar.selectbox("What would you like to do?", ["Menu","IP Address Query", "Call Record Query", "OSINT Tool" , "Recognizing Deep Fake", " Recognizing Fake News", "Log Analysis Tool"])
# Main content area
if tool_option == "Menu":
    st.title("Gurugram Police Project")
    
    st.header("Welcome! Warriors")
    st.write("""
            Welcome to the Gurugram Police Summer internship Project! This app is designed to help cybersecurity domain
            """)
        
        

    
    st.subheader("Objective")
    st.write("""
            The objective of this project is to develop tools and utilities that aid in digital forensics,
            helping law enforcement personnel and cybersecurity experts in investigating cybercrimes and 
            securing digital evidence effectively.
            """)

    # Footer for additional information
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f0f0f0; border-radius: 5px;">
        <p>Made with ❤️ by ARJUN,MEGASHRI,person3,person4</p>
        <p>Contact us at sdearjunkumar@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)





elif tool_option == "IP Address Query":
    st.header("IP Address Query")
    def main():
        # Add a sidebar menu option for accessing the notes app
        
        lookup_app = lookup()  # Instantiate the Notes class
        lookup_app.run()      # Run the Notes application
        

        # Add other sections of your Streamlit app (e.g., Home) based on user selection
        

    # Run the main function to start the Streamlit app
    if __name__ == "__main__":
        main()
    

elif tool_option == "Call Record Query":
    st.header("Call Record Query")
    def main():
        ipdr_app = iprecord() 
        ipdr_app.run()
    if __name__ == "__main__":
        main()
    
elif tool_option == "OSINT Tool":
    st.header("OSINT Tool")
    def main():
        osint_tool = OSINTTool()
        osint_tool.run()
        
    # Run the main function to start the Streamlit app
    if __name__ == "__main__":
        main()
    
elif tool_option == "Recognizing Deep Fake":
    st.title("Recognizing Deep Fake")

elif tool_option == "Recognizing Fake News":
    st.title("Recognizing  Fake News")
               

elif tool_option == "Log Analysis Tool":
    st.title("Log Analysis Tool")
    def main():
        log_analysis = CybersecurityLogAnalyzer()
        log_analysis.run()
        
    # Run the main function to start the Streamlit app
    if __name__ == "__main__":
        main()



st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)


st.sidebar.markdown("""
<style>
.made-by {
    font-family: monospace;
    color: #0C2637;
    font-size: 30px;
    text-align: center;
}
.made-by-links {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    margin: 10px 0;
}
.made-by-link {
    margin: 5px;
    text-decoration: none;
    color: #0C2637;
    font-size: 18px;
    transition: color 0.3s ease;
}
.made-by-link:hover {
    color: #0077B5;
}
.made-by-link img {
    width: 24px;
    height: 24px;
    margin-right: 5px;
}
</style>
<div class="made-by">💙 Made by : </div>
<div class="made-by-links">
    <a href="https://github.com/pingArJun" target="_blank" class="made-by-link">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/> GitHub
    </a>
    <a href="https://www.linkedin.com/in/arjunkumar7/" target="_blank" class="made-by-link">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/linkedin.png"/> LinkedIn
    </a>
    <a href="https://twitter.com/pingarjun" target="_blank" class="made-by-link">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/twitter.png"/> Twitter
    </a>
</div>
""", unsafe_allow_html=True)

# Add icons and hover effects to the "Follow me on" section

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<style>
.follow-me {
    font-family: monospace;
    color: #0C2637;
    font-size: 30px;
    text-align: center;
}
.follow-me-icons {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    margin: 10px 0;
}
.follow-me-icon {
    margin: 5px;
    transition: transform 0.3s ease;
}
.follow-me-icon:hover {
    transform: scale(1.2);
}
</style>


<div class="follow-me">🚀  Follow me  : </div>
<div class="follow-me-icons">
    <a href="https://www.linkedin.com/in/arjunkumar7/" target="_blank" class="follow-me-icon">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/linkedin.png"/>
    </a>
    <a href="https://twitter.com/pingarjun" target="_blank" class="follow-me-icon">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/twitter.png"/>
    </a>
    <a href="https://github.com/pingArJun" target="_blank" class="follow-me-icon">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
    </a>
</div>
""", unsafe_allow_html=True)




