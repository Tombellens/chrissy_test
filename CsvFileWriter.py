class CsvFileWriter:
    def __init__(self, csvFileName, fieldsArray):
        try:
            self.file = open("data/" + csvFileName + ".csv", "r")
        except FileNotFoundError:
            self.file = open("data/" + csvFileName + ".csv", "a+")
            self.file.write(self.column_array_into_csv_string(fieldsArray))
            return
        self.file = open("data/" + csvFileName + ".csv", "a+")


    def column_array_into_csv_string(self, column_array):
        csv_string = ""
        for column in range(len(column_array)):
            if column == 0:
                csv_string = str(column_array[column])
                continue
            if column == (len(column_array)-1):
                csv_string = csv_string + "," + str(column_array[column]) + "\n"
                continue
            csv_string = csv_string + "," + str(column_array[column])

        return csv_string

    def add_row(self, column_array):
        self.file.write(self.column_array_into_csv_string(column_array))