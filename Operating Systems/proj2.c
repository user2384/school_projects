/**
 * @file proj2.c
 * @author Viktoria Haleckova,FIT VUT
 * @brief program sa zaobera synchronizaciou procesov, riesi sa the Senate bus problem
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <signal.h>

//Konstanty - mena semaforov
#define SEMAPHORE1_NAME "/1046"
#define SEMAPHORE2_NAME "/1047"
#define SEMAPHORE3_NAME "/1048"
#define SEMAPHORE4_NAME "/1049"

//Konstanty pouzivane pri vytvarani semaforov
#define LOCKED 0
#define UNLOCKED 1

//Semafory
sem_t *mutex = NULL;
sem_t *bus = NULL;
sem_t *boarded = NULL;
sem_t *sem_end = NULL;

//Zdielane premenne
int *operation_number = NULL;
int *waiting_riders = NULL;
int *arg_riders = NULL;

//ID zdielanych premennych
int shm_op;
int shm_wait;
int shm_rid;

//vstupne argumenty programu
int riders;
int capacity;
int art;
int abt;

//pre pouzivanie funkcie strtol
char *ptr;

//subor, do ktoreho budem apisovat data
FILE *logFile;

int main(int argc, char *argv[])
{
    // otvaranie suboru, do ktoreho zapisujem
    logFile=fopen("proj2.out","w");
    if(logFile == NULL) //kontrola
    {
	fprintf(stderr,"CHYBA! Nepodarilo sa vytvorit subor 'proj2.out'.\n");
	exit(1);
    }
    setbuf(logFile, NULL); //prevencia bufferingu
    setbuf(stderr, NULL);
    if(argc != 5) 
    {
    	fprintf(stderr,"CHYBA! Program nebol spusteny so spravnym poctom argumentov.\n");
    	exit(1);
    }
    riders=strtol(argv[1],&ptr,10); //ukladanie zadanych argumentov do premennych
    if(riders <= 0 || *ptr != '\0')
    {
	fprintf(stderr,"CHYBA! Parameter [R] nieje v pozadovanom tvare.\n");
	exit(1);
    }
    capacity=strtol(argv[2],&ptr,10);
    if(capacity <= 0 || *ptr != '\0')
    {
	fprintf(stderr,"CHYBA! Parameter [C] nieje v pozadovanom tvare.\n");
	exit(1);
    }
    art=strtol(argv[3],&ptr,10);
    if(art < 0 || art > 1000 || *ptr != '\0')
    {
	fprintf(stderr,"CHYBA! Parameter [ART] nieje v pozadovanom tvare.\n");
	exit(1);
    }
    abt=strtol(argv[4],&ptr,10);
    if(abt < 0 || abt > 1000 || *ptr != '\0')
    {
	fprintf(stderr,"CHYBA! Parameter [ABT] nieje v pozadovanom tvare.\n");
	exit(1);
    }
    
    // vytvorenie semaforov
    if ((mutex = sem_open(SEMAPHORE1_NAME, O_CREAT | O_EXCL, 0666, UNLOCKED)) == SEM_FAILED)
    {
        fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit semafor.\n");
	fclose(logFile);
	exit(1);
    }

    if ((bus = sem_open(SEMAPHORE2_NAME, O_CREAT | O_EXCL, 0666, LOCKED)) == SEM_FAILED)
    {
        fprintf(stderr,"CHYBA! Nepodarilo sa vytvorit semafor.\n");
	sem_close(mutex);
	sem_unlink(SEMAPHORE1_NAME);
	fclose(logFile);
	exit(1);
    }
    
    if ((boarded = sem_open(SEMAPHORE3_NAME, O_CREAT | O_EXCL, 0666, LOCKED)) == SEM_FAILED)
    {
	fprintf(stderr,"CHYBA! Nepodarilo sa vytvorit semafor.\n");
	sem_close(mutex);
	sem_close(bus);
	sem_unlink(SEMAPHORE1_NAME);
	sem_unlink(SEMAPHORE2_NAME);
	fclose(logFile);
	exit(1);
    }

    if ((sem_end = sem_open(SEMAPHORE4_NAME, O_CREAT | O_EXCL , 0666, LOCKED)) == SEM_FAILED)
    {
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit semafor.\n");
	sem_close(mutex);
	sem_close(bus);
	sem_close(boarded);
	sem_unlink(SEMAPHORE1_NAME);
	sem_unlink(SEMAPHORE2_NAME);
	sem_unlink(SEMAPHORE3_NAME);
	fclose(logFile);
	exit(1);
    }
    if((shm_op = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {	
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit ID pre zdielanu premennu.\n");
	sem_close(mutex);
	sem_close(bus);
	sem_close(boarded);
	sem_close(sem_end);
	sem_unlink(SEMAPHORE1_NAME);
	sem_unlink(SEMAPHORE2_NAME);
	sem_unlink(SEMAPHORE3_NAME);
	sem_unlink(SEMAPHORE4_NAME);
	fclose(logFile);
	exit(1);
    }
    if((shm_wait = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit ID pre zdielanu premennu.\n");
	shmctl(shm_op, IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    if((shm_rid = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit ID pre zdielanu premennu.\n");
        shmctl(shm_op, IPC_RMID, NULL);
	shmctl(shm_wait, IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    if((operation_number = shmat(shm_op,NULL,0)) == NULL)
    {
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit zdielanu premennu.\n");
        shmctl(shm_op, IPC_RMID, NULL);
        shmctl(shm_wait, IPC_RMID, NULL);
	shmctl(shm_rid, IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    if((waiting_riders = shmat(shm_wait,NULL, 0)) == NULL)
    {
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit ID pre zdielanu premennu.\n");
        shmctl(shm_op, IPC_RMID, NULL);
        shmctl(shm_wait, IPC_RMID, NULL);
	shmctl(shm_rid, IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    if((arg_riders = shmat(shm_rid,NULL, 0)) == NULL)
    {
	fprintf(stderr, "CHYBA! Nepodarilo sa vytvorit ID pre zdielanu premennu.\n");
        shmctl(shm_op, IPC_RMID, NULL);
        shmctl(shm_wait, IPC_RMID, NULL);
        shmctl(shm_rid,	IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    (*operation_number) = 1; //zdielana premenna sluziaca ako cislo prevadzanej cinnosti
    (*waiting_riders) = 0; //zdielana premenna sluziaca ako pocet riders, ktori cakaju na zastavke
    (*arg_riders) = riders; //zdielana premenna, zadany pocet riders od uzivatela
    pid_t processGen; //deklaracia procesu generator, ktory budem nasledne pouzivat na fork()
    pid_t processBus = fork();
    
    if (processBus < 0) 
    {
	fprintf(stderr, "CHYBA! Fork sa nepodaril.\n");
        shmctl(shm_op, IPC_RMID, NULL);
        shmctl(shm_wait, IPC_RMID, NULL);
        shmctl(shm_rid, IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    else if (processBus == 0) // ak je to dieta - proces bus
    {
            sem_wait(mutex); //uzamknem semafor na vypis
            fprintf(logFile,"%d:\tBUS:\tstart\n", *operation_number);
 	    sem_post(mutex); //naspat odomknem
	    int not_yet = 1; //privatna premenna podla ktorej urcujem, ci este prebehne jazda - ci su na zastavke este nejaki riders
	    while(not_yet)
	    {
	    	sem_wait(mutex);
	    	(*operation_number)++;
	    	fprintf(logFile,"%d:\tBUS:\tarrival\n",*operation_number);
            	int n;
		int tmp = *waiting_riders; //tzv. get minimum funkcia
	    	if(tmp < capacity)
			n = tmp;
		else
			n = capacity;
	   	if(n > 0) //pokial su na zastavke nejaki riders - inak odchadza
		{
            		(*operation_number)++;
	    		fprintf(logFile,"%d:\tBUS:\tstart boarding:\t%d\n",*operation_number,*waiting_riders);
	    		for(int i = 0; i < n; i++) //pre kazdeho ridera (v ramci kapacity) otvaram semafor bus, moze nastupovat
	    		{
	    			sem_post(bus);
	 			sem_wait(boarded); //cakam dokial niesu vsetci nastupeni
	    		}
			if((tmp-capacity) > 0) //implementacia funkcie tzv. get maximum
				(*waiting_riders) = (tmp-capacity);
			else
				(*waiting_riders) = 0;
			(*operation_number)++; //koniec nastupovania
			fprintf(logFile,"%d:\tBUS:\tend boarding:\t%d\n",*operation_number,*waiting_riders);
		}
		(*operation_number)++; //odchod autobusu
	    	fprintf(logFile,"%d:\tBUS:\tdepart\n",*operation_number);
            	sem_post(mutex);
		if(abt != 0) //simulacia jazdy - uspanie na abt
			usleep((rand() % (abt+1)) * 1000);
		else
			usleep(0);
	    	sem_wait(mutex);
	    	(*operation_number)++; //autobus prichadza spat na zastavku
	    	fprintf(logFile, "%d:\tBUS:\tend\n",*operation_number);
	    	sem_post(mutex);
		for(int i = 1; i <= n; i++) //otvara n-semaforov pre finish riders
			sem_post(sem_end);
		sem_wait(mutex); 
		if((*arg_riders) > 0) //ak este niekto je na zastavke
			not_yet = 1;
		else
			not_yet = 0;
		sem_post(mutex);
	}
	sem_wait(mutex);
	(*operation_number)++; 
	fprintf(logFile,"%d:\tBUS:\tfinish\n",*operation_number);
	sem_post(mutex); //zatvaram vsetky semafory
	sem_close(mutex);
	sem_close(bus);
     	sem_close(boarded);
	sem_close(sem_end);
        exit(0);
    }else
    {
    	pid_t processRider; //deklaracia processRider, ktory budem nasledne pouzivat na fork()
    	processGen = fork(); //generator riders
    	if (processGen == 0) //child
    	{
		for(int i = 1; i <= riders; i++) //for cyklus, pre vsetkych riders zadanych argumentom
	    	{
	    		if(art != 0) //uspanie na dobu art
				usleep((rand() % (art+1)) * 1000);
			else
				usleep(0);
	        	processRider = fork();
			if(processRider == 0)
			{
            			sem_wait(mutex);
	    			(*operation_number)++; //vytvorenie ridera
	    			fprintf(logFile,"%d:\tRID %d:\tstart\n",*operation_number,i);
	    			sem_post(mutex);
    	    			sem_wait(mutex);
	    			(*operation_number)++;
				(*waiting_riders)++; //rider vstupuje na zastavku
	    			fprintf(logFile,"%d:\tRID %d:\tenter: %d\n",*operation_number,i,*waiting_riders);
	    			sem_post(mutex);
            			sem_wait(bus); //ak mu autobus odomkne semafor na nastupenie
				(*operation_number)++; //moze nastupit
				fprintf(logFile,"%d:\tRID %d:\tboarding\n",*operation_number,i);
				(*arg_riders)--; //nastupil, odcitam od zdielanej premennej
				sem_post(boarded); 
				sem_wait(sem_end);
				sem_wait(mutex);
				(*operation_number)++; //po navrate autobusu z jazdy nasleduje tzv finish ridera
				fprintf(logFile,"%d:\tRID %d:\tfinish\n",*operation_number,i);
				sem_post(mutex);
				exit(0);
			}else if(processRider < 0)
			{
				fprintf(stderr, "CHYBA! Nepodaril sa fork procesu.\n");
        			shmctl(shm_op, IPC_RMID, NULL);
        			shmctl(shm_wait, IPC_RMID, NULL);
        			shmctl(shm_rid, IPC_RMID, NULL);
        			sem_close(mutex);
        			sem_close(bus);
        			sem_close(boarded);
        			sem_close(sem_end);
        			sem_unlink(SEMAPHORE1_NAME);
        			sem_unlink(SEMAPHORE2_NAME);
        			sem_unlink(SEMAPHORE3_NAME);
        			sem_unlink(SEMAPHORE4_NAME);
        			fclose(logFile);
        			exit(1);
			}	
	    	}
	    if(processRider > 0) //ak je to rodic
	    {
		while (wait(NULL) > 0);
	    }
	    sem_close(mutex); //zatvorim vsetky semafory
	    sem_close(bus);
	    sem_close(boarded);
	    sem_close(sem_end);
	    exit(0);
    }
    else if(processGen < 0)
    {
	fprintf(stderr, "CHYBA! Nepodaril sa fork procesu.\n");
        shmctl(shm_op, IPC_RMID, NULL);
        shmctl(shm_wait, IPC_RMID, NULL);
        shmctl(shm_rid, IPC_RMID, NULL);
        sem_close(mutex);
        sem_close(bus);
        sem_close(boarded);
        sem_close(sem_end);
        sem_unlink(SEMAPHORE1_NAME);
        sem_unlink(SEMAPHORE2_NAME);
        sem_unlink(SEMAPHORE3_NAME);
        sem_unlink(SEMAPHORE4_NAME);
        fclose(logFile);
        exit(1);
    }
    }
    if(processBus > 0 || processGen > 0)
    {
	while (wait(NULL)>0);
    }
    shmctl(shm_op, IPC_RMID,NULL);
    shmctl(shm_wait, IPC_RMID, NULL);
    shmctl(shm_rid, IPC_RMID, NULL);
    // zatvorim vsetky semafory
    sem_close(mutex);
    sem_close(bus);
    sem_close(boarded);
    sem_close(sem_end);
    // odstranim semafory
    sem_unlink(SEMAPHORE1_NAME);
    sem_unlink(SEMAPHORE2_NAME);
    sem_unlink(SEMAPHORE3_NAME);
    sem_unlink(SEMAPHORE4_NAME);
    fclose(logFile); //zavriem subor
    return 0;
}
