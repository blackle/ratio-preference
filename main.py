from calculators import ChoiceAxiomDeviationCalculator
from statistics import CollectiveStatistics, PairwiseStatistics
from database import PreferenceDatabase, PreferenceDatabaseBuilder, CSVParser, EntityId, EntityIdTuple

def main() -> None:
	db = None #type: PreferenceDatabase
	with open("data.csv", 'r') as file:

		parser = CSVParser(file)
		builder = PreferenceDatabaseBuilder(parser)
		db = builder.build()

	col_stats = CollectiveStatistics(db)
	pair_stats = PairwiseStatistics(db)
	ca_dev_calc = ChoiceAxiomDeviationCalculator(col_stats, pair_stats)

	for key in pair_stats.keys():
		print(db.name_for_id(key[0]) + " or " + db.name_for_id(key[1]) + "?")
		print(ca_dev_calc.lookup(key))

if __name__ == "__main__":
	main()
