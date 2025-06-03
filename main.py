from decouple import config
import base64
import requests



client_id = config('SPOTIFY_CLIENT_ID', cast=str)
client_secret = config('SPOTIFY_CLIENT_SECRET', cast=str)



class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        form_data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=form_data)
        if response.ok:
            self.client_credentials = response.json()
            return self.client_credentials

        else:
            raise Exception(response.status_code, response.json())

    def get_access_token(self):
        client_credentials = self.get_client_credentials()
        access_token = client_credentials['access_token']
        return access_token

    def get_auth_header(self):
        client_credentials = self.get_client_credentials()
        access_token = client_credentials['access_token']
        return {
            "Authorization": f"Bearer {access_token}"

        }

    def search_for_artist(self):
        artist_name: str = input("Search by  artist name: ")
        headers = self.get_auth_header()
        url = "https://api.spotify.com/v1/search"
        query = f"?q={artist_name}&type=artist&limit=1"

        query_url = f"{url}{query}"
        response = requests.get(query_url, headers=headers)
        artist_id = response.json()["artists"]["items"][0]["id"]
        return artist_id

    def search_for_track(self):
        track_name: str = input("Search by track name: ")
        headers = self.get_auth_header()
        url = "https://api.spotify.com/v1/search"
        query = f"?q={track_name}&type=track&limit=1"
        query_url = f"{url}{query}"
        response = requests.get(query_url, headers=headers)
        track_id = response.json()['tracks']['items'][0]['id']
        return track_id

    def get_track(self):
        track_id = self.search_for_track()
        headers = self.get_auth_header()
        if track_id:
            url = f"https://api.spotify.com/v1/tracks/{track_id}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.json())

            else:
                result = response.json()
                return {
                    "id": track_id,
                    "name": result["name"],
                    "artists": result["artists"],
                    "artist_name": result["artists"][0]["name"],
                }

        else:
            self.get_track()

    def play_music(self):
        headers = self.get_auth_header()
        url = "https://api.spotify.com/v1/player"
        response = requests.get(url, headers=headers)


        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.status_code, response.json())




    def getProfile(self, access_token=None):
        access_token = self.get_access_token()

        if access_token:
            url = "https://api.spotify.com/v1/me"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get(url, headers=headers)
            if response.ok:
                return response.json()
            else:
                raise Exception(response.status_code, response.json()['error']['message'])
        else:
            raise Exception("Access Token Error")


if __name__ == '__main__':
    spotify = SpotifyClient(client_id, client_secret)
    #print(spotify.get_access_token())
    print(spotify.search_for_artist())
    print(spotify.search_for_track())
    print(spotify.get_track())


