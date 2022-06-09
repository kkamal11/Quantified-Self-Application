# Quantified-Self-Application

## Description
A self-tracking web application where users can save and keep track of their activities and tasks. They can create, read, update and delete trackers and logs as per their requirements. Moreover, they can also visualise their progress over time graphically.

## Technologies used
    ★ Technologies Used: HTML, CSS, Flask (Python), Flask_sqlalchemy, Jinja2 and minimal JavaScript
    ★ Database: SQLite
HTML and CSS have been used for structure and styling respectively. I have used Flask as the web framework, Jinja2 for templating and SQlite for database. Additionally, JavaScript has been used once to provide extra information for MCQ type trackers the user may create

## Database Schema Design
<img src="https://github.com/kkamal11/Quantified-Self-Application/blob/main/db_image.JPG" alt="db schema image" style="height: 350px; width:450px;"/>

## Architecture and Structure
The web application is based on Client-server architecture and uses MVC (Model, View, Controller) software design pattern. <br>
The structure of the project is as follows:
<ul>
  <li>❖ Application</li>
    <ul>
      <li>Config.py :- It sets up the configuration for the application. Currently, it is set only to Local Development.</li>
      <li>controllers.py :-It contains all the controllers for the application.</li>
      <li>models.py :-It defines classes for the database tables and creates the database schema. It also enforces the integrity constraint and sets the relationship between the tables. </li>
      <li>database.py :- It simply sets up and initiates the database object.</li>
    </ul>
  <li>
    Database Directory :- This folder contains the database file.
  </li>
  <li>
    Static :-It contains all the CSS files and image files required for styling and graph generation.
  </li>
  <li>
    Templates :- It contains all the HTML files.
  </li>
  <li>
     app.py :- It is the main python file that invokes the application and initiates the server.
  </li>
 </ul>
