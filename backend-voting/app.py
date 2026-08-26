from flask import Flask, jsonify, request
import os
import redis
import json


app = Flask(__name__)


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "service": "backend"
    })


@app.route("/vote", methods=["POST"])
def vote():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400


    choice = data.get("choice")


    if choice not in ["cat", "dog"]:

        return jsonify({
            "error": "Choice must be cat or dog"
        }), 400


    vote_data = json.dumps({
        "choice": choice
    })


    redis_client.rpush(
        "votes",
        vote_data
    )


    return jsonify({
        "message": "Vote queued",
        "choice": choice
    }), 202


@app.route("/results")
def results():

    results = redis_client.hgetall("results")

    cat_votes = int(
        results.get("cat", 0)
    )

    dog_votes = int(
        results.get("dog", 0)
    )


    return jsonify({

        "cat": cat_votes,

        "dog": dog_votes,

        "total": cat_votes + dog_votes

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080
    )
