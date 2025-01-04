# Preparing the database

There are a few steps a DBA will need to perform in order to set up an existing PostgreSQL database to be used for a ticketing-hsg deployment.

1. Create the ticketing-hsg database user and choose a secure password.
```postgresql
CREATE ROLE ticketing-hsg LOGIN PASSWORD 'your password here'
```
2. Create the ticketing-hsg database and set the ticketing-hsg database user as the database owner.
```postgresql
CREATE DATABASE ticketing-hsg OWNER ticketing-hsg
```
3. Connect to the ticketing-hsg database as the new ticketing-hsg role you just created and run the `setup.sql` file in the root of this repository. This will create all the database tables needed for operation.