from dotenv import load_dotenv
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import networkx as nx
from io import BytesIO
import google.generativeai as genai
from geopy.geocoders import Nominatim
from datetime import datetime
from fpdf import FPDF
from sklearn.ensemble import IsolationForest

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class iprecord:
    def __init__(self):
        st.header("Internet Protocol Digital Forensics for Police Investigations")
        self.input_text = st.text_area("Case Details: ", key="input")
        self.uploaded_file = st.file_uploader("Upload digital evidence (CSV)...", type=["csv"])
        self.submit = st.button("Generate Insights")
        self.input_prompt_ip = """
        You are an expert in Internet Protocol Digital Forensics. Analyze the provided digital evidence against known patterns and anomalies. 
        Provide insights into the origin, data flow, and potential security implications of the network traffic or communication patterns.
        """

    def run(self):
        if self.submit:
            if self.uploaded_file is not None:
                with st.spinner("Processing..."):
                    df = self.input_csv_setup(self.uploaded_file)
                    preprocessed_csv = self.preprocess_data(df)

                    suspicious_df = self.detect_suspicious_numbers(df)
                    st.write("Suspicious Numbers Detected:")
                    st.write(suspicious_df)

                    st.write("Analyzing all calls...")
                    filtered_cdr, call_durations = self.analyze_call_patterns(df)

                    self.visualize_data(filtered_cdr)

                    st.markdown(self.generate_download_link(filtered_cdr, None, call_durations), unsafe_allow_html=True)

                    response = self.get_ip_forensics_response(self.input_text, preprocessed_csv, self.input_prompt_ip)
                    st.subheader("Insights from IP Digital Forensics")
                    st.write(response)
            else:
                st.write("Please upload the digital evidence (CSV)")

        st.subheader("User Feedback")
        feedback = st.text_area("Provide your feedback:", key="feedback")
        if st.button("Submit Feedback"):
            st.write("Thank you for your feedback!")

    @staticmethod
    def input_csv_setup(uploaded_file):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df.columns = df.columns.str.strip()
            df['caller'] = df['caller'].astype(str).str.strip()
            df['callee'] = df['callee'].astype(str).str.strip()
            return df
        else:
            raise FileNotFoundError("No file uploaded")

    @staticmethod
    def preprocess_data(df):
        st.write("Preview of the uploaded CSV file:")
        st.write(df.head())

        if st.checkbox("Show column statistics"):
            st.write(df.describe())

        return df.to_csv(index=False)

    @staticmethod
    def detect_suspicious_numbers(df):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        features = df[['duration']].values

        model = IsolationForest(contamination=0.05)
        df['suspicious'] = model.fit_predict(features)
        suspicious_df = df[df['suspicious'] == -1]
        return suspicious_df

    @staticmethod
    def analyze_call_patterns(df, suspicious_number=None):
        if suspicious_number:
            filtered_cdr = df[(df['caller'] == suspicious_number) | (df['callee'] == suspicious_number)]
        else:
            filtered_cdr = df

        filtered_cdr['timestamp'] = pd.to_datetime(filtered_cdr['timestamp'])

        call_frequency = filtered_cdr['timestamp'].value_counts()
        call_durations = filtered_cdr['duration']

        st.write("Filtered Records:")
        st.write(filtered_cdr)
        st.write("Call Frequency:")
        st.write(call_frequency)
        st.write("Call Durations:")
        st.write(call_durations.describe())

        plt.figure(figsize=(10, 6))
        plt.plot(call_durations.values, marker='o', linestyle='-', color='b')
        plt.title('Call Durations Over Time')
        plt.xlabel('Call Index')
        plt.ylabel('Duration (seconds)')
        st.pyplot(plt)

        return filtered_cdr, call_durations

    def visualize_data(self, df):
        st.write("## Geographical Visualization")
        # Dummy data for geolocation visualization
        geoloc_data = pd.DataFrame({
            'latitude': [12.9716, 13.0827, 28.7041],
            'longitude': [77.5946, 80.2707, 77.1025],
            'call_count': [10, 15, 5]
        })

        st.map(geoloc_data)

        st.write("## Social Network Analysis")
        self.generate_network_graph(df)

    @staticmethod
    def generate_network_graph(df, suspicious_number=None):
        G = nx.Graph()

        for _, row in df.iterrows():
            caller, callee = row['caller'], row['callee']
            G.add_edge(caller, callee)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 10))
        nx.draw_networkx(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
        if suspicious_number:
            plt.title(f'Network of Contacts for {suspicious_number}')
        else:
            plt.title('Network of All Contacts')
        st.pyplot(plt)

    @staticmethod
    def generate_report(df, suspicious_number, call_durations):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Detailed Report", ln=True, align="C")

        pdf.cell(200, 10, txt="Key Insights", ln=True, align="L")
        if suspicious_number:
            pdf.cell(200, 10, txt=f"Suspicious Number: {suspicious_number}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Call Frequency: {len(df)}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Total Duration of Calls: {call_durations.sum()}", ln=True, align="L")

        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue().decode('utf-8')
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        pdf.multi_cell(200, 10, txt=csv_data)

        pdf_buffer = pdf.output(dest='S').encode('latin1')  # Encode PDF to bytes
        return pdf_buffer

    @staticmethod
    def generate_download_link(df, suspicious_number, call_durations):
        pdf_bytes = iprecord.generate_report(df, suspicious_number, call_durations)
        b64_pdf = base64.b64encode(pdf_bytes).decode()  # Encode PDF bytes to base64
        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="detailed_report.pdf">Download PDF Report</a>'
        return href

    @staticmethod
    def get_ip_forensics_response(input_text, csv_content, prompt):
        model = genai.GenerativeModel('gemini-pro')  # Replace with your model name
        response = model.generate_content([input_text, csv_content, prompt])
        return response.text

