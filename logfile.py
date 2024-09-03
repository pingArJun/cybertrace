from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import streamlit as st
import pandas as pd
import tempfile
from datetime import datetime
import geoip2.database
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import plotly.express as px
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Configure API key for Google Gemini
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("API_KEY not found in environment variables.")
    st.stop()

genai.configure(api_key=API_KEY)

# Initialize the GeoIP database
geoip_db_path = "path/to/GeoLite2-City.mmdb"

class CybersecurityLogAnalyzer:
    @staticmethod
    def run():
        CybersecurityLogAnalyzer.handle_file_upload()

    @staticmethod
    def add_features_to_logs(logs_df):
        """
        Add cybersecurity-specific features to the log DataFrame.
        """
        if not all(col in logs_df.columns for col in ['Date', 'Time']):
            logs_df['Date and Time'] = pd.to_datetime(logs_df['Date and Time'], errors='coerce')
        else:
            logs_df['Date and Time'] = pd.to_datetime(logs_df['Date'] + ' ' + logs_df['Time'], errors='coerce')

        logs_df['Hour'] = logs_df['Date and Time'].dt.hour
        logs_df['Day'] = logs_df['Date and Time'].dt.day
        logs_df['Month'] = logs_df['Date and Time'].dt.month

        # Advanced Anomaly Detection
        logs_df = CybersecurityLogAnalyzer.detect_anomalies(logs_df)

        # Geolocation and IP reputation
        if 'Source' in logs_df.columns:
            logs_df['Country'] = logs_df['Source'].apply(CybersecurityLogAnalyzer.get_country_from_ip)

        return logs_df

    @staticmethod
    def detect_anomalies(logs_df):
        """
        Detect anomalies using clustering techniques.
        """
        clustering_features = logs_df.select_dtypes(include=[np.number]).dropna()
        if clustering_features.empty:
            logs_df['Is Anomalous'] = False
        else:
            dbscan = DBSCAN(eps=3, min_samples=2).fit(clustering_features)
            logs_df['Cluster'] = dbscan.labels_
            logs_df['Is Anomalous'] = logs_df['Cluster'] == -1

        return logs_df

    @staticmethod
    def get_country_from_ip(ip_address):
        try:
            with geoip2.database.Reader(geoip_db_path) as reader:
                response = reader.city(ip_address)
                return response.country.name
        except Exception:
            return "Unknown"

    @staticmethod
    def analyze_logs(llm, csv_path, query):
        agent = create_csv_agent(llm, csv_path, verbose=True,allow_dangerous_code=True)
        with st.spinner(text="Analyzing logs..."):
            try:
                st.write(agent.run(query))
            except Exception as e:
                st.error(f"Error during log analysis: {e}")

    @staticmethod
    def handle_file_upload():
        st.subheader("Upload System Log (CSV)")
        csv_file = st.file_uploader("Choose a CSV file", type=['csv'])

        if csv_file is not None:
            try:
                logs_df = pd.read_csv(csv_file)
                st.write("Log File Content:")
                st.dataframe(logs_df)
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
                return

            # Add cybersecurity features to the log file
            logs_df = CybersecurityLogAnalyzer.add_features_to_logs(logs_df)

            query = st.text_input("Enter your query for log analysis:")

            if st.button("Analyze Logs"):
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=API_KEY)
                except Exception as e:
                    st.error(f"Failed to initialize LLM: {e}")
                    return

                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                    temp_file_path = temp_file.name
                    logs_df.to_csv(temp_file_path, index=False)

                CybersecurityLogAnalyzer.analyze_logs(llm, temp_file_path, query)

            st.write("Anomaly Detection Results:")
            st.write(logs_df[['Date and Time', 'Event ID', 'Task Category', 'Source', 'Is Anomalous', 'Country']])

            # Visualize anomalies
            if not logs_df.empty:
                fig = px.scatter(logs_df, x='Date and Time', y='Event ID', color='Is Anomalous', title="Anomalies in Log Data")
                st.plotly_chart(fig)

if __name__ == "__main__":
    CybersecurityLogAnalyzer.run()