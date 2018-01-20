from typing import NewType, Dict, Tuple
from database import EntityId, EntityIdTuple, EntityIdTupleList, EntityIdListTupleDict, PreferenceDatabase

PairwiseStat = NewType("PairwiseStat", Tuple[int, int])
PairwiseStatsDict = Dict[EntityIdTuple, PairwiseStat]

class PairwiseStatistics:
	def __init__(self, db : PreferenceDatabase) -> None:
		self.__dict = {} #type: PairwiseStatsDict
		db_pairwise_dict = db.pairwise_dict()
		for key in db_pairwise_dict:
			values = db_pairwise_dict[key]
			for value in values:
				self.__process_sample(key, value)

	def __process_sample(self, pair: EntityIdTuple, winner: EntityId) -> None:		
		if not pair in self.__dict:
			self.__dict[pair] = PairwiseStat((0, 0))

		winner_index = pair.index(winner)

		tmp_list = list(self.__dict[pair])
		tmp_list[winner_index] += 1
		self.__dict[pair] = PairwiseStat((tmp_list[0], tmp_list[1]))

	def lookup(self, key : EntityIdTuple) -> PairwiseStat:
		return self.__dict[key]

	def keys(self) -> EntityIdTupleList:
		return sorted(list(self.__dict.keys()))


def __pairwise_statistics_test() -> None:
	from database import EntityName

	e0 = EntityName("Dr. Peepo")
	e1 = EntityName("Pepis")
	e2 = EntityName("RC Squampy")

	key_list = [e0, e1, e2]
	collective_list = [e0, e0, e1, e1, e1, e2]
	pair_dict = {
		(e0, e1): [e0, e0, e0, e0, e0, e1],
		(e0, e2): [e0, e0, e0, e0, e2, e2],
		(e2, e1): [e1, e1, e2, e2, e2, e2]
	}

	db = PreferenceDatabase(key_list, collective_list, pair_dict)
	stats = PairwiseStatistics(db)

	for key in stats.keys():
		print(key, stats.lookup(key))

if __name__ == "__main__":
	__pairwise_statistics_test()
