import os

import googleapiclient.discovery

from youtubedev.settings import YT_API


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = YT_API

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def youtube_request_channel(channel_id, username, parts='contentDetails,statistics'):
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

    return response['items'][0]


def youtube_request_playlist(playlist_id, nextPageToken=''):
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

    return response


def youtube_request_video(video_id):
    request = youtube.videos().list(
        part="statistics, snippet",
        id=video_id
    )
    response = request.execute()

    if response['pageInfo']['totalResults'] == 0:
        return None
    else:
        return response['items'][0]
