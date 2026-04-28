from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

def get_random_anime():
    try:
        
        random_page = random.randint(1, 5)
        
        params = {
            'start_date': '2010-01-01',
            'order_by': 'score',
            'sort': 'desc',
            'sfw': 'true',
            'page': random_page
        }
        
        
        response = requests.get("https://api.jikan.moe/v4/anime", params=params, timeout=5)
        
        if response.status_code == 200:
            data_list = response.json().get('data', [])
            if data_list:
                
                data = random.choice(data_list)
                return {
                    'title': data.get('title_japanese') or data.get('title'),
                    'english_title': data.get('title_english'),
                    'image': data['images']['jpg']['large_image_url'],
                    'score': data.get('score', 'N/A'),
                    'synopsis': data.get('synopsis', 'ไม่มีเรื่องย่อ'),
                    'url': data.get('url', '#')
                }
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    return None
@app.route('/')
def index():
    anime = get_random_anime()
    return render_template('index.html', anime=anime)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
