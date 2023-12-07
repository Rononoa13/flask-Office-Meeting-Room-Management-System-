from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect
from models import db, SetMeeting, User, UserRole, ModelView, UserView
from flask_admin import Admin
from flask_migrate import Migrate
# from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db.init_app(app)
migrate = Migrate(app, db)
admin = Admin(template_mode='bootstrap4')


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("common_templates/dashboard.html")


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

#  Create function to get start time and end time:
def human_readable_format_time(start_time_dt, end_time_dt,room_dt):
    date_only = start_time_dt.date()

    start_time = start_time_dt.strftime('%I:%M %p')
    end_time = end_time_dt.strftime('%I:%M %p')

    room_name = room_dt

    formatted_date = date_only.strftime('%B %d, %Y')

    return formatted_date, start_time, end_time, room_name
# 
@app.route('/view-meeting-details', methods=['GET', 'POST'])
def view_meeting_details():
    owners = db.session.query(SetMeeting.owner).all()
    ids = db.session.query(SetMeeting.id).all()
    meeting_times = db.session.query(SetMeeting.start_time, SetMeeting.end_time, SetMeeting.room_name)
    formatted_meeting_times = [] # to store out of for loop

    for start_time, end_time, room_name in meeting_times:
        formatted_date, start_time, end_time, room_name = human_readable_format_time(start_time, end_time, room_name)
        formatted_meeting_times.append({
            'formatted_date': formatted_date,
            'start_time': start_time,
            'end_time': end_time,
            'room_name': room_name
        })

    return render_template('team_lead/meeting_room_details.html', times=formatted_meeting_times, ids=ids, owners=owners)


admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(UserRole, db.session))

if __name__ == "__main__":
    with app.app_context():
        admin.init_app(app)
        db.create_all()
    app.run(debug=True)
