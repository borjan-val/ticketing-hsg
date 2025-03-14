from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy import CheckConstraint, text, PrimaryKeyConstraint, ForeignKeyConstraint
import json
import os

# Retrieve database connection details from environment variables
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Construct database connection string
connection_string = f"postgresql+psycopg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

# Initialize the Flask application and connect to the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app)

# For information concerning the database layout as represented by SQLAlchemy
# syntax below, consult the technical documentation of the repository.

# SQLAlchemy can only create all tables at once safely
# and the database has both a table the function depends on (`tevent`)
# and a table that depends on this function (`helper`),
# so we define a dummy function to avoid getting an error
# when creating our tables because of an unsatisfied dependency function.
teventid_fk_or_decoupled_check_dummy = text("""
DO $$
BEGIN
	CREATE FUNCTION teventid_fk_or_decoupled_check(teventid uuid) 
	RETURNS boolean
	LANGUAGE SQL
	IMMUTABLE
	RETURNS NULL ON NULL INPUT
	RETURN TRUE;
EXCEPTION
	WHEN duplicate_function THEN
		NULL;
END $$;
""")

# This is the actual function, we replace the dummy function.
teventid_fk_or_decoupled_check = text("""
CREATE OR REPLACE FUNCTION teventid_fk_or_decoupled_check(teventid uuid) 
RETURNS boolean
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT
RETURN teventid = uuid '00000000-0000-0000-0000-000000000000' OR teventid IN (SELECT teventid FROM tevent);
""")

class Tevent(db.Model):
	teventid = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
	teventname = db.Column(db.Text, nullable=False)
	ticketstart = db.Column(db.DateTime, nullable=False)
	ticketend = db.Column(db.DateTime, nullable=False)
	
	__table_args__ = (
		CheckConstraint('teventid <> uuid \'00000000-0000-0000-0000-000000000000\'', name='teventid_not_decoupled'), # This comma at the end here is absolutely stupid but necessary. `__table_args__` needs to be a tuple, which can't have size 1 in Python. Fuck Python. Also yes, this line is far longer than the 80 columns recommended by K&R. Well, this isn't the Linux kernel, so deal with it.
	)
	
	helpers = db.relationship('Helper', backref='event', viewonly=True)

class Ticket(db.Model):
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

class Helper(db.Model):
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

class Helpersession(db.Model):
	tokenid = db.Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
	expires = db.Column(db.DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP + interval \'P0000-00-14T00:00:00\''))
	teventid = db.Column(SQLAlchemyUUID(as_uuid=True), nullable=False)
	username = db.Column(db.Text, nullable=False)
	
	__table_args__ = (
		ForeignKeyConstraint(['teventid', 'username'], ['helper.teventid', 'helper.username'], name='fk_helper', ondelete='RESTRICT', onupdate='RESTRICT'), # See line 64 for why this comma is here
	)
	
	helper = db.relationship('Helper', backref='helpersessions')

# Setup the database
with app.app_context():
	# Create the dummy function if the real one is not defined.
	# For details on this shitty workaround, check lines 23+.
	with db.engine.connect() as connection:
		connection.execute(teventid_fk_or_decoupled_check_dummy)
		connection.commit()
	
	db.create_all()
	
	with db.engine.connect() as connection:
		connection.execute(teventid_fk_or_decoupled_check)
		connection.commit()

# Load locales
locales = {}
for filename in os.listdir('locales'):
	if filename.endswith('.json'):
		language = filename[:-5] # Remove the .json file extension
		try:
			with open(f'locales/{filename}', 'r', encoding='utf-8') as f:
				locales[language] = json.load(f)
		except (json.JSONDecodeError, OSError) as e:
			print(f"Error loading {filename}: {e}")

# Compact little function to get the localized string for a key string (e.g. "noevent" -> "No event selected")
# Use only in request contexts!
def _(key):
	# Language of the returned string is defined by browser headers, defaults to English
	lang = request.accept_languages.best_match(locales.keys()) or 'en'
	# Get the requested translation from the dictionary of the determined language,
	# or return the key if no translation was found 
	return locales.get(lang, {}).get(key, key)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html', _=_), 404

@app.route("/test/account/")
def account_test():
	return render_template(
		'account.html',
		_=_,
		forevent="Example event A",
		username="testuser",
		cansell=True,
		cancheck=True,
		canaddhelpers=True
	)

@app.route("/test/change-password/")
def change_password_test():
	return render_template(
		'change-password.html',
		_=_,
		username="testuser"
	)

@app.route("/test/create-event/")
def create_event_test():
	return render_template(
		'create-event.html',
		_=_
	)

@app.route("/test/create-helper/")
def create_helper_test():
	return render_template(
		'create-helper-account.html',
		_=_,
		eventname="Example event A"
	)

@app.route("/test/event-management/")
def event_management_test():
	return render_template(
		'event-management.html',
		_=_
	)

@app.route("/test/event-picker/")
def event_picker_test():
	return render_template(
		'event-picker.html',
		_=_,
		currently_selling=[
			("Example event A", "0000-01-01", "9999-12-31"),
			("Example event B", "0000-01-01", "9999-12-31"),
			("Example event C", "0000-01-01", "9999-12-31")
		],
		not_currently_selling=[
			("Example event D", "1969-12-31", "1970-01-01"),
			("Example event E", "1969-12-31", "1970-01-01"),
			("Example event F", "1969-12-31", "1970-01-01")
		]
	)

@app.route("/test/login/")
def login_test():
	return render_template(
		'login.html',
		_=_,
		event_selected=False
	)

@app.route("/test/select-action/")
def select_action_test():
	return render_template(
		'select-action.html',
		_=_
	)

@app.route("/test/ticket-create/")
def ticket_create_test():
	return render_template(
		'ticket-create.html',
		_=_,
		eventname="Example event A"
	)

@app.route("/test/ticket-info/")
def ticket_info_test():
	return render_template(
		'ticket-info.html',
		_=_,
		eventname="Example event A",
		ticketcode="ABC123",
		ticket_valid=False,
		cancheck=True,
		cansell=True,
		name="John",
		surname="Doe"
	)