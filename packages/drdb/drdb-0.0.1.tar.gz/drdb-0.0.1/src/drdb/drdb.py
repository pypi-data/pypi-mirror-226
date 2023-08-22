class DrDB:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, columns):
        self.tables[table_name] = {'columns': columns, 'data': []}

    def insert_data(self, table_name, values):
        if table_name in self.tables:
            if len(values) == len(self.tables[table_name]['columns']):
                self.tables[table_name]['data'].append(dict(zip(self.tables[table_name]['columns'], values)))
                print("Data inserted successfully.")
            else:
                print("Incorrect number of values.")
        else:
            print("Table does not exist.")

    def fetch_data(self, table_name, condition=None):
        if table_name in self.tables:
            if condition:
                data = []
                for row in self.tables[table_name]['data']:
                    if all(row[col] == val for col, val in condition.items()):
                        data.append(row)
                return data
            else:
                return self.tables[table_name]['data']
        else:
            print("Table does not exist.")

    def join_tables(self, table1_name, table2_name, column1, column2):
        if table1_name in self.tables and table2_name in self.tables:
            table1_data = self.tables[table1_name]['data']
            table2_data = self.tables[table2_name]['data']
            
            joined_data = []
            for row1 in table1_data:
                for row2 in table2_data:
                    if row1[column1] == row2[column2]:
                        joined_data.append({**row1, **row2})
            return joined_data
        else:
            print("Table does not exist.")

