#!/bin/sh

#Testas patikrinimui ar programa skaito iš failo
rm -rf test/result.log
for i in {1..24}
do
	python3 encoder.py teststuff/tekstas.txt $i 
	python3 decoder.py teststuff/tekstas.txt.huf 
	ORIGINAL=`cat teststuff/tekstas.txt`
	RESTORED=`cat teststuff/tekstas_restored.txt`
	if [ "$ORIGINAL" = "$RESTORED" ]; then
  		echo "TEST SUCCEDED. K= $i" >> test/result.log
  	else echo "-!!- FAILED  K= $i -!!-" >> test/result.log
	fi
	mv teststuff/tekstas.txt.huf test/$itekstas.txt.huf
	mv teststuff/tekstas_restored.txt test/$itekstas_restored.txt
	echo "FILES MOVED TO TEST FOLDER..." >> test/result.log
done