import datetime as dt
from datetime import timedelta

import pytz
from pytz import timezone
import requests
import base64
import six

client_id = '84f79134cc6341df9ee8c8a43cca3ec7'
client_secret = 'b48317acf809490db2e8b021b85ade71'

basic_code = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
basic_code = basic_code.decode('ascii')

refresh_token = 'AQCY4DKQcCvcet5-QoGPNci-__YH72hwQoLANfLhg0DR7gZbFDgkguuF-EjFphu_7iFVVfxVPRt83lCLRS-872WN_Pofbya2TtYcpnbPxKioWe91GjDhzAW09Efmad0x6f4'

redirect_uri = 'https://pitouteng.github.io/blank_html/'


def get_refresh_token():
    '''
    endpoint_code currently expired
    URL for getting short lived endpoint_code
    https://accounts.spotify.com/authorize?client_id=84f79134cc6341df9ee8c8a43cca3ec7&response_type=code&redirect_uri=https%3A%2F%2Fpitouteng.github.io%2Fblank_html%2F&scope=user-read-recently-played%20user-read-email&state=34fFs29kd0
    '''
    endpoint_code = 'AQC29ez1Q4znvFSkBKSwzfzY79hEwdzfHkzwcfLbxygtlBxFWnpbs6ItJFRC6ApXZNpuPvle1t77SwbS_jJ60zuNgJFbXkqk7kFv24sJw3qgyitWc9CuyplOvxuWL4zpRR1-JZFl3u8l6U-gL49Iu825eOGxYGOyop76MYc_OFvqsZIJuYbMK7orIQKjkNhrX08-y71f9dF_tOIx7sapIJmKokUeNYHvPcxGdvA5IYRpI2mMyXhQbnTtG99upraXpr67KrV57tq-'

    headers = {
        'Authorization': 'Basic ' + basic_code,
    }

    data = {
      'grant_type': 'authorization_code',
      'code': endpoint_code,
      'redirect_uri': redirect_uri
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    print(response.json())
    return response


def get_token(refresh_token):
    headers = {
        'Authorization': 'Basic ' + basic_code,
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    data = response.json()
    return data['access_token']


def make_spotify_api_request(access_token):
    """
    this function make spotify api get request with given access token
    :param access_token: token has to have user-read-recently-played scope
    :return:
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }
    params = (
        ('limit', '10'),
    )
    response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers, params=params)
    data = response.json()
    return data


def get_my_spotify_recently_played_song_dict():
    song_dict = {}
    access_token = get_token(refresh_token)
    data = make_spotify_api_request(access_token)
    for item in data['items']:
        song_id = item['track']['id']
        string_date = item['played_at']
        # date = get_date(string_date)
        date = convert_my_iso_8601(string_date, timezone('US/Eastern'))
        if date.date() == get_today_date():
            played_at = 'Today - ' + date.strftime('%I:%M %p') + ' EST'
        elif date.date() == get_yesterday_date():
            played_at = 'Yesterday - ' + date.time().strftime('%I:%M %p') + ' EST'
        else:
            played_at = date.strftime('%m/%d/%Y - %I:%M %p') + ' EST'

        song_dict[song_id] = played_at
    return song_dict


def get_date(date_string):
    date_string = date_string.split('.')[0]
    datetime_object = dt.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
    return datetime_object


def get_today_date():
    my_date = dt.datetime.now(pytz.timezone('US/Eastern'))
    return my_date.date()


def get_yesterday_date():
    today = dt.datetime.now(pytz.timezone('US/Eastern'))
    return today.date() - timedelta(days=1)


def convert_my_iso_8601(iso_8601, tz_info):
    assert iso_8601[-1] == 'Z'
    iso_8601 = iso_8601[:-1] + '000'
    iso_8601_dt = dt.datetime.strptime(iso_8601, '%Y-%m-%dT%H:%M:%S.%f')
    return iso_8601_dt.replace(tzinfo=timezone('UTC')).astimezone(tz_info)



