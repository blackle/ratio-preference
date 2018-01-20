from typing import NewType, Callable, IO, Any
from csv import DictReader

CSVField = NewType("CSVField", str);
CSVRow = NewType("CSVRow", str);
CSVFieldCallback = Callable[[CSVField], None]
CSVRowCallback = Callable[[CSVField, CSVRow], None]

class CSVReader:
	def __init__(self, file: IO[Any]) -> None:
		self.__reader = DictReader(file)

	def process_fields(self, callback: CSVFieldCallback) -> None:
		for field_str in self.__reader.fieldnames:
			field = CSVField(field_str)
			callback(field)

	def process_rows(self, callback: CSVRowCallback) -> None:
		for row_dict in self.__reader:
			for field_str in self.__reader.fieldnames:
				row = CSVRow(row_dict[field_str])
				field = CSVField(field_str)
				callback(field, row)


def reader_test_field_callback(field: CSVField) -> None:
	if field != "Timestamp" and field != "Choose your most preferred candy":
		print(field)

def reader_test_row_callback(field: CSVField, row: CSVRow) -> None:
	if field != "Timestamp" and field != "Choose your most preferred candy":
		print(field, row)

if __name__ == "__main__":
	with open("data.csv", 'r') as file:

		reader = CSVReader(file)
		reader.process_fields(reader_test_field_callback)
		reader.process_rows(reader_test_row_callback)
