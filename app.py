from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

class Disaster(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    typeClassified=db.Column(db.String(50),nullable=False)
    text=db.Column(db.String(200),nullable=False) 
    Location=db.Column(db.String(200),nullable=True,default="N/A") 
    date_made=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return "Classified as"+self.typeClassified

@app.route('/',methods=['GET','POST'])
def home():

    if request.method=='POST':
        text=request.form["message"]
        type='Flood'
        location="Mumbai"
        new_disaster=Disaster(typeClassified=type,text=text,Location=location);
        db.session.add(new_disaster)
        db.session.commit()
        return render_template("home.html")
        # return "There Was And Err Please try Later"
    else:
        return render_template("home.html")
 
@app.route('/helper')
def helper():
    cards=Disaster.query.order_by(Disaster.typeClassified).all()
    return render_template('helper.html',cards=cards);

x={
    "Health":[{"location":"Allahbad","message":"wounded"},{"location":"Lucknow","message":"need healthcare"},{"location":"Jhansi","message":"help"}],
    "Dog":[{"location":"Chennai","message":"Dog Wounded"},{"location":"Texas","message":"need Dog Food"},{"location":"MLA","message":"Dog Care"}]
}

@app.route('/dummy')
def dummy():
    return render_template('dict.html',obj=x)

if __name__ == '__main__':
    app.run()
