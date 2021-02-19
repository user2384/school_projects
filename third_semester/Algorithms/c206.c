
/* c206.c **********************************************************}
 {* Téma: Dvousměrně vázaný lineární seznam
 **
 **                   Návrh a referenční implementace: Bohuslav Křena, říjen 2001
 **                            Přepracované do jazyka C: Martin Tuček, říjen 2004
 **                                            Úpravy: Kamil Jeřábek, září 2018
 **
 ** Implementujte abstraktní datový typ dvousměrně vázaný lineární seznam.
 ** Užitečným obsahem prvku seznamu je hodnota typu int.
 ** Seznam bude jako datová abstrakce reprezentován proměnnou
 ** typu tDLList (DL znamená Double-Linked a slouží pro odlišení
 ** jmen konstant, typů a funkcí od jmen u jednosměrně vázaného lineárního
 ** seznamu). Definici konstant a typů naleznete v hlavičkovém souboru c206.h.
 **
 ** Vaším úkolem je implementovat následující operace, které spolu
 ** s výše uvedenou datovou částí abstrakce tvoří abstraktní datový typ
 ** obousměrně vázaný lineární seznam:
 **
 **      DLInitList ...... inicializace seznamu před prvním použitím,
 **      DLDisposeList ... zrušení všech prvků seznamu,
 **      DLInsertFirst ... vložení prvku na začátek seznamu,
 **      DLInsertLast .... vložení prvku na konec seznamu,
 **      DLFirst ......... nastavení aktivity na první prvek,
 **      DLLast .......... nastavení aktivity na poslední prvek,
 **      DLCopyFirst ..... vrací hodnotu prvního prvku,
 **      DLCopyLast ...... vrací hodnotu posledního prvku,
 **      DLDeleteFirst ... zruší první prvek seznamu,
 **      DLDeleteLast .... zruší poslední prvek seznamu,
 **      DLPostDelete .... ruší prvek za aktivním prvkem,
 **      DLPreDelete ..... ruší prvek před aktivním prvkem,
 **      DLPostInsert .... vloží nový prvek za aktivní prvek seznamu,
 **      DLPreInsert ..... vloží nový prvek před aktivní prvek seznamu,
 **      DLCopy .......... vrací hodnotu aktivního prvku,
 **      DLActualize ..... přepíše obsah aktivního prvku novou hodnotou,
 **      DLSucc .......... posune aktivitu na další prvek seznamu,
 **      DLPred .......... posune aktivitu na předchozí prvek seznamu,
 **      DLActive ........ zjišťuje aktivitu seznamu.
 **
 ** Při implementaci jednotlivých funkcí nevolejte žádnou z funkcí
 ** implementovaných v rámci tohoto příkladu, není-li u funkce
 ** explicitně uvedeno něco jiného.
 **
 ** Nemusíte ošetřovat situaci, kdy místo legálního ukazatele na seznam
 ** předá někdo jako parametr hodnotu NULL.
 **
 ** Svou implementaci vhodně komentujte!
 **
 ** Terminologická poznámka: Jazyk C nepoužívá pojem procedura.
 ** Proto zde používáme pojem funkce i pro operace, které by byly
 ** v algoritmickém jazyce Pascalovského typu implemenovány jako
 ** procedury (v jazyce C procedurám odpovídají funkce vracející typ void).
 **/

#include "c206.h"

int errflg;
int solved;

void DLError() {
    /*
     ** Vytiskne upozornění na to, že došlo k chybě.
     ** Tato funkce bude volána z některých dále implementovaných operací.
     **/
    printf ("*ERROR* The program has performed an illegal operation.\n");
    errflg = TRUE;             /* globální proměnná -- příznak ošetření chyby */
    return;
}

void DLInitList (tDLList *L) {
    /*
     ** Provede inicializaci seznamu L před jeho prvním použitím (tzn. žádná
     ** z následujících funkcí nebude volána nad neinicializovaným seznamem).
     ** Tato inicializace se nikdy nebude provádět nad již inicializovaným
     ** seznamem, a proto tuto možnost neošetřujte. Vždy předpokládejte,
     ** že neinicializované proměnné mají nedefinovanou hodnotu.
     **/
    
    L->Act = NULL; //inicializácia aktívneho prvku na NULL
    L->Last = NULL; //inicializácia posledného prvku na NULL
    L->First = NULL; //inicializácia prvého prvku na NULL
}

void DLDisposeList (tDLList *L) {
    /*
     ** Zruší všechny prvky seznamu L a uvede seznam do stavu, v jakém
     ** se nacházel po inicializaci. Rušené prvky seznamu budou korektně
     ** uvolněny voláním operace free.
     **/
    
    while (L->First != NULL) //pokial je zoznam neprázdny
    {
        L->Act = L->First; //prvý prvok je aktívny
	L->First = L->First->rptr; 
        free(L->Act); //uvoľní aktívny prvok
    }
    L->Last = NULL;
    L->Act = NULL;
}

void DLInsertFirst (tDLList *L, int val) {
    /*
     ** Vloží nový prvek na začátek seznamu L.
     ** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
     ** volá funkci DLError().
     **/
   
    tDLElemPtr newElem = malloc(sizeof(struct tDLElem));
    if (newElem == NULL) //v prípade, že nastala chyba pri alokácii pamäte
    {
        DLError();
        return;
    }
    else
    {
        newElem->data = val;
        newElem->rptr = L->First; //pravý prvok nového prvku ukazuje na prvý prvok
        newElem->lptr = NULL; //ľavý prvok nového prvku ukazuje na NULL
        if (L->First != NULL) //v prípade, že zoznam už prvý prvok mal
        {
            L->First->lptr = newElem; //prvý prvok pôjde doľava, ukazovať na nový prvok
        }
        else
        {
            L->Last = newElem; //inak sa vloží prvok do prázdneho zoznamu
        }
        L->First = newElem; //finálna korekcia ukazateľa začiatku
    }
}

void DLInsertLast(tDLList *L, int val) {
    /*
     ** Vloží nový prvek na konec seznamu L (symetrická operace k DLInsertFirst).
     ** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
     ** volá funkci DLError().
     **/
    
    tDLElemPtr elem = malloc(sizeof(struct tDLElem));
    if (elem == NULL) //v prípade, že nastala chyba pri alokácii pamäte
    {
        DLError();
        return;
    }
    elem->data = val;
    elem->lptr = L->Last; //naľavo od novo vloženého prvku sa nachádza bývalý posledný prvok
    elem->rptr = NULL; //napravo je NULL
    if (L->First != NULL) //v prípade, že zoznam nieje prázdny
    {
        L->Last->rptr = elem;
    }
    else
    {
        L->First = elem;
    }
    L->Last = elem;
}

void DLFirst (tDLList *L) {
    /*
     ** Nastaví aktivitu na první prvek seznamu L.
     ** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
     ** aniž byste testovali, zda je seznam L prázdný.
     **/
    
    L->Act = L->First; //aktívny prvok je prvý prvok
}

void DLLast (tDLList *L) {
    /*
     ** Nastaví aktivitu na poslední prvek seznamu L.
     ** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
     ** aniž byste testovali, zda je seznam L prázdný.
     **/
    
    
    L->Act = L->Last; //aktívny prvok je posledný prvok
}

void DLCopyFirst (tDLList *L, int *val) {
    /*
     ** Prostřednictvím parametru val vrátí hodnotu prvního prvku seznamu L.
     ** Pokud je seznam L prázdný, volá funkci DLError().
     **/
    
    if (L->First != NULL) //v prípade, že zoznam nieje prázdny
    {
        (*val) = L->First->data;
    }
    else
    {
        DLError();
        return;
    }
}

void DLCopyLast (tDLList *L, int *val) {
    /*
     ** Prostřednictvím parametru val vrátí hodnotu posledního prvku seznamu L.
     ** Pokud je seznam L prázdný, volá funkci DLError().
     **/
    
    if (L->First != NULL) //v prípade, že zoznam nieje prázdny
    {
        (*val) = L->Last->data;
    }
    else
    {
        DLError();
        return;
    }
}

void DLDeleteFirst (tDLList *L) {
    /*
     ** Zruší první prvek seznamu L. Pokud byl první prvek aktivní, aktivita
     ** se ztrácí. Pokud byl seznam L prázdný, nic se neděje.
     **/
    
    tDLElemPtr elem;
    if (L->First != NULL)
    {
        elem = L->First;
        if (L->Act == L->First) //v prípade, že prvý prvok bol aktívny
        {
            L->Act = NULL; //ruší sa jeho aktivita
        }
        if (L->First == L->Last) //v prípade, že mal zoznam jediný prvok
        {
            L->First = NULL; //ruší sa
            L->Last = NULL; //ruší sa
        }
        else
        {
            L->First = L->First->rptr; //aktualizácia začiatku zoznamu
            L->First->lptr = NULL; //ukazateľ prvého doľava na NULL
        }
        free(elem);
    }
}

void DLDeleteLast (tDLList *L) {
    /*
     ** Zruší poslední prvek seznamu L. Pokud byl poslední prvek aktivní,
     ** aktivita seznamu se ztrácí. Pokud byl seznam L prázdný, nic se neděje.
     **/
    
    if (L->First != NULL) //v prípade, že zoznam nieje prázdny
    {
        tDLElemPtr elem = L->Last; //uloženie posledného prvku zoznamu
        if (L->Act == L->Last) //v prípade, že posledný prvok je zároveň aktívny
        {
            L->Act = NULL; //zoznam prestáva byť aktívny
        }
        if (L->First == L->Last) //ak je prvý prvok zároveň posledným
        {
            L->First = NULL; //prvky sa rušia
            L->Last = NULL;
        }
        else
        {
            L->Last = L->Last->lptr; //prvok naľavo od posledného sa stáva novým posledným prvkom
            L->Last->rptr = NULL; //prvok od nového posledného napravo zrušíme
        }
        free(elem);
    }
}

void DLPostDelete (tDLList *L) {
    /*
     ** Zruší prvek seznamu L za aktivním prvkem.
     ** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
     ** posledním prvkem seznamu, nic se neděje.
     **/
    
    if (L->Act != NULL) //v prípade, že je zoznam aktívny
    {
        if (L->Act->rptr != NULL) //v prípade, že "je čo rušiť"
        {
            tDLElemPtr elem;
            elem = L->Act->rptr; //ukazateľ na prvok, ktorý bude zrušený
            L->Act->rptr = elem->rptr;
            if (elem == L->Last) //v prípade, že rušený prvok bol posledným prvkom
            {
                L->Last = L->Act; //posledný prvok bude aktívny
            }
            else
            {
                elem->rptr->lptr = L->Act; //prvok za zrušeným prvkom ukazuje doľava na aktívny prvok
            }
            free(elem);
        }
    }
}

void DLPreDelete (tDLList *L) {
    /*
     ** Zruší prvek před aktivním prvkem seznamu L .
     ** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
     ** prvním prvkem seznamu, nic se neděje.
     **/
    
    if (L->Act != NULL) //v prípade, že je zoznam aktívny
    {
        if (L->Act->lptr != NULL) //v prípade, že "je čo rušiť"
        {
            tDLElemPtr elem;
            elem = L->Act->lptr; //ukazateľ na rušený prvok
            L->Act->lptr = elem->lptr;
            if (elem == L->First) //v prípade, že je rušený prvok prvým prvkom
            {
                L->First = L->Act; //prvý prvok bude aktívny
            }
            else
            {
                elem->lptr->rptr = L->Act; //prvok pred zrušeným prvkom ukazuje doprava na aktívny prvok
            }
            free(elem);
        }
    }
}

void DLPostInsert (tDLList *L, int val) {
    /*
     ** Vloží prvek za aktivní prvek seznamu L.
     ** Pokud nebyl seznam L aktivní, nic se neděje.
     ** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
     ** volá funkci DLError().
     **/
    
    if (L->Act != NULL) //v prípade, že zoznam je aktívny (že je kam vkládať)
    {
        tDLElemPtr newElem = malloc(sizeof(struct tDLElem));
        if (newElem == NULL) //v prípade, že pri alokácii pamäte nastala chyba
        {
            DLError();
            return;
        }
        else
        {
            newElem->data = val;
            newElem->rptr = L->Act->rptr;
            newElem->lptr = L->Act;
            L->Act->rptr = newElem; //naviazanie ľavého suseda na nový prvok
            if (L->Act == L->Last) //ak je aktívny prvok zároveň posledný, vkladá za posledného
            {
                L->Last = newElem; //korekcia ukazateľa na koniec
            }
            else
            {
                newElem->rptr->lptr = newElem; //naviazanie pravého suseda na nový prvok
            }
        }
    }
}

void DLPreInsert (tDLList *L, int val) {
    /*
     ** Vloží prvek před aktivní prvek seznamu L.
     ** Pokud nebyl seznam L aktivní, nic se neděje.
     ** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
     ** volá funkci DLError().
     **/
    
    if (L->Act != NULL) //v prípade, že zoznam je aktívny
    {
        tDLElemPtr elem = malloc(sizeof(struct tDLElem));
        if (elem == NULL)
        {
            DLError(); //v prípade, že nastala chyba pri alokácii pamäte
            return;
        }
        elem->data = val; //nastaví zložku data novozniknutého prvku na hodnotu val
        elem->rptr = L->Act; //prvok napravo od neho je aktívnym prvkom
        elem->lptr = L->Act->lptr; //prvok naľavo od neho je prvok naľavo od aktívneho prvku
        L->Act->lptr = elem; //prvok naľavo od aktívneho prvku je nový prvok
        if (L->Act == L->First) //v prípade, že aktívny prvok bol zároveň prvým prvkom
        {
            L->First = elem; //prvým prvkom je nový prvok
        }
        else
        {
            elem->lptr->rptr = elem; 
        }
    }
    else
    {
        return;
    }
}

void DLCopy (tDLList *L, int *val) {
    /*
     ** Prostřednictvím parametru val vrátí hodnotu aktivního prvku seznamu L.
     ** Pokud seznam L není aktivní, volá funkci DLError ().
     **/
    
    
    if (L->Act != NULL) //v prípade, že zoznam je aktívny
    {
        (*val) = L->Act->data;
    }
    else
    {
        DLError();
        return;
    }
}

void DLActualize (tDLList *L, int val) {
    /*
     ** Přepíše obsah aktivního prvku seznamu L.
     ** Pokud seznam L není aktivní, nedělá nic.
     **/
    
    if (L->Act == NULL) //v prípade, že zoznam nie je aktívny
    {
        return; //funkcia nevykonáva nič
    }
    else
    {
	L->Act->data = val;
    }
}

void DLSucc (tDLList *L) {
    /*
     ** Posune aktivitu na následující prvek seznamu L.
     ** Není-li seznam aktivní, nedělá nic.
     ** Všimněte si, že při aktivitě na posledním prvku se seznam stane neaktivním.
     **/

    if (L->Act == NULL) //v prípade, že zoznam nieje aktívny
    {
        return;
    }
    if (L->Act == L->Last) //v prípade, že aktívny prvok je posledným prvkom
    {
        L->Act = NULL; //zoznam sa stáva neaktívnym
    }
    else
    {
        L->Act = L->Act->rptr;
    }
}


void DLPred (tDLList *L) {
    /*
     ** Posune aktivitu na předchozí prvek seznamu L.
     ** Není-li seznam aktivní, nedělá nic.
     ** Všimněte si, že při aktivitě na prvním prvku se seznam stane neaktivním.
     **/
    
    if (L->Act == NULL) //v prípade, že zoznam nieje aktívny
    {
        return;
    }
    if (L->Act == L->First) //v prípade, že aktívny prvok je prvým prvkom
    {
        L->Act = NULL;
    }
    else
    {
        L->Act = L->Act->lptr;
    }
}

int DLActive (tDLList *L) {
    /*
     ** Je-li seznam L aktivní, vrací nenulovou hodnotu, jinak vrací 0.
     ** Funkci je vhodné implementovat jedním příkazem return.
     **/
    
    return L->Act != NULL; //vráti FALSE (0) v prípade, že L->Act nadobúda hodnotu NULL
}

/* Konec c206.c*/