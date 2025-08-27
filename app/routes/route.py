from flask import Blueprint,jsonify,url_for,redirect,request,render_template
import requests
import os
import jwt

route=Blueprint('rote',__name__)

# route.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")  # replace in production

# LinkedIn OAuth settings
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("PRIMARY_CLIENT_SECRET_ID" or "SECONDARY_CLIENT_SECRET_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")  # st match LinkedIn app settings





@route.route("/")
def index():
    return render_template("index.html")
    

# Step 1: Redirect user to LinkedIn login
@route.route("/login/linkedin",methods=['POST','GET'])
def login_linkedin():
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=openid%20profile%20email"
    )
    return redirect(auth_url)

# Step 2: LinkedIn redirects back with authorization code
@route.route("/callback/linkedin")
def callback_linkedin():
    code = request.args.get("code")
    if not code:
        return {"error": request.args.get("error_description", "No code returned")}, 400

    # Step 3: Exchange code for tokens
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    token_res = requests.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    token_json = token_res.json()
    id_token = token_json.get("id_token")  # OpenID Connect JWT
    if not id_token:
        return {"error": "No id_token in response", "details": token_json}, 400

    # Step 4: Decode ID Token (JWT)
    try:
        # WARNING: In production, fetch LinkedIn's public keys (JWKS) to verify signature
        decoded = jwt.decode(id_token, options={"verify_signature": False})
    except Exception as e:
        return {"error": "Failed to decode ID token", "details": str(e)}, 400

    # decoded contains email + profile info
    return {"id_token_claims": decoded, "raw_token_response": token_json}
