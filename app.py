from flask import Flask, render_template, request, redirect, url_for, json
import os

app = Flask(__name__)

def load_posts():
    try:
        with open('static/storage.json') as f:
            posts = json.load(f)
            return posts
    except FileNotFoundError:
        print("File not found. Ensure 'static/storage.json' exists.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. Ensure 'static/storage.json' contains valid JSON.")
        return []

def save_posts(posts):
    with open('static/storage.json', 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing posts
        blog_posts = load_posts()

        # Create new post with a unique ID
        new_post = {
            'id': max([post['id'] for post in blog_posts], default=0) + 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Add new post to the list
        blog_posts.append(new_post)

        # Save posts back to the JSON file
        save_posts(blog_posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # Load existing posts
    blog_posts = load_posts()

    # Remove the post with the given ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    save_posts(blog_posts)

    # Redirect to the home page
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
