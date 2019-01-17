#!/bin/sh

#Testas patikrinimui ar programa skaito iš failo
rm -rf test/result.log
for i in {1..24}
do
	python3 encoder.py teststuff/LAND.bmp $i 
	python3 decoder.py teststuff/LAND.bmp.huf 
	ORIGINAL=`cat teststuff/antras.txt`
	RESTORED=`cat teststuff/LAND_restored.bmp`
	if [ "$ORIGINAL" = "$RESTORED" ]; then
  		echo "TEST SUCCEDED. K= $i" >> test/result.log
  	else echo "-!!- FAILED  K= $i -!!-" >> test/result.log
	fi
	mv teststuff/LAND.bmp.huf test/$i_LAND.bmp.huf
	mv teststuff/LAND_restored.bmp test/$i_LAND_restored.bmp
	echo "FILES MOVED TO TEST FOLDER..." >> test/result.log
done