# Frontend (FE)
import requests
import streamlit as st
import pandas as pd

# Streamlit interface
st.set_page_config(page_title="Disease X Analytics Panel", layout="wide", page_icon="🧊")
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.logo("https://upload.wikimedia.org/wikipedia/commons/8/8b/Pfizer_%282021%29.png")

# Function to display Tableau workbook
def display_tableau_workbook(embed_code):
   st.components.v1.html(embed_code, height=800, width=1520, scrolling=True)

def prediction_page():
    # Definición de la URL de la API
    API_URL = "http://localhost:8000/predict/"

    st.header("Drug A Administration Predictor")
    st.write("This tool helps healthcare providers determine the likelihood of a patient receiving Drug A for treating mild to moderate infections of Disease X. By analyzing patient data, we aim to support informed decision-making in clinical settings.")
    st.write("### How to Use:")
    st.write("1. **Enter Patient Data:** Provide the necessary information about the patient.")
    st.write("2. **Submit & Predict:** Click the 'Predict' button to get the prediction.")
    uploaded_file = st.file_uploader("Choose patient data as CSV format", type="csv")
    if st.button('Predict'):
        if uploaded_file is not None:
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
            payload = {'username': 'NLC', 'filename': uploaded_file.name}
            try:
                response = requests.post(API_URL, params=payload, files=files)
                if response.status_code == 200:
                    prediction = response.json()
                    if {prediction['prediction']} == 1.0:
                        st.write(f"Prediction: Patient is eligible to receive Drug A")
                    else:
                        st.write(f"Prediction: Patient is not eligible to receive Drug A")
            except requests.exceptions.RequestException as e:
                st.write(f"Error: Unable to get prediction from API: {e}")
    st.markdown('''
    **Important Note:** This AI tool is designed to assist but not replace clinical judgment.
    ''')

def disease_x_factors_dashboard():
    # Tableau Embed Code
    tableau_embed_code = '''
    <div class='tableauPlaceholder' id='viz1734478282396' style='position: relative'><noscript><a href='#'><img alt='Overview ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Di&#47;DiseaseXFactors&#47;Overview&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='DiseaseXFactors&#47;Overview' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Di&#47;DiseaseXFactors&#47;Overview&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1734478282396');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1520px';vizElement.style.height='795px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1520px';vizElement.style.height='795px';} else { vizElement.style.width='100%';vizElement.style.height='2377px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    '''

    display_tableau_workbook(tableau_embed_code)

def main():
    # Create Tabs
    tab_1, tab_2 = st.tabs(['Drug A Administration Predictor', 'Disease X Factors Dashboard'])
    with tab_1:
        prediction_page()
    with tab_2:
        disease_x_factors_dashboard()


if __name__ == "__main__":
    main()



