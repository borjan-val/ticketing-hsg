# Ticketing database layout
```text
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ Event                ┃
┠──────────────────────┨
┃ eventid UUID PRIMARY ┃
┃ eventname TEXT       ┃
┃ ticketstart DATE     ┃
┃ ticketend DATE       ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛
```
```text
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Ticket                ┃
┠───────────────────────┨
┃ eventid UUID PRIMARY  ┃
┃ ticketid TEXT PRIMARY ┃
┃ tname TEXT            ┃
┃ tsurname TEXT         ┃
┃ grade NUMBER          ┃
┃ paidfor BOOLEAN       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
```
```text
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Helper                 ┃
┠────────────────────────┨
┃ eventid UUID PRIMARY   ┃
┃ username TEXT PRIMARY  ┃
┃ saltedpasshash TEXT    ┃
┃ cansell BOOLEAN        ┃
┃ cancheck BOOLEAN       ┃
┃ canaddhelpers BOOLEAN  ┃
┃ salt TEXT              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┛
```
```text
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ Session              ┃
┠──────────────────────┨
┃ tokenid UUID PRIMARY ┃
┃ expires DATE         ┃
┃ eventid UUID         ┃
┃ username TEXT        ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛
```