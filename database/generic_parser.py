from typing import List, NewType, Tuple, Dict

EntityName = NewType("EntityName", str)
EntityNameList = List[EntityName]
EntityNameTuple = Tuple[EntityName, EntityName]
EntityNameListTupleDict = Dict[EntityNameTuple, EntityNameList]

class GenericParser:
	def __init__(self) -> None:
		pass

	def key_list(self) -> EntityNameList:
		raise NotImplementedError('Unimplemented!')

	def collective_list(self) -> EntityNameList:
		raise NotImplementedError('Unimplemented!')

	def pair_dict(self) -> EntityNameListTupleDict:
		raise NotImplementedError('Unimplemented!')
