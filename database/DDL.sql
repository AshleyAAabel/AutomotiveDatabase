/*

CS340 Project Step 2 Draft: Normalized Schema + DDL with Sample Data

Project Title: 

Pawtomotive Dealership Customer Vehicle Recall Tracking System

Members:
Dawn Arrington
Ashley Abel

*/

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS VehicleRecallStatus;
DROP TABLE IF EXISTS Recalls;
DROP TABLE IF EXISTS CustomersVehicles;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS CarsRecalls;


/*Creating the Tables*/


CREATE TABLE Cars(

        carModelID int AUTO_INCREMENT NOT NULL,
        carMake varchar(45) NOT NULL,
        carModel varchar(45) NOT NULL,
        carYear varchar(45) NOT NULL,
        PRIMARY KEY (carModelID)

);


CREATE TABLE Recalls(

        recallID int AUTO_INCREMENT NOT NULL,
        recallType varchar(255) NOT NULL,
        dateIssued date NOT NULL,
        PRIMARY KEY (recallID)

);


CREATE TABLE Customers(

        customerID int AUTO_INCREMENT NOT NULL,
        firstName varchar(45) NOT NULL,
        lastName varchar(45) NOT NULL,
        phoneNumber varchar(13) NOT NULL,
        email varchar(255) NOT NULL,
        PRIMARY KEY (customerID)

);


CREATE TABLE CustomersVehicles(

        customerVehicleID int AUTO_INCREMENT NOT NULL,
        customerID int NOT NULL,
        carModelID int NOT NULL,
        vinNumber varchar(255) NOT NULL,
        saleDate date NOT NULL,
        lastServiceDate date,
        PRIMARY KEY (customerVehicleID),
        FOREIGN KEY (customerID) REFERENCES Customers(customerID),
        FOREIGN KEY (carModelID) REFERENCES Cars(carModelID)

);

CREATE TABLE CarsRecalls(

        carModelID int NOT NULL,
        recallID int NOT NULL,
        FOREIGN KEY (carModelID) REFERENCES Cars(carModelID) ON DELETE CASCADE,
        FOREIGN KEY (recallID) REFERENCES Recalls(recallID)

);

CREATE TABLE VehicleRecallStatus(

        customerVehicleID int NOT NULL,
        recallID int NOT NULL,
        recallStatus tinyint(1) NOT NULL DEFAULT 0,
        PRIMARY KEY (customerVehicleID, recallID),
        FOREIGN KEY (recallID) REFERENCES Recalls(recallID),
        FOREIGN KEY (customerVehicleID) REFERENCES CustomersVehicles(customerVehicleID) ON DELETE CASCADE

);



/*Inserting data into tables*/

INSERT INTO Cars (carMake, carModel, carYear)
VALUES
('Cadillac', 'CT6', '2018'),
('Buick', 'Regal', '2019'),
('Mazda', 'Mazda3', '2017');

INSERT INTO Recalls (recallType, dateIssued)
VALUES
('Brakes Software', '2022-07-18'),
('Seatbelt', '2019-09-26'),
('Windshield Wipers', '2019-04-03');

INSERT INTO Customers(firstName, lastName, phoneNumber, email)
VALUES
('Dawn', 'Arrington', '333-567-1590', 'arringtd@oregonstate.edu'),
('Ashley', 'Abel', '254-247-0021', 'abelas@oregonstate.edu'),
('Hannah', 'Montana', '555-236-1845', 'montanh@oregonstate.edu');

INSERT INTO CustomersVehicles(customerID, carModelID, vinNumber, saleDate, lastServiceDate)
VALUES
((SELECT customerID FROM Customers WHERE firstName = 'Dawn' AND lastName = 'Arrington'), (SELECT carModelID FROM Cars WHERE carMake = 'Buick' AND carModel = 'Regal' AND carYear = '2019' ), '1LNHM86S32Y623854', '2019-10-23', '2022-01-25'),
((SELECT customerID FROM Customers WHERE firstName = 'Ashley' AND lastName = 'Abel'), (SELECT carModelID FROM Cars WHERE carMake = 'Mazda' AND carModel = 'Mazda3' AND carYear = '2017'), '5NPE34AF2FH047906', '2017-07-23', '2022-10-09'),
((SELECT customerID FROM Customers WHERE firstName = 'Hannah' AND lastName = 'Montana'), (SELECT carModelID FROM Cars WHERE carMake = 'Cadillac' AND carModel = 'CT6' AND carYear = '2018'), '1FDZA90W1LVA48400', '2018-12-24', '2020-08-23');

INSERT INTO CarsRecalls(carModelID, recallID)
VALUES
((SELECT carModelID FROM Cars WHERE carMake = 'Buick' AND carModel = 'Regal' AND carYear = '2019'), (SELECT recallID FROM Recalls WHERE recallType = 'Brakes Software' and dateIssued = '2022-07-18')),
((SELECT carModelID FROM Cars WHERE carMake = 'Mazda' AND carModel = 'Mazda3' AND carYear = '2017'), (SELECT recallID FROM Recalls WHERE recallType = 'Windshield Wipers' and dateIssued = '2019-04-03')),
((SELECT carModelID FROM Cars WHERE carMake = 'Cadillac' AND carModel = 'CT6' AND carYear = '2018'), (SELECT recallID FROM Recalls WHERE recallType = 'Seatbelt' and dateIssued = '2019-09-26'));

INSERT INTO VehicleRecallStatus(customerVehicleID, recallID, recallStatus)
VALUES
((SELECT customerVehicleID FROM CustomersVehicles WHERE vinNumber ='1LNHM86S32Y623854'), (SELECT recallID FROM Recalls WHERE recallType = 'Brakes Software' AND dateIssued = '2022-07-18'), 0),
((SELECT customerVehicleID FROM CustomersVehicles WHERE vinNumber = '5NPE34AF2FH047906'), (SELECT recallID FROM Recalls WHERE recallType = 'Windshield Wipers' and dateIssued = '2019-04-03'), 1),
((SELECT customerVehicleID FROM CustomersVehicles WHERE vinNumber = '1FDZA90W1LVA48400'), (SELECT recallID FROM Recalls WHERE recallType = 'Seatbelt' AND dateIssued = '2019-09-26'), 1);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;