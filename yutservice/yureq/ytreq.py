from asyncore import read
import googleapiclient.discovery
from httplib2 import GoogleLoginAuthentication
from yutservice.utils.readyaml import read_config_yaml

api_service_name = 'youtube'
API_KEY = read_config_yaml()['KEY']
api_version = "v3"

youtube = googleapiclient.discovery.build(
    serviceName=api_service_name,
    version=api_version,
    developerKey=API_KEY,
)

request = youtube.search().list(
    part='snippet',
    q='Whistling Dissel',
    maxResults=3,
    order='date',
    type='video',
)

responce = request.execute()
print(dict(responce))
