def create_app():
    import os
    import base64
    from flask import Flask
    from .views import views
    from .auth import auth
    app = Flask(__name__) #Initiliazes Flask
    app.config.from_pyfile('config.py') #Pulls SECRET_KEY Created in config.py
    app.register_blueprint(views, url_prefix='/') #Initiliazes views
    app.register_blueprint(auth, url_prefix='/') #Initiliazes auth
    app.run(host='10.0.0.35', port=8081) #Initiliazes server hosting on itself. 
