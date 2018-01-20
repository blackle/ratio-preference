import csv
from typing import NewType, Tuple, Dict, List
from typedefs import CandyId, CandyTuple, CandyTupleList
from statistics import CollectiveStatistics
from parsers import CSVReader, CSVField, CSVFieldCallback

PairwiseSample = Tuple[int, int]
# CandyId = NewType('CandyId', int)
CandyIdDict = NewType('CandyIdDict', Dict[CandyId, int])
# CandyTuple = NewType('CandyTuple', Tuple[CandyId, CandyId])
# CandyTupleList = NewType('CandyTupleList', List[CandyTuple])
CandyTuplePairwiseSampleDict = NewType('CandyTuplePairwiseSampleDict', Dict[CandyTuple, PairwiseSample])

class CandyDatabase:
	__candies = [
		"Mars Bar",
		"Snickers",
		"Twix",
		"M&Ms",
		"Nerds",
		"Sour Patch Kids",
		"Skittles"
	]

	def candyIds() -> List[CandyId]:
		return [CandyDatabase.idForCandy(x) for x in CandyDatabase.__candies]

	def idForCandy(candy : str) -> CandyId:
		return CandyId(CandyDatabase.__candies.index(candy))

	def candyForId(id : CandyId) -> str:
		return CandyDatabase.__candies[id]

	def tupleForHeader(header : str) -> CandyTuple:
		ret = []
		header = header.replace("?","")
		for candy in header.split(" or "):
			ret.append(CandyDatabase.idForCandy(candy))
		return CandyTuple((ret[0], ret[1]))

	def headerForTuple(tuple : CandyTuple) -> str:
		candy_a = CandyDatabase.candyForId(tuple[0])
		candy_b = CandyDatabase.candyForId(tuple[1])
		return "{0} or {1}?".format(candy_a, candy_b)


# class CollectiveStatistics:
# 	def __init__(self):
# 		self.__dict = CandyIdDict({})
# 		self.__total = 0

# 		for id in CandyDatabase.candyIds():
# 			self.__dict[id] = 0

# 	def processSample(self, winner : CandyId) -> None:
# 		self.__total += 1
# 		self.__dict[winner] += 1

# 	def total(self) -> int:
# 		return self.__total

# 	def lookup(self, id : CandyId) -> int:
# 		return self.__dict[id]


class PairwiseStatistics:
	def __init__(self):
		self.__dict = CandyTuplePairwiseSampleDict({})

	def __normalizeTuple(pair: CandyTuple) -> CandyTuple:
		if pair[0] > pair[1]:
			pair = CandyTuple((pair[1], pair[0]))

		return pair

	def processSample(self, pair: CandyTuple, winner: CandyId) -> None:
		pair = PairwiseStatistics.__normalizeTuple(pair)
		
		if not pair in self.__dict:
			self.__dict[pair] = (0, 0)

		winner_index = pair.index(winner)

		tmp_list = list(self.__dict[pair])
		tmp_list[winner_index] += 1
		self.__dict[pair] = tuple(tmp_list)

	def lookup(self, key : CandyTuple) -> PairwiseSample:
		return self.__dict[key]

	def keys(self) -> CandyTupleList:
		return sorted(list(self.__dict.keys()))


# Luce's choice axiom, not the axiom of choice
class ChoiceAxiomDeviationCalculator:
	def __init__(self, col_stats : CollectiveStatistics, pair_stats : PairwiseStatistics) -> None:
		self.__col_stats = col_stats
		self.__pair_stats = pair_stats

	def lookup(self, key : CandyTuple) -> float:
		pair_a, pair_b = self.__pair_stats.lookup(key)

		col_a = self.__col_stats.lookup(key[0])
		col_b = self.__col_stats.lookup(key[1])

		pair_total = pair_a + pair_b
		col_total = col_a + col_b

		# see formula 1.9 in Rapoport 1989 Ch. 1
		# likelihood of option a being chosen when the subset {a, b} is presented
		pAx = (pair_a / pair_total)
		# likelihood of a or b being chosen when entire selection is presented
		pTA = col_total / self.__col_stats.total()
		# likelihood of option a being chosen when entire selection is presented
		pTx = col_a / self.__col_stats.total()

		return pTx - pAx * pTA


def csv_parser(filename : str) -> Tuple[CollectiveStatistics, PairwiseStatistics]:
	col_stats = CollectiveStatistics()
	pair_stats = PairwiseStatistics()

	with open(filename, 'r') as csvfile:
		data = csv.DictReader(csvfile)

		for row in data:
			for field in data.fieldnames:
				if field == "Choose your most preferred candy":
					row_winner = CandyDatabase.idForCandy(row[field])
					col_stats.processSample(row_winner)

				elif " or " in field:
					header_tuple = CandyDatabase.tupleForHeader(field)
					row_winner = CandyDatabase.idForCandy(row[field])
					pair_stats.processSample(header_tuple, row_winner)

	return (col_stats, pair_stats)


def main():
	col_stats, pair_stats = csv_parser('data.csv')

	trans_dev_calc = ChoiceAxiomDeviationCalculator(col_stats, pair_stats)

	for key in pair_stats.keys():

		print(CandyDatabase.headerForTuple(key))
		print(trans_dev_calc.lookup(key))


if __name__ == "__main__":
	main()
