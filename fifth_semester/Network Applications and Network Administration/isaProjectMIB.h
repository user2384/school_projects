/*
 * File: isaProjectMIB.h
 * Project: SNMP Agent Extension
 * Course: ISA (Network Applications and Network Administration)
 * Author: Viktoria Haleckova
 */

#ifndef ISAPROJECTMIB_H
#define ISAPROJECTMIB_H

/* function declarations */
void init_isaProjectMIB(void);
Netsnmp_Node_Handler handle_loginObject;
Netsnmp_Node_Handler handle_timeObject;
Netsnmp_Node_Handler handle_integerObject;
Netsnmp_Node_Handler handle_infoObject;

#endif /* ISAPROJECTMIB_H */
