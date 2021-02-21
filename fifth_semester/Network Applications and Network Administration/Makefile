CC=gcc

CFLAGS=-I. `net-snmp-config --cflags`

DLFLAGS=-fPIC -shared

isaProjectMIB.so: isaProjectMIB.c Makefile
	$(CC) $(CFLAGS) $(DLFLAGS) -c -o isaProjectMIB.o isaProjectMIB.c
	$(CC) $(CFLAGS) $(DLFLAGS) -o isaProjectMIB.so isaProjectMIB.o
