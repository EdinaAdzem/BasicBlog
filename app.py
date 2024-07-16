from flask import Flask, render_template, request, redirect, url_for, json
import os

app = Flask(__name__)

def load_posts():
    with open('static/storage.json') as f:
        posts = json.load(f)
        for post in posts:
            if 'likes' not in post:
                post['likes'] = 0
        return posts

def save_posts(posts):
    with open('static/storage.json', 'w') as f:
        json.dump(posts, f, indent=4)


def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts = load_posts()

        new_post = {
            'id': max([post['id'] for post in blog_posts], default=0) + 1,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """delete post route"""
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """update post route"""
    post = fetch_post_by_id(post_id)#create later fetcher function
    if post is None:
        return "Post not found", 404
    #update and redirect to index
    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        blog_posts = load_posts()
        for idx, p in enumerate(blog_posts):
            if p['id'] == post_id:
                blog_posts[idx] = post
                break
        save_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

#trying the bonus like button
@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    save_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
