# group-20
software engineer project
1
Readme file for group_20's Dublin Bike Software Engineering project.

Team members:

Yi Wu
Wingki Chung
Yiyuan Geng
The application can be accessed at: http://18.203.168.242

The main goal of the application is to allow the users to plan their journey with Dublin Bike.

Weather data and bike stations information are constantly collected and stored in a SQL database. The application back-end consists of a Flask application that runs on a remote server. 

Installation instructions:

The application can be accessed at: http://18.203.168.242

To run the application locally

Pull git repository

Run flask application web/app.py

Access the web application from your browser using the local address given by flask

To run the scrapers and collect data on weather and bikes stations
Run weather_data.py and bikeMix.py to scrape data

To train and update the machine learning model
Run /web/models.py to regenerate ML models
