import os
from flask import Flask, redirect, render_template, flash, url_for, request, session, abort
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from bson.objectid import ObjectId
import datetime
import bcrypt
import re
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config['MONGODB_NAME'] = "traditional-Herbs"
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)
CKEditor(app)

@app.route('/')
@app.route("/index")
def index():
    herbs = mongo.db.herbs
    top_trending = ([herb for herb in herbs.aggregate
                        ([{"$sample": {"size": 4}}])])
    return render_template('index.html', top_trending=top_trending,
                           title='Home')

@app.route('/all_herbs')
def all_herbs():
    today = datetime.datetime.now().strftime('%d/%B/%Y - %H:%M')
    # If there is a user logged: Username is printed in the Nav
    if 'username' in session:
        # Puts the herb in order Newest to oldest
        return render_template("all_herbs.html",
                               session_name=session['username'],
                               today=today,
                               herbs=mongo.db.herbs.find().sort("_id", -1))
    # Puts the herbs in order Newest to oldest but with out the login username
    return render_template("all_herbs.html",
                           herbs=mongo.db.herbs.find().sort("_id", -1))


@app.route('/my_herbs')
def my_herbs():
    session_name = session['username']
    return render_template("all_herbs.html",
                           session_name=session['username'],
                           herbs=mongo.db.herbs.find({
                               'username': session_name}))


@app.route('/herb/<herb_id>')
def herb(herb_id): 
    herb = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
    if 'username' in session:
        return render_template('herb.html',
                               session_name=session['username'],
                               herb=herb)
    return render_template('herb.html', herb=herb)



@app.route('/add_herb', methods=['POST', 'GET'])
def add_herb():
    today_string = datetime.datetime.now().strftime('%d/%m/%y')
    today_iso = datetime.datetime.now()
    if 'username' in session:
        if request.method == 'POST':
            herbs = mongo.db.herbs
            herbs.insert({
                'username': session['username'],  #Now gets the username from session
                'herb_name': request.form.get('herb_name'),
                'herb_cure': request.form.get('herb_cure'),
                'herb_description': request.form.get('herb_description'),
                'herb_preparation': request.form.get('herb_preparation'),
                'herb_usage': request.form.get('herb_usage'),
                'herb_image': request.form.get('herb_image'),
                'date_added': today_string,
                'date_iso': today_iso})
            flash('Your Herb was successfully added')
            return redirect(url_for('all_herbs'))
        return render_template("add_herb.html",
                               session_name=session['username'])
    flash('You must be logged in to add a new herb')
    return redirect(url_for('login'))


@app.route('/edit_herb/<herb_id>', methods=['POST', 'GET'])
def edit_herb(herb_id):
    if 'username' in session:
        herb = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
        if session['username'] == herb['username']:
            if request.method == 'POST':
                herbs = mongo.db.herbs
                herbs.update({'_id': ObjectId(herb_id)},
                               {'username': request.form.get('username'),
                                'herb_name': request.form.get('herb_name'),
                                'herb_cure': request.form.get('herb_cure'),
                                'herb_description': request.form.get('herb_description'),
                                'herb_preparation': request.form.get('herb_preparation'),
                                'herb_usage': request.form.get('herb_usage'),
                                'herb_image': request.form.get('herb_image'),
                                'date_added': request.form.get('date_added'),
                                'update_iso': datetime.datetime.now()})
                flash(' You have Successfully Updated Your Herb', 'success')
                return redirect(url_for('my_herbs', herb=herb))
            return render_template('edit_herb.html',
                                   session_name=session['username'],
                                   herb=herb)
    flash('Sorry! You must be logged in first')
    return redirect(url_for('login'))


@app.route('/delete_herb/<herb_id>')
def delete_herb(herb_id):
    if 'username' in session:
        herbs = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
        if session['username'] == herbs['username']:
            herb = mongo.db.herbs.remove({'_id': ObjectId(herb_id)})
            return redirect(url_for('all_herbs'))
        flash('Sorry! You must be logged in first')
        return redirect(url_for('login'))
    flash('Sorry! You must be logged in first')
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        time = datetime.datetime.now()
        existing_email = users.find_one({'email': request.form['userEmail']})
        if existing_email is None:
            hashpass = bcrypt.hashpw(
                request.form['userPassword'].encode('utf-8'), bcrypt.gensalt())
            users.insert({
                'name': request.form['username'].capitalize(),
                'email': request.form['userEmail'].lower(),
                'password': hashpass,
                'reg_date': time
            })
            session['username'] = request.form['username']
            session['logged_in'] = True
            flash('Hello ' + session['username'] + ' You have successfull signedup')
            return redirect(url_for('all_herbs',))
        flash('That email already exists')
        return render_template('signup.html')
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['userEmail']})
        if login_user:
            if bcrypt.checkpw(request.form['userPassword'].encode('utf-8'),
                              login_user['password']):
                session['username'] = login_user['name']
                session['logged_in'] = True
                flash('Welcome Back ' +
                      session['username'] + ' You are now Logged In', 'success')
                return redirect(url_for('all_herbs'))
            flash('This Username or Password is invalid')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('all_herbs'))

@app.route('/all_reviews')
def all_reviews():
    return render_template('all_reviews.html',
                           reviews=mongo.db.reviews.find().sort("_id", -1))


@app.route('/add_review', methods=['POST', 'GET'])
def add_review():
    today_string=datetime.datetime.now().strftime('%d/%m/%y')
    today_iso=datetime.datetime.now()
    if 'username' in session:
        if request.method == 'POST':
            reviews = mongo.db.reviews
            reviews.insert({
                'username': session['username'], 
                'your_review': request.form.get('your_review'),
                'date_added': today_string,
                'date_iso': today_iso})
            flash('Your Review has been successfully added')
            return redirect(url_for('all_reviews'))
        return render_template("add_review.html", session_name = session['username'])
    flash('You must be logged in to add a review')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    app.logger.info(f'Page not found: {request.url}')
    return render_template('errors/404.html', error=error)


@app.errorhandler(500)
def page_not_found(error):
    app.logger.info(f'Server Error: {request.url}')
    return render_template('errors/500.html', error=error)


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)



