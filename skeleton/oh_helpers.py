import urllib.request, json

class oh_helper:

    def __init__(self, oh_member):
        self.oh_member = oh_member

    def get_oh_member(self):
        return self.oh_member

    def set_oh_member(self, oh_member):
        self.oh_member = oh_member

    def build_experiences_list(self):
        experiences_array = []

        file_urls = self.oh_member.list_files()

        for file_url in file_urls:
            with urllib.request.urlopen(file_url) as url:
                data = json.loads(url.read().decode())
            if data is not None:
                return data
            else:
                # django error here ideally
                print("error")
                return None

