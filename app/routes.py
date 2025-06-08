import jwt, os, bcrypt
from datetime import datetime, timedelta
from flask    import Flask, request, jsonify
from db       import connector, create_table

""" SECRET_KEY = os.gentenv("SECRET_KEY", key) """

SECRET_KEY = "test"

app = Flask(__name__)

create_table()

@app.route("/register", methods=["POST"])
def register():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    cursor.execute("SELECT * FROM users WHERE useremail = ?", (data["useremail"],))

    user = cursor.fetchone()

    if user is not None:
        return jsonify({"error": "true", "return": "Email already registered!"}), 400

    cursor.execute("INSERT INTO users (username, useremail, password) VALUES (?, ?, ?)",
                   (data["username"], data["useremail"], bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "User registered successfully!"}), 200

@app.route("/login", methods=["POST"])
def login():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400
    
    cursor.execute("SELECT * FROM users WHERE useremail = ?", (data["useremail"],))

    user = cursor.fetchall()

    if user.__len__() > 0:
        if bcrypt.checkpw(data["password"].encode('utf-8'), user[0][3]):
            cursor.execute("SELECT * FROM users WHERE useremail = ? AND password = ?", (data["useremail"], user[0][3],))

            user = cursor.fetchone()
        else:
            return jsonify({"error": "true", "return": "Password invalid!"})
    else:
        return jsonify({"error": "true", "return": "Email provided not registered!"})

    if user.__len__() > 0:
        token = jwt.encode(
            {"user": data["useremail"], "exp": datetime.utcnow() + timedelta(weeks=1)},
            SECRET_KEY,
            algorithm="HS256"
        )

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({"error": "true", "return": "Login successful!", "token": token}), 200

    return jsonify({"error": "true", "return": "invalid credentials!"}), 400

@app.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "true", "return": "Access denied!"}), 400

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify({"error": "true", "return": "Authetication failed, please try again!"}), 400

    token = parts[1]

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"error": "false", "return": "Logout successful!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "true", "return": "Expired token. Please login again"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "true", "return": "Invalid token!"}), 400

@app.route("/validateToken", methods=["GET"])
def validateToken():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "true", "return": "Access denied!"}), 400

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify({"error": "true", "return": "Authetication failed, please try again!"}), 400

    token = parts[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return jsonify({"error": "false", "return": "Access granted!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "true", "return": "Expired token. Please login again"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "true", "return": "Invalid token!"}), 400

@app.route("/registerItems", methods=["POST"])
def registerItems():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    cursor.execute("INSERT INTO items (name, price, categ, weight, mass, qtde, active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (data["name"], data["price"], data["categ"], data["weight"], data["mass"], data["qtde"], data["active"]))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Item registered successfully!"}), 200

@app.route("/getUsers", methods=["GET"])
def getUsers():
    conn   = connector()
    cursor = conn.cursor()

    cursor.execute("SELECT username, useremail FROM users")

    users = cursor.fetchall()

    print(users)

    conn.commit()
    conn.close()

    return jsonify({"users": users}), 200

if __name__ == "__main__":
    app.run()