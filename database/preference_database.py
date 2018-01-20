from typing import List, NewType, Tuple, Dict
from database.generic_parser import EntityName, EntityNameList, EntityNameTuple, EntityNameListTupleDict

EntityId = NewType('EntityId', int)
EntityIdList = List[EntityId]
EntityIdTuple = Tuple[EntityId, EntityId]
EntityIdTupleList = List[EntityIdTuple]
EntityIdListTupleDict = Dict[EntityIdTuple, EntityIdList]

class PreferenceDatabase:

	def __init__(self, key_list : EntityNameList, collective_list: EntityNameList, pair_dict : EntityNameListTupleDict) -> None:
		self.__list = key_list

		self.__collective = [self.id_for_name(x) for x in collective_list]

		self.__pairwise = {} #type: EntityIdListTupleDict
		for key in pair_dict:
			key_id = (self.id_for_name(key[0]), self.id_for_name(key[1]))
			key_id = self.__normalize_tuple(key_id)
			self.__pairwise[key_id] = []

			for entity in pair_dict[key]:
				entity_id = self.id_for_name(entity)
				assert entity_id == key_id[0] or entity_id == key_id[1]
				self.__pairwise[key_id].append(entity_id)

	def __normalize_tuple(self, pair: EntityIdTuple) -> EntityIdTuple:
		if pair[0] > pair[1]:
			pair = (pair[1], pair[0])
		return pair

	def name_for_id(self, id : EntityId) -> EntityName:
		return self.__list[id]

	def id_for_name(self, name : EntityName) -> EntityId:
		return EntityId(self.__list.index(name))

	def key_list(self) -> EntityIdList:
		return [self.id_for_name(x) for x in self.__list]

	def collective_list(self) -> EntityIdList:
		return self.__collective

	def pairwise_dict(self) -> EntityIdListTupleDict:
		return self.__pairwise


def __preference_database_test() -> None:
	e0 = EntityName("Dr. Peepo")
	e1 = EntityName("Pepis")
	e2 = EntityName("RC Squampy")

	key_list = [e0, e1, e2]
	collective_list = [e0, e0, e1, e1, e1, e2]
	pair_dict = {
		(e0, e1): [e0, e1, e1, e0, e0, e1],
		(e0, e2): [e0, e2, e0, e2, e2, e0],
		(e2, e1): [e2, e1, e2, e2, e1, e1]
	}

	db = PreferenceDatabase(key_list, collective_list, pair_dict)

	print(db.key_list())
	print(db.collective_list())
	print(db.pairwise_dict())

if __name__ == "__main__":
	__preference_database_test()
