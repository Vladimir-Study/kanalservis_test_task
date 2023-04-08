from datetime import datetime
import requests
import xml.etree.ElementTree as ET


def get_quotes() -> dict:
    today = datetime.strftime(datetime.today(), '%d/%m/%Y')
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={today}"
    responce = requests.get(url)
    three = ET.fromstring(responce.text)
    for child in three:
        if child.attrib['ID'] == 'R01235':
            return child[4].text


if __name__ == '__main__':
    pass