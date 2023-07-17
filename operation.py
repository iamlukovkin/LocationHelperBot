import database

db = database.DB('Database/User.txt')

with open('Database/OlDDB.txt', 'r') as file:
    for line in file:
        line = line.strip()
        parts = line.split(': ')
        print(parts[0], parts[1:])
        db.AddString(parts[0], parts[1:])