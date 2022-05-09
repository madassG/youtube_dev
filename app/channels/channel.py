import os
import logging
import googleapiclient.discovery

from config.settings import YT_API
from datetime import datetime

logger = logging.getLogger(__name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = YT_API

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def youtube_request_channel(channel_id, username, parts='contentDetails,statistics,brandingSettings'):
    """ Youtube API request function to get channel info """
    if username:
        request = youtube.channels().list(
            part=parts,
            forUsername=channel_id
        )
    else:
        request = youtube.channels().list(
            part=parts,
            id=channel_id
        )

    response = request.execute()
    if response_check(response) is not None:
        logger.error(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} : youtube_request_channel {channel_id}"
                     f" - Error code : {response_check(response)}")
        return None
    if 'items' not in response:
        return None
    return response['items'][0]


def youtube_request_playlist(playlist_id, nextPageToken=''):
    """ Youtube API request function to get playlist info """
    if nextPageToken:
        request = youtube.playlistItems().list(
            part="contentDetails",
            pageToken=nextPageToken,
            playlistId=playlist_id
        )
    else:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id
        )
    response = request.execute()
    if response_check(response) is not None:
        logger.error(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} : youtube_request_playlist {playlist_id}"
                     f" - Error code : {response_check(response)}")
        return None
    return response


def youtube_request_video(video_id):
    """ Youtube API request function to get video info """
    request = youtube.videos().list(
        part="statistics, snippet",
        id=video_id
    )
    response = request.execute()
    if response_check(response) is not None:
        logger.error(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} : youtube_request_video {video_id}"
                     f" - Error code : {response_check(response)}")
        return None
    if response['pageInfo']['totalResults'] == 0:
        return None
    else:
        if 'items' not in response:
            return None
        return response['items'][0]


def response_check(response):
    if response.get('error'):
        return response['error']['code']
    return None
