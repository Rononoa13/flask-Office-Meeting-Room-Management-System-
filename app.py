from datetime import datetime
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
        times = set(db.session.query(SetMeeting.room_name).all())
        return render_template("team_lead/meeting_form.html", times=times)

#  Create function to get start time and end time:


@app.route('/view-meeting-details/<selected_room>', methods=['GET', 'POST'])
def view_meeting_details(selected_room):

    meeting_times = SetMeeting.query.all()
    print(f"meeting times -> {meeting_times}")
    
    filtered_date_time = []
    for time in meeting_times:
        print(time.id)
        # Convert string to datetime object
        start_time_string = time.start_time
        end_time_string = time.end_time

        date_format = "%Y-%m-%dT%H:%M"

        parsed_start_datetime = datetime.strptime(start_time_string, date_format)
        parsed_end_datetime = datetime.strptime(end_time_string, date_format)

        # %b for abbreviated month name, %d for day, and %Y for the year. 
        formatted_date = parsed_start_datetime.strftime("%b %d, %Y")
        # %I for hours (12-hour clock), %M for minutes, and %p for AM/PM
        formatted_start_time = parsed_start_datetime.strftime("%I:%M %p")
        formatted_end_time = parsed_end_datetime.strftime("%I:%M %p")

        if time.room_name == selected_room:
            filtered_date_time.append((time.id, formatted_date, formatted_start_time, formatted_end_time))

    return render_template('team_lead/meeting_room_details.html', id=time.id, filtered_date_time=sorted(filtered_date_time, reverse=True), selected_room=selected_room)

# Endpoint for deleting a time slot
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    time = SetMeeting.query.get(id)
    
    if time:
        # Get the selected_room before deleting the record
        selected_room = time.room_name

        db.session.delete(time)
        db.session.commit()
        
        # Redirect to the view-meeting-details page with the encoded selected room
        return redirect(f'/view-meeting-details/{selected_room}')


admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(UserRole, db.session))

if __name__ == "__main__":
    with app.app_context():
        admin.init_app(app)
        db.create_all()
    app.run(debug=True)
