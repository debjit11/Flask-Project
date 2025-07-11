from flask import Blueprint,request,render_template,session,url_for,redirect,flash

# Create a blueprint for authentication
auth_bp = Blueprint("auth",__name__)


# Hardcoded user credentials (for testing/demo only)
user_cradentials = {
    'username' : 'admin',
    'password':'1234'
}

@auth_bp.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check if the username and password match
        if username == user_cradentials["username"] and password == user_cradentials["password"]:
            session["user"] = username
            
            flash("Login Successful","success")
            
        else:
            flash("Invalid username or password","danger")
            
    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
      session.pop("user",None)  
      flash("Logged out","info")
      return redirect(url_for("auth.login"))  
    