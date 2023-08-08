import datetime
from flask import Flask, render_template, request, redirect
from models import db, SetMeeting


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db.init_app(app)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route('/set-meeting', methods=['GET', 'POST'])
def set_meeting():
    if request.method == 'POST':

        room_name = request.form.get('selected_option')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        
        # Add to database
        time = SetMeeting(room_name=room_name, start_time=start_time, end_time=end_time)
        db.session.add(time)
        db.session.commit()
        return redirect("/set-meeting")
    else:
        times = SetMeeting.query.all()
        return render_template("team_lead/meeting_form.html", times=times)
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
