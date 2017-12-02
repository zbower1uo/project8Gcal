## Project 8/10 free times

-Note, the project is in a "working" alpha condition. Many of the features I wished to implement would not be feasable in the ammmount of time given, and a lot of the logic could be reworked to make it run faster.

Project 8 last commit is on  Nov 23, 2017 
Also proj 10 starts on 12/1/2017 all commits prior are for proj8


## Some notes regarding the project
I had a lot of fun with my implementation of the free/busy times.

I chose to quantize time in 15 min intervals and chose to represent them as a bitstring and perform bitwise operations on them to find free times (1 is busy 0 is free). Although this was fun (at least more so than thinking of them as time chunks, I did run into difficulty with python and int values). I am not too familiar with python, so there may be a better way to achieve what I did, but at first I wanted to get it working.

I tried to document all of my functions with parameters as well as the inteded outcome of said function, so some places are very heavily commented while. I tried to do a good mix of readability and comments

The database is working and multiple users are able to input a "meetingID" to be part of the same meeting group ( I was unable to implement a hash of sorts, so now it is user inputed data, I know not the right way)


The only additional libraries needed for this are:
	numpy
	as this made it much easier to work with arrays of ints, but that is included in the requirements.txt



git clone

make install

cd meetings

python3 flask_main.py




## Zachary Bower
## zbower@uoregon.edu