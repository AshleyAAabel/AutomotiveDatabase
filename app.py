
from flask import Flask, render_template, request, redirect, json
import os
import database.db_connector as db
import MySQLdb
import mysql.connector

# Configuration

app = Flask(__name__)

db_connection = db.connect_to_database()
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_arringtd'
app.config['MYSQL_PASSWORD'] = '4451' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_arringtd'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Routes 

@app.route('/')
def root():

    return render_template("index.j2")

@app.route('/customers', methods=["POST", "GET", "DELETE"])
def customers():
    if request.method == "GET":
        query = "SELECT * FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("customers.j2", customers=results)

    if request.method == "POST":
        if request.form.get("addCustomer"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            phoneNumber = request.form["phoneNumber"]
            email = request.form["email"]
            if firstName != '' and lastName != '' and phoneNumber != '' and email != '':
                query = "INSERT INTO Customers (firstName, lastName, phoneNumber, email) VALUES (%s, %s, %s, %s);"
                cursor = db_connection.cursor()
                cursor.execute(query, (firstName, lastName, phoneNumber, email,))
                db_connection.commit()

        return redirect("/customers")

@app.route('/edit_customer/<int:customerID>', methods=["POST", "GET"])
def edit_customer(customerID):

    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
        # cur = db_connection.cursor()
        # cur.execute(query)
        # data = cur.fetchall()
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()
        return render_template("edit_customer.j2", customers=data)

    if request.method == "POST":
        if request.form.get("editCustomer"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            phoneNumber = request.form["phoneNumber"]
            email = request.form["email"]

            query = "UPDATE Customers SET Customers.firstName = %s, Customers.lastName = %s, Customers.phoneNumber = %s, Customers.email = %s WHERE Customers.customerID = %s;"
            print(query)
            cur = db_connection.cursor()
            cur.execute(query, (firstName, lastName, phoneNumber, email, customerID))
            db_connection.commit()
        return redirect("/customers")

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
            if carMake != '' and carModel != '' and carYear != '':
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



    port = int(os.environ.get('PORT', 6767)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)