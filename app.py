from flask import Flask, render_template, request, redirect
from utils.db import db
from models.data import *
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db.init_app(flask_app)


@flask_app.route('/')
def index():
    data = Mobile.query.all()
    return render_template('index.html', content=data)


@flask_app.route('/help')
def help():
    return render_template('help.html')


@flask_app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@flask_app.route('/add_data')
def add_data():
    return render_template('add_data.html')


with flask_app.app_context():
    db.create_all()


@flask_app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")


    age = form_data.get('age')
    gender = form_data.get('gender')
    UserBehaviorClass = form_data.get('UserBehaviorClass')


    DeviceModel = form_data.get('DeviceModel')
    OperatingSystem = form_data.get('OperatingSystem')
    AppusageTime = form_data.get('AppusageTime')
    BatteryDrain = form_data.get('BatteryDrain')
    ScreenOnTime_hours_per_day = form_data.get('ScreenOnTime_hours_per_day')
    NumberofAppsInstalled = form_data.get('NumberofAppsInstalled')
    DataUsage_MB_per_day = form_data.get('DataUsage_MB_per_day')

    user = User.query.filter_by(age=age).first()
    if not user:
        user = User( age=age, gender=gender, UserBehaviorClass=UserBehaviorClass)
        db.session.add(user)
        db.session.commit()

    data = Mobile(DeviceModel=DeviceModel, OperatingSystem=OperatingSystem,AppusageTime=AppusageTime,
                  BatteryDrain=BatteryDrain,
                  ScreenOnTime_hours_per_day=ScreenOnTime_hours_per_day,
                  NumberofAppsInstalled=NumberofAppsInstalled, DataUsage_MB_per_day=DataUsage_MB_per_day,user_id=user.id)
    db.session.add(data)
    db.session.commit()

    print("submitted successfully")
    return redirect('/')


if __name__ == '__main__':
    flask_app.run(host='127.0.0.1', port=8005,debug=True)
