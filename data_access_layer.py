import json
import logging
import sys
# Date handling 
import arrow   
from dateutil import tz  # For interpreting local times
# Mongo database
from pymongo import MongoClient
import config

#######GLOBAL VARS####
#
#
#####################
CONFIG = config.configuration()
MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
CONFIG.DB_USER,
CONFIG.DB_USER_PW,
CONFIG.DB_HOST, 
CONFIG.DB_PORT, 
CONFIG.DB)

class DataAccessLayer:

	def __init__(self):
		self.collection = self.init_client()

	def init_client(self):
		"""
		Function to initialize the database client 

		"""
		try:
			dbclient = MongoClient(MONGO_CLIENT_URL)
			db = getattr(dbclient , CONFIG.DB)
			self.collection = db.freetimest
		except Exception as err:
			print("Error initializing database client")

	def insert_custom_time(self,date, index , duration,bittime, databaseid):
		"""s
		date: Date block begins 
		index: start time
		duration: how many 15min intervals are after the start time

		Second function/alternative function to insert values into database, I was having issues overloading
		the function, so for now created a second function

		"""
		try:
			dbclient = MongoClient(MONGO_CLIENT_URL)
			db = getattr(dbclient , CONFIG.DB)
			self.collection = db.freetimest
		except Exception as err:
			print("Error initializing database client")

		freeTime = {
					"type": "timeblock",
					"date": date,
					"index": index,
					"duration": duration,
					"bittime": bittime,
					"databaseid": databaseid				
					}
		self.collection.insert(freeTime)


	def insert_busy_times(self , timeblock, databaseid):
		"""
		timeblock: A timeblock obj, including start/end times 
		and bittime

		blocktype: A description of the timeblocks inserted into the database
		ex: free times/busy times/ custom input

		Function to create free times and add to database, information
		will be pulled from the obj and then added to database
		"""
		#break apart timeblock object and insert needed parts into the database
		
		try:
			dbclient = MongoClient(MONGO_CLIENT_URL)
			db = getattr(dbclient , CONFIG.DB)
			self.collection = db.busytimes
		except Exception as err:
			print("Error initializing database client")

		start = str(timeblock.start)
		end = str(timeblock.end)
		date = str(timeblock.date)
		bittime = timeblock.bittime.tolist() 
		dbid = databaseid

		busyTime = {
					"type": "busy",
					"date": date, 
					"start":start,
					"end":end,
					"bittime":bittime,
					"databaseid": dbid				
					}
		self.collection.insert(busyTime)


	def delete_timeblock(self, timeblock, databaseid):
		"""
		timeblock: timeblock obj will get values from and delete from database
		databaseid: The uniqe id of the record in database
		Function to delete a record from 
		
		"""
		date = timeblock.date
		start = timeblock.start
		end = timeblock.end
		bittime = timeblock.bittime
		dbid = databaseid

		self.collection.remove(
			{
				"type": "timeblock",
				"date": date, 
				"start":start,
				"end":end,
				"bittime":bittime,
				"databaseid": dbid	
			})


	#add userid / email
	def retrieve_database_items(self,databaseid ):
		"""
		Retrives items from database and sends as a list

		date: Date to query
		start: Start time query
		end: End tim/e Query
		databaseid: The unique id of database

		"""
		try:
			dbclient = MongoClient(MONGO_CLIENT_URL)
			db = getattr(dbclient , CONFIG.DB)
			self.collection = db.busytimes
		except Exception as err:
			print("Error initializing database client")

		records = [ ]
		print(databaseid)
		for record in self.collection.find({ 
			"databaseid": str(databaseid)
			} ):
			del record['_id']
			records.append(record)
		return records 
