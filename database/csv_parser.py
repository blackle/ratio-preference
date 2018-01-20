from typing import NewType, Callable, IO, Any
from csv import DictReader
from database.generic_parser import EntityName, EntityNameList, EntityNameTuple, EntityNameListTupleDict, GenericParser

class CSVParser(GenericParser):
	def __init__(self, file: IO[Any]) -> None:
		self.__file = file
		self.__key_list = [] #type: EntityNameList
		self.__collective_list = [] #type: EntityNameList
		self.__pair_dict = {} #type: EntityNameListTupleDict

		self.__process_key_list()
		self.__process_collective_list()
		self.__process_pair_dict()

	def __split(self, field_name : str) -> EntityNameList:
		split = field_name.replace("?","").split(" or ")
		assert len(split) == 2
		return [EntityName(x) for x in split]

	def __new_reader(self) -> DictReader:
		self.__file.seek(0)
		return DictReader(self.__file)

	def __process_key_list(self) -> None:
		reader = self.__new_reader()
		for field_str in reader.fieldnames:
			try:
				split = self.__split(field_str)
				self.__key_list += split
			except AssertionError:
				continue
		self.__key_list = list(set(self.__key_list))

	def __process_collective_list(self) -> None:
		reader = self.__new_reader()
		collective_key = "Choose your most preferred candy"
		for row in reader:
			entity = EntityName(row[collective_key])
			assert entity in self.__key_list
			self.__collective_list.append(entity)

	def __process_pair_dict(self) -> None:
		reader = self.__new_reader()
		for row in reader:
			for field_str in reader.fieldnames:
				try:
					split = self.__split(field_str)
					key = (split[0], split[1])

					if not key in self.__pair_dict:
						self.__pair_dict[key] = []

					entity = EntityName(row[field_str])
					self.__pair_dict[key].append(entity)
				except AssertionError:
					continue

	def key_list(self) -> EntityNameList:
		return self.__key_list;

	def collective_list(self) -> EntityNameList:
		return self.__collective_list;

	def pair_dict(self) -> EntityNameListTupleDict:
		return self.__pair_dict;


if __name__ == "__main__":
	with open("data.csv", 'r') as file:

		parser = CSVParser(file)

		print(parser.key_list())
		print(parser.collective_list())
		print(parser.pair_dict())
