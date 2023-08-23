#!/usr/bin/python3

import requests
import os
import re
import shlex

def __main__():
    VIDEO_ID = input('Video id: ')
    API_KEY = input('YouTube Data API v3 key (empty if use no-key service): ')
    COMMENT_REGEX = input('Comment regex: ')
    OPEN_IN_FIREFOX = input('Open comment in firefox (yes or no): ') == 'yes'

    nextPageToken = ''
    commentRegexCompiled = re.compile(COMMENT_REGEX)

    def getContentFromURL(url):
        if API_KEY != '':
            url = f'https://www.googleapis.com/youtube/v3/{url}&key={API_KEY}'
        else:
            url = f'https://yt.lemnoslife.com/noKey/{url}'
        data = requests.get(url).json()
        return data

    def treatComment(comment):
        textOriginal = comment['snippet']['textOriginal']
        if commentRegexCompiled.search(textOriginal):
            id = comment['id']
            url = f'https://www.youtube.com/watch?v={VIDEO_ID}&lc={id}'
            print(f'{url} {textOriginal}')
            if OPEN_IN_FIREFOX:
                os.system(f'firefox -new-tab {shlex.quote(url)}')

    while True:
        data = getContentFromURL(f'commentThreads?part=snippet,replies&videoId={VIDEO_ID}&maxResults=100&pageToken={nextPageToken}')
        for item in data['items']:
            snippet = item['snippet']
            treatComment(snippet['topLevelComment'])
            totalReplyCount = snippet['totalReplyCount']
            if totalReplyCount > 5:
                parentId = item['id']
                commentsNextPageToken = ''
                while True:
                    commentsData = getContentFromURL(f'comments?part=snippet&parentId={parentId}&maxResults=100&pageToken={commentsNextPageToken}')
                    for item in commentsData['items']:
                        treatComment(item)
                    if not 'nextPageToken' in commentsData:
                        break
                    commentsNextPageToken = commentsData['nextPageToken']
            else:
                # This condition is to manage properly `item`s without `replies` entry.
                if totalReplyCount > 0:
                    for comment in item['replies']['comments']:
                        treatComment(comment)
        if not 'nextPageToken' in data:
            break
        nextPageToken = data['nextPageToken']

