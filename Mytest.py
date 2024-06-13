import requests
import base64
import xml.etree.ElementTree as ET

URL = "https://essitymedical.esko-saas.com/WebCenter/dashboard.jsp?dashboardId=00002_0000000507&00002_0000000507-TabLayoutContentBlock0=ButtonBlock4"
GET_PROJECTS_URL = f"{URL}/GetProjects.jsp"

USERNAME = "DEHMOUU"
PASSWORD = "Mohamad_22912"
encoded_password = base64.b64encode(PASSWORD.encode()).decode()

def open_session():
    url = f"{URL}/j_spring_security_check"
    payload = {
        'j_username': USERNAME,
        'j_password': encoded_password
    }
    try:
        response = requests.post(url, data=payload, allow_redirects=False)
        response.raise_for_status()
        if response.status_code == 302 and 'JSESSIONID' in response.cookies:
            session_id = response.cookies.get('JSESSIONID')
            print("Session opened. Session ID:", session_id)
            return session_id
        else:
            print("Failed to open session.")
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error opening session:", e)
        return None

def get_projects(session_id):
    all_projects_xml = ""
    cur_page = 1
    try:
        while True:
            params = {
                'username': USERNAME,
                'password': encoded_password,
                'type': '2',  # Projects I am in
                'curpage': str(cur_page)
            }
            headers = {
                'Cookie': f'JSESSIONID={session_id}'  # Include session ID in headers
            }
            response = requests.get(GET_PROJECTS_URL, params=params, headers=headers)
            response.raise_for_status()
            
            # Check if the response content is HTML (indicating an error page)
            if 'html' in response.headers.get('content-type', '').lower():
                print("Received HTML instead of XML. Possible error page.")
                print(f"HTML content: {response.text}")
                return None
            
            projects_xml = response.text
            all_projects_xml += projects_xml
            root = ET.fromstring(projects_xml)
            num_pages = int(root.find('totalpages').text)
            if cur_page >= num_pages:
                break
            cur_page += 1
    except requests.exceptions.RequestException as e:
        print(f"Request error retrieving projects: {e}")
        return None
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        print(f"Faulty XML snippet: {projects_xml[:100]}")  # Print first 100 characters of XML
        return None
    except Exception as e:
        print(f"Error retrieving projects: {e}")
        return None

    return all_projects_xml


def save_xml_to_file(xml_data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(xml_data)
        print(f"XML data saved to '{filename}'.")
    except IOError as e:
        print(f"Error saving XML to file '{filename}': {e}")

def close_session(session_id):
    url = f"{URL}/CloseSession.jsp"
    params = {
        'sessionID': session_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print("Session closed.")
    except requests.exceptions.RequestException as e:
        print("Error closing session:", e)


def main():
    session_id = open_session()
    if session_id:
        projects_xml = get_projects(session_id)
        if projects_xml:
            save_xml_to_file(projects_xml, 'projects_i_am_in.xml')
        close_session(session_id)



if __name__ == "__main__":
    main()