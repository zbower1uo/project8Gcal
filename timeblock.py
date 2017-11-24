import arrow

class TimeBlock:
	#TODO add type for busy/free
	def __init__(self, _start="00:00", _end="00:00", _summary=" ", ):
		self._start = arrow.get(_start)
		self._end = arrow.get(_end)
		
		self._startdate = self.get_start_date()
		self._enddate = self.get_end_date()
		self._starttime = self._start.time()
		self._endtime = self._end.time()
		self._summary = _summary

	def __eq__(self,timeblock):
		#see if two timeblocks are equal 
		return self._summary == timeblock._summary and self._start == timeblock._starttime and self._end == timeblock._end

	def __str__(self):
		#tostring
		return "Start: {0} End: {1} Summary: {2}".format(self._start,self._end,self._summary)

	#getters/setters
	def get_start_date(self):
		sdate = arrow.get(self._start)
		return sdate.date()

	def get_end_date(self):
		edate = arrow.get(self._end)
		return edate.date()


	def get_summary(self):
		return self._summary

	def get_start_time(self):
		return self._start

	def get_end_time(self):
		return self._end

	def set_start_time(self,st):
		_start = st
	
	def set_end_time(self,et):
		_end = et

	def set_description(self,summary):
		_summary = summary
	
	#printing function
	def to_string(self):
		return "Start: {0} End: {1} Summary: {2}".format(self._start,self._end,self._summary)

	def does_overlap(self,timeblock):
		# checks if two blocks are essentially the same/ checks their overlap
		if self._end < timeblock._start or other._end < self._start:
			return False
		return True

	def get_overlap(self,timeblock):

		mergedSummary = self._summary + " | " + timeblock._summary
		#self ends after
		if self._end > timeblock._end:
			overlap = TimeBlock(timeblock._start,timeblock._end,mergedSummary)
		else:
			overlap = TimeBlock(other.start_time,self.end_time,description)
		if timeblock._start < self._start:
			if self._end > timeblock._end:
				overlap = TimeBlock(self._start, timeblock._end, mergedSummary)
			else:
				overlap = TimeBlock(self._start, self._end, mergedSummary)

		return overlap
	
	def merge_blocks(self,timeblock):
		#merges two time blocks
		mergedSummary = self._summary + " | " + timeblock._summary
		merged = TimeBlock(self._start,timeblock._end, mergedSummary)
		return merged


	def split_block(self ,timeblock):
		timeblock1 = TimeBlock(self._start, timeblock._start, self._summary)
		timeblock2 = TimeBlock(timeblock._end, self._end, self._summary)
		return timeblock1,timeblock2
###TODO overload + op, index and comparison ops