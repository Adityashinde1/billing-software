from flask import Flask, request, jsonify
from source.components.user_auth import UserSignUp, UserLogin, UserLogout

app = Flask(__name__)

@app.route("/signup", method=['POST'])
def signup():
    try:
        data = request.get_json()
        user_name = data["user_name"]
        user_emailid = data["user_emailid"]
        user_password = data["user_password"]

        signup = UserSignUp(user_name=user_name, user_emailid=user_emailid, user_password=user_password)
        message = signup.start_user_sign_up()

        if message == "User signed up successfully...!":
            return jsonify({"message": "Signup successful..!", "status": "success"}), 200
        else:
            return jsonify({"message": "Signup failed..!", "status": "error"}), 400
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route("/login", method=['POST'])
def login():
    try:
        data = request.get_json()
        user_name = data["user_name"]
        user_emailid = data["user_emailid"]
        user_password = data["user_password"]

        login = UserLogin(user_name=user_name, user_emailid=user_emailid, user_password=user_password)
        token = login.start_login()

        if token:
            return jsonify({
                "message": "Login successful..!",
                "token": token,
                "status": "success"
            }), 200
        else:
            return jsonify({"message": "Login failed", "status": "error"}), 401
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/logout', method=['POST'])
def logout():
    try:
        data = request.get_json()
        token = data['token']

        logout = UserLogout()
        flag = logout.start_logout(token=token)

        if flag:
            return jsonify({"message": "Logout successful!", "status": "success"}), 200
        else:
            return jsonify({"message": "Logout failed!", "status": "error"}), 400
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
