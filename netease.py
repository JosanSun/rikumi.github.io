# -*- coding: utf-8 -*-
import base64
import hashlib

import requests
from concurrent.futures import ProcessPoolExecutor
from requests import Session
from requests_futures.sessions import FuturesSession

session = FuturesSession(executor=ProcessPoolExecutor(max_workers=10), session=Session())


def netease_hymn():
    return """
    player's Game Over,
    u can abandon.
    u get pissed,
    get pissed,
    Hallelujah my King!
    errr oh! fuck ohhh!!!!
    """


def encrypted_id(dfs_id):
    x = [ord(i[0]) for i in netease_hymn().split()]
    y = ''.join([chr(i - 61) if i > 96 else chr(i + 32) for i in x])
    byte1 = bytearray(y, encoding='ascii')
    byte2 = bytearray(str(dfs_id), encoding='ascii')
    for i in range(len(byte2)):
        byte2[i] ^= byte1[i % len(byte1)]
    m = hashlib.md5()
    m.update(byte2)
    result = base64.b64encode(m.digest()).decode('ascii')
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result


def make_url(song_net, dfs_id):
    enc_id = encrypted_id(dfs_id)
    mp3_url = "http://%s/%s/%s.mp3" % (song_net, enc_id, dfs_id)
    return mp3_url


def netease_cloud_music(genre, rid, qlrc):
    if genre == "album":
        album_info = {}
        j = requests.get("http://music.163.com/api/album/%s?id=%s&csrf_token=" % (rid, rid),
                         headers={"Referer": "http://music.163.com/"}).json()
        album_info["artist"] = j['album']['artists'][0]['name']
        album_info["album"] = j['album']['name']
        album_info["pic_url"] = j['album']['picUrl']
        songs_info = []
        for i in j['album']['songs']:
            songs_info.append(get_song_info(i))
        album_info["songs_info"] = songs_info
        return album_info

    elif genre == "playlist":
        playlist_info = {}
        j = requests.get("http://music.163.com/api/playlist/detail?id=%s&csrf_token=" % rid,
                         headers={"Referer": "http://music.163.com/"}).json()
        playlist_info["playlist"] = j["result"]["name"]
        playlist_info["pic_url"] = j['result']['coverImgUrl']
        songs_info = []
        for i in j['result']['tracks']:
            songs_info.append(get_song_info(i))
        playlist_info["songs_info"] = songs_info
        return playlist_info

    elif genre == "song":
        j = requests.get("http://music.163.com/api/song/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid),
                         headers={"Referer": "http://music.163.com/"}).json()
        song_info = get_song_info(j["songs"][0])
        if qlrc == 1:
            try:
                lyric = netease_lyric_download(rid)
            except:
                lyric = None
            song_info["lyric"] = lyric
        else:
            pass
        return song_info

    elif genre == "program":
        j = requests.get("http://music.163.com/api/dj/program/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid),
                         headers={"Referer": "http://music.163.com/"}).json()
        song_info = get_song_info(j["program"]["mainSong"])
        return song_info

    elif genre == "radio":
        j = requests.get("http://music.163.com/api/dj/program/byradio/?radioId=%s&ids=[%s]&csrf_token=" % (rid, rid),
                         headers={"Referer": "http://music.163.com/"}).json()
        songs_info = []
        for i in j['programs']:
            songs_info.append(get_song_info(i["mainSong"]))
        return songs_info

    elif genre == "mv":
        j = requests.get("http://music.163.com/api/mv/detail/?id=%s&ids=[%s]&csrf_token=" % (rid, rid),
                         headers={"Referer": "http://music.163.com/"}).json()
        return netease_video_download(j["data"])

    return None


def get_song_info(song):
    song_net = 'p' + song['mp3Url'].split('/')[2][1:]
    if 'hMusic' in song and song['hMusic'] is not None:
        url_best = make_url(song_net, song['hMusic']['dfsId'])
    elif 'mp3Url' in song:
        url_best = song['mp3Url']
    elif 'bMusic' in song:
        url_best = make_url(song_net, song['bMusic']['dfsId'])
    else:
        url_best = ''
    try:
        title = song["name"]
        album = song["album"]["name"]
        pic_url = song["album"]["picUrl"]
        artist = song["artists"][0]["name"]
    except:
        title = None
        album = None
        pic_url = None
        artist = None
    return {"url_best": url_best, "title": title, "album": album, "pic_url": pic_url, "artist": artist}


def netease_video_download(vinfo):
    title = "%s - %s" % (vinfo['name'], vinfo['artistName'])
    url_best = sorted(vinfo["brs"].items(), reverse=True,
                      key=lambda x: int(x[0]))[0][1]
    pic_url = vinfo["cover"]
    return {"title": title, "url_best": url_best, "pic_url": pic_url}


def netease_lyric_download(rid):
    l = requests.get("http://music.163.com/api/song/lyric/?id=%s&lv=-1&csrf_token=" % rid,
                     headers={"Referer": "http://music.163.com/"}).json()
    lyric = l["lrc"]["lyric"].replace("\n", "\\n")
    return lyric


def netease_search(s):
    # t1 = time.time()
    sj = session.post("http://music.163.com/api/search/get/",
                      {"s": s, "limit": 100, "sub": "false", "type": 1, "offset": 0},
                      headers={"Referer": "http://music.163.com/"})
    aj = session.post("http://music.163.com/api/search/get/",
                      {"s": s, "limit": 100, "sub": "false", "type": 10, "offset": 0},
                      headers={"Referer": "http://music.163.com/"})
    pj = session.post("http://music.163.com/api/search/get/",
                      {"s": s, "limit": 100, "sub": "false", "type": 1000, "offset": 0},
                      headers={"Referer": "http://music.163.com/"})
    mj = session.post("http://music.163.com/api/search/get/",
                      {"s": s, "limit": 100, "sub": "false", "type": 1004, "offset": 0},
                      headers={"Referer": "http://music.163.com/"})
    rj = session.post("http://music.163.com/api/search/get/",
                      {"s": s, "limit": 100, "sub": "false", "type": 1009, "offset": 0},
                      headers={"Referer": "http://music.163.com/"})
    sjr = sj.result().json()
    ajr = aj.result().json()
    pjr = pj.result().json()
    mjr = mj.result().json()
    rjr = rj.result().json()
    # t2 = time.time()
    # print(t2-t1)
    songs_info = []
    albums_info = []
    playlists_info = []
    mvs_info = []
    radios_info = []
    try:
        for i in sjr["result"]["songs"]:
            if i["status"] < 0:
                pass
            else:
                song_info = {"song_id": i["id"], "name": i["name"], "album": i["album"]["name"],
                             "album_id": i["album"]["id"], "artist": i["artists"][0]["name"]}
                songs_info.append(song_info)
    except:
        pass
    try:
        for i in ajr["result"]["albums"]:
            if i["status"] < 0:
                pass
            else:
                album_info = {"album_id": i["id"], "name": i["name"], "artist": i["artists"][0]["name"]}
                albums_info.append(album_info)
    except:
        pass
    try:
        for i in pjr["result"]["playlists"]:
            playlist_info = {"playlist_id": i["id"], "name": i["name"], "trackCount": i["trackCount"],
                             "creator": i["creator"]["nickname"]}
            playlists_info.append(playlist_info)
    except:
        pass
    try:
        for i in mjr["result"]["mvs"]:
            mv_info = {"mv_id": i["id"], "name": i["name"], "artist": i["artists"][0]["name"]}
            mvs_info.append(mv_info)
    except:
        pass
    try:
        for i in rjr["result"]["djRadios"]:
            radio_info = {"radio_id": i["id"], "name": i["name"], "dj": i["dj"]["nickname"]}
            radios_info.append(radio_info)
    except:
        pass
    return [songs_info, albums_info, playlists_info, mvs_info, radios_info]


def song_search(s, limit):
    stype = 1
    data = {"s": s, "limit": limit, "sub": "false", "type": stype, "offset": 0}
    j = session.post("http://music.163.com/api/search/get/", data,
                     headers={"Referer": "http://music.163.com/"}).result().json()
    songs_info = []
    for i in j["result"]["songs"]:
        if i["status"] < 0:
            pass
        else:
            song_info = {"song_id": i["id"], "name": i["name"], "album": i["album"]["name"],
                         "album_id": i["album"]["id"], "artist": i["artists"][0]["name"]}
            songs_info.append(song_info)
    return songs_info


def album_search(s):
    limit = 100
    stype = 10
    data = {"s": s, "limit": limit, "sub": "false", "type": stype, "offset": 0}
    j = session.post("http://music.163.com/api/search/get/", data,
                     headers={"Referer": "http://music.163.com/"}).result().json()
    albums_info = []
    for i in j["result"]["albums"]:
        if i["status"] < 0:
            pass
        else:
            album_info = {"album_id": i["id"], "name": i["name"], "artist": i["artists"][0]["name"]}
            albums_info.append(album_info)
    return albums_info


def playlist_search(s):
    limit = 100
    stype = 1000
    data = {"s": s, "limit": limit, "sub": "false", "type": stype, "offset": 0}
    j = session.post("http://music.163.com/api/search/get/", data,
                     headers={"Referer": "http://music.163.com/"}).result().json()
    playlists_info = []
    for i in j["result"]["playlists"]:
        playlist_info = {"playlist_id": i["id"], "name": i["name"], "trackCount": i["trackCount"],
                         "creator": i["creator"]["nickname"]}
        playlists_info.append(playlist_info)
    return playlists_info


def mv_search(s):
    limit = 100
    stype = 1004
    data = {"s": s, "limit": limit, "sub": "false", "type": stype, "offset": 0}
    j = session.post("http://music.163.com/api/search/get/", data,
                     headers={"Referer": "http://music.163.com/"}).result().json()
    mvs_info = []
    for i in j["result"]["mvs"]:
        mv_info = {"mv_id": i["id"], "name": i["name"], "artist": i["artists"][0]["name"]}
        mvs_info.append(mv_info)
    return mvs_info


def radio_search(s):
    limit = 100
    stype = 1009
    data = {"s": s, "limit": limit, "sub": "false", "type": stype, "offset": 0}
    j = session.post("http://music.163.com/api/search/get/", data,
                     headers={"Referer": "http://music.163.com/"}).result().json()
    radios_info = []
    for i in j["result"]["djRadios"]:
        radio_info = {"radio_id": i["id"], "name": i["name"], "dj": i["dj"]["nickname"]}
        radios_info.append(radio_info)
    return radios_info


def api_v2(genre, s, qlrc):
    if genre == "song":
        if type(s) is int:
            return netease_cloud_music("song", s, qlrc)
        else:
            return netease_cloud_music("song", song_search(s, 1)[0]["song_id"], qlrc)
    else:
        return netease_cloud_music(genre, s, 0)
