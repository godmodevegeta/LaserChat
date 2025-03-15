Here are the **three designs** for securing and routing requests to the **/upload** endpoint.

---

# **1️⃣ Direct Authentication in Converter Service**
### ✅ Pros: Simple, avoids extra network calls  
### ❌ Cons: Each service must handle authentication independently  

### **Flow**
1. The **client** sends a request directly to `/upload` with a JWT token.
2. The **converter service** verifies the JWT.
3. If valid, the service processes the request.
4. If invalid, it returns a 401 error.

```
Client ────> Converter Service (/upload) ────> JWT Validation
```

### **Implementation (Converter Service)**
```python
from flask import Flask, request, jsonify
import jwt

SECRET_KEY = "your_secret_key"

app = Flask(__name__)

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            token = token.split(" ")[1]  # Remove "Bearer "
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/upload", methods=["POST"])
@token_required
def upload():
    return jsonify({"message": "File uploaded successfully!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

---

# **2️⃣ Auth Microservice Validates JWT**
### ✅ Pros: Centralized authentication logic  
### ❌ Cons: Extra network call for each request  

### **Flow**
1. The **client** sends a request to `/upload` with a JWT token.
2. The **converter service** sends the token to the **auth service** for validation.
3. The **auth service** returns user details if the token is valid.
4. The **converter service** processes the request.

```
Client ────> Converter Service (/upload) ────> Auth Service (/validate-token) ────> Validation
```

### **Implementation**
#### **Auth Service (/validate-token)**
```python
from flask import Flask, request, jsonify
import jwt

SECRET_KEY = "your_secret_key"

app = Flask(__name__)

@app.route("/validate-token", methods=["POST"])
def validate_token():
    token = request.json.get("token")
    if not token:
        return jsonify({"message": "Token is missing!"}), 401
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"user": payload["user"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 401

if __name__ == "__main__":
    app.run(port=5001, debug=True)
```

#### **Converter Service**
```python
import requests
from flask import Flask, request, jsonify

AUTH_SERVICE_URL = "http://auth-service:5001/validate-token"

app = Flask(__name__)

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            token = token.split(" ")[1]
            response = requests.post(AUTH_SERVICE_URL, json={"token": token})

            if response.status_code != 200:
                return jsonify({"message": "Token is invalid!"}), 401
            
            request.user = response.json()
        except Exception as e:
            return jsonify({"message": f"Token validation failed: {str(e)}"}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/upload", methods=["POST"])
@token_required
def upload():
    return jsonify({"message": "File uploaded successfully!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

---

# **3️⃣ API Gateway in Front of Converter Service**
### ✅ Pros: Authentication is completely offloaded from microservices  
### ❌ Cons: Requires maintaining an extra service  

### **Flow**
1. The **client** sends a request to the **gateway** (`/upload`).
2. The **gateway** validates the JWT.
3. If valid, the **gateway** forwards the request to the **converter service**.
4. The **converter service** processes the request.

```
Client ────> API Gateway (/upload) ────> JWT Validation ────> Converter Service (/upload)
```

### **Implementation**
#### **Gateway Service**
```python
from flask import Flask, request, jsonify
import requests
import jwt

SECRET_KEY = "your_secret_key"
CONVERTER_SERVICE_URL = "http://converter-service:5000"

app = Flask(__name__)

def validate_jwt(token):
    """ Validates JWT Token """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.before_request
def authenticate_request():
    """ Intercepts all requests and validates JWT """
    if request.path.startswith("/upload"):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        token = token.split(" ")[1]
        user_data = validate_jwt(token)
        
        if not user_data:
            return jsonify({"message": "Invalid or expired token!"}), 401
        
        request.user = user_data  # Attach user data to request

@app.route("/upload", methods=["POST"])
def upload():
    """ Proxy request to Converter Microservice """
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.post(f"{CONVERTER_SERVICE_URL}/upload", headers=headers, files=request.files)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=4000, debug=True)
```

#### **Converter Service (No JWT validation needed)**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    return jsonify({"message": "File uploaded successfully!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

---

# **🔹 Which One Should You Choose?**
| Approach | ✅ Pros | ❌ Cons | When to Use? |
|----------|--------|---------|--------------|
| **1️⃣ JWT Validation in Converter** | Simple, no extra services needed | Each service must handle auth separately | Small projects with fewer services |
| **2️⃣ Auth Microservice Validates JWT** | Centralized auth logic | Extra network call on every request | When multiple services share auth logic |
| **3️⃣ API Gateway in Front** | Fully offloads auth from microservices | Requires maintaining a gateway service | Best for scaling and microservice architecture |

---

# **🚀 Next Steps**
Would you like help:
- Deploying this with **Docker & Kubernetes**?  
- Using **Kong or Traefik API Gateway** instead of Flask?  
- Adding **role-based access control (RBAC)**?  

Let me know how you’d like to extend this! 🚀