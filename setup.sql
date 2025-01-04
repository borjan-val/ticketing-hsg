CREATE TABLE tevent (
	teventid uuid DEFAULT gen_random_uuid() PRIMARY KEY CONSTRAINT teventid_not_decoupled CHECK (eventid <> uuid '00000000-0000-0000-0000-000000000000'),
	teventname text NOT NULL,
	ticketstart timestamp NOT NULL,
	ticketend timestamp NOT NULL
);

CREATE TABLE ticket (
	teventid uuid,
	ticketid char(6),
	tname text NOT NULL,
	tsurname text NOT NULL,
	grade smallint NOT NULL,
	paidfor boolean DEFAULT FALSE NOT NULL,
	PRIMARY KEY (teventid, ticketid),
	CONSTRAINT fk_teventid FOREIGN KEY (teventid) REFERENCES tevent (teventid) ON DELETE RESTRICT ON UPDATE RESTRICT
);

CREATE TABLE helper (
	teventid uuid,
	username text,
	spasshashdigest char(64) NOT NULL,
	cansell boolean DEFAULT FALSE NOT NULL,
	cancheck boolean DEFAULT FALSE NOT NULL,
	canaddhelpers boolean DEFAULT FALSE NOT NULL,
	salt char(20) NOT NULL,
	PRIMARY KEY (teventid, ticketid),
	CONSTRAINT teventid_fk_or_decoupled CHECK (teventid = uuid '00000000-0000-0000-0000-000000000000' OR teventid IN (SELECT teventid FROM tevent))
);

CREATE TABLE helpersession (
	tokenid uuid DEFAULT gen_random_uuid() PRIMARY KEY,
	expires timestamp DEFAULT CURRENT_TIMESTAMP + interval 'P0000-00-14T00:00:00' NOT NULL,
	teventid uuid NOT NULL,
	username text NOT NULL,
	CONSTRAINT fk_helper FOREIGN KEY (teventid, username) REFERENCES helper (teventid, username) ON DELETE RESTRICT ON UPDATE RESTRICT
);