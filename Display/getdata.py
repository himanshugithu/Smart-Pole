import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
M2M_ORIGIN = os.getenv("M2M_ORIGIN")
if not M2M_ORIGIN:
    raise ValueError("M2M_ORIGIN is missing in the .env file.")

def load_existing_data(filename="result.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: Corrupted JSON file, starting fresh.")
                return None
    return None

def fetch_and_process_data(urls, index_mapping, filename="result.json"):
    existing_data = load_existing_data(filename)

    def clean_and_convert(value):
        try:
            return float(value.strip(" []'\""))
        except ValueError:
            print(f"Error processing value: {value}")
            return None  # Return None instead of 0

    def fetch_data(session, resource_url):
        headers = {"X-M2M-Origin": M2M_ORIGIN, "Content-Type": "application/json"}
        try:
            response = session.get(resource_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_data = response.json()
            raw_data = response_data.get('m2m:cin', {}).get('con', '')
            return raw_data.split(',')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {resource_url}: {e}")
            return None  # Return None if fetching fails

    def process_url_with_indices(session, url, indices):
        raw_data = fetch_data(session, url)
        if raw_data is None:
            return None  # Return None if fetching fails
        cleaned_data = [clean_and_convert(value) for value in raw_data]
        return [cleaned_data[index] if index < len(cleaned_data) and cleaned_data[index] is not None else None for index in indices]

    all_data = []
    with requests.Session() as session:
        for url, indices in index_mapping.items():
            processed_data = process_url_with_indices(session, url, indices)
            if processed_data is None:
                print("Error occurred, keeping old JSON data.")
                return existing_data  # Retain old data if fetching fails
            all_data.extend(processed_data)

    if len(all_data) < 10 or any(val is None for val in all_data):
        print("Insufficient valid data fetched, keeping old JSON data.")
        return existing_data

    data_dict = {
        "CO2": all_data[0],
        "Temperature": all_data[1],
        "Humidity": all_data[2],
        "Water Quality": all_data[3],
        "Energy": all_data[4],
        "Water Flow": all_data[5],
        "AQI": all_data[6],
        "Strength": all_data[7],
        "Signal": all_data[8],
        "ESG": all_data[9]
    }

    with open(filename, "w") as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(data_dict)
    return data_dict

if __name__ == "__main__":
    urls = [
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-AQ/SR-AQ-KH95-00/Data/la",
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WD/WM-WD-KH95-00/Data/la",
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN02-00/Data/la",
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WF/WM-WF-KB04-70/Data/la",
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-AQ/AQ-SN00-00/Data/la",
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WN/WN-L001-03/Data/la",
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN95-00/Data/la",
    ]

    index_mapping = {
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-AQ/SR-AQ-KH95-00/Data/la": [1, 2, 3],
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WD/WM-WD-KH95-00/Data/la": [4],
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN02-00/Data/la": [1],
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WF/WM-WF-KB04-70/Data/la": [2],
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-AQ/AQ-SN00-00/Data/la": [11],
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WN/WN-L001-03/Data/la": [2, 4],
        "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SL/SL-VN95-00/Data/la": [1],
    }
    while True:
        result = fetch_and_process_data(urls, index_mapping)
        if result:
            print(result)
