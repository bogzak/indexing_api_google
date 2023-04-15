from oauth2client.service_account import ServiceAccountCredentials
import json
import requests


class IndexingGoogle:
    SCOPES = ['https://www.googleapis.com/auth/indexing']

    def __init__(self):
        self.credentials_file = None

    def set_credentials(self, credentials):
        credentials_dict = json.loads(credentials)
        self.credentials_file = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scopes=IndexingGoogle.SCOPES)

    def get_links(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            links = [link.strip() for link in file.readlines()]
        return links

    def index_url(self, url):
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        content = {'url': url.strip(), 'type': "URL_UPDATED"}
        json_ctn = json.dumps(content)
        # response = requests.post(ENDPOINT, params={'access_token': self.credentials_file}, data=json_ctn)
        response = requests.post(
            ENDPOINT,
            headers={'Authorization': 'Bearer ' + self.credentials_file.get_access_token().access_token},
            json=content
        )
        result = json.loads(response.content.decode())
        if 'error' in result:
            return f'Error({result["error"]["code"]} - {result["error"]["status"]}): {result["error"]["message"]}'
        else:
            return f'URL: {result["urlNotificationMetadata"]["url"]}\n \
                   latestUpdate.url: {result["urlNotificationMetadata"]["latestUpdate"]["url"]}\n \
                   Type: {result["urlNotificationMetadata"]["latestUpdate"]["type"]}\n \
                   Time: {result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]}'

    def send_urls(self, urls):
        if not self.credentials_file:
            return 'Error: Credentials file not set'
        try:
            results = []
            for url in urls:
                result = self.index_url(url)
                results.append(result)
            return results
        except Exception as ex:
            return [str(ex)]