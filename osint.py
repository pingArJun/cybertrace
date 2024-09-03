import streamlit as st
import requests
from bs4 import BeautifulSoup
import dns.resolver
import socket
import re
bearer_token = "AAAAAAAAAAAAAAAAAAAAAL%2BvuQEAAAAAYsGqVoIcespsiVYXO9pr9hmovVA%3DehmJQrpWZztmrcOSQkOEob48rtxBRJLZvHFcLSyAJeqN4qeJ9d"


class OSINTTool:

    @staticmethod
    def run():
        st.title("OSINT Tool")

        # Choose the type of input
        input_type = st.radio("Select input type", ("Domain/IP", "Email", "Username"))
        
        if input_type == "Domain/IP":
            input_value = st.text_input("Enter a domain or IP address (e.g., example.com or 8.8.8.8)")
            
            if input_value:
                if OSINTTool.is_valid_domain(input_value):
                    operation = st.radio("Choose the operation", ('WHOIS Lookup', 'DNS Lookup'))
                elif OSINTTool.is_valid_ip(input_value):
                    operation = st.radio("Choose the operation", ('IP Lookup', 'Reverse DNS Lookup', 'Geolocation'))
                else:
                    st.error("Please enter a valid domain or IP address.")
                    return

                if st.button("Lookup"):
                    if operation == 'WHOIS Lookup':
                        with st.spinner("Fetching WHOIS data..."):
                            whois_data = OSINTTool.fetch_whois(input_value)
                        st.subheader("WHOIS Data")
                        OSINTTool.display_whois_table(whois_data)
                    elif operation == 'DNS Lookup':
                        with st.spinner("Fetching DNS records..."):
                            dns_records = OSINTTool.get_dns_records(input_value)
                        st.subheader("DNS Records")
                        OSINTTool.display_dns_table(dns_records)
                    elif operation == 'IP Lookup':
                        with st.spinner("Fetching IP information..."):
                            ip_info = OSINTTool.get_ip_info(input_value)
                        st.subheader("IP Information")
                        OSINTTool.display_ip_info_table(ip_info)
                    elif operation == 'Reverse DNS Lookup':
                        with st.spinner("Fetching Reverse DNS information..."):
                            reverse_dns = OSINTTool.get_reverse_dns(input_value)
                        st.subheader("Reverse DNS Information")
                        st.write(reverse_dns)
                    elif operation == 'Geolocation':
                        with st.spinner("Fetching Geolocation information..."):
                            geo_info = OSINTTool.get_geolocation(input_value)
                        st.subheader("Geolocation Information")
                        OSINTTool.display_geolocation_table(geo_info)
        
        elif input_type == "Email":
            email = st.text_input("Enter an email address (e.g., example@example.com)")
            
            if email and st.button("Validate Email"):
                with st.spinner("Validating email..."):
                    is_valid = OSINTTool.validate_email(email)
                st.subheader("Email Validation")
                if is_valid:
                    st.success("The email address is valid.")
                else:
                    st.error("The email address is not valid.")
        
        elif input_type == "Username":
            username = st.text_input("Enter a social media username (e.g., @example)")
            platform = st.selectbox("Select platform", ["Twitter", "GitHub", "LinkedIn"])

            if username and st.button("Lookup Profile"):
                if platform == "Twitter":
                    with st.spinner("Fetching Twitter profile..."):
                        profile = OSINTTool.get_twitter_profile(username)
                    st.subheader("Twitter Profile")
                    st.write(profile)
                elif platform == "GitHub":
                    with st.spinner("Fetching GitHub profile..."):
                        profile = OSINTTool.get_github_profile(username)
                    st.subheader("GitHub Profile")
                    st.write(profile)
                elif platform == "LinkedIn":
                    with st.spinner("Fetching LinkedIn profile..."):
                        profile = OSINTTool.get_linkedin_profile(username)
                    st.subheader("LinkedIn Profile")
                    st.write(profile)
                
    @staticmethod
    def is_valid_domain(domain):
        regex = r'^(?!:\/\/)([a-zA-Z0-9-_]+\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11}?$'
        return re.match(regex, domain)

    @staticmethod
    def is_valid_ip(ip):
        regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return re.match(regex, ip)

    @staticmethod
    def fetch_whois(domain):
        url = f"https://www.whois.com/whois/{domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                whois_info = soup.find('pre', class_='df-raw').text.strip()

                # Split WHOIS data into lines
                lines = whois_info.split('\n')

                # Extract WHOIS data up to the "DNSSEC" information
                extracted_info = []
                for line in lines:
                    extracted_info.append(line)
                    if "DNSSEC" in line:
                        break

                return '\n'.join(extracted_info)
            else:
                return f"Failed to fetch WHOIS information. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @staticmethod
    def get_dns_records(domain):
        records = {}
        try:
            records['A'] = [rdata.to_text() for rdata in dns.resolver.resolve(domain, 'A')]
        except Exception as e:
            records['A'] = str(e)
        try:
            records['AAAA'] = [rdata.to_text() for rdata in dns.resolver.resolve(domain, 'AAAA')]
        except Exception as e:
            records['AAAA'] = str(e)
        try:
            records['MX'] = [rdata.to_text() for rdata in dns.resolver.resolve(domain, 'MX')]
        except Exception as e:
            records['MX'] = str(e)
        try:
            records['NS'] = [rdata.to_text() for rdata in dns.resolver.resolve(domain, 'NS')]
        except Exception as e:
            records['NS'] = str(e)
        return records

    @staticmethod
    def get_ip_info(ip):
        url = f"https://ipinfo.io/{ip}/json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return f"Failed to fetch IP information. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @staticmethod
    def get_reverse_dns(ip):
        try:
            result = socket.gethostbyaddr(ip)
            return result[0]
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    @staticmethod
    def get_geolocation(ip):
        url = f"https://ipapi.co/{ip}/json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return f"Failed to fetch geolocation information. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    
    

    @staticmethod
    def get_twitter_profile(username):
        url = f"https://api.twitter.com/1/users/by/username/{username.lstrip('@')}"
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {str(e)}"

            
        @staticmethod
        def get_github_profile(username):
            url = f"https://api.github.com/users/{username.lstrip('@')}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    return f"Failed to fetch GitHub profile. Status code: {response.status_code}"
            except Exception as e:
                return f"An error occurred: {str(e)}"
    

    @staticmethod
    def get_linkedin_profile(username):
        url = f"https://www.linkedin.com/in/{username}/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                name = soup.find("li", {"class": "inline t-24 t-black t-normal break-words"}).get_text().strip()
                headline = soup.find("h2", {"class": "mt1 t-18 t-black t-normal break-words"}).get_text().strip()
                location = soup.find("li", {"class": "t-16 t-black t-normal inline-block"}).get_text().strip()
                return {"Name": name, "Headline": headline, "Location": location}
            else:
                return f"Failed to fetch LinkedIn profile. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @staticmethod
    def display_linkedin_profile(profile):
        if isinstance(profile, dict):
            st.write(f"Name: {profile.get('Name')}")
            st.write(f"Headline: {profile.get('Headline')}")
            st.write(f"Location: {profile.get('Location')}")
        else:
            st.error("Failed to fetch LinkedIn profile.")


    @staticmethod
    def display_whois_table(whois_data):
        whois_table = {}
        lines = whois_data.split('\n')
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                whois_table[key.strip()] = value.strip()

        # Remove rows where value is '0'
        whois_table = {k: v for k, v in whois_table.items() if v != '0'}

        st.table({"WHOIS Record": list(whois_table.keys()), "WHOIS Data": list(whois_table.values())})

    @staticmethod
    def display_dns_table(dns_records):
        st.table({"DNS Record": list(dns_records.keys()), "DNS Data": [', '.join(values) for values in dns_records.values()]})

    @staticmethod
    def display_ip_info_table(ip_info):
        if isinstance(ip_info, dict):
            ip_table = {
                "IP Info": list(ip_info.keys()),
                "Data": list(ip_info.values())
            }
            st.table(ip_table)
        else:
            st.write(ip_info)
    
    @staticmethod
    def display_geolocation_table(geo_info):
        if isinstance(geo_info, dict):
            geo_table = {
                "Geolocation Info": list(geo_info.keys()),
                "Data": list(geo_info.values())
            }
            st.table(geo_table)
        else:
            st.write(geo_info)

    @staticmethod
    def validate_email(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(regex, email))


