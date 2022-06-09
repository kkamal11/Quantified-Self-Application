import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import url_for,redirect,request,render_template,session
import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import current_app as app

from application.models import User,Tracker,Logs
from .database import db
app.secret_key = "thisisasecretkey"


@app.route("/",methods=["GET","POST"])
def front():
    return render_template("front.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        session["username"] = username
        user = db.session.query(User).filter(User.username == session["username"]).first()
        if user is not None and user.username == username:
                if password == user.password:
                    tr = user.users_tracker
                    if tr != []:
                        return redirect(url_for("dashboard"))
                    today_date = datetime.date.today()
                    return render_template("no_tracker.html",today_date = today_date)
                return render_template("wrong_pass.html")
        else:
            u = User(
            username = username,
            password = password
            )
            db.session.add(u)
            db.session.commit()
            today_date = datetime.date.today()
            return render_template("no_tracker.html",today_date = today_date)


@app.route("/reset/account/<string:username>",methods=["GET","POST"])
def del_account(username):
    u = db.session.query(User).filter(User.username==username).first()
    app.logger.debug("To delete account, returning from DB {}".format(u))
    if u is not None:
        db.session.delete(u)
        db.session.commit()
    return redirect("/")

@app.route("/create_tracker",methods=["GET","POST"])
def create_tracker():
    if request.method == "GET":
        today_date = datetime.date.today()
        return render_template("create_tracker.html",today_date = today_date)
    else:
        t = datetime.datetime.now()
        tracker_name = request.form.get("tracker_name")
        tracker_description = request.form.get("description")
        type = request.form.get("tracker_type")
        setting = request.form.get("setting")
        if setting == "":
            setting = "Null"
        user = db.session.query(User).filter(User.username == session["username"]).first()
        #tr = db.session.query(Tracker).filter(Tracker.user_id == u_id.user_id).all()
        tr = user.users_tracker
        for tracker in tr:
            if tracker.tracker_name == tracker_name:
                return render_template("tracker_exists.html")
        u = Tracker(
            tracker_type = type,
            tracker_name = tracker_name,
            tracker_description = tracker_description,
            user_id = user.user_id,
            track_time = t,
            setting = setting
        )
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    try:
        todayz_date = datetime.date.today()
        user = db.session.query(User).filter(User.username == session["username"]).first()
        return render_template("dashboard.html",trackers = user.users_tracker,today_date = todayz_date)
    except KeyError:
        return "<h2>Please login first</h1>"

@app.route("/grid_view",methods=["GET","POST"])
def gridview():
    user = db.session.query(User).filter(User.username == session["username"]).first()
    todayz_date = datetime.date.today()
    return render_template("card_view.html",trackers = user.users_tracker,today_date = todayz_date)


@app.route("/delete/<string:place>/<int:tracker_id>",methods=["GET","POST"])
def delete_tracker(tracker_id,place):
    while True: #first deleting all the logs corresponding to the tracker
        log = db.session.query(Logs).filter(Logs.tracker_id == tracker_id).first()
        if log is None:
            break
        db.session.delete(log)
        db.session.commit()
    u = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
    db.session.delete(u)
    db.session.commit()
    if place == 'grid':
        return redirect(url_for('gridview'))
    return redirect(url_for("dashboard"))


@app.route("/update/<int:tracker_id>",methods=["GET","POST"])
def update_tracker(tracker_id):
    if request.method == "GET":
        today_date = datetime.date.today()
        u = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
        return render_template("update_tracker.html",tracker = u, today_date = today_date)

    else:
        t = datetime.datetime.now()
        tname = request.form.get("tracker_name")
        tracker_description = request.form.get("description")
        u = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
        u.tracker_name = tname
        u.tracker_description = tracker_description
        u.tracker_type = u.tracker_type
        u.user_id = u.user_id
        u.track_time = t
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route("/log/<int:tracker_id>",methods=["GET","POST"])
def log_input(tracker_id):
    u = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
    setting_list = u.setting
    t_type = u.tracker_type
    t=datetime.datetime.now()
    today_date = datetime.date.today()
    if request.method == "GET":
        if t_type == "Numerical":
            return render_template("log_input_numerical.html",ctime = t,tt = tracker_id,tracker_type = t_type,today_date = today_date)
        elif t_type == "Multiple Choice":
            return render_template("log_input_mcq.html",ctime = t,tt = tracker_id,trname = u.tracker_name,tracker_type = t_type,L = setting_list.split(','),today_date = today_date)
        elif t_type == "Boolean":
            return render_template("log_input_boolean.html",tt=tracker_id,tname=u.tracker_name,ctime=t,tracker_type=t_type,today_date = today_date)
    else:
        u = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
        time =datetime.datetime.now()
        v = request.form.get("value")
        notes = request.form.get("notes") 
        if t_type == "Boolean":
            d = {"YES":1,"NO":0}
            if v not in d:
                return render_template("wrong_boolean.html",tid = tracker_id )
            v = d[v]
        if t_type == "Numerical":
            try:
                if "." in v:
                    _ = float(v)
                else:
                    _ = int(v)
            except:
                return render_template("wrong_numerical.html",trname =u.tracker_id )
        log = Logs(
            log_time = time,
            value = v,
            note=notes,
            tracker_id = tracker_id,
        )
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("dashboard"))


@app.route("/tracker_detail/<int:tracker_id>",methods=["GET"])
def tracker_details(tracker_id):
    u = db.session.query(Tracker).filter(Tracker.tracker_id == tracker_id).first()
    tracker_desc = u.tracker_description 
    logs = u.trackers_log
    total_value = []
    date = []
    for log in logs:
        try:
            t = int(log.value) #avoiding graph for trackers whose value is string(MCQ  type tracker)
            total_value.append(float(log.value))
            date.append("{:%d, %m, %Y}".format(log.log_time))
        except:
            total_value = []
            
    #Bar graph
    c = ['red', 'yellow', 'black', 'blue', 'orange','green']
    path = "static/numerical_log.png"
    if os.path.exists(path):
        os.remove(path)
    fig, ax = plt.subplots()
    plt.bar(date, total_value, color = c,width=0.7)
    fig.autofmt_xdate()
    plt.xlabel("Timestamp")
    plt.ylabel("Values")
    ax.set_facecolor("lightyellow")
    plt.savefig("static/numerical_log_barchart.png")
    plt.clf()
    
    #Line chart
    path = "static/numerical_log_linechart.png"
    if os.path.exists(path):
        os.remove(path)
    fig, ax = plt.subplots()
    plt.plot(date,total_value,"-g")
    fig.autofmt_xdate()
    plt.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.xlabel("Timestamp")
    plt.ylabel("Values")
    ax.set_facecolor("lightyellow")
    plt.savefig("static/numerical_log_linechart.png")
    plt.clf()

    #scatter plot
    path = "static/numerical_log_scatterplot.png"
    if os.path.exists(path):
        os.remove(path)
    fig, ax = plt.subplots()
    #plt.figure(facecolor="orange")  changing the image
    plt.scatter(date,total_value)
    fig.autofmt_xdate()
    plt.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.xlabel("Timestamp")
    plt.ylabel("Values")
    ax.set_facecolor("lawngreen")
    plt.savefig("static/numerical_log_scatterplot.png")
    plt.clf()

    today_date = datetime.date.today()
    return render_template("tracker_details.html",tr = u.tracker_name,td=tracker_desc,t=logs,total=sum(total_value),tracker_type = u.tracker_type,today_date = today_date)


@app.route("/delete/log/<int:log_id>",methods=["GET","POST"])
def delete_log(log_id):
    log = db.session.query(Logs).filter(Logs.logs_id == log_id).first()
    t_id = log.tracker_id
    u = db.session.query(Tracker).filter(Tracker.tracker_id == t_id).first()
    db.session.delete(log)
    db.session.commit()
    return redirect("/tracker_detail/{}".format(t_id))


@app.route("/update/log/<int:log_id>",methods=["GET","POST"])
def update_log(log_id):
    if request.method == "GET":
        log = db.session.query(Logs).filter(Logs.logs_id == log_id).first()
        t_id = log.tracker_id
        tracker = db.session.query(Tracker).filter(Tracker.tracker_id == t_id).first()
        t_type = tracker.tracker_type
        t=datetime.datetime.now()
        if t_type == "Numerical":
            return render_template("update_log_numerical.html",ctime=t,log_id = log_id,tt = tracker.tracker_name)
        elif t_type == "Multiple Choice":
            setting_list = tracker.setting.split(',')
            return render_template("update_log_mcq.html",ctime=t,log_id = log_id,tt = tracker.tracker_name,L=setting_list)
        elif t_type == "Boolean":
            return render_template("update_log_boolean.html",ctime=t,log_id = log_id,tt = tracker.tracker_name)
    else:
        log = db.session.query(Logs).filter(Logs.logs_id == log_id).first()
        t_id = log.tracker_id
        tracker = db.session.query(Tracker).filter(Tracker.tracker_id == t_id).first()
        t_type = tracker.tracker_type
        v = request.form.get("value")
        notes = request.form.get("notes") 
        time=datetime.datetime.now()
        if t_type == "Boolean":
            d = {"YES":1,"NO":0}
            if v not in d:
                return render_template("wrong_boolean.html",trname = tracker.tracker_name )
            v = d[v]
        log.log_time = time
        log.value = v
        log.note=notes
        log.tracker_id = tracker.tracker_id
        log.user_id = tracker.user_id
        db.session.commit()
        return redirect("/tracker_detail/{}".format(t_id))
    
# @app.route("/my_diary",methods=["GET","POST"])
# def diary():
#     todayz_date = datetime.date.today()
#     if request.method == "GET":
#         return render_template("diary.html",today_date = todayz_date)
#     else:
#         pass
