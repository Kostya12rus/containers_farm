import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def get_steam_profile_info(session: requests.Session = None, url_profile: str = 'https://steamcommunity.com/my') -> dict:
    if session:
        req = session.get(url=f'{url_profile}/?xml=1')
    else:
        req = requests.get(url=f'{url_profile}/?xml=1')
    if not req.ok: return {}

    soup = BeautifulSoup(req.text, 'html.parser')
    profile_fatalerror = soup.find('div', class_='profile_fatalerror')
    if profile_fatalerror: return {}

    root = ET.fromstring(req.text)
    def xml_to_dict(element):
        data = {}
        for child in element:
            item_data = xml_to_dict(child) if len(child) > 0 else child.text
            if child.tag in data:
                if type(data[child.tag]) is list:
                    data[child.tag].append(item_data)
                else:
                    data[child.tag] = [data[child.tag], item_data]
            else:
                data[child.tag] = item_data
        return data

    return xml_to_dict(root)
