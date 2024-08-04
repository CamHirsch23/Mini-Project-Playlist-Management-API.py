from flask import Flask, request, jsonify

app = Flask(__name__)

# Data storage
songs = {}
playlists = {}

# Helper functions
def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half, key)
        merge_sort(right_half, key)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i][key] < right_half[j][key]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def binary_search(arr, key, value):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid][key] == value:
            return mid
        elif arr[mid][key] < value:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Song Endpoints
@app.route('/song', methods=['POST'])
def create_song():
    song_id = request.json['id']
    songs[song_id] = request.json
    return jsonify(songs[song_id]), 201

@app.route('/song/<song_id>', methods=['PUT'])
def update_song(song_id):
    if song_id in songs:
        songs[song_id].update(request.json)
        return jsonify(songs[song_id])
    return jsonify({'error': 'Song not found'}), 404

@app.route('/song/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id in songs:
        del songs[song_id]
        return jsonify({'message': 'Song deleted'})
    return jsonify({'error': 'Song not found'}), 404

@app.route('/song/<song_id>', methods=['GET'])
def get_song(song_id):
    if song_id in songs:
        return jsonify(songs[song_id])
    return jsonify({'error': 'Song not found'}), 404

# Playlist Endpoints
@app.route('/playlist', methods=['POST'])
def create_playlist():
    playlist_id = request.json['id']
    playlists[playlist_id] = {'id': playlist_id, 'songs': []}
    return jsonify(playlists[playlist_id]), 201

@app.route('/playlist/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    if playlist_id in playlists:
        return jsonify(playlists[playlist_id])
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlist/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    if playlist_id in playlists:
        playlists[playlist_id].update(request.json)
        return jsonify(playlists[playlist_id])
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlist/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id in playlists:
        del playlists[playlist_id]
        return jsonify({'message': 'Playlist deleted'})
    return jsonify({'error': 'Playlist not found'}), 404

# Additional Endpoints
@app.route('/playlist/<playlist_id>/add_song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    if playlist_id in playlists:
        song_id = request.json['song_id']
        if song_id in songs:
            playlists[playlist_id]['songs'].append(songs[song_id])
            return jsonify(playlists[playlist_id])
        return jsonify({'error': 'Song not found'}), 404
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlist/<playlist_id>/remove_song', methods=['POST'])
def remove_song_from_playlist(playlist_id):
    if playlist_id in playlists:
        song_id = request.json['song_id']
        playlists[playlist_id]['songs'] = [song for song in playlists[playlist_id]['songs'] if song['id'] != song_id]
        return jsonify(playlists[playlist_id])
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlist/<playlist_id>/sort_songs', methods=['POST'])
def sort_songs_in_playlist(playlist_id):
    if playlist_id in playlists:
        key = request.json['key']
        merge_sort(playlists[playlist_id]['songs'], key)
        return jsonify(playlists[playlist_id])
    return jsonify({'error': 'Playlist not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
