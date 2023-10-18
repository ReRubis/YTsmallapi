from asyncore import read
from re import search
import requests
from yutservice.config import CONFIG

API_KEY = CONFIG['KEY']


def search_for_videos(
    q: str,
    pageToken: str = None,
    publishedAfter: str = None,
    publishedBefore: str = None
):
    """Makes a YouTube API call"""
    search_params = {
        'key': API_KEY,
        'q': q,  # Search query
        'part': 'snippet',
        'type': 'video',
        'maxResults': 10,
        'pageToken': pageToken,
        'publishedAfter': publishedAfter,
        'publishedBefore': publishedBefore,
    }
    search_url = 'https://www.googleapis.com/youtube/v3/search'

    # Send the search request
    response = requests.get(search_url, params=search_params)

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        # for item in data['items']:
        #     video_id = item['id']['videoId']
        #     video_title = item['snippet']['title']
        #     video_description = item['snippet']['description']
        #     channel_title = item['snippet']['channelTitle']
        #     video_thumbnail = item['snippet']['thumbnails']['default']['url']
        return data
    else:
        print(f'Request failed with status code {response.status_code}')
        return response.status_code
