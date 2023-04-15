from oauth2client.service_account import ServiceAccountCredentials
import os
import glob
import json
import requests


class IndexingGoogle:
    SCOPES = ['https://www.googleapis.com/auth/indexing']

    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def set_credentials(self, credentials_file):
        self.credentials_file = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes=IndexingGoogle.SCOPES)

    def get_links(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            links = [link.strip() for link in file.readlines()]
        return links

    def index_url(self, url):
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        content = {'url': url.strip(), 'type': "URL_UPDATED"}
        json_ctn = json.dumps(content)
        response = requests.post(ENDPOINT, params={'access_token': self.credentials_file}, data=json_ctn)

        result = json.loads(response.content.decode())
        if "error" in result:
            return f"Error({result['error']['code']} - {result['error']['status']}): {result['error']['message']}"
        else:
            return f"urlNotificationMetadata.url: {result['urlNotificationMetadata']['url']}\n" \
                   f"urlNotificationMetadata.latestUpdate.url: {result['urlNotificationMetadata']['latestUpdate']['url']}\n" \
                   f"urlNotificationMetadata.latestUpdate.type: {result['urlNotificationMetadata']['latestUpdate']['type']}\n" \
                   f"urlNotificationMetadata.latestUpdate.notifyTime: {result['urlNotificationMetadata']['latestUpdate']['notifyTime']}"

    def send_urls(self, urls):
        if not self.credentials_file:
            return "Error: Credentials file not set"
        try:
            for url in urls:
                result = self.index_url(url)
                print(result)
        except Exception as ex:
            print(ex)