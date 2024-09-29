from firebase_admin import auth

def sign_up(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return {"success": True, "message": "User created successfully!", "user": user}
    except Exception as e:
        return {"success": False, "message": f"Error creating user: {e}"}

def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        return {"success": True, "message": f"Welcome back, {user.email}!", "user": user}
    except Exception as e:
        return {"success": False, "message": f"Login failed: {e}"}
