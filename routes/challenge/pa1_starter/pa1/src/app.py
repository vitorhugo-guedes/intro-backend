import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",
        "comments": {
            0: {
                "id": 0,
                "upvotes": 8,
                "text": "Wow, my first Reddit gold!",
                "username": "alicia98"
            }
        }
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
        "comments": {
            1: {
                "id": 1,
                "upvotes": 5,
                "text": "what a cute puppy aww",
                "username": "raahi014"
            }
        }
    }
}

posts_counter = 2
comments_counter = 2

@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here
@app.route("/api/posts/")
def getPosts():
    res = list(posts.values())
    return json.dumps(res), 200

@app.route("/api/posts/", methods=["POST"])
def createPost():
    global posts_counter

    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")

    if not title:
        return json.dumps({"error": "Posts need to have a title!"}), 400
    if not link:
        return json.dumps({"error": "Posts need to have a link!"}), 400
    if not username:
        return json.dumps({"error": "Posts need to have a username!"}), 400

    post = {"id": posts_counter, "upvotes": 1, "title": title, "link": link, "username": username}
    posts[posts_counter] = post
    posts_counter += 1

    return json.dumps(post), 201
    
@app.route("/api/posts/<int:post_id>/")
def getPost(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post do not exist or not found"}), 404
    
    return json.dumps(post), 200

@app.route("/api/posts/<int:post_id>/", methods=["POST"])
def deletePost(post_id):
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    
    del posts[post_id]

    return json.dumps(post), 200

# Comments routes

@app.route("/api/posts/<int:post_id>/comments/")
def getPostComments(post_id):
    post = posts.get(post_id)
    allComments = post.get("comments")

    if not post:
        return json.dumps({"error": "Post not found"}), 404
    if not allComments:
        return json.dumps({"error": "This post has no comments"}), 404

    res = list(allComments.values())
    
    return json.dumps(res), 200

@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def createComment(post_id):
    global comments_counter
    
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404

    body = json.loads(request.data)
    text = body.get("text")
    user = body.get("username")
    
    if not text:
        return json.dumps({"error": "Comment need to have a text"}), 400
    if not user:
        return json.dumps({"error": "Comment need to have a username"}), 400

    comment = {"id": comments_counter, "upvotes": 1, "text": text, "username": user}
    post["comments"][comments_counter] = comment
    comments_counter += 1

    return json.dumps(comment), 201

@app.route("/api/posts/<int:post_id>/comments/<int:com_id>/", methods=["POST"])
def editComment(post_id, com_id):
    post = posts.get(post_id)
    
    if not post:
        return json.dumps({"error": "Post not found"}), 404

    postComments = post.get("comments")
    comment = postComments.get(com_id)
    
    if not comment:
        return json.dumps({"error": "Comment not found"}), 404
    
    body = json.loads(request.data)
    text = body.get("text")
    comment["text"] = text

    if not text:
        return json.dumps({"error": "Edit needs a text"}), 400

    return json.dumps(comment), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
