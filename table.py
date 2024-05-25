import pickle
import os
from dataclasses import dataclass


@dataclass
class C:
    cols: list

    def set_cols(self):
        for index, col in enumerate(self.cols):
            col.set_index(index)
            setattr(self, col.title, col)

    def __contains__(self, other: str):
        for col in self.cols:
            if col.title == other:
                return True
        return False

    def __getitem__(self, item: str | int):
        if isinstance(item, int):
            for col in self.cols:
                if col.index == item:
                    return col

        elif isinstance(item, str):
            for col in self.cols:
                if col.title == item:
                    return col

    def with_default(self, keys):
        return tuple(col for col in self.cols if col.title not in keys)


class Select:
    def __init__(self, col_titles, table, data):
        self.table = table
        self.rows = tuple(pickle.loads(row) for row in data.split(self.table.gap_with) if row != b"")
        self.indexes = tuple(col.index for col in self.table.c.cols if col.title in col_titles)

    def where(self, **cols):
        custom_data = []

        for row in self.rows:

            for key, val in cols.items():
                if row[self.table.c[key].index] != val:
                    break
            else:
                custom_data.append(tuple(row[index] for index in self.indexes))

        return custom_data


class Update:
    def __init__(self, table, cols, data):
        self.table = table
        self.rows = data.split(self.table.gap_with)
        self.index_val = dict()
        for key, val in cols.items():
            self.index_val[self.table.c[key].index] = val

    def where(self, **cols):

        with open(self.table.path, "wb") as file:

            for row in self.rows:
                if row == b"":
                    continue

                row_list = pickle.loads(row)

                for key, val in cols.items():
                    if row_list[self.table.c[key].index] != val:
                        file.write(self.table.gap_with)
                        file.write(row)
                        break
                else:
                    file.write(self.table.gap_with)

                    for index, val in self.index_val.items():
                        row_list[index] = val

                    file.write(pickle.dumps(row_list))


class Delete:
    def __init__(self, table, data):
        self.table = table
        self.rows = data.split(self.table.gap_with)

    def where(self, **cols):

        with open(self.table.path, "wb") as file:
            for row in self.rows:
                if row == b"":
                    continue

                row_list = pickle.loads(row)
                for key, val in cols.items():
                    if row_list[self.table.c[key].index] != val:
                        file.write(self.table.gap_with)
                        file.write(row)
                        break
                else:
                    pass


class Table:
    def __init__(self, table_name: str, *cols):
        self.table_name = table_name
        self.gap_with = b"&"
        self.database = ...
        self.path: str = ...
        self.echo: bool = ...
        self.c = C(list(cols))
        self.c.set_cols()

    def create_table(self, database):
        self.database = database
        self.path = f"{self.database.path}/{self.table_name}.txt"

        if not os.path.exists(self.path):
            with open(self.path, "a"):
                pass

    def insert(self, **column):
        data = []
        for key, val in column.items():
            if key not in self.c:
                raise OSError(f"Column {key} does not exists")

            col = self.c[key]
            data.insert(col.index, col.transform(value=val))

        take_default = self.c.with_default(column.keys())
        for col in take_default:
            data.insert(col.index, col.transform(value=None))

        write_data = pickle.dumps(data)

        with open(self.path, "ab") as file:
            file.write(self.gap_with)
            file.write(write_data)

    def update(self, **columns):
        with open(self.path, "rb") as file:
            data = file.read()
            return Update(self, data=data, cols=columns)

    def delete(self):
        with open(self.path, "rb") as file:
            data = file.read()
            return Delete(self, data=data)

    def select(self, *cols: str):
        if cols == ():
            cols = (col.title for col in self.c.cols)

        with open(self.path, "rb") as file:
            all_rows = file.read()
            return Select(col_titles=cols, table=self, data=all_rows)
