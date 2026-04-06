from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__)

# 🔥 Free Books API (Open Library)
BASE_URL = "https://openlibrary.org/search.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def get_books():
    try:
        # 🔥 Search different categories randomly
        queries = [
            "fiction", "programming", "python", "history", 
            "science", "adventure", "mystery", "romance"
        ]
        query = random.choice(queries)
        
        params = {
            'q': query,
            'limit': 10,
            'fields': 'title,author_name,cover_i,key'
        }
        
        response = requests.get(BASE_URL, params=params)
        books_data = response.json().get('docs', [])
        
        result = []
        for book in books_data[:8]:  # Top 8 books
            cover_id = book.get("cover_i")
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "https://via.placeholder.com/200x300/ff6b6b/ffffff?text=No+Image"

            work_key = book.get("key")
            description = "No description available"
            
            # 🔥 Description fetch karo
            try:
                if work_key:
                    work_url = f"https://openlibrary.org{work_key}.json"
                    work_response = requests.get(work_url, timeout=2)
                    if work_response.status_code == 200:
                        work_data = work_response.json()
                        desc = work_data.get("description")
                        if isinstance(desc, dict):
                            description = desc.get("value", "No description available")
                        elif isinstance(desc, str) and desc.strip():
                            description = desc[:200] + "..."  # Short description
            except:
                pass

            result.append({
                "title": book.get("title", "No Title"),
                "author": book.get("author_name", ["Unknown"])[0] if book.get("author_name") else "Unknown",
                "cover": cover_url,
                "description": description,
                "preview": f"https://openlibrary.org{work_key}" if work_key else None
            })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)