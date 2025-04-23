**FinAPI**

**API Setup and Running Instructions**

**Requirements**

 - Makefile command
 - Docker Engine

**Steps to Run API**

 -    Create a network:
    `make create-network`

Build the development environment:
`make build-dev`

Run the development server:
`make run-dev`

Shutdown the development server:
`make kill-dev`

Run test cases:
`make run-tests`


The server will start and by default run at localhost:8000.

**Question 2.**
Race Conditions in Database Operations
A **race condition** is a situation where read/write operations on a database row occur simultaneously, potentially leading to data corruption or incorrect updates.

Scenario:
In this API, if User A sends funds to User B while User B is simultaneously sending funds to User C, a race condition could result in lost funds by:

 1. The system fetches User B's information
 2. User A's deposit to User B occurs
 3. The system uses the old balance of User B (before receiving funds from User A)
 4. The system saves this outdated balance to the database

This results in "lost" money in the system  

**Solution**

A recommended solution is to implement row-level locking on the affected database rows whenever they are retrieved for modification purposes. This prevents simultaneous modifications and ensures data integrity during financial transactions.
