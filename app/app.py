from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy import CheckConstraint, ForeignKey, func, text, PrimaryKeyConstraint, ForeignKeyConstraint
import uuid as python_uuid
import secrets
import os

# Helper function to generate cryptographically secure UUIDs in Python
def python_secure_uuid4():
	return python_uuid.UUID(bytes=secrets.token_bytes(16))

# Retrieve database connection details from environment variables
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Construct the connection string for psycopg3
connection_string = f"postgresql+psycopg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Initialize the Flask application and configure the database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app)

# Custom constraint for Helper UUIDs
teventid_fk_or_decoupled_check = text("""
CREATE OR REPLACE FUNCTION teventid_fk_or_decoupled_check(teventid uuid) 
RETURNS boolean
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT
RETURN teventid = uuid '00000000-0000-0000-0000-000000000000' OR teventid IN (SELECT teventid FROM tevent);
""")

# Represents the `tevent` table in the database
class Tevent(db.Model):
	__tablename__ = 'tevent'
	
	teventid = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=python_secure_uuid4, server_default=text('gen_random_uuid()'))
	teventname = db.Column(db.Text, nullable=False)
	ticketstart = db.Column(db.DateTime, nullable=False)
	ticketend = db.Column(db.DateTime, nullable=False)
	
	__table_args__ = (
		CheckConstraint('teventid <> uuid \'00000000-0000-0000-0000-000000000000\'', name='teventid_not_decoupled'),
	)

# Represents the `ticket` table in the database
class Ticket(db.Model):
	__tablename__ = 'ticket'
	
	teventid = db.Column(SQLAlchemyUUID(as_uuid=True))
	ticketid = db.Column(db.CHAR(6))
	tname = db.Column(db.Text, nullable=False)
	tsurname = db.Column(db.Text, nullable=False)
	grade = db.Column(db.SmallInteger, nullable=False)
	paidfor = db.Column(db.Boolean, nullable=False, default=False)
	
	__table_args__ = (
		PrimaryKeyConstraint('teventid', 'ticketid'),
		ForeignKeyConstraint(['teventid'], ['tevent.teventid'], name='fk_teventid', ondelete='RESTRICT', onupdate='RESTRICT')
	)
	
	tevent = db.relationship('Tevent', backref='tickets')

# Represents the `helper` table in the database
class Helper(db.Model):
	__tablename__ = 'helper'
	
	teventid = db.Column(SQLAlchemyUUID(as_uuid=True))
	username = db.Column(db.Text)
	spasshashdigest = db.Column(db.CHAR(64), nullable=False)
	cansell = db.Column(db.Boolean, nullable=False, default=False)
	cancheck = db.Column(db.Boolean, nullable=False, default=False)
	canaddhelpers = db.Column(db.Boolean, nullable=False, default=False)
	salt = db.Column(db.CHAR(20), nullable=False)
	
	__table_args__ = (
		PrimaryKeyConstraint('teventid', 'username'),
		CheckConstraint('teventid_fk_or_decoupled_check(teventid)', name='teventid_fk_or_decoupled')
	)

# Represents the `helpersession` table in the database
class Helpersession(db.Model):
	__tablename__ = 'helpersession'
	
	tokenid = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=python_secure_uuid4, server_default=text('gen_random_uuid()'))
	expires = db.Column(db.DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP + interval \'P0000-00-14T00:00:00\''))
	teventid = db.Column(SQLAlchemyUUID(as_uuid=True), nullable=False)
	username = db.Column(db.Text, nullable=False)
	
	__table_args__ = (
		ForeignKeyConstraint(['teventid', 'username'], ['helper.teventid', 'helper.username'], name='fk_helper', ondelete='RESTRICT', onupdate='RESTRICT'),
	)

# Ensure the application context is available for database operations
with app.app_context():
	# Step 1: Create the `tevent` table
	Tevent.__table__.create(db.engine)
	
	# Step 2: Create the custom PostgreSQL function
	with db.engine.connect() as connection:
		connection.execute(teventid_fk_or_decoupled_check)
		connection.commit()
	
	# Step 3: Create the remaining tables (`ticket`, `helper`, and `helpersession`)
	Ticket.__table__.create(db.engine)
	Helper.__table__.create(db.engine)
	Helpersession.__table__.create(db.engine)