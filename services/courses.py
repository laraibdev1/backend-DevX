# services/courses.py
from flask import Blueprint, jsonify
import requests
import os

# Define the blueprint (make sure the name matches what you import in __init__.py)
courses_bp = Blueprint('courses', __name__)

# Function to fetch video details using the YouTube API
def get_video_details(video_url):
    # Extract video ID from the URL
    video_id = video_url.split('v=')[1]
    youtube_api_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={os.getenv("YOUTUBE_API_KEY")}'
    
    # Send a request to the YouTube API
    response = requests.get(youtube_api_url)
    
    # Return the JSON response from YouTube API
    return response.json()

# Route to fetch Python-related YouTube videos
@courses_bp.route('/python', methods=['GET'])
def get_python_videos():
    # List of video URLs to fetch details for
    video_urls = [
        "https://www.youtube.com/watch?v=nLRL_NcnK-4",
        "https://www.youtube.com/watch?v=HGOBQPFzWKo",
        "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "https://www.youtube.com/watch?v=rfscVS0vtbw",
        "https://www.youtube.com/watch?v=_uQrJ0TkZlc"
    ]

    videos_data = []

    # Iterate over each video URL
    for url in video_urls:
        # Get video details from YouTube API
        details = get_video_details(url)
        
        # Extract necessary data from the API response
        if details.get('items'):
            snippet = details['items'][0]['snippet']
            statistics = details['items'][0]['statistics']
            
            # Prepare video information without the description
            video_info = {
                "title": snippet['title'],
                "views": statistics.get('viewCount', 'N/A'),
                "likes": statistics.get('likeCount', 'N/A'),
                "url": url
            }

            # Append video info to the list
            videos_data.append(video_info)
    
    # Return the videos data as a JSON response
    return jsonify({"videos": videos_data})
