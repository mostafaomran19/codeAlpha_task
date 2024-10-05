import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse

# Spotify API credentials
CLIENT_ID = "a477f3cc36024d5ba07065fc7543f252"
CLIENT_SECRET = "56f58122bce1425d96010beda24c0dda"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Customizing the page configuration
st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")

# Applying background color and custom CSS styles for beauty
def set_background():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f5;
            color: #333;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #663399;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
        }
        .stSelectbox {
            border-radius: 10px;
            background-color: #f0e6ff;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

set_background()

# Function to get the album cover URL of a song
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit app header with styled title
st.title('🎶 Music Recommender System')

# Load the pre-trained models
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for song selection, with a styled selectbox
st.subheader("Select a song to get recommendations:")
music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list,
    key="selectbox",
    help="Choose a song to get similar recommendations"
)

# Display recommendations when the button is clicked
if st.button('Show Recommendation'):
    st.write("Here are some songs you might like:")
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        col.text(recommended_music_names[idx])
        col.image(recommended_music_posters[idx])
        # Encode the song name for the URL
        song_url_encoded = urllib.parse.quote(recommended_music_names[idx])
        col.markdown(f"[🎧 Open in Spotify](https://open.spotify.com/search/{song_url_encoded})")

# Footer style
st.markdown("""
    <style>
    footer {
        visibility: hidden;
    }
    .footer-content {
        color: #ffffff;
        text-align: center;
        padding: 20px;
        background-color: #333333;
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
    }
    </style>
    <div class="footer-content">
        Made with ❤️ by Mostafa Omran
    </div>
""", unsafe_allow_html=True)
