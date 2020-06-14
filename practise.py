@app.route('/')
@app.route('/all_herb')
def all_herb():
    today = datetime.datetime.now().strftime('%d/%B/%Y - %H:%M')
    # If there is a user logged: Username is printed in the Nav
    if 'username' in session:
        # Puts the herb in order Newest to oldest
        return render_template("all_herbs.html",
                               session_name=session['username'],
                               today=today,
                               herbs=mongo.db.herbs.find().sort("_id", -1))
    # Puts the resipe in order Newest to oldest but with out the login username
    return render_template("all_herbs.html",
                           herbs=mongo.db.herbs.find().sort("_id", -1))



@app.route('/myherbs')
def myherbs():

    session_name = session['username']
    return render_template("public/all_herbs.html",
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
            flash('Hello ' + session['username'] +
                  ' You have successfull signedup')
            return redirect(url_for('all_herb',))
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
                return redirect(url_for('all_herb'))
            flash('This Username or Password is invalid)
            return render_template('login.html')
    return render_template('login.html')


@app.route('/add_herb, methods=['POST', 'GET'])
def add_herb():
    today_string = datetime.datetime.now().strftime('%d/%m/%y')
    today_iso = datetime.datetime.now()
    if 'username' in session:
        if request.method == 'POST':
            herbs = mongo.db.herbs
            herbs.insert({
                'username': request.form.get('username'),
                'herb_name': request.form.get('herb_name'),
                'herb_cure': request.form.get('herb_cure'),
                'herb_description': request.form.get('herb_description'),
                'herb_preparation': request.form.get('herb_preparation'),
                'herb_usage': request.form.get('herb_usage'),
                'herb_image': request.form.get('herb_image'),
                'date_added': today_string,
                'date_iso': today_iso})
            flash('Your Herb was successfully added')
            return redirect(url_for('all_herb'))
        return render_template("add_herb.html",
                               session_name=session['username'])
    flash('You must be logged in to add a new herb')
    return redirect(url_for('login'))


@app.route('/delete_herb/<herb_id>')
def delete_herb(herb_id):

    if 'username' in session:
        herbs = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
        if session['username'] == recipes['username']:
            herb = mongo.db.herbs.remove({'_id': ObjectId(herb_id)})
            return redirect(url_for('all_herb'))
        flash('Sorry! You must be logged in first')
        return redirect(url_for('login'))
    flash('Sorry! You must be logged in first')
    return redirect(url_for('login'))


@app.route('/edit_herb/<herb_id>', methods=['POST', 'GET'])
def edit_herb(herb_id):

    if 'username' in session:
        herb = mongo.db.herbs.find_one({'_id': ObjectId(herb_id)})
        if session['username'] == herb['username']:
            if request.method == 'POST':
                herbs = mongo.db.herbs
                herbs.update({'_id': ObjectId(recipe_id)},
                               {'username': request.form.get('username'),
                                'herb_name': request.form.get('herb_name'),
                                'herb_cure': request.form.get('herb_cure'),
                                'herb_description': request.form.get('herb_description'),
                                'herb_preparation': request.form.get('herb_preparation'),
                                'herb_usage': request.form.get('herb_usage'),
                                'herb_image': request.form.get('herb_image'),
                                'date_added': request.form.get('date_added'),
                                'update_iso': datetime.datetime.now()})
                flash(' You have Successfully Updated Your Heb', 'success')
                return redirect(url_for('all_herb', herb=herb))
            return render_template('edit_herb.html',
                                   session_name=session['username'],
                                   herb=herb)
    flash('Sorry! You must be logged in first')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
   
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('all_herb'))


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