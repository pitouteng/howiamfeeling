from django.shortcuts import render
from string import Template

import my_spotify_authorization_code

# Create your views here.
from django.http import HttpResponse


def index(request):
    song_dict_iframe = {}
    iframe_template = '<iframe src="https://open.spotify.com/embed/track/${song_id}" width="500" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
    song_dict = my_spotify_authorization_code.get_my_spotify_recently_played_song_dict()

    for song_id, played_at in song_dict.items():
        iframe = Template(iframe_template).safe_substitute(song_id=song_id)
        song_dict_iframe[iframe] = played_at
    return render(request, 'songs/index.html', {"song_dict": song_dict_iframe})
