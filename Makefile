# NAME: Jun Kai Ong, Arti Patankar
# EMAIL: junkai@g.ucla.edu, artipatankar@ucla.edu
# ID: 604606304, 604594513
#

.SILENT:

default:
	cat lab3b.py > lab3b
	chmod u+x lab3b 
	echo "python compiled with no errors" > /dev/null
clean:
	rm *tar.gz lab3b
dist: default
	tar -czf lab3b-604606304.tar.gz Makefile lab3b.py README
