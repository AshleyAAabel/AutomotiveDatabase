
from flask import Flask, render_template, request, redirect, json
import os
import database.db_connector as db
import mysql.connector
from flask_mysqldb import MySQL

# Configuration

app = Flask(__name__)

# db_connection = db.connect_to_database()
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_arringtd'
app.config['MYSQL_PASSWORD'] = '4451' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_arringtd'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)
# Routes 

@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/customers', methods=["POST", "GET", "DELETE"])
def customers():
    if request.method == "GET":
        query = "SELECT * FROM Customers;"
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
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
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (firstName, lastName, phoneNumber, email,))
                # db_connection.commit()
                mysql.connection.commit()

        return redirect("/customers")

@app.route('/edit_customer/<int:customerID>', methods=["POST", "GET"])
def edit_customer(customerID):

    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
        # cur = db_connection.cursor()
        # cur.execute(query)
        # data = cur.fetchall()
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template("edit_customer.j2", customers=data)

    if request.method == "POST":
        if request.form.get("editCustomer"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            phoneNumber = request.form["phoneNumber"]
            email = request.form["email"]

            query = "UPDATE Customers SET Customers.firstName = %s, Customers.lastName = %s, Customers.phoneNumber = %s, Customers.email = %s WHERE Customers.customerID = %s;"
            # cursor = db_connection.cursor()
            cursor = mysql.connection.cursor()
            cursor.execute(query, (firstName, lastName, phoneNumber, email, customerID))
            # db_connection.commit()
            mysql.connection.commit()
        return redirect("/customers")

@app.route('/cars', methods=["POST", "GET", "DELETE"])
def cars():

    if request.method == "GET":
        query = "SELECT * FROM Cars;"
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("cars.j2", cars=results)

    if request.method == "POST":
        if request.form.get("addCar"):
            carMake = request.form["carMake"]
            carModel = request.form["carModel"]
            carYear = request.form["carYear"]
            if carMake != '' and carModel != '' and carYear != '':
                query = "INSERT INTO Cars (carMake, carModel, carYear) VALUES (%s, %s, %s);"
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (carMake, carModel, carYear,))
                # db_connection.commit()
                mysql.connection.commit()

        return redirect("/cars")

@app.route('/delete_cars/<int:carModelID>')
def delete_cars(carModelID):

    query = "DELETE FROM Cars WHERE carModelID = '%s';"
    # cursor = db_connection.cursor()
    cursor = mysql.connection.cursor()
    cursor.execute(query, (carModelID,))
    # db_connection.commit()
    mysql.connection.commit()

    return redirect("/cars")

@app.route('/recalls', methods=["POST", "GET"])
def recalls():
    if request.method == "GET":
        query = "SELECT * FROM Recalls;"
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("recalls.j2", recalls=results)

    if request.method == "POST":
        if request.form.get("addRecall"):
            recallType = request.form["recallType"]
            dateIssued = request.form["dateIssued"]
            if recallType != '' and dateIssued != '':
                query = "INSERT INTO Recalls (recallType, dateIssued) VALUES (%s, %s);"
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (recallType, dateIssued,))
                # db_connection.commit()
                mysql.connection.commit()
        return redirect("/recalls")

@app.route('/customers_vehicles', methods=["POST", "GET", "DELETE"])
def customers_vehicles():
    if request.method == "GET":
        
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        customers_query = "SELECT * FROM Customers ORDER BY Customers.firstName;"
        customers_cursor = mysql.connection.cursor()
        customers_cursor.execute(customers_query)
        customers_results = customers_cursor.fetchall()

        cars_query = "SELECT * FROM Cars ORDER BY Cars.carMake;"
        cars_cursor = mysql.connection.cursor()
        cars_cursor.execute(cars_query)
        cars_results = cars_cursor.fetchall()

        query = "SELECT CustomersVehicles.customerVehicleID, CustomersVehicles.vinNumber, CustomersVehicles.saleDate, CustomersVehicles.lastServiceDate, Customers.firstName, Customers.lastName, Customers.phoneNumber, Cars.carMake, Cars.carModel, Cars.carYear FROM CustomersVehicles INNER JOIN Customers ON CustomersVehicles.customerID = Customers.customerID INNER JOIN Cars ON CustomersVehicles.carModelID = Cars.carModelID;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        return render_template("customers_vehicles.j2", customersVehicles=results, cars=cars_results, customers=customers_results)

    if request.method == "POST":
        if request.form.get("addCustomersVehicle"):
            customerID = request.form["customerID"]
            carModelID = request.form["carModelID"]
            vinNumber = request.form["vinNumber"]
            saleDate = request.form["saleDate"]
            lastServiceDate = request.form["lastServiceDate"]
            if customerID != '' and carModelID != '' and vinNumber != '' and saleDate != '' and lastServiceDate != '':
                query = "INSERT INTO CustomersVehicles (customerID, carModelID, vinNumber, saleDate, lastServiceDate) VALUES (%s, %s, %s, %s, %s);"
                print("DEBUGGG" + customerID + carModelID + vinNumber + saleDate + lastServiceDate)
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (customerID, carModelID, vinNumber, saleDate, lastServiceDate,))
                # db_connection.commit()
                mysql.connection.commit()
        return redirect("/customers_vehicles")

@app.route('/edit_customers_vehicle/<int:customerVehicleID>', methods=["POST", "GET"])
def edit_customers_vehicles(customerVehicleID):
    if request.method == "GET":
        query = "SELECT * FROM CustomersVehicles WHERE customerVehicleID = %s;" % (customerVehicleID)
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("edit_customers_vehicle.j2", customersVehicle=results)

    if request.method == "POST":
        if request.form.get("editCustomersVehicle"):
            lastServiceDate = request.form["lastServiceDate"]
            if lastServiceDate != '':
                query = "UPDATE CustomersVehicles SET CustomersVehicles.lastServiceDate = %s WHERE CustomersVehicles.customerVehicleID = %s;"
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (lastServiceDate, customerVehicleID,))
                # db_connection.commit()
                mysql.connection.commit()
        # if request.form.get("cancelEditCustomersVehicle"):
        #     return redirect("/customers_vehicles")
        return redirect("/customers_vehicles")

@app.route('/delete_customers_vehicle/<int:customerVehicleID>')
def delete_customers_vehicle(customerVehicleID):

    query = "DELETE FROM CustomersVehicles WHERE customerVehicleID = '%s';"
    # cursor = db_connection.cursor()
    cursor = mysql.connection.cursor()
    cursor.execute(query, (customerVehicleID,))
    # db_connection.commit()
    mysql.connection.commit()

    return redirect("/customers_vehicles")

# Listener

if __name__ == "__main__":



    port = int(os.environ.get('PORT', 6768)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)