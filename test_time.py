import TimeBlock:
import arrow

test = arrow.utcnow()
arrowobj = arrow.get('2013-05-11T21:23:58.970460+00:00')



def match(input , expected):
	if input == expected:
		return True
	else 
		return false


def test_obj_default():
	timeblock.TimeBlock()
	return match(test , arrow.utcnow())

def test_obj_functions():
	arrowobjdate = arrowobj.date()
	tb = timeblock.TimeBlock(arrowobj)
	return match(tb._startdate ,arrowobjdate)

