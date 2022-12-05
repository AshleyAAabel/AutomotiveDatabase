
from flask import Flask, render_template, request, redirect, json, flash, url_for
import os
import database.db_connector as db
import mysql.connector
from flask_mysqldb import MySQL

# Configuration

app = Flask(__name__)
app.secret_key = "secret key"

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
            query = "SELECT * FROM Customers;"
            # cursor = db.execute_query(db_connection=db_connection, query=query)
            cursor = mysql.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()


            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            phoneNumber = request.form["phoneNumber"]
            email = request.form["email"]
            error = None
            if not firstName or not lastName or not phoneNumber or not email:
                error = 'Please fill out all of the inputs to the form'

            if error:
                return render_template("customers.j2", customers=results, error = error)
            else:
                query = "INSERT INTO Customers (firstName, lastName, phoneNumber, email) VALUES (%s, %s, %s, %s);"
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (firstName, lastName, phoneNumber, email,))
                # db_connection.commit()
                mysql.connection.commit()
            return redirect("/customers")

        if request.form.get("findCustomer"):
            lastName = request.form["lastName"]
            return redirect(url_for('find_customer', lastName = lastName))
    

@app.route('/view_customers_vehicles/<customerID>')
def view_customers_vehicles(customerID):

    query1 = "SELECT firstName, lastName FROM Customers  WHERE customerID = %s;"
    cursor1 = mysql.connection.cursor()
    cursor1.execute(query1, (customerID))
    results1 = cursor1.fetchall()

    query = "SELECT * FROM CustomersVehicles INNER JOIN Customers ON CustomersVehicles.customerID = Customers.customerID INNER JOIN Cars ON CustomersVehicles.carModelID = Cars.carModelID WHERE CustomersVehicles.customerID = %s;;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (customerID))
    results = cursor.fetchall()

    return render_template("view_customers_vehicles.j2", customersVehicles=results, customer = results1)        
    
@app.route('/find_customer/<lastName>', methods=["GET"])
def find_customer(lastName):

    query = "SELECT * FROM Customers WHERE Customers.lastName = '%s'" % (lastName)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("find_customer.j2", customers=data, last = lastName)


@app.route('/edit_customer/<int:customerID>', methods=["POST", "GET"])
def edit_customer(customerID):

    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
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

            query = "SELECT * FROM Cars;"
            # cursor = db.execute_query(db_connection=db_connection, query=query)
            cursor = mysql.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            carMake = request.form["carMake"]
            carModel = request.form["carModel"]
            carYear = request.form["carYear"]
            error = None

            if not carMake or not carModel or not carYear:
                error = 'Please fill out all inputs for the form'


            if error:
                return render_template("cars.j2", cars=results, error = error)

            else:
                query = "INSERT INTO Cars (carMake, carModel, carYear) VALUES (%s, %s, %s);"
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (carMake, carModel, carYear,))
                # db_connection.commit()
                mysql.connection.commit()

        return redirect("/cars")

@app.route('/delete_cars/<int:carModelID>')
def delete_cars(carModelID):

    try:
        query = "DELETE FROM Cars WHERE carModelID = '%s';"
        # cursor = db_connection.cursor()
        cursor = mysql.connection.cursor()
        cursor.execute(query, (carModelID,))
        # db_connection.commit()
        mysql.connection.commit()
    except:
        flash("Cannot delete car owned by Customer")
        return render_template("flash_temp.j2")
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

        query = "SELECT CustomersVehicles.customerVehicleID, CustomersVehicles.vinNumber, CustomersVehicles.saleDate, CustomersVehicles.lastServiceDate, Customers.firstName, Customers.lastName, Customers.phoneNumber, Cars.carMake, Cars.carModel, Cars.carYear FROM CustomersVehicles LEFT JOIN Customers ON CustomersVehicles.customerID = Customers.customerID LEFT JOIN Cars ON CustomersVehicles.carModelID = Cars.carModelID;"
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
        
        if request.form.get("findVin"):
            vin = request.form["vinNumber"]
            return redirect(url_for('find_vin', vinNumber = vin))

@app.route('/find_vin/<vinNumber>', methods=["GET"])
def find_vin(vinNumber):

    query = "SELECT CustomersVehicles.customerVehicleID, CustomersVehicles.vinNumber, CustomersVehicles.saleDate, CustomersVehicles.lastServiceDate, Customers.firstName, Customers.lastName, Customers.phoneNumber, Cars.carMake, Cars.carModel, Cars.carYear FROM CustomersVehicles LEFT JOIN Customers ON CustomersVehicles.customerID = Customers.customerID LEFT JOIN Cars ON CustomersVehicles.carModelID = Cars.carModelID WHERE CustomersVehicles.vinNumber = '%s'" % (vinNumber)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("find_vin.j2", customersVehicles=data)

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
                query = "UPDATE CustomersVehicles SET CustomersVehicles.lastServiceDate = %s  WHERE CustomersVehicles.customerVehicleID = %s"
                # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (lastServiceDate, customerVehicleID,))
                # db_connection.commit()
                mysql.connection.commit()
        # if request.form.get("cancelEditCustomersVehicle"):
        #     return redirect("/customers_vehicles")
        return redirect("/customers_vehicles")

@app.route('/edit_customers_vehicle_customer/<customerVehicleID>', methods=["POST", "GET"])
def edit_customers_vehicles2(customerVehicleID):
    if request.method == "GET":
       
        customers_query = "SELECT * FROM Customers ORDER BY Customers.firstName;"
        customers_cursor = mysql.connection.cursor()
        customers_cursor.execute(customers_query)
        customers_results = customers_cursor.fetchall()

       
        query = "SELECT * FROM CustomersVehicles WHERE customerVehicleID = %s;" % (customerVehicleID)
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("edit_customers_vehicle2.j2", customersVehicle=results, customers = customers_results)

    if request.method == "POST":
        if request.form.get("editCustomersVehicle"):
            customerID = request.form["customerID"]
            if customerID != "":
                query = "UPDATE CustomersVehicles SET CustomersVehicles.customerID = %s  WHERE CustomersVehicles.customerVehicleID = %s;"
            # cursor = db_connection.cursor()
                cursor = mysql.connection.cursor()
                cursor.execute(query, (customerID, customerVehicleID,))
            # db_connection.commit()
                mysql.connection.commit()
            if customerID == "":
                query = "UPDATE CustomersVehicles SET CustomersVehicles.customerID = NULL WHERE CustomersVehicles.customerVehicleID = %s;" % (customerVehicleID)
                cursor = mysql.connection.cursor()
                cursor.execute(query)
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

@app.route('/cars_recalls', methods=["POST", "GET"])
def cars_recalls():

    if request.method == "GET":
        
        cars_query = "SELECT * FROM Cars ORDER BY Cars.carMake;"
        cars_cursor = mysql.connection.cursor()
        cars_cursor.execute(cars_query)
        cars_results = cars_cursor.fetchall()

        recalls_query = "SELECT * FROM Recalls ORDER BY Recalls.dateIssued"
        recalls_cursor = mysql.connection.cursor()
        recalls_cursor.execute(recalls_query)
        recalls_results = recalls_cursor.fetchall()

        query = "SELECT Cars.carMake, Cars.carModel, Cars.carYear, Recalls.recallType, Recalls.dateIssued, CarsRecalls.carModelID, CarsRecalls.recallID FROM CarsRecalls INNER JOIN Cars ON CarsRecalls.carModelID = Cars.carModelID INNER JOIN Recalls ON CarsRecalls.recallID =Recalls.recallID;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        return render_template("cars_recalls.j2", carsRecalls=results, cars=cars_results, recalls=recalls_results)



    if request.method == "POST":
        if request.form.get("addCarRecall"):
            carModelID = request.form["carModelID"]
            recallID = request.form["recallID"]
            query = "INSERT INTO CarsRecalls (carModelID, recallID) VALUES (%s, %s)"
            """vrsquery = "INSERT INTO VehicleRecallStatus (customerVehicleID, recallID) SELECT CustomersVehicles.customerVehicleID, Recalls.recallID FROM CustomersVehicles INNER JOIN Cars ON CustomersVehicles.carModelID = Cars.carModelID INNER JOIN CarsRecalls ON Cars.carModelID = CarsRecalls.carModelID INNER JOIN Recalls ON CarsRecalls.recallID = Recalls.recallID WHERE Cars.carModelID = %s AND Recalls.recallID = %s"
            vrscursor = mysql.connection.cursor()
            vrscursor.execute(vrsquery,(carModelID, recallID,))"""
            cursor = mysql.connection.cursor()
            cursor.execute(query, (carModelID, recallID,))
            mysql.connection.commit()
        return redirect("/cars_recalls")

@app.route('/view_cars_recalls/<carModelID>')
def view_cars_recalls(carModelID):

    query = "SELECT Cars.carMake, Cars.carModel, Cars.carYear, Recalls.recallType, Recalls.dateIssued, CarsRecalls.carModelID, CarsRecalls.recallID FROM CarsRecalls INNER JOIN Cars ON CarsRecalls.carModelID=Cars.carModelID INNER JOIN Recalls ON CarsRecalls.recallID=Recalls.recallID WHERE CarsRecalls.carModelID = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (carModelID))
    results = cursor.fetchall()

    return render_template("view_cars_recalls.j2", viewRecalls=results)

@app.route('/view_recalls_cars/<recallID>')
def view_recalls_cars(recallID):

    query = "SELECT Cars.carMake, Cars.carModel, Cars.carYear, Recalls.recallType, Recalls.dateIssued, CarsRecalls.carModelID, CarsRecalls.recallID FROM CarsRecalls INNER JOIN Cars ON CarsRecalls.carModelID=Cars.carModelID INNER JOIN Recalls ON CarsRecalls.recallID=Recalls.recallID WHERE CarsRecalls.recallID = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (recallID))
    results = cursor.fetchall()

    return render_template("view_cars_recalls.j2", viewRecalls=results)

@app.route('/vehicle_recall_status', methods=["POST", "GET"])
def vehicle_recall_status():

    if request.method == "GET":

        cars_query = "SELECT * FROM CustomersVehicles ORDER BY CustomersVehicles.vinNumber;"
        cars_cursor = mysql.connection.cursor()
        cars_cursor.execute(cars_query)
        cars_results = cars_cursor.fetchall()

        recalls_query = "SELECT * FROM Recalls ORDER BY Recalls.dateIssued;"
        recalls_cursor = mysql.connection.cursor()
        recalls_cursor.execute(recalls_query)
        recalls_results = recalls_cursor.fetchall()

        query = "SELECT CustomersVehicles.vinNumber, Recalls.recallType, Recalls.dateIssued, VehicleRecallStatus.customerVehicleID, VehicleRecallStatus.recallID, VehicleRecallStatus.recallStatus FROM VehicleRecallStatus INNER JOIN CustomersVehicles ON VehicleRecallStatus.customerVehicleID=CustomersVehicles.customerVehicleID INNER JOIN Recalls ON VehicleRecallStatus.recallID = Recalls.recallID;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("vehicle_recall_status.j2", recallStats=results, cars=cars_results, recalls=recalls_results)
    
    if request.method == "POST":
        if request.form.get("addCustomerRecall"):
            customerVehicleID = request.form["customerVehicleID"]
            recallID = request.form["recallID"]
            recallStatus = int(request.form["recallStatus"])
            query = "INSERT INTO VehicleRecallStatus VALUES (%s, %s, %s)"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (customerVehicleID, recallID, recallStatus))
            mysql.connection.commit()
        return redirect("/vehicle_recall_status")


@app.route('/update_vehicle_recall_status/<customerVehicleID>/<recallID>', methods=["POST", "GET"])
def update_vehicle_recall_status(customerVehicleID, recallID):
    if request.method == "GET":
        query = "SELECT VehicleRecallStatus.customerVehicleID, VehicleRecallStatus.recallID, VehicleRecallStatus.recallStatus FROM VehicleRecallStatus INNER JOIN CustomersVehicles ON VehicleRecallStatus.customerVehicleID=CustomersVehicles.customerVehicleID INNER JOIN Recalls ON VehicleRecallStatus.recallID = Recalls.recallID WHERE VehicleRecallStatus.customerVehicleID = %s AND VehicleRecallStatus.recallID = %s;"
        # cursor = db.execute_query(db_connection=db_connection, query=query)
        cursor = mysql.connection.cursor()
        cursor.execute(query, (customerVehicleID, recallID))
        results = cursor.fetchall()
        return render_template("update_vehicle_recall_status.j2")

    if request.method == "POST":
        if request.form.get("updateVehicleRecallStatus"):
            recallStatus = request.form["recallStatus"]
            query = "UPDATE VehicleRecallStatus SET VehicleRecallStatus.recallStatus = %s WHERE VehicleRecallStatus.customerVehicleID = %s;"
            # cursor = db_connection.cursor()
            cursor = mysql.connection.cursor()
            cursor.execute(query, (recallStatus, customerVehicleID))
            # db_connection.commit()
            mysql.connection.commit()
        # if request.form.get("cancelEditCustomersVehicle"):
        #     return redirect("/customers_vehicles")
        return redirect("/vehicle_recall_status")




# Listener

if __name__ == "__main__":



    port = int(os.environ.get('PORT', 6768)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)
