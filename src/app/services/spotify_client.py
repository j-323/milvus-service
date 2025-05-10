import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.core.config import settings

_auth = SpotifyClientCredentials(
    client_id=settings.spotify.client_id,
    client_secret=settings.spotify.client_secret
)
_sp = spotipy.Spotify(auth_manager=_auth)

def fetch_spotify_features(artist: str, title: str) -> dict:
    q = f"artist:{artist} track:{title}"
    res = _sp.search(q=q, type="track", limit=1)
    items = res.get("tracks", {}).get("items", [])
    if not items:
        return {}
    track = items[0]
    feats = _sp.audio_features(track["id"])[0]
    return {
        "tempo": feats["tempo"],
        "key": feats["key"],
        "mode": feats["mode"],
        "time_signature": feats["time_signature"],
        "loudness": feats["loudness"]
    }