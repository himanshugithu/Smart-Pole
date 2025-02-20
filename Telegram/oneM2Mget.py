import requests

def getTemperature():
    resource_url = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-SR/SR-AQ/SR-AQ-KH95-00/Data/la"
    headers = {"X-M2M-Origin": "iiith_guest:iiith_guest", "Content-Type": "application/json"}

    try:
        response = requests.get(resource_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

    except requests.exceptions.HTTPError as err:
        print(f"GET request failed with status code: {err.response.status_code}")
        print(err.response.text)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

    if response.status_code == 200:
        print("GET request successful!")
        data = response.json()  # Assuming the response is JSON data
        return data['m2m:cin']['con'].split(',')
    else:
        print(f"Unexpected status code: {response.status_code}")
        return None
    



def getairquality():
    resource_url = "https://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-AQ/AQ-SN00-00/Data/la"
    headers = {"X-M2M-Origin": "iiith_guest:iiith_guest", "Content-Type": "application/json"}

    try:
        response = requests.get(resource_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

    except requests.exceptions.HTTPError as err:
        print(f"GET request failed with status code: {err.response.status_code}")
        print(err.response.text)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

    if response.status_code == 200:
        print("GET request successful!")
        data = response.json()  # Assuming the response is JSON data
        return data['m2m:cin']['con'].split(',')
    else:
        print(f"Unexpected status code: {response.status_code}")
        return None
    


if __name__ == "__main__":
    pass
