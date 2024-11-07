from flask import Flask, request, jsonify
from source.components.user_auth import UserSignUp, UserLogin, UserLogout
from source.components.products import Products
from source.components.customers import Customers
from flask_cors import CORS

app = Flask(__name__)
products = Products()
customers = Customers()

CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

@app.route("/signup", methods=['POST'])
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
    
@app.route("/login", methods=['POST', 'OPTIONS'])
def login():
    try:
        if request.method == 'OPTIONS':
            # CORS preflight response for OPTIONS method
            response = jsonify({'message': 'Preflight request accepted'})
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            return response, 204
        
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
    
@app.route('/logout', methods=['POST'])
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
    
@app.route('/api/products', methods=['POST'])
def create_product():
    try:    
        data = request.get_json()

        if isinstance(data, list):
            product_details = products.create_product(product_list=data)
            return jsonify({"message": "Products created successfully.!", "Details of the products -": product_details}), 201

        elif isinstance(data, dict):
            product_name = data.get("product_name")
            product_number = data.get("product_number")
            company_for = data.get("company_for")

            # Check if all parameters are provided
            if not all([product_name, product_number, company_for]):
                return jsonify({"error": "Missing required fields"}), 400
        
            product_details = products.create_product(data=data)
            return jsonify({"message": "Product created successfully.!", "Details of the product -": product_details}), 201
        
        else:
            return jsonify({"error": "Invalid input format"}), 400

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/api/products', methods=['GET'])
def read_product():
    try:
        # Get query parameters
        product_name = request.args.get("product_name")
        product_number = request.args.get("product_number")
        company_for = request.args.get("company_for")
        
        # Check if all parameters are provided
        if not all([product_name, product_number, company_for]):
            return jsonify({"error": "Missing required query parameters"}), 400

        # Call the read_product method from the products class
        product = products.read_product(product_name=product_name, product_number=product_number, company_for=company_for)
        
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"message": "Product not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/api/products', methods=['PUT'])
def update_product():
    try:
        data = request.get_json()

        data_needs_to_update = data.get("data_needs_to_update")
        updated_data = data.get("updated_data")

        if not data_needs_to_update or not updated_data:
            return jsonify({"error": "Both 'data_needs_to_update' and 'updated_data' are required."}), 400

        result = products.update_product(data_needs_to_update=data_needs_to_update, updated_data=updated_data)

        return jsonify(result), 200 if result["modified_count"] > 0 else 404
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500

@app.route('/api/products', methods=['DELETE'])
def delete_product():
    try:
        product_name = request.args.get("product_name")
        product_number = request.args.get("product_number")
        company_for = request.args.get("company_for")

        if not all([product_name, product_number, company_for]):
            return jsonify({"error": "Missing required query parameters"}), 400

        result = products.delete_product(product_name=product_name, product_number=product_number, company_for=company_for)

        if result["deleted_count"] > 0:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/api/customers', methods=['POST'])
def create_customer():
    try:    
        data = request.get_json()

        if isinstance(data, list):
            customer_details = customers.create_customer(customer_list=data)
            return jsonify({"message": "Products created successfully.!", "Details of the products -": customer_details}), 201

        elif isinstance(data, dict):
            customer_name = data.get("customer_name")
            contact_person = data.get("contact_person")
            pincode = data.get("pincode")

            # Check if all parameters are provided
            if not all([customer_name, contact_person, pincode]):
                return jsonify({"error": "Missing required fields"}), 400
        
            customer_details = customers.create_customer(data=data)
            return jsonify({"message": "Product created successfully.!", "Details of the product -": customer_details}), 201
        
        else:
            return jsonify({"error": "Invalid input format"}), 400

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/api/customers', methods=['GET'])
def read_customer():
    try:
        # Get query parameters
        customer_name = request.args.get("customer_name")
        
        # Check if all parameters are provided
        if not customer_name:
            return jsonify({"error": "Missing required query parameters"}), 400

        # Call the read_customer method from the customers class
        customer = customers.read_customer(customer_name=customer_name)
        
        if customer:
            return jsonify(customer), 200
        else:
            return jsonify({"message": "Product not found"}), 404
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/api/customers', methods=['PUT'])
def update_customer():
    try:
        data = request.get_json()

        data_needs_to_update = data.get("data_needs_to_update")
        updated_data = data.get("updated_data")

        if not data_needs_to_update or not updated_data:
            return jsonify({"error": "Both 'data_needs_to_update' and 'updated_data' are required."}), 400

        result = customers.update_customer(data_needs_to_update=data_needs_to_update, updated_data=updated_data)

        return jsonify(result), 200 if result["modified_count"] > 0 else 404
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
@app.route('/api/customers', methods=['DELETE'])
def delete_product():
    try:
        customer_name = request.args.get("customer_name")
        contact_person = request.args.get("contact_person")
        pincode = request.args.get("pincode")

        if not all([customer_name, contact_person, pincode]):
            return jsonify({"error": "Missing required query parameters"}), 400

        result = customers.delete_customer(customer_name=customer_name, contact_person=contact_person, pincode=pincode)

        if result["deleted_count"] > 0:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)