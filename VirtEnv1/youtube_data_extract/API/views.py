from http.client import HTTPResponse
import stat
from django.http import HttpResponse
from django.shortcuts import render
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from django.templatetags.static import static
import json

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
#TODO: Find a way to make this path relative instead of hardcoded to my machine
CLIENT_SECRETS_FILE = r'C:\Users\morga\OneDrive\Documents\GitHub\CPT-200-SCCC\VirtEnv1\youtube_data_extract\API\static\secret file.json'

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    ##credentials = flow.run_console()
    credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(
    **kwargs
    ).execute()

    return response

def api(request):
    # Disable OAuthlib's HTTPs verification when running locally.
    # *DO NOT* leave this option enabled when running in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    youtubeAnalytics = get_service()

    response2 = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="api_return.txt"'},
    )
    
    #TODO: Figure out a way to write to a CSV in a better format
    writer = response2.write(json.dumps(   
    (execute_api_request(
    youtubeAnalytics.reports().query,
    ids='channel==MINE',
    startDate='2017-01-01',
    endDate='2017-12-31',
    metrics='estimatedMinutesWatched,views,likes,subscribersGained',
    dimensions='day',
    sort='day'
    ))))

    return response2