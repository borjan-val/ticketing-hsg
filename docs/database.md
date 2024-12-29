# Ticketing database layout
```text
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ Event                ┃
┠──────────────────────┨
┃ eventid UUID PRIMARY ┃
┃ name TEXT            ┃
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
┃ name TEXT             ┃
┃ surname TEXT          ┃
┃ birthday DATE         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
```
```text
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Ticketseller          ┃
┠───────────────────────┨
┃ eventid UUID PRIMARY  ┃
┃ username TEXT PRIMARY ┃
┃ saltedpasshash TEXT   ┃
┃ salt TEXT             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
```