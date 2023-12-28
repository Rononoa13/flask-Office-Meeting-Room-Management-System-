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


@app.route("/")
def index():
    return redirect('dashboard')

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
        # distinct_room = db.session.query(SetMeeting.room_name).distinct().all()
        # times = db.session.query(SetMeeting.room_name).distinct().all()
        return render_template("team_lead/meeting_form.html", times=times)

#  Create function to get start time and end time:
# def human_readable_format_time(start_time_dt, end_time_dt,room_dt):
#     date_only = start_time_dt.date()

#     start_time = start_time_dt.strftime('%I:%M %p')
#     end_time = end_time_dt.strftime('%I:%M %p')

#     room_name = room_dt

#     formatted_date = date_only.strftime('%B %d, %Y')

#     return formatted_date, start_time, end_time, room_name

@app.route('/view-meeting-details', methods=['GET', 'POST'])
def view_meeting_details():
    meeting_times = SetMeeting.query.all()
    print(f"meeting times -> {meeting_times}")

    filtered_date_time = []

    for time in meeting_times:
        # Convert string to datetime object
        start_time_string = time.start_time
        end_time_string = time.end_time

        print(f"start_time_string {start_time_string}")
        print(f"end_time_string {end_time_string}")

        date_format = "%Y-%m-%dT%H:%M"

        parsed_start_datetime = datetime.strptime(start_time_string, date_format)
        parsed_end_datetime = datetime.strptime(end_time_string, date_format)

        # %b for abbreviated month name, %d for day, and %Y for the year. 
        formatted_date = parsed_start_datetime.strftime("%b %d, %Y")
        # %I for hours (12-hour clock), %M for minutes, and %p for AM/PM
        formatted_start_time = parsed_start_datetime.strftime("%I:%M %p")
        formatted_end_time = parsed_end_datetime.strftime("%I:%M %p")

        print(f"formatted date {formatted_date}")
        print(f"formatted start time {formatted_start_time}")

        print(parsed_start_datetime)
        print(f"parsed end datetime {parsed_end_datetime}")
        # print(parsed_end_datetime)
        filtered_date_time.append((formatted_date, formatted_start_time, formatted_end_time))
        print(filtered_date_time)

    return render_template('team_lead/meeting_room_details.html', filtered_date_time=filtered_date_time)

# @app.route('/view-meeting-details/<string:room_name>', methods=['GET', 'POST'])
# def view_meeting_detail(selected_room_name):
#     if selected_room_name is None:
#         return redirect('set_meeting')
#     selected_room = db.session.query(SetMeeting.room_name).all()
#     meeting_times = db.session.query(SetMeeting.id, SetMeeting.room_name, SetMeeting.start_time, SetMeeting.end_time).all()
#     print(selected_room)
#     filtered_times = [] 
#     for time in meeting_times:
#         # print(f"time => {time.room_name}")
#         # print(f"meeting_time = {meeting_times}")
#         # print(f"selected room = {selected_room}")
#         if time.room_name == selected_room[1]:
#             print(time.room_name)
#             filtered_times.append(time)

#     return render_template('team_lead/meeting_room_details.html', times=meeting_times)


# Endpoint for deleting a time slot
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    time = SetMeeting.query.get(id)
    db.session.delete(time)
    db.session.commit()
    return redirect('/view-meeting-details')


admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(UserRole, db.session))

if __name__ == "__main__":
    with app.app_context():
        admin.init_app(app)
        db.create_all()
    app.run(debug=True)
