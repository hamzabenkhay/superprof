import os
from flask import Flask, flash, render_template, request, redirect, url_for
from celery import Celery


app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

# set up celery client
client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)


@client.task
def process_form(data):
    print("start processing data")
    print(data)
    print("data processed successfully")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        data = {}
        data['email'] = request.form['email']
        data['first_name'] = request.form['first_name']
        data['last_name'] = request.form['last_name']
        data['message'] = request.form['message']
        duration = int(request.form['duration'])
        duration_unit = request.form['duration_unit']

        # calculate time in seconds
        if duration_unit == 'minutes':
            duration *= 60
        elif duration_unit == 'hours':
            duration *= 3600
        elif duration_unit == 'days':
            duration *= 86400

        process_form.apply_async(args=[data], countdown=duration)
        flash(f"Data will be processed in {request.form['duration']} {duration_unit}")

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
