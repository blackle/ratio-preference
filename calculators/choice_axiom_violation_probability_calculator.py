from statistics import CollectiveStatistics, PairwiseStatistics
from database import EntityId, EntityIdTuple
from typing import Tuple
import numpy as np
from math import sqrt
from scipy.stats.mstats import normaltest
from scipy.special import erf

#see ChoiceAxiomDeviationCalculator first
class ChoiceAxiomViolationProbabilityCalculator:
	__SAMPLE_NUMBER = 100000

	def __init__(self, col_stats : CollectiveStatistics, pair_stats : PairwiseStatistics) -> None:
		self.__col_stats = col_stats
		self.__pair_stats = pair_stats

	# def gauss_from_sample(self, sample: Tuple[float, float]) -> Tuple[float, float]:
	# 	#these are the parameters for a beta distribution, which models the probability of the preference between each item in the pair. beta distributions are hard to work with, so we will use a gaussian distribution of the same mean and variance to approximate it.
	# 	alpha = sample[0] + 1.0
	# 	beta = sample[1] + 1.0

	# 	mean = alpha / (alpha + beta)
	# 	std = alpha * beta / (pow(alpha + beta, 2) * (alpha + beta + 1))

	# 	return (mean, std)

	def generate_trinary_simulation(self, sample: Tuple[float, float, float]) -> np.ndarray:
		a1 = sample[0] + 1.0
		a2 = sample[1] + 1.0
		a3 = sample[2] + 1.0

		return np.random.dirichlet((a1, a2, a3), ChoiceAxiomViolationProbabilityCalculator.__SAMPLE_NUMBER)

	def generate_binary_simulation(self, sample: Tuple[float, float]) -> np.ndarray:
		alpha = sample[0] + 1.0
		beta = sample[1] + 1.0

		return np.random.beta(alpha, beta, ChoiceAxiomViolationProbabilityCalculator.__SAMPLE_NUMBER)

	def calc_bias(self, pair : EntityIdTuple) -> float:
		#models statistics on pAx 
		pAx_sample = self.__pair_stats.lookup(pair)
		pAx_samples = self.generate_binary_simulation(pAx_sample)

		col_a = self.__col_stats.lookup(key[0])
		col_b = self.__col_stats.lookup(key[1])
		col_total = col_a + col_b

		trinary_samples = self.generate_trinary_simulation((col_a, col_b, self.__col_stats.total() - col_total))

		#models statistics on pTa 
		pTA_samples = trinary_samples[:,0] + trinary_samples[:,1]

		#models statistics on pTx
		pTx_samples = trinary_samples[:,0]

		distro_samples = pTx_samples - pTA_samples * pAx_samples
		distro_mean = np.mean(distro_samples)
		distro_std = np.std(distro_samples)

		distance_to_mean = (distro_mean - 0)/distro_std

		return distance_to_mean

if __name__ == "__main__":
	from database import PreferenceDatabase, PreferenceDatabaseBuilder, CSVParser

	db = None #type: PreferenceDatabase
	with open("data.csv", 'r') as file:

		parser = CSVParser(file)
		builder = PreferenceDatabaseBuilder(parser)
		db = builder.build()

	# for item in db.collective_list():
	# 	print(item + 1)

	col_stats = CollectiveStatistics(db)
	pair_stats = PairwiseStatistics(db)
	ca_vprob_calc = ChoiceAxiomViolationProbabilityCalculator(col_stats, pair_stats)

	total = 1.0

	for key in pair_stats.keys():
		print(db.name_for_id(key[0]) + " or " + db.name_for_id(key[1]) + "?")
		calc = ca_vprob_calc.calc_bias(key)
		total *= calc
		print(calc)

	print("total", 1-total)
