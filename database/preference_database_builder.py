from database.preference_database import PreferenceDatabase
from database.generic_parser import GenericParser

class PreferenceDatabaseBuilder:
	def __init__(self, parser: GenericParser) -> None:
		self.__key_list = parser.key_list()
		self.__collective_list = parser.collective_list()
		self.__pair_dict = parser.pair_dict()

	def build(self) -> PreferenceDatabase:
		return PreferenceDatabase(self.__key_list, self.__collective_list, self.__pair_dict)


if __name__ == "__main__":
	from database.csv_parser import CSVParser

	db = None #type: PreferenceDatabase
	with open("data.csv", 'r') as file:

		parser = CSVParser(file)
		builder = PreferenceDatabaseBuilder(parser)
		db = builder.build()

	print([db.name_for_id(x) for x in db.key_list()])
	print([db.name_for_id(x) for x in db.collective_list()])
