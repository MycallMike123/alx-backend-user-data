#!/usr/bin/env python3

"""
Basic Flask App setup.
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome():
    """
    Welcome message for the API
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    POST '/users' route that registers a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email,
                        "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    POST '/sessions' route that logs in a
    user Log in users if provided credentials
    are correct, and create a new session for them
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    if not AUTH.valid_login(email, password):
        abort(401)  # Abort the request if login credentials are invalid

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)  # Abort request if session creation fails

    response = make_response(jsonify({"email": f"{email}",
                                      "message": "logged in"}))
    # Set the session_id as a cookie in the response
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    DELETE '/sessions' route that logs out a user
    Log out users by deleting their current session
    """
    # Get session_id from request cookies
    session_id = request.cookies.get("session_id")
    # Get the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)  # Abort the request with a 403 Forbidden status code
        # Destroy the session for the user
    AUTH.destroy_session(user.id)
    # Redirect the user to the home page
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    GET '/sessions' route that returns the user's profile(email)
    """
    # Get the session_id from the request cookies
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)  # Abort request if session_id is missing
    # Get the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)  # Abort the request if user is not found

    # Return the user's email as a JSON response with a 200 status code
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST '/reset_password' route that generates a reset token
    For resetting a user's password
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"message": "email required"}), 400

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    PUT '/reset_password' route that updates a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
