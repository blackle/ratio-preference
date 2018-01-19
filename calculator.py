import csv
import numpy as np
from typing import NewType, Tuple, Dict, List

PairwiseSample = Tuple[int, int]
CandyId = NewType('CandyId', int)
CandyTuple = NewType('CandyTuple', Tuple[CandyId, CandyId])
CandyTupleList = NewType('CandyTupleList', List[CandyTuple])
CandyTupleDict = NewType('CandyTupleDict', Dict[CandyTuple, PairwiseSample])

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


class PairwiseStatistics:
	def __init__(self):
		self.__dict = CandyTupleDict({})

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


def main():
	stats = PairwiseStatistics()

	with open('data.csv', 'r') as csvfile:
		data = csv.DictReader(csvfile)

		for row in data:
			for field in data.fieldnames:
				if field == "Choose your most preferred candy" or field == "Timestamp":
					continue

				header_tuple = CandyDatabase.tupleForHeader(field)
				row_winner = CandyDatabase.idForCandy(row[field])
				stats.processSample(header_tuple, row_winner)

	for key in stats.keys():
		candy_a, candy_b = key
		count_a, count_b = stats.lookup(key)
		print(CandyDatabase.headerForTuple(key), stats.lookup(key))

if __name__ == "__main__":
	main()
