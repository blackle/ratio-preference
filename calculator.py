import csv
from statistics import CollectiveStatistics, PairwiseStatistics
from database import PreferenceDatabase, PreferenceDatabaseBuilder, CSVParser, EntityId, EntityIdTuple

# Luce's choice axiom, not the axiom of choice
class ChoiceAxiomDeviationCalculator:
	def __init__(self, col_stats : CollectiveStatistics, pair_stats : PairwiseStatistics) -> None:
		self.__col_stats = col_stats
		self.__pair_stats = pair_stats

	def lookup(self, key : EntityIdTuple) -> float:
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


def main():
	db = None #type: PreferenceDatabase
	with open("data.csv", 'r') as file:

		parser = CSVParser(file)
		builder = PreferenceDatabaseBuilder(parser)
		db = builder.build()

	col_stats = CollectiveStatistics(db)
	pair_stats = PairwiseStatistics(db)
	ca_dev_calc = ChoiceAxiomDeviationCalculator(col_stats, pair_stats)

	for key in pair_stats.keys():
		print(db.name_for_id(key[0]) + " or " + db.name_for_id(key[1]))
		print(ca_dev_calc.lookup(key))

if __name__ == "__main__":
	main()
