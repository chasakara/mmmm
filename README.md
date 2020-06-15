# Traditional Herbs 

Traditional Herbs is a website that encourages the use of 
traditional herbs to cure some mild infections or mild pains 

### Features

#### As a user l want 

* to know what each herb cures 

* to know how to prepaire the herbs

* to know the effectiveness rating of the herbs 

* to read reviews about the medicine 

* to add my own herbs

* to edit my own herbs

* to delete my own herbs

* to add my own herbs

### Future Features

### Wireframes

### Technologies Used 

[https://www.gitpod.io/] - an online IDE for developing this project.

#### Front End

[https://developer.mozilla.org/en-US/docs/Web/HTML] - to build the foundation of the project.

[https://developer.mozilla.org/en-US/docs/Web/CSS] - to create custom styles.

#### Back End

[https://www.python.org/] - back-end programming language used in this project.

[https://flask.palletsprojects.com/en/1.1.x/] - microframework for building and rendering pages.

[https://www.mongodb.com/] -  NoSQL database for storing back-end data.

[https://jquery.com/] - to simplify DOM manipulation

[https://developer.mozilla.org/en-US/docs/Web/JavaScript] - to create and control dynamic website content

[https://pymongo.readthedocs.io/en/stable/] - for Python to get access the MongoDB database.

[https://www.heroku.com/] - to host the project.

#### Libraries 

[https://fonts.google.com/] - to import fonts.

[https://fontawesome.com/] - to provide icons used across the project.

[https://getbootstrap.com/] - Is a framework to help you design websites faster and easier. It includes HTML and CSS based design templates

### Testing

### Problems encountered
 

### Deployed on Heroku at { website URL HERE Traditional Herbs].

Clone the repository by copying the clone url
In the terminal type git clone followed by the copied url
cd into Traditional Herbs
In the terminal type pip3 install -r requirements.txt to install all the dependencies
Create an account on Heroku if you don't have one yet and create a new app
In the terminal, type echo "web: python main.py" > Procfile
Create a new folder inside the apps directory called secret_settings and in it a .env file or change path in app_setup.py and create the .env file anywhere you'd like
In the .env file set DBNAME, URI and SECRET_KEY
In the terminal, heroku login
git init to create a new repository
heroku git:remote -a (name of your heroku app, no brackets)
git add .
git commit -m "Initial commit"
git push heroku master
heroku ps:scale web=1
In your heroku app navigate to settings and reveal config vars, set IP = 0.0.0.0, PORT = 5000, DBNAME, URI and SECRET_KEY
restart all dynos and open your heroku app

### Credits

### Contents 

### Media

### Acknowdgements

#### This website is for educational purpose only 

