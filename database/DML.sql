--Get car make for dropdown in CustomersVehicles and CarsRecalls
SELECT carMake FROM Cars;

--Get car model for dropdown in CustomersVehicles and CarsRecalls
SELECT carModel FROM Cars;

--Get year for dropwdown in CustomersVehicles and CarsRecalls
SELECT carYear FROM Cars;


--CARS TABLE GENERAL QUERIES(READ AND CREATE)

--Display all cars in Cars table
SELECT * FROM Cars;

--Insert new car into Cars table
INSERT INTO Cars(carMake, carModel, carYear)
VALUES(:carMakeInput, :carModelInput, :carYearInput);


--CUSTOMERS TABLE GENERAL QUERIES(READ, CREATE, AND UPDATE)

--Display all customers in Customers table
SELECT * FROM Customers;

--Insert new customer into Customers table
INSERT INTO Customers(firstName, lastName, phoneNumber, email)
VALUES(:firstNameInput, :lastNameInput, :phoneNumberInput, :emailInput);

--Update customer information in Customers table
UPDATE Customers 
SET firstName = :firstNameInput, lastName = :lastNameInput, phoneNumber = :phoneNumberInput, email = :emailInput
WHERE customerID = :selectedCustomer;

--Implements Search feature for Customers
SELECT * FROM Customers WHERE firstName = :firstNameInput AND lastName = :lastNameInput;

--CUSTOMERS VEHICLES TABLE GENERAL QUERIES(READ, CREATE, UPDATE, AND DELETE)

--Display all vehicles owned
SELECT * FROM CustomersVehicles;

--Display all vehicles owned by selected customer
SELECT * FROM CustomersVehicles WHERE customerID = :selectedCustomer;

--Add new vehicle for customer
INSERT INTO CustomersVehicles(carModelID, customerID, salesDate, lastServiceDate, vinNumber)
VALUES((SELECT carModelID FROM Cars WHERE carModel = :carModelSelected AND carMake = :carMakeSelected AND carYear = :carYearSelected),
(SELECT customerID FROM Customers WHERE firstName = :firstNameInput AND lastName = :lastNameInput AND phoneNumber = :phoneNumberInput)
, :salesDateInput, :lastServiceDateInput, :vinNumberInput);

--Update last service date of vehicle
UPDATE CustomersVehicles
SET lastServiceDate = :lastServiceDateInput
WHERE customerVehicleID = :customerVehicleIDSelected;

--Delete customers vehicle
DELETE FROM CustomersVehicles WHERE customerVehicleID = :customerVehicleIDSelected;


--RECALLS TABLE GENERAL QUERIES(READ, CREATE)

--Display all recalls
SELECT * FROM Recalls;

--Add new recall
INSERT INTO Recalls(recallType, dateIssued)
VALUES(:recallTypeInput, :dateIssuedInput);


--VEHICLE RECALL STATUS TABLE GENERAL QUERIES(READ, CREATE, UPDATE)

--Display all entries
SELECT * FROM VehicleRecallStatus;

--Create new vehicle recall status
INSERT INTO VehicleRecallStatus(recallID, customerVehicleID, recallStatus)
VALUES(:recallIDSelected, 
(SELECT customerVehicleID FROM CustomersVehicles WHERE vinNumber = :vinNumberSelected)
, :recallStatusSelected);

--Update vehicle recall status
UPDATE VehicleRecallStatus
SET recallStatus = :recallStatusSelected
WHERE recallID = :recallIDSelected AND customerVehicleID = :customerVehicleIDSelected;


--CARS RECALL TABLE GENERAL QUERIES(READ AND CREATE)

--Display all cars and recalls
SELECT * FROM CarsRecalls

--Display recalls for specific car
SELECT recallID FROM CarsRecalls 
WHERE carModelID = (SELECT carModelID FROM Cars WHERE carMake = :carMakeSelected AND carModel = :carModelSelected AND carYear = :carYearSelected);

--Display cars for specific recall
SELECT carModelID FROM CarsRecalls WHERE recallID = :recallIDSelected;

--Create new recall and car relationship
INSERT INTO CarsRecalls(recallID, carModelID)
VALUES(:recallIDSelected, (SELECT carModelID FROM Cars WHERE carModel = :carModelSelected AND carMake = :carMakeSelected AND carYear = :carYearSelected);



