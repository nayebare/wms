#importing of the neccessary modules and method
#the os  path module implements some useful functions on pathnames and directory access
#imports that are making big changes
from os.path import abspath, dirname, join

from flask import flash, Flask, Markup, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#making a path to the database
_cwd = dirname(abspath(__file__))

SECRET_KEY = 'flask-session-insecure-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'wms.db')
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = 'this-should-be-more-random'


app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

#making table for tracking_site
class Site(db.Model):
    __tablename__ = 'received_goods'
    incoming_itemID = db.Column(db.Integer,primary_key = True)
    product_id = db.Column(db.String(80))
    product_name = db.Column(db.String(120))
    supplyer_name = db.Column(db.String(300))
    amount = db.Column(db.Integer(9))
#this tells python how to print  objects of this class
    def __repr__(self):
       return '<Site %s>' % (self.base_url)

    def __str__(self):
        return self.base_url
    
class SiteForm(Form):
        product_id = fields.StringField()
        product_name = fields.StringField()
        supplyer_name = fields.StringField()
        amount = fields.StringField()
        
#perform the url mapping
@app.route("/")
def index():
    site_form = SiteForm()
    return render_template("index.html",site_form = site_form)

#the form is loaded as the index page
@app.route("/site",methods =("POST",))
def add_site():
    form = SiteForm()
    if form.validate_on_submit():
        site = Site()
        form.populate_obj(site)
        db.session.add(site)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("validation_error.html",form = form)

#get the data inserted on this page url mappeteing
@app.route("/sites")
def view_sites():
    data = Site.query.filter(Site.product_id >= 0)
    #data = [next(data)] + [[_make_link(cell) if i == 0 else cell for i, cell in enumerate(row)] for row in data]
    return render_template("display_data.html", data=data ,type="Sites")






#display the data down here without on reload

if __name__ == "__main__":
    app.debug = True

    db.create_all()
    app.run()


