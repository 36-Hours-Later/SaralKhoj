from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# import vonage

# vonage_client = vonage.Client(
#     api_key=VONAGE_API_KEY, api_secret=VONAGE_API_SECRET
# )

app = Flask(__name__)
app.secret_key="it's_not_what_you_think"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    job_desc=db.Column(db.String(1000))
    job_date=db.Column(db.String(100))
    location=db.Column(db.String(500))
    district=db.Column(db.String(100))
    contact=db.Column(db.Integer)

class emp_info(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    address=db.Column(db.String(1000))
    contact=db.Column(db.Integer)
    count=db.Column(db.Integer)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create",methods=["POST","GET"])
def create():
    if request.method=="POST":
        desc = request.form["desc"]
        date = request.form["date"]
        loc = request.form["loc"]
        dist = request.form["dist"]
        contact = request.form["contact"]
        new_post = post(job_desc=desc, job_date=date, location=loc, district=dist, contact=contact)
        db.session.add(new_post)
        db.session.commit()
        flash("Job opportunity added")
        return redirect(url_for("index"))
    
    return render_template("create_job.html")

@app.route("/view",methods=["POST","GET"])
def view():
    try:
        if request.method=="GET":
            query = request.form["search"]
            lis=[]
            for item in post.query.all():
                if query in item.district:
                    lis.append(item)
            return render_template("search_job.html",data=lis)
    except:
        pass
    posts = post.query.all()
    return render_template("search_job.html",data=posts)

@app.route("/check-in/<id>",methods=["POST","GET"])
def checkin(id):
    if request.method=="POST":
        name = request.form["name"]
        loca = request.form["loca"]
        contact = request.form["contact"]
        for item in emp_info.query.all():
            # print(type(item.contact),type(contact))
            if contact==str(item.contact):
                user = emp_info.query.filter_by(contact=contact).first()
                user.count = user.count+1
                db.session.commit()
                flash("Details saved...")
                return redirect(url_for("index"))
        new_user = emp_info(name=name, address=loca, contact=contact, count=1)
        db.session.add(new_user)
        db.session.commit()
        flash("Details saved...")
        return redirect(url_for("index"))
    
    posts = post.query.get(id)
    return render_template("view_job.html",data=posts)

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
