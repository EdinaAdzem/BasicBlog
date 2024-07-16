from flask import Flask, render_template, json, request
import os

app = Flask(__name__)


def load_posts():
    with open('static/storage.json') as f:
        posts = json.load(f)
        print("Posts loaded successfully: ", posts)  # Debug statement
        return posts


def save_posts(posts):
    with open('static/storage.json', 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """add route"""
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
