from flask import Flask, render_template, json
import os

app = Flask(__name__)


def load_posts():
    with open('static/storage.json') as f:
        posts = json.load(f)
        print("Posts loaded successfully: ", posts)  # Debug statement
        return posts


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
