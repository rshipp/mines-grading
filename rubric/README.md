General Usage
-----
// TODO document arguments needed for scripts

1. Download zipped collection of students files.
2. Run `unzip.py` to extract user directories and name them accordingly
3. Create a `Rubric.txt` with the general format:

	```
	Item1            3
	Item2          2.3
	Item3            4
	==================
	Total 
	```

	A couple things to notice about the file format
	1. Items are separted from numbers with at least one space (TODO not sure if
	   tabs are okay?)
	2. Items are separated from total line with = equals
	3. Total line should be left blank as it will be populated later

4. Run `generateRubric.py`.  This will create rubrics for each of the students
   in the form of `username.txt`

TODO
--------
lots of other cool things

