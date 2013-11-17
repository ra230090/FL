FL
==

fault localization


put fautloc.py,mystart.c,problemIO,ucodes,ufiles,delc.sh,delf.sh at same folder

problemIO contains the correct input output ,sorted by problemID

put usercode(ie. test.c/test.cpp) in folder ucodes

type cmd: "python3.3 fautloc.py User_code problemID" to run
ie. python3.3 fautloc.py test.c 10400

check the fault.txt in ufiles sorted by name

if ufiles or ucodes are getting mess
run delc.sh,delf.sh
