import TimeBlock:
import arrow

test = arrow.utcnow()
arrowobj = arrow.get('2013-05-11T21:23:58.970460+00:00')

def create_timeblock(arrowo):
	t1 = arrowo.shift(days=+1)
	tb = timeblock.TimeBlock(arrowo, t1 , "Test")
	return tb

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

def test_obj_eq():
	tb1 = create_timeblock(arrowobj)
	tb2 = create_timeblock(arrowobj)
	return match(tb1 , tb2)

