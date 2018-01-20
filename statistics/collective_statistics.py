from typing import NewType, Dict
from database import EntityId, EntityName, PreferenceDatabase

class CollectiveStatistics:
	def __init__(self, db : PreferenceDatabase) -> None:
		self.__dict = {} #type: Dict[EntityId, int]
		self.__total = 0 #type: int

		for id in db.key_list():
			self.__dict[id] = 0

		for entity in db.collective_list():
			self.__total += 1
			self.__dict[entity] += 1

	def total(self) -> int:
		return self.__total

	def lookup(self, id : EntityId) -> int:
		return self.__dict[id]


def __collective_statistics_test() -> None:
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
	stats = CollectiveStatistics(db)

	print(stats.total())
	for key in db.key_list():
		print(key, stats.lookup(key))

if __name__ == "__main__":
	__collective_statistics_test()
