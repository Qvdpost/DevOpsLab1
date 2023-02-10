from swagger_server.db.database import Database, Collection

db = Database()
students = Collection(db, 'students')
grades = Collection(db, 'grades')