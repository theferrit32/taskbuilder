
default: clean arraylist

clean:
	rm -f arraylist

arraylist: arraylist.c
	gcc -Wall -std=c11 -o arraylist arraylist.c
