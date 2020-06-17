from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

db=SQLAlchemy()

def create_app():
    app.debug=True
    app.secret_key="38xa30sc6n3ap7lle2d23ghg"

    bootstrap = Bootstrap(app)
    
    from . import views
    app.register_blueprint(views.bp)

    # Admin blueprint
    # Uncomment these to allow database to be reset and initialised
    #from . import admin
    #app.register_blueprint(admin.bp)

    # Setting the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///penultimate.sqlite'

    # Initialising the database with the flask app
    db.init_app(app)

    return app

@app.errorhandler(404)
def not_found_error(e):
    return render_template("error404.html")

@app.errorhandler(405)
def not_allowed_error(e):
    return render_template("error405.html")

@app.errorhandler(500)
def internal_error(e):
    return render_template("error500.html")