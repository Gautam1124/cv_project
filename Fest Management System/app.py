from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError,InputRequired, Length
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,IntegerField,BooleanField,FileField,DateField,TimeField
from wtforms.fields.simple import EmailField
import random
import string
import os
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_login import current_user  # Add this import
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import select
from sqlalchemy import not_


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/fms'
app.config['SECRET_KEY'] = 'gkmv' 

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return participant.query.get(int(user_id))


class participant(db.Model, UserMixin):
    Pid = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(2000), nullable=False, unique=True)
    Name = db.Column(db.String(2000), nullable=False)
    Contact = db.Column(db.Integer(), nullable=False)
    CollegeName = db.Column(db.String(2000), nullable=False)
    CollegeLocation = db.Column(db.String(2000), nullable=False)
    AccBool = db.Column(db.Boolean, nullable=False)
    Accomodation = db.Column(db.String(2000), nullable=False)
    Password = db.Column(db.String(2000), nullable=False)
    is_active=db.Column(db.Boolean)

    # Override the get_id method to return the Pid
    def get_id(self):
        return str(self.Pid)




class Event_and_Participant(db.Model):
    __tablename__ = "event_and_participant"
    eid = Column(Integer, ForeignKey("event.eid"), primary_key=True)
    pid = Column(Integer, ForeignKey("participant.Pid"), primary_key=True)


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password", validators=[InputRequired()], render_kw={"placeholder": "Password"}
    )
    name = StringField(
        "Name",
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Name"},
    )
    contact = IntegerField(
        "Contact", validators=[InputRequired()], render_kw={"placeholder": "Contact"}
    )
    college_name = StringField(
        "College Name",
        validators=[InputRequired()],
        render_kw={"placeholder": "College Name"},
    )
    college_location = StringField(
        "College Location",
        validators=[InputRequired()],
        render_kw={"placeholder": "College Location"},
    )
    acc_bool = BooleanField("Accommodation Required", default=False)
    # accommodation = StringField('Accommodation', validators=[InputRequired()], render_kw={"placeholder": "Accommodation"})
    submit = SubmitField("Register")

    def validate_user(self, email):
        # Custom validation logic for the email field
        existing_user = participant.query.filter_by(Email=email.data).first()
        if existing_user:
            flash("This email is already registered.", "error")
            return 0
        return True



class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")




class Student(db.Model,UserMixin):
    roll_no=db.Column(db.String(200),primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    department=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String(2000),nullable=False,unique=True)
    is_active=db.Column(db.Boolean)
    def get_id(self):
        return self.roll_no

class Admin(db.Model):
    email=db.Column(db.String(200),nullable=False,primary_key=True)
    password=db.Column(db.String(2000),nullable=False,unique=True)
    def get_id(self):
        return self.email

class Event(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    organizer = db.Column(db.String(200))
    description = db.Column(db.String(200), nullable=False)
    winner = db.Column(db.String(200))
    runner_up = db.Column(db.String(200))
    event_over = db.Column(db.Boolean)
    image = db.Column(
        db.String(2000),
        default="login/static/images/danny-howe-bn-D2bCvpik-unsplash.jpg",
    )
    aut_bool=db.Column(db.Boolean)

class Volunteer(db.Model):
    eid=db.Column(db.Integer,primary_key=True)
    roll_no=db.Column(db.String(200),primary_key=True)

class Role(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    rname=db.Column(db.String(200),nullable=False)
    eid=db.Column(db.Integer,db.ForeignKey('event.eid'),nullable=False)
    description=db.Column(db.String(200),nullable=True)
    event=db.relationship('Event',backref=db.backref('roles',lazy=True))
 
class Student_role_event(db.Model):
    __tablename__ = 'student_role_event'
    rid = db.Column(db.Integer, db.ForeignKey('role.rid'), primary_key=True)
    roll_no = db.Column(db.String(200), db.ForeignKey('student.roll_no'), primary_key=True)
    role = db.relationship('Role', backref=db.backref('student_role_events', lazy=True))
    student = db.relationship('Student', backref=db.backref('student_role_events', lazy=True))
 
class student_register_form(FlaskForm):
    roll = StringField('Student Roll No.', validators=[DataRequired()])
    name = StringField('Student Name', validators=[DataRequired()])
    dept = StringField('Student Department', validators=[DataRequired()])
    email = StringField('Student Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
        
class student_login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class create_event_form(FlaskForm):
    image = FileField('Image', validators=[DataRequired()])
    name = StringField('Event Name', validators=[DataRequired()])
    type = StringField('Event Type', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    time = TimeField('Event Time', validators=[DataRequired()])
    venue = StringField('Event Venue', validators=[DataRequired()])
    organizer = StringField('Event Organizer',validators=[DataRequired()])
    description = StringField('Event Description', validators=[DataRequired()])
    role1_name = StringField('Role1 name')
    role1_description = StringField('Role1 Description')
    role2_name = StringField('Role2 name')
    role2_description = StringField('Role2 Description')
    role3_name = StringField('Role3 name')
    role3_description = StringField('Role3 Description')
    submit = SubmitField('Create')

class update_event(FlaskForm):
    role_name = StringField('Role name')
    role_description = StringField('Role Description')
    winner=StringField('Winner Name')
    runner=StringField('Runner Up Name')
    submit=SubmitField('Update')

class search_event_form(FlaskForm):
    event_name = StringField('Event name')
    submit=SubmitField('Search')



@app.route('/signup/student', methods=['GET', 'POST'])
def student_signup():
    form = student_register_form()
    if form.validate_on_submit():
        existing_user_email = Student.query.filter_by(
            email=form.email.data).first()
        existing_user_roll = Student.query.filter_by(
            roll_no=form.roll.data).first()
        if existing_user_email or existing_user_roll:
            flash("Student with same email/roll number exists")
            return render_template('student_register.html', form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_student = Student(roll_no=form.roll.data, name=form.name.data,department=form.dept.data,email=form.email.data,password=hashed_password,is_active=1)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash("Successfully Registered!")
        except Exception as e:
            flash("Unsuccessful!")
            return render_template('student_register.html' , form=form)

        return redirect(url_for('student_login'))
       
    return render_template('student_register.html' , form=form)


@app.route('/login/student', methods = ['GET', 'POST'])
def student_login():
    form = student_login_form()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_active==0:
                flash("User is Inactive/deleted")
                return render_template('student_login.html', form=form)
            elif bcrypt.check_password_hash(user.password, form.password.data):
                return redirect(url_for('student_dashboard',roll_no=user.roll_no))

            else:
                flash("Incorrect email/password")
                return render_template('student_login.html', form=form)
        else:
            flash("Incorrect email/password")
            return render_template('student_login.html', form=form)

    return render_template('student_login.html', form=form)

@app.route('/logout/student/<string:roll_no>', methods = ['GET', 'POST'])
def student_logout(roll_no):
    return redirect(url_for('student_login'))
    

@app.route('/dashboard/student/<string:roll_no>', methods=['GET','POST'])
def student_dashboard(roll_no):
   user=Student.query.filter_by(roll_no=roll_no).first()
   form = search_event_form()
   if user:
        Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1,Event.aut_bool==1).subquery() #HYPER-Getting only the events whose creator is active
        events_with_role = db.session.query(Event.eid).join(Event1,Event.eid==Event1.c.eid).join(Role).join(Student_role_event).filter(Student_role_event.roll_no == roll_no) #changed
        event_volunteer=db.session.query(Volunteer.eid).join(Event1,Event1.c.eid==Volunteer.eid).filter(Volunteer.roll_no==roll_no) #changed
        events_roles = db.session.query(Event.eid,Event.ename,Event.type,Event.date,Event.time,Role.rname).join(Event1,Event.eid==Event1.c.eid).join(Role).join(Student_role_event).filter(Student_role_event.roll_no == roll_no) #changed

        # Get all events except the ones where the student is playing a role
        events = (
    Event.query.join(Event1,Event.eid==Event1.c.eid).filter(~Event.eid.in_(events_with_role), ~Event.eid.in_(event_volunteer)).all()
)
        # events = db.session.query(Event).join(Event1).filter(~Event.eid.in_(events_with_role),~Event.eid.in_(event_volunteer)).all()
        if form.validate_on_submit():
            events = Event.query.join(Event1,Event.eid==Event1.c.eid).filter(~Event.eid.in_(events_with_role),~Event.eid.in_(event_volunteer)).all()
            nevents=[]
            for e in events:
                evname=e.ename.lower()
                squery=form.event_name.data.lower()
                if squery in evname:
                    nevents.append(e)
            events=nevents
        return render_template('student_dashboard.html',user=user,events=events,events_roles=events_roles,form=form)
   flash("Please login")
   return redirect(url_for('student_login'))

@app.route('/dashboard/student/<string:roll_no>/create_event', methods=['GET', 'POST'])
def create_event(roll_no):
    form=create_event_form()
    user=Student.query.filter_by(roll_no=roll_no).first()
    if user:
        if form.validate_on_submit():
            existing_event=Event.query.filter_by(ename=form.name.data).first()
            if existing_event:
                flash("Event with same name exists")
                return render_template('create_event.html',form=form,user=user)
            img_path=f"images/{form.image.data}"
            new_event = Event(ename=form.name.data, type=form.type.data,date=form.date.data,time=form.time.data,venue=form.venue.data,organizer = form.organizer.data,description=form.description.data,winner=None,runner_up=None,event_over=False,image=img_path,aut_bool=0)
            try:
                db.session.add(new_event)
                db.session.commit()
                new_eid=Event.query.filter_by(ename=form.name.data).first().eid
                new_role=Role(eid=new_eid,rname='admin',description='created this event')
                db.session.add(new_role)
                db.session.commit()
                new_rid=Role.query.filter_by(eid=new_eid,rname='admin').first().rid
                new_stu_role=Student_role_event(roll_no=roll_no,rid=new_rid)
                db.session.add(new_stu_role)
                db.session.commit()
                if form.role1_name.data:
                    new_role=Role(eid=new_eid,rname=form.role1_name.data,description=form.role1_description.data)
                    db.session.add(new_role)
                    db.session.commit()
                if form.role2_name.data:
                    new_role=Role(eid=new_eid,rname=form.role2_name.data,description=form.role2_description.data)
                    db.session.add(new_role)
                    db.session.commit()
                if form.role3_name.data:
                    new_role=Role(eid=new_eid,rname=form.role3_name.data,description=form.role3_description.data)
                    db.session.add(new_role)
                    db.session.commit()
                # print(form.image.data)
                flash("Request for event creation Successful")
            except Exception as e:
                flash("Unsuccessful")
        return render_template('create_event.html',form=form,user=user)
    flash("Please login")
    return redirect(url_for('student_login'))

@app.route('/dashboard/student/<string:roll_no>/event/<string:event_id>', methods=['GET','POST'])
def choose_role(roll_no, event_id):
    user=Student.query.filter_by(roll_no=roll_no).first()
    if request.method == 'POST':
        selected_roles = request.form.getlist('selected_roles[]')
        for role_id in selected_roles:
            if role_id=='volunteer':
                new_student_volunteer=Volunteer(eid=event_id,roll_no=roll_no)
                try:
                    db.session.add(new_student_volunteer)
                    db.session.commit()  # Add this line to commit the changes
                    flash("Role selection Successful")
                except Exception as e:
                    print(f"Error: {str(e)}")  # Print the error message
                    flash("Unsuccessful")
                continue
            new_student_role_event = Student_role_event(rid=role_id, roll_no=roll_no)
            try:
                db.session.add(new_student_role_event)
                db.session.commit()  # Add this line to commit the changes
                flash("Role selection Successful")
            except Exception as e:
                print(f"Error: {str(e)}")  # Print the error message
                flash("Unsuccessful")
        return redirect(url_for('student_dashboard', roll_no=roll_no))
    roles = Role.query.filter(Role.eid == event_id, Role.rname != 'admin').all()
    event = Event.query.filter_by(eid=event_id).first()
    return render_template('choose_a_role.html',user=user, roles=roles, roll_no=roll_no, event_id=event_id, event=event)
 
@app.route('/dashboard/student/<string:roll_no>/view_profile',methods=['GET'])
def view_profile(roll_no):
    user=Student.query.filter_by(roll_no=roll_no).first()
    return render_template("student_profile.html",user=user)

@app.route('/dashboard/student/<string:roll_no>/managed_events',methods=['GET','POST'])
def managed_events(roll_no):
    user = Student.query.filter_by(roll_no=roll_no).first()
    form = search_event_form()
    if user:
        Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1,Event.aut_bool==1).subquery() #HYPER-Getting only the events whose creator is active
        events_managed = db.session.query(Event.eid, Event.ename,Event.event_over).join(Role).join(Event1,Event.eid==Event1.c.eid).join(Student_role_event).filter(Student_role_event.roll_no == roll_no,Role.rname != "admin").all()#changed
        events_created = db.session.query(Event.eid, Event.ename,Event.event_over).join(Role).join(Event1,Event.eid==Event1.c.eid).join(Student_role_event).filter(Student_role_event.roll_no == roll_no).filter(Role.rname == 'admin').all() #changed
        events_volunteered = db.session.query(Event.eid, Event.ename,Event.event_over).join(Event1,Event.eid==Event1.c.eid).filter(Volunteer.roll_no == roll_no).filter(Event.eid == Volunteer.eid).all() #changed
        events_managed=list(set(events_managed))
        if form.validate_on_submit():
            nevents=[]
            for e in events_managed:
                evname=e.ename.lower()
                squery=form.event_name.data.lower()
                if squery in evname:
                    nevents.append(e)
            events_managed=nevents
            nevents=[]
            for e in events_created:
                evname=e.ename.lower()
                squery=form.event_name.data.lower()
                if squery in evname:
                    nevents.append(e)
            events_created=nevents
            nevents=[]
            for e in events_volunteered:
                evname=e.ename.lower()
                squery=form.event_name.data.lower()
                if squery in evname:
                    nevents.append(e)
            events_volunteered=nevents
        flag = len(list(events_managed)) + len(list(events_created))+ len(list(events_volunteered))
        print(events_volunteered)
        return render_template('student_management.html', user=user, events_managed=events_managed, events_created=events_created, events_volunteered=events_volunteered,flag=flag, roll_no=roll_no,form=form)
    flash("Please login")
    return redirect(url_for('student_login'))


@app.route('/dashboard/student/<string:roll_no>/managed_events/view_created_event/<int:event_id>/<int:over_flag>', methods=['GET','POST'])
def view_created_event(roll_no, event_id,over_flag):
    user = Student.query.filter_by(roll_no=roll_no).first()
    event = Event.query.filter(Event.eid == event_id).first()

    # Use select_from to explicitly set the left side of the join
    managers = (
        db.session.query(Student.name, Role.rname)
    .select_from(Student)
    .join(Student_role_event, Student_role_event.roll_no == Student.roll_no)
    .join(Role)
    .join(Event)
    .filter(Event.eid == event_id, Role.rname != 'admin',Student.is_active==1) # HYPER-changed
    .all()
    )
    registerd_participants = (
        db.session.query(participant.Pid,participant.Name)
    .select_from(participant)
    .join(Event_and_Participant,Event_and_Participant.pid==participant.Pid) #Hyper-changed
    .filter(participant.is_active==1,Event_and_Participant.eid==event_id)
    .all()
    )
    volunteers = (
        db.session.query(Student.name)
    .select_from(Student)
    .join(Volunteer, Volunteer.roll_no == Student.roll_no) 
    .join(Event,Event.eid==Volunteer.eid)
    .filter(Event.eid == event_id,Student.is_active==1) #changed
    .all()
    )
    roles=db.session.query(Role.rname).select_from(Role).join(Event).filter(Event.eid==event_id,Role.rname!='admin').all()
    form=update_event()
    if over_flag==1 and event.event_over==0:
        event.event_over=1
        db.session.commit()
        flash("Event Finished!")
        return redirect(url_for('view_created_event', roll_no=user.roll_no, event_id=event_id,over_flag=over_flag))
    # if over_flag==1:
    #     flash("Event Finished")


    if form.validate_on_submit():
        if form.role_name.data:
                    new_role=Role(eid=event_id,rname=form.role_name.data,description=form.role_description.data)
                    db.session.add(new_role)
                    db.session.commit()
                    flash("Role Created!")
                    return redirect(url_for('view_created_event', roll_no=user.roll_no, event_id=event_id,over_flag=over_flag))
        if form.winner.data:
            event.winner=form.winner.data
            event.runner_up=form.runner.data
            print(event.runner_up)
            db.session.commit()
            flash("Winner and Runner added!")
            return redirect(url_for('view_created_event', roll_no=user.roll_no, event_id=event_id,over_flag=over_flag))

    return render_template('view_created_event.html',volunteers=volunteers, event=event, user=user,managers=managers,registerd_participants=registerd_participants,roles=roles,form=form,over_flag=over_flag)

@app.route('/dashboard/student/<string:roll_no>/managed_events/view_managed_event/<int:event_id>/<int:over_flag>', methods=['GET'])
def view_managed_event(roll_no,event_id,over_flag):
    user = Student.query.filter_by(roll_no=roll_no).first()
    event = Event.query.filter(Event.eid == event_id).first()
    # Use select_from to explicitly set the left side of the join
    managers = (
        db.session.query(Student.name, Role.rname)
    .select_from(Student)
    .join(Student_role_event, Student_role_event.roll_no == Student.roll_no) #Hyper-changed
    .join(Role)
    .join(Event)
    .filter(Event.eid == event_id, Role.rname != 'admin',Student.is_active==1)
    .all()
    )
    registerd_participants = (
        db.session.query(participant.Pid,participant.Name)
    .select_from(participant)
    .join(Event_and_Participant,Event_and_Participant.pid==participant.Pid) #Hyper-changed
    .filter(participant.is_active==1,Event_and_Participant.eid==event_id)
    .all()
    )
    volunteers = (
        db.session.query(Student.name)
    .select_from(Student)
    .join(Volunteer, Volunteer.roll_no == Student.roll_no) #Hyper-changed
    .join(Event,Event.eid==Volunteer.eid)
    .filter(Event.eid == event_id,Student.is_active==1)
    .all()
    )
    admin=(db.session.query(Student.name)
    .select_from(Student)
    .join(Student_role_event, Student_role_event.roll_no == Student.roll_no)
    .join(Role)
    .join(Event)
    .filter(Event.eid == event_id, Role.rname == 'admin')
    .first())
    roles=db.session.query(Role.rname).select_from(Role).join(Event).filter(Event.eid==event_id,Role.rname!='admin').all()
    if over_flag==1:
        flash("Event Finished")

    return render_template('view_managed_event.html', event=event, user=user,managers=managers,roles=roles,over_flag=over_flag,admin=admin,volunteers=volunteers,registerd_participants=registerd_participants)   
    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard/<int:pid>", methods=["GET", "POST"])
@login_required
def dashboard(pid):
    if current_user.Pid != pid:
        flash("You are not authorized to view this dashboard.", "error")
        return redirect(url_for("dashboard", pid=current_user.Pid))

    # Get the search query
    search_query = request.args.get("search")

    # Query all Existing events
    Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1,Event.aut_bool==1).subquery() #HYPER-Getting only the events whose creator is active
    events_query = db.session.query(Event1)

    # If there's a search query, filter events
    if search_query:
        events_query = events_query.filter(Event.ename.ilike(f"%{search_query}%"))

    # Get all events participated by the user
    participated_event_ids = [
        event.eid for event in db.session.query(Event_and_Participant).join(Event).join(Event1,Event.eid==Event1.c.eid).filter(Event_and_Participant.pid==pid).all() #Hyper-changed1
    ]

    print(participated_event_ids)

    # Filter participated events
    participated_events = [
        event for event in events_query.all() if event.eid in participated_event_ids
    ]

    # Filter not participated events
    not_participated_events = [
        event for event in events_query.all() if event.eid not in participated_event_ids
    ]
    
    completed_events = [
        event for event in events_query.filter_by(event_over=True)
    ]
    
    not_completed_events = [
        event for event in events_query.filter_by(event_over=False)
    ]
    
    common_events = set(not_participated_events) & set(not_completed_events)

    return render_template(
        "dashboard.html",
        pid=pid,
        participated_events=participated_events,
        not_participated_events=not_participated_events,
        completed_events=completed_events,
        not_completed_events=not_completed_events,
        search_query=search_query,
        common_events=common_events,
    )


@app.route("/dashboard/Participant_account_details/<int:pid>", methods=["GET", "POST"])
@login_required
def account_details(pid):
    # Check if the current user's Pid matches the requested Pid
    if current_user.Pid != pid:
        flash("You are not authorized to view this dashboard.", "error")
        return redirect(url_for("dashboard", pid=current_user.Pid))

    Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1,Event.aut_bool==1).subquery() #HYPER-Getting only the events whose creator is active
    participated_events = (
        db.session.query(Event)
        .join(Event1,Event.eid==Event1.c.eid) #HYPER-changed
        .join(Event_and_Participant, Event.eid == Event_and_Participant.eid)
        .filter(Event_and_Participant.pid == pid)
        .all()
    )

    return render_template(
        "participant_account.html", pid=pid, participated_events=participated_events
    )


@app.route("/dashboard/<int:pid>/<int:eid>", methods=["GET", "POST"])
@login_required
def event(pid, eid):
    event = Event.query.get_or_404(eid)
    Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1,Event.aut_bool==1).subquery() #HYPER-Getting only the events whose creator is active
    events_query = db.session.query(Event1) #changed
    participated_event_ids = [
        event.eid for event in db.session.query(Event_and_Participant).join(Event).join(Event1,Event1.c.eid==Event.eid).filter(Event_and_Participant.pid==pid).all() #HYPER-changed
    ]
    
    participated_events = [
        event for event in events_query.all() if event.eid in participated_event_ids
    ]
    
    if request.method == "POST":
        # Check if the participant is already registered for the event
        # Check if the event is over
        event = db.session.query(Event).join(Event1,Event1.c.eid==Event.eid).filter_by(eid=eid).first()
        if event.event_over:

            flash("This event is already over. You cannot register for it.")
            return redirect(url_for("event", pid=pid, eid=eid))

        if db.session.query(Event_and_Participant).join(Event).join(Event1,Event1.c.eid==Event.eid).filter(Event_and_Participant.pid==pid, Event.eid==eid).first(): #HYPER-changed
            flash("You are already registered for this event.")
            return redirect(url_for("event", pid=pid, eid=eid))

        # Register the participant for the event
        registration = Event_and_Participant(pid=pid, eid=eid)
        db.session.add(registration)
        db.session.commit()

        flash("You have successfully registered for the event.", "success")
        return redirect(url_for("event", pid=pid, eid=eid))

    return render_template("event.html", event=event, pid=pid,participated_events=participated_events)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        newuser = participant.query.filter_by(Email=form.email.data).first()

        if newuser and newuser.is_active==0:
                flash("User is Inactive/deleted")
                return render_template('login.html', form=form)
        elif newuser and bcrypt.check_password_hash(newuser.Password, form.password.data):
            login_user(newuser)
            return redirect(url_for("dashboard", pid=newuser.Pid))
        

        flash("Invalid email or password.", "error")

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit() and form.validate_user(form.email):
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        Accomodation = "N/A"

        if form.acc_bool.data:
            random_number = random.randint(0, 25)
            random_letter = random.choice(string.ascii_uppercase)
            Accomodation = f"HALL{random_letter}{random_number}"
        new_user = participant(
            Email=form.email.data,
            Name=form.name.data,
            Contact=form.contact.data,
            CollegeName=form.college_name.data,
            CollegeLocation=form.college_location.data,
            AccBool=form.acc_bool.data,
            Accomodation=Accomodation,
            Password=hashed_password,
            is_active=1
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
    form=LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.password==form.password.data:
            return redirect(url_for("admin_dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("admin_login.html", form=form)

@app.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():
    Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1).subquery() #HYPER-Getting only the events whose creator is active
    active_students = db.session.query(Student).filter_by(is_active=True).all()
    deleted_students = db.session.query(Student).filter_by(is_active=False).all()
    active_participants = db.session.query(participant).filter_by(is_active=True).all()
    deleted_participants = db.session.query(participant).filter_by(is_active=False).all()
    unverified_events=db.session().query(Event).join(Event1,Event1.c.eid==Event.eid).filter(Event.aut_bool==0).all()
    verified_events=db.session().query(Event).join(Event1,Event1.c.eid==Event.eid).filter(Event.aut_bool==1).all()
    return render_template("admin_dashboard.html", a_s=active_students, d_s=deleted_students, a_p=active_participants, d_p=deleted_participants,u_e=unverified_events,v_e=verified_events)

@app.route("/admin_dashboard/delete_student/<string:roll_no>",methods=["GET"])
def delete_student(roll_no):
    stud=db.session.query(Student).filter_by(roll_no=roll_no).first()
    print(stud)
    stud.is_active=0
    db.session.commit()
    return(redirect(url_for('admin_dashboard')))

@app.route("/admin_dashboard/addback_student/<string:roll_no>",methods=["GET"])
def addback_student(roll_no):
    stud=db.session.query(Student).filter_by(roll_no=roll_no).first()
    print(stud)
    stud.is_active=1
    db.session.commit()
    return(redirect(url_for('admin_dashboard')))

@app.route("/admin_dashboard/delete_participant/<int:Pid>",methods=["GET"])
def delete_participant(Pid):
    part=db.session.query(participant).filter_by(Pid=Pid).first()
    print(part)
    part.is_active=0
    db.session.commit()
    return(redirect(url_for('admin_dashboard')))

@app.route("/admin_dashboard/addback_participant/<int:Pid>",methods=["GET"])
def addback_participant(Pid):
    part=db.session.query(participant).filter_by(Pid=Pid).first()
    print(part)
    part.is_active=1
    db.session.commit()
    return(redirect(url_for('admin_dashboard')))

@app.route('/admin_dashboard/logout/admin', methods = ['GET', 'POST'])
def admin_logout():
    return redirect(url_for('admin_login'))

@app.route('/admin_dashboard/authenticate_event/<int:eid>')
def authenticate_event(eid):
    Event1=db.session.query(Event).join(Role).join(Student_role_event).join(Student).filter(Role.rname=='admin',Student.is_active==1).subquery() #HYPER-Getting only the events whose creator is active
    event=db.session.query(Event).join(Event1,Event1.c.eid==Event.eid).filter_by(eid=eid).first()
    event.aut_bool=1
    db.session.commit()
    print(event.aut_bool)
    flash(f"Authentication of Event {event.ename} done")
    return(redirect(url_for('admin_dashboard')))

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
    app.run(debug=True)