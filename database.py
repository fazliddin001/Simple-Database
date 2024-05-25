import os


class Database:
    def __init__(self, path: str):
        self.tables = []
        self.path = path
        self.connection = False

    def create_database(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def create(self, table):
        table.create_table(self)
        self.tables.append(table)
