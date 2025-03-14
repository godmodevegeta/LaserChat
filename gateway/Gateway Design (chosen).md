By having a **/validate** endpoint in the Auth Service, the API Gateway can offload JWT validation to the Auth Service instead of handling it internally.  

---

## **🚀 How It Works**
1️⃣ **User sends a request to `/upload` via the Gateway Service**, including the JWT token in the headers.  
2️⃣ **Gateway Service calls the Auth Service `/validate` endpoint** to verify the JWT.  
3️⃣ **If valid**, the Gateway forwards the request to the **Converter Service**.  
4️⃣ **If invalid**, the Gateway rejects the request with a `401 Unauthorized` response.  

### **📌 Architecture Diagram**
```
Client ───> API Gateway (/upload) ───> Auth Service (/validate) ───> JWT Validation
                                              │
                                              ▼
                                    Valid ✔ / Invalid ❌
                                              │
                        ┌────────────────────┘
                        ▼
          Converter Service (/upload)
```

---

## **🖥 Implementation**

### **1️⃣ Auth Service (`/validate` Endpoint)**
This service validates the JWT and responds with user info if valid.

```python
from flask import Flask, request, jsonify
import jwt

SECRET_KEY = "your_secret_key"

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate_token():
    token = request.json.get("token")  # Expecting JSON payload: { "token": "JWT_TOKEN" }
    
    if not token:
        return jsonify({"message": "Token is missing!"}), 401
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"user": payload["user"]}), 200  # Return user info
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401

if __name__ == "__main__":
    app.run(port=5001, debug=True)  # Auth Service runs on port 5001
```

---

### **2️⃣ API Gateway (`/upload` Route)**
The Gateway calls the Auth Service before forwarding the request.

```python
from flask import Flask, request, jsonify
import requests

AUTH_SERVICE_URL = "http://auth-service:5001/validate"
CONVERTER_SERVICE_URL = "http://converter-service:5000"

app = Flask(__name__)

def validate_jwt(token):
    """ Calls the Auth Service to validate JWT """
    response = requests.post(AUTH_SERVICE_URL, json={"token": token})
    return response if response.status_code == 200 else None

@app.before_request
def authenticate_request():
    """ Intercepts all requests and validates JWT """
    if request.path.startswith("/upload"):  # Protect only /upload
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        token = token.split(" ")[1]  # Remove "Bearer "
        validation_response = validate_jwt(token)

        if not validation_response:
            return jsonify({"message": "Invalid or expired token!"}), 401

        request.user = validation_response.json()  # Attach user data

@app.route("/upload", methods=["POST"])
def upload():
    """ Forwards request to the Converter Microservice """
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.post(f"{CONVERTER_SERVICE_URL}/upload", headers=headers, files=request.files)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=4000, debug=True)  # API Gateway runs on port 4000
```

---

### **3️⃣ Converter Service (No JWT Handling)**
This service just handles file uploads since authentication is already done by the API Gateway.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    return jsonify({"message": "File uploaded successfully!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # Converter Service runs on port 5000
```

---

## **🔥 Why Is This a Good Design?**
✅ **Centralized Authentication** – Only the **Auth Service** handles JWTs, making it easier to manage.  
✅ **Microservices Stay Focused** – The **Converter Service** doesn’t deal with authentication.  
✅ **API Gateway Adds Security** – It blocks unauthorized requests **before** they hit the backend.  
✅ **Scalable** – The API Gateway and Auth Service can be **replicated** for higher availability.  

---

## **🔹 Next Steps**
- **Dockerizing** these services?  
- Adding **role-based access control (RBAC)**?  
- Using **Kong API Gateway** instead of Flask?  
