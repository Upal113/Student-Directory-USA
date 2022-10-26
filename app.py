from calendar import firstweekday
import imp
from os import name
import firebase_admin
from flask import *
from firebase_admin import credentials, initialize_app, storage, db
import tempfile
import requests
import urllib3
import json
import fsspec
import tempfile
import json
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'superb'
# Init firebase with your credentials
cred = credentials.Certificate("student-directory-51dda-firebase-adminsdk-kv7tu-514cd4e2b7.json")


student_connect_app = initialize_app(credential=cred)
ref = db.reference("/users/", url='https://student-directory-51dda-default-rtdb.firebaseio.com/')




@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        profile_pic = request.files['profile_pic']
        temp = tempfile.NamedTemporaryFile(delete=False)
        profile_pic.save(temp.name)
        bucket = storage.bucket(name='student-directory-51dda.appspot.com', app=student_connect_app)
        blob = bucket.blob(temp.name)
        blob.upload_from_filename(temp.name)
        # Opt : if you want to make public access from the URL
        blob.make_public()
        profile_pic_url = blob.public_url
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        country = request.form.get('country')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        year = request.form.get('year')
        state = request.form.get('state')
        zip = request.form.get('zip')
        website = request.form.get('website')
        comment = request.form.get('comment')
        ref.push(
            {
                'Profile_Pic' : profile_pic_url,
                'Name' : str(first_name) + ' ' + str(last_name),
                'Country' : country,
                'About' : comment,
                'Email' : email,
                'Password' : password,
                'Phone' : phone,
                'Address' : address,
                'City' : city,
                'Year' : year,
                'State' : state,
                'Zip' : zip,
                'Instagram' : website
            }

        )
        return redirect(url_for('signup'))
    else:
        return render_template('signup.html')

@app.route('/', methods=['GET'])
def view_all():
    users_list  = ref.get()
    df = pd.read_json(json.dumps(users_list), orient='index')
    return render_template('index.html', students= df.values.tolist())


if __name__=='__main__':
    app.run(debug=True)
