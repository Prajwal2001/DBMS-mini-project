import os
from pathlib import Path


def delete_tickets():
    os.chdir(Path.cwd() / "tickets")
    tickets = os.listdir()
    if len(tickets) > 4:
        del(tickets[len(tickets) - 4:])
        tickets.remove("sample.txt")
        for ticket in tickets:
            os.unlink(ticket)
    os.chdir(Path.home() / "Desktop/DBMS-mini-project")
