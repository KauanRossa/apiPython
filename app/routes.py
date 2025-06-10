import bcrypt
from datetime import datetime
from flask    import Flask, request, jsonify
from db       import connector, create_table

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
    
    cursor.execute("INSERT INTO addresses (user_id, street, number, complement, neighborhood, city, state, zip_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (cursor.lastrowid, data["street"], data["number"], data["complement"], data["neighborhood"], data["city"], data["state"], data["zip_code"]))

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

    if user.__len__() == 0:
        return jsonify({"error": "true", "return": "Email provided not registered!"})
    
    cursor.execute("SELECT * FROM users WHERE useremail = ? AND active = 1", (data["useremail"],))

    user = cursor.fetchall()

    if user.__len__() == 0:
        return jsonify({"error": "true", "return": "User not activated!"}), 400

    if bcrypt.checkpw(data["password"].encode('utf-8'), user[0][3]):
            cursor.execute("SELECT * FROM users WHERE useremail = ? AND password = ?", (data["useremail"], user[0][3],))

            user = cursor.fetchone()
    else:
        return jsonify({"error": "true", "return": "Password invalid!"})
        
    if user.__len__() > 0:
        cursor.execute("UPDATE users SET token = ? WHERE useremail = ?", (data["token"], data["useremail"]))

        return jsonify({"error": "false", "return": "Login successful!"}), 200

    return jsonify({"error": "true", "return": "invalid credentials!"}), 400

@app.route("/getUsers", methods=["GET"])
def getUsers():
    conn   = connector()
    cursor = conn.cursor()

    cursor.execute("SELECT username, useremail, active FROM users")

    users = cursor.fetchall()

    print(users)

    conn.commit()
    conn.close()

    return jsonify({"error": "false","return": users}), 200

@app.rout("/myData", methods=["GET"])
def myData():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400
    
    cursor.execute("SELECT * FROM users WHERE useremail = ?", (data["useremail"],))

    user = cursor.fetchall()

    cursor.execute("SELECT * FROM addresses WHERE user_id = ?", (data[0][0],))

    user += cursor.fetchall()

    if user.__len__() == 0:
        return jsonify({"error": "true", "return": "User not found!"}), 400
    
    return jsonify({"error": "false", "return": user})

@app.route("/updateUser", methods=["PUT"])
def updateUser():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400
    
    cursor.execute("SELECT * FROM users WHERE useremail = ?", (data["useremail"],))

    user = cursor.fetchall()

    if user.__len__() == 0:
        return jsonify({"error": "true", "return": "User not found!"}), 400
    
    cursor.execute("UPDATE users SET username = ?, useremail = ?, password = ?, type = ?, active = ? WHERE useremail = ?",
                   (data["username"], data["useremail"], bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()), data["type"], data["active"], data["useremail"]))
    
    cursor.execute("UPDATE addresses SET street = ?, number = ?, complement = ?, neighborhood = ?, city = ?, state = ?, zip_code = ? WHERE user_id = ?",
                   (data["street"], data["number"], data["complement"], data["neighborhood"], data["city"], data["state"], data["zip_code"], user[0][0]))
    
    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "User updated successfully!"}), 200

@app.route("/deleteUser", methods=["DELETE"])
def deleteUser():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400
    
    cursor.execute("SELECT * FROM users WHERE useremail = ?", (data["useremail"],))

    user = cursor.fetchall()

    if user.__len__() == 0:
        return jsonify({"error": "true", "return": "User not found!"}), 400
    
    cursor.execute("DELETE FROM users WHERE useremail = ?", (data["useremail"],))

    cursor.execute("DELETE FROM addresses WHERE user_id = ?", (user[0][0],))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "User deleted successfully!"}), 200

@app.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "true", "return": "Access denied!"}), 400

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify({"error": "true", "return": "Authetication failed, please try again!"}), 400

    token = parts[1]

    """ try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"error": "false", "return": "Logout successful!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "true", "return": "Expired token. Please login again"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "true", "return": "Invalid token!"}), 400 """

@app.route("/validateToken", methods=["GET"])
def validateToken():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    """ auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "true", "return": "Access denied!"}), 400

    try:
        return jsonify({"error": "false", "return": "Access granted!"}), 200
    except jwt.InvalidTokenError:
        return jsonify({"error": "true", "return": "Invalid token!"}), 400 """

@app.route("/registerItems", methods=["POST"])
def registerItems():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    cursor.execute("INSERT INTO items (name, price, categ, weight, mass, quantity, active) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (data["name"], data["price"], data["categ"], data["weight"], data["mass"], data["quantity"], data["active"]))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Item registered successfully!"}), 200

@app.route("/getItems", methods=["GET"])
def getItems():
    conn   = connector()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")

    items = cursor.fetchall()

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": items}), 200

@app.route("/updateItem", methods=["PUT"])
def updateItem():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (data["id"],))

    item = cursor.fetchall()

    if item.__len__() == 0:
        return jsonify({"error": "true", "return": "Item not found!"}), 400

    cursor.execute("UPDATE items SET name = ?, price = ?, categ = ?, weight = ?, mass = ?, quantity = ?, active = ? WHERE id = ?",
                   (data["name"], data["price"], data["categ"], data["weight"], data["mass"], data["quantity"], data["active"], data["id"]))
    
    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Item updated sucessfully!"}), 200
    
@app.route("/deleteItem", methods=["DELETE"])
def deleteItem():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    cursor.execute("SELECT * FROM items WHERE id = ?", (data["id"],))

    item = cursor.fetchall()

    if item.__len__() == 0:
        return jsonify({"error": "true", "return": "Item not found!"}), 400

    cursor.execute("DELETE FROM items WHERE id = ?", (data["id"],))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Item deleted sucessfully!"}), 200

@app.route("/createCart", methods=["POST"])
def createCart():
    data   = request.get_json()
    conn   = connector()
    cursor = conn.cursor()

    if not data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    cursor.execute("SELECT id FROM cart WHERE user_id = ? AND active = 1", (data["user_id"],))

    cart = cursor.fetchone()

    if cart is None:
        cursor.execute("INSERT INTO cart (user_id, created_at, active) VALUES (?, ?, ?)",
                       (data["user_id"], datetime.now(), 1))

        cart_id = cursor.lastrowid
    else:
        cart_id = cart[0]

    cursor.execute("INSERT INTO cartitem (cart_id, item_id, quantity) VALUES (?, ?, ?)",
                   (cart_id, data["item_id"], data["quantity"]))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Item added to cart successfully!"}), 200

@app.route("/getCart/<int:user_id>", methods=["GET"])
def getCart(user_id):
    conn   = connector()
    cursor = conn.cursor()

    cursor.execute(""" SELECT ci.id, ci.item_id, i.name, ci.quantity, i.price FROM cart c JOIN cartitem ci ON c.id = ci.cart_id JOIN items i ON ci.item_id = i.id WHERE c.user_id = ? AND c.active = 1 """, (user_id,))

    items = cursor.fetchall()

    conn.close()

    return jsonify({"error": "false", "return": items}), 200

@app.route("/updateCart/<int:cartitem_id>", methods=["PUT"])
def updateCart(cartitem_id):
    data = request.get_json()
    conn = connector()
    cursor = conn.cursor()

    if not data or "quantity" not in data:
        return jsonify({"error": "true", "return": "No data send, please try again!"}), 400

    cursor.execute("UPDATE cartitem SET quantity = ? WHERE id = ?", (data["quantity"], cartitem_id))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Cart item updated successfully!"}), 200

@app.route("/deleteCart/<int:cartitem_id>", methods=["DELETE"])
def deleteCart(cartitem_id):
    conn = connector()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cartitem WHERE id = ?", (cartitem_id,))

    conn.commit()
    conn.close()

    return jsonify({"error": "false", "return": "Cart item deleted successfully!"}), 200

def log_request(endpoint, data):
    log = {
        "time": str(datetime.datetime.now()),
        "endpoint": endpoint,
        "ip": request.remote_addr,
        "method": request.method,
        "user_agent": request.headers.get('User-Agent'),
        "payload": data
    }

    with open("logs.txt", "a") as file:
        file.write(str(log) + "\n")

    if endpoint in ["/login", "/register"]:
        print(f"Request logged: {log}")

if __name__ == "__main__":
    app.run()