import io
import requests
from swiftclient.service import SwiftService, SwiftUploadObject


css_template = """
.status a[href^='{0}'] {{
    border-bottom: solid 1px {{3}} ;
}}
.status a[href^='{0}']
.display-name:before {{
    color: {2} !important ;
    background-color: {3} !important ;
    content: '[{1}]' !important ;
}}
"""

if __name__ == '__main__':
    sheet_url = 'https://docs.google.com/spreadsheets/d/すぷれっどしーとのID/export?format=csv'
    container_name = 'コンテナ名'

    auth = {
        'auth_version': '2.0',
        'os_username': '',
        'os_password': '',
        'os_tenant_name': '',
        'os_auth_url': '',
    }

    ret = requests.get(sheet_url)
    ret.encoding = ret.apparent_encoding
    sheet = ret.text

    out = ''
    for line in sheet.splitlines():
        if line.startswith('#'):
            continue

        sp = line.split(',')
        out += css_template.format(*sp)

    with SwiftService(options=auth) as swift, io.BytesIO(out.encode(encoding='utf-8')) as s:
        obj = SwiftUploadObject(source=s, object_name='instance_tip.css')

        ret = swift.upload(container=container_name, objects=[obj])
        print(list(ret))

