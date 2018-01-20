from typing import NewType, Tuple, List

CandyId = NewType('CandyId', int)
CandyIdList = NewType('CandyIdList', List[CandyId])
CandyTuple = NewType('CandyTuple', Tuple[CandyId, CandyId])
CandyTupleList = NewType('CandyTupleList', List[CandyTuple])
