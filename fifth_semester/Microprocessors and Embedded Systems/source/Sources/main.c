/*
 *Author: Viktoria Haleckova, xhalec00@stud.fit.vutbr.cz
 *File: main.c
 *Project: LED watch
 *Course: Microprocessors and Embedded Systems
 */


#include "MKL05Z4.h"
#include <time.h>
#include <stdio.h>
#include <string.h>


/* Activation of particular LED display (DS1 - DS4) */
#define D1 0x0700
#define D2 0x0B00
#define D3 0x0D00
#define D4 0x0E00


/* Encoding of digits as active segments on specific LED display (DS1 - DS4) */
#define N0 0x0707
#define N1 0x0006
#define N2 0x0B03
#define N3 0x0907
#define N4 0x0C06
#define N5 0x0D05
#define N6 0x0F05
#define N7 0x0007
#define N8 0x0F07
#define N9 0x0D07


/* Bit-level masks that help to enable/disable DP segment on LED display */
#define MASK_DOT_ON 0x0008
#define MASK_DOT_OFF 0xFFF7


#define PB4_ISF_MASK 0x10


int show_dot = 1;
int n_2 = 0; 
int n_1 = 0;
int n_3 = 0;
int n_4 = 0;
int set_hours = 0;
int set_mins = 0;
int all_set = 0;
int init = 0;
int c = 0;


/* Just an ordinary delay loop */
void delay(long long bound) {

  long long i;
  for(i=0;i<bound;i++);
}


/* Let's turn off individual segments on the whole display */
void off() {

  PTB->PDOR = GPIO_PDOR_PDO(0x0000);
  PTA->PDOR = GPIO_PDOR_PDO(D1);
  PTA->PDOR = GPIO_PDOR_PDO(D2);
  PTA->PDOR = GPIO_PDOR_PDO(D3);
  PTA->PDOR = GPIO_PDOR_PDO(D4);

}


/* Basic initialization of GPIO features on PORTA and PORTB */
void ports_init (void)
{

  SIM->COPC = SIM_COPC_COPT(0x00);							   // Just disable the usage of WatchDog feature
  SIM->SCGC5 = (SIM_SCGC5_PORTA_MASK | SIM_SCGC5_PORTB_MASK);  // Turn on clocks for PORTA and PORTB
  SIM->SCGC6 |= SIM_SCGC6_RTC_MASK;

  /* Set corresponding PORTA pins for GPIO functionality */
  PORTA->PCR[8] = ( 0|PORT_PCR_MUX(0x01) );  // display DS4
  PORTA->PCR[9] = ( 0|PORT_PCR_MUX(0x01) );  // display DS3
  PORTA->PCR[10] = ( 0|PORT_PCR_MUX(0x01) ); // display DS2
  PORTA->PCR[11] = ( 0|PORT_PCR_MUX(0x01) ); // display DS1

  /* Set corresponding PORTA port pins as outputs */
  PTA->PDDR = GPIO_PDDR_PDD( 0x0F00 );  // "1" configures given pin as an output

  NVIC_DisableIRQ(31);  // Disable the eventual generation of the interrupt caused by the control button

  /* Set corresponding PORTB pins for GPIO functionality */
  PORTB->PCR[0] = ( 0|PORT_PCR_MUX(0x01) );   // seg A
  PORTB->PCR[1] = ( 0|PORT_PCR_MUX(0x01) );   // seg B
  PORTB->PCR[2] = ( 0|PORT_PCR_MUX(0x01) );   // seg C
  PORTB->PCR[3] = ( 0|PORT_PCR_MUX(0x01) );   // seg DP
  PORTB->PCR[8] = ( 0|PORT_PCR_MUX(0x01) );   // seg D
  PORTB->PCR[9] = ( 0|PORT_PCR_MUX(0x01) );   // seg E
  PORTB->PCR[10] = ( 0|PORT_PCR_MUX(0x01) );  // seg F
  PORTB->PCR[11] = ( 0|PORT_PCR_MUX(0x01) );  // seg G

  /* Set corresponding PORTB port pins as outputs */
  PTB->PDDR = GPIO_PDDR_PDD( 0x0F0F ); // "1" configures given pin as an input
  PORTB->PCR[4] = ( 0 | PORT_PCR_ISF(1) | PORT_PCR_IRQC(0x0A) | PORT_PCR_MUX(0x01) |
					    PORT_PCR_PE(1) | PORT_PCR_PS(1)); // display SW1

  /* Let's clear any previously pending interrupt on PORTB and allow its subsequent generation */
 NVIC_ClearPendingIRQ(31);
 NVIC_EnableIRQ(31);
}


/* Service routine invoked upon the press of a control button */
void PORTB_IRQHandler( void )
{
	delay(100);
	int held = 0;
	if (PORTB->ISFR & GPIO_PDIR_PDI(PB4_ISF_MASK)) {
	  if (!(PTB->PDIR & GPIO_PDIR_PDI(PB4_ISF_MASK)))
		  while (PORTB->ISFR & GPIO_PDIR_PDI(PB4_ISF_MASK) && !(PTB->PDIR & GPIO_PDIR_PDI(PB4_ISF_MASK))) {
			  off();
			  delay(100);
			  held++;
		  }
	  if (held < 3000)
		  	  if (init == 0)
		  		  ;
		  	  else if (set_hours == 1)
	  			  if (n_1 == 2 && n_2 < 3)
	  				  n_2++;
	  			  else if (n_1 == 2) {
	  				  n_2 = 0;
	  				  n_1 = 0;
	  			  }
	  			  else if (n_2 < 9)
	  				  n_2++;
	  			  else {
	  				  n_2 = 0;
	  				  if (n_1 < 2)
	  					  n_1++;
	  				  else
	  					  n_1 = 0;
	  			  }
	  		  else if (set_mins == 1)
	  			  if (n_3 == 5 && n_4 < 9)
	  				  n_4++;
	  			  else if (n_3 == 5) {
	  				  n_3 = 0;
	  				  n_4 = 0;
	  			  }
	  			  else if (n_4 < 9)
	  				  n_4++;
	  			  else {
	  				  n_4 = 0;
	  				  if (n_3 < 5)
	  					  n_3++;
	  				  else
	  			  		  n_3 = 0;
	  			  }
	  	  if (held > 3000) {
	  		  if (init == 0) {
	  			  set_hours = 1;
	  			  init = 1;
	  		  }
	  		  else if (set_hours == 1) {
	  			  set_mins = 1;
	  			  set_hours = 0;
	  		  }
	  		  else if (set_mins == 1) {
	  			  all_set = 1;
	  			  set_mins = 0;
	  		  }
	  		  else if (all_set == 1) {
	  			  set_hours = 1;
	  			  all_set = 0;
	  		  }
	  	  }
	  PORTB->PCR[4] |= PORT_PCR_ISF(0x01);  // Confirmation of interrupt after button press
	}
}

void set_time() {
	int seconds = RTC->TSR;
	int hours = seconds / 3600;
	seconds -= 3600* hours;
	int minutes = seconds / 60;
	seconds -= 60*minutes;
	if (hours < 10)
		n_1 = 0;
	else
		n_1 = hours / 10;
	n_2 = hours % 10;
	if (minutes < 10)
		n_3 = 0;
	else
		n_3 = minutes / 10;
	n_4 = minutes % 10;
}

unsigned concatenate(int x, int y) {
	char s1[20];
	char s2[20];
	sprintf(s1,"%d",x);
	sprintf(s2,"%d",y);
	strcat(s1,s2);
	int d = strtol(s1,NULL,10);
	return d;
}

int convert() {
	int no1 = concatenate(n_1,n_2);
	int no2 = concatenate(n_3,n_4);
	int h = no1 * 3600;
	int s = no2 * 60;
	return h + s;
}

void rtc_init() {
	RTC->CR |= RTC_CR_SWR_MASK; // reset all RTC registers
	RTC->CR &= ~RTC_CR_SWR_MASK; // SWR = 0
	RTC->TCR = 0x0000; // reset CIR and TCR
	RTC->CR |= RTC_CR_OSCE_MASK; // 32.768 kHz oscillator
	delay(0x600000);
	RTC->SR &= ~RTC_SR_TCE_MASK; // turn RTC off
	RTC->TSR = 0x00000000; // minimum value 
	RTC->TAR = 0xFFFFFFFF; // maximum value
	RTC->IER = RTC_IER_TAIE_MASK;
	RTC->SR |= RTC_SR_TCE_MASK; // turn RTC on
}

/* Single digit shown on a particular section of the display  */
void show_number(int number, uint32_t display, int showdot) {

  uint32_t n;

  switch (number) {
    case 0:
      n = N0; break;
    case 1:
      n = N1; break;
    case 2:
      n = N2; break;
    case 3:
      n = N3; break;
    case 4:
      n = N4; break;
    case 5:
      n = N5; break;
    case 6:
      n = N6; break;
    case 7:
      n = N7; break;
    case 8:
      n = N8; break;
    case 9:
      n = N9; break;
    default:
      n = N0;
  }

  if (showdot == 0)
	  n |= MASK_DOT_ON;
  else
	  n &= MASK_DOT_OFF;

  PTA->PDOR = GPIO_PDOR_PDO(display);
  PTB->PDOR = GPIO_PDOR_PDO(n);

  delay(10); //10
}

int main(void)
{
	ports_init();
	rtc_init();
	delay(500);


	for (;;) {
		if (init == 0) {
			show_number(n_1,D1,1);
			show_number(n_2,D2,0);
			show_number(n_3,D3,1);
			show_number(n_4,D4,0);
		}
		if (set_hours == 1) {
			show_number(n_1,D1,1);
			show_number(n_2,D2,0);
		}
		if (set_mins == 1) {
			show_number(n_3,D3,1);
			show_number(n_4,D4,0);
		}
		if (all_set == 1) {
			c = convert();
			RTC->SR &= ~RTC_SR_TCE_MASK; // turn RTC off
			RTC->TSR = c; // set
			RTC->SR |= RTC_SR_TCE_MASK; // turn RTC on
			for (;;) {
				set_time();
				show_number(n_1,D1,1);
				show_number(n_2,D2,0);
				show_number(n_3,D3,1);
				show_number(n_4,D4,0);
				if (set_hours == 1)
					break;
			}
		}

	}

	return 0;
}
////////////////////////////////////////////////////////////////////////////////
// EOF
////////////////////////////////////////////////////////////////////////////////

