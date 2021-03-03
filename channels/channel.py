# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery

from youtubedev.settings import YT_API


def youtube_request_channel(channel_id, username, parts='statistics'):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = YT_API

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
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
    if parts == 'statistics':
        return response['items'][0]['statistics']
    if parts == 'contentDetails':
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        return response