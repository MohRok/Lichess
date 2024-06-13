import requests
import base64
import xml.etree.ElementTree as ET
from lxml import etree

# WebCenter-Konfiguration
URL = "https://essitymedical.esko-saas.com/WebCenter/dashboard.jsp?dashboardId=00002_0000000507&00002_0000000507-TabLayoutContentBlock0=ButtonBlock4"
GET_PROJECTS_URL = f"{URL}/GetProjects.jsp"

USERNAME = "DEHMOUU"
PASSWORD = "Mohamad_22912"
# Base64-Encode des Passworts
encoded_password = base64.b64encode(PASSWORD.encode()).decode()

# 1. Sitzung öffnen
def open_session():
    url = f"{URL}/j_spring_security_check"
    payload = {
        'j_username': USERNAME,
        'j_password': encoded_password
    }
    response = requests.post(url, data=payload, allow_redirects=False)  # Deaktiviere Redirects vorerst
    if response.status_code == 302 and 'JSESSIONID' in response.cookies:
        session_id = response.cookies.get('JSESSIONID')
        print("Sitzung geöffnet. Session ID:", session_id)
        return session_id
    else:
        print("Fehler beim Öffnen der Sitzung.")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None

# 2. Projekte abrufen und in XML speichern
def get_and_save_projects(session_id):
    offset = 0
    all_projects = []
    
    while True:
        params = {
            'username': USERNAME,
            'password': encoded_password,
            'offset': offset
        }
        response = requests.get(GET_PROJECTS_URL, params=params)
        if response.status_code == 200:
            projects_xml = response.text
            
            # Versuche, die XML-Daten zu bereinigen
            cleaned_xml = cleanup_xml(projects_xml)
            if cleaned_xml is None:
                print("Fehler beim Bereinigen der XML-Daten.")
                break
            
            root = ET.fromstring(cleaned_xml)
            projects = root.findall('.//project')
            if not projects:
                print("Keine Projekte mehr gefunden.")
                break  # Keine Projekte mehr gefunden, Abbruch der Schleife
            all_projects.extend(projects)
            offset += len(projects)
        else:
            print(f"Fehler beim Abrufen der Projekte. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            break
    
    # Erstelle XML-Dokument und speichere es
    if all_projects:
        root = ET.Element("projects")
        for project in all_projects:
            root.append(project)
        
        xml_tree = ET.ElementTree(root)
        xml_tree.write("projects_data.xml", encoding="utf-8", xml_declaration=True)
        print("XML-Daten in Datei 'projects_data.xml' gespeichert.")
    else:
        print("Keine Projekte gefunden oder Fehler beim Abrufen.")



# Funktion zur Bereinigung der XML-Daten
def cleanup_xml(xml_string):
    try:
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(xml_string, parser=parser)
        return etree.tostring(root, encoding="utf-8", pretty_print=True).decode()
    except etree.XMLSyntaxError as e:
        print(f"XMLSyntaxError beim Parsen der XML-Daten: {e}")
        return None

# 3. Sitzung schließen
def close_session(session_id):
    url = f"{URL}/CloseSession.jsp"
    params = {
        'sessionID': session_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Sitzung geschlossen.")
    else:
        print("Fehler beim Schließen der Sitzung.")

def main():
    session_id = open_session()
    if session_id:
        get_and_save_projects(session_id)
        close_session(session_id)

if __name__ == "__main__":
    main()

