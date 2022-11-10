
from flask import Flask, render_template, request, redirect, json
import os
import database.db_connector as db
import MySQLdb
import mysql.connector


# Configuration

app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = 'cs340_arringtd'
# app.config['MYSQL_PASSWORD'] = '4451' #last 4 of onid
# app.config['MYSQL_DB'] = 'cs340_arringtd'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Routes 

@app.route('/')
def root():

    return render_template("index.j2")

@app.route('/cars', methods=["POST", "GET", "DELETE"])
def cars():

    if request.method == "GET":
        query = "SELECT * FROM Cars;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("cars.j2", cars=results)

    if request.method == "POST":
        if request.form.get("addCar"):
            carMake = request.form["carMake"]
            carModel = request.form["carModel"]
            carYear = request.form["carYear"]
            # if carMake != '' and carModel != '' and carYear != '':
            query = "INSERT INTO Cars (carMake, carModel, carYear) VALUES (%s, %s, %s);"
            cursor = db_connection.cursor()
            cursor.execute(query, (carMake, carModel, carYear,))
            db_connection.commit()

        return redirect("/cars")

@app.route('/delete_cars/<int:carModelID>')
def delete_cars(carModelID):
    query = "DELETE FROM Cars WHERE carModelID = '%s';"
    cursor = db_connection.cursor()
    cursor.execute(query, (carModelID,))
    db_connection.commit()

    return redirect("/cars")

# Listener

if __name__ == "__main__":

    db_connection = db.connect_to_database()

    port = int(os.environ.get('PORT', 6767)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)