# Queries used internally
## Recurring
### Helper sessions
```postgresql
SELECT helper.username, helper.teventid, helper.cansell, helper.cancheck, helper.canaddhelpers FROM helpersession INNER JOIN helper ON helpersession.username = helper.username AND helpersession.teventid = helper.teventid WHERE helpersession.tokenid = uuid '...' LIMIT 1
```
```postgresql
DELETE FROM helpersession WHERE tokenid = uuid '...' AND CURRENT_TIMESTAMP >= expires LIMIT 1
```
```postgresql
SELECT eventname FROM tevent WHERE teventid = uuid '...' LIMIT 1
```
## Event selector
```postgresql
SELECT teventid, eventname, ticketstart, ticketend FROM tevent WHERE ticketstart <= CURRENT_TIMESTAMP AND CURRENT_TIMESTAMP < ticketend
```
```postgresql
SELECT teventid, eventname, ticketstart, ticketend FROM tevent WHERE ticketstart > CURRENT_TIMESTAMP OR CURRENT_TIMESTAMP >= ticketend
```
## Ticket info
```postgresql
SELECT paidfor FROM ticket WHERE teventid = uuid '...' AND ticketid = '...' LIMIT 1
```
```postgresql
SELECT tname, tsurname, grade, paidfor FROM ticket WHERE teventid = uuid '...' AND ticketid = '...' LIMIT 1
```
```postgresql
UPDATE ticket SET paidfor = TRUE WHERE teventid = uuid '...' AND ticketid = '...' LIMIT 1
```
## Login
```postgresql
SELECT salt, saltedpasshash FROM helper WHERE teventid = uuid '...' AND username = '...' LIMIT 1
```
```postgresql
INSERT INTO helpersession (expires, teventid, username) VALUES (CURRENT_TIMESTAMP + INTERVAL 'P0000-00-14T00:00:00', uuid '...', '...') RETURNING tokenid
```
## My account
```postgresql
DELETE FROM helpersession WHERE teventid = uuid '...' AND username = '...'
```
## Change password
```postgresql
SELECT salt, saltedpasshash FROM helper WHERE teventid = uuid '...' AND username = '...' LIMIT 1
```
```postgresql
UPDATE helper SET salt = '...', saltedpasshash = '...' WHERE teventid = uuid '...' AND username = '...' LIMIT 1
```
## Create Helper account
```postgresql
INSERT INTO helper (teventid, username, saltedpasshash, cansell, cancheck, canaddhelpers, salt) VALUES (uuid '...', '...', '...', ?, ?, ?, '...')
```
## Create event
```postgresql
INSERT INTO tevent (eventname, ticketstart, ticketend) VALUES ('...', timestamp '...', timestamp '...')
```