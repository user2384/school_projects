
/* c201.c *********************************************************************}
 {* Téma: Jednosměrný lineární seznam
 **
 **                     Návrh a referenční implementace: Petr Přikryl, říjen 1994
 **                                          Úpravy: Andrea Němcová listopad 1996
 **                                                   Petr Přikryl, listopad 1997
 **                                Přepracované zadání: Petr Přikryl, březen 1998
 **                                  Přepis do jazyka C: Martin Tuček, říjen 2004
 **                                            Úpravy: Kamil Jeřábek, září 2018
 **
 ** Implementujte abstraktní datový typ jednosměrný lineární seznam.
 ** Užitečným obsahem prvku seznamu je celé číslo typu int.
 ** Seznam bude jako datová abstrakce reprezentován proměnnou typu tList.
 ** Definici konstant a typů naleznete v hlavičkovém souboru c201.h.
 **
 ** Vaším úkolem je implementovat následující operace, které spolu s výše
 ** uvedenou datovou částí abstrakce tvoří abstraktní datový typ tList:
 **
 **      InitList ...... inicializace seznamu před prvním použitím,
 **      DisposeList ... zrušení všech prvků seznamu,
 **      InsertFirst ... vložení prvku na začátek seznamu,
 **      First ......... nastavení aktivity na první prvek,
 **      CopyFirst ..... vrací hodnotu prvního prvku,
 **      DeleteFirst ... zruší první prvek seznamu,
 **      PostDelete .... ruší prvek za aktivním prvkem,
 **      PostInsert .... vloží nový prvek za aktivní prvek seznamu,
 **      Copy .......... vrací hodnotu aktivního prvku,
 **      Actualize ..... přepíše obsah aktivního prvku novou hodnotou,
 **      Succ .......... posune aktivitu na další prvek seznamu,
 **      Active ........ zjišťuje aktivitu seznamu.
 **
 ** Při implementaci funkcí nevolejte žádnou z funkcí implementovaných v rámci
 ** tohoto příkladu, není-li u dané funkce explicitně uvedeno něco jiného.
 **
 ** Nemusíte ošetřovat situaci, kdy místo legálního ukazatele na seznam předá
 ** někdo jako parametr hodnotu NULL.
 **
 ** Svou implementaci vhodně komentujte!
 **
 ** Terminologická poznámka: Jazyk C nepoužívá pojem procedura.
 ** Proto zde používáme pojem funkce i pro operace, které by byly
 ** v algoritmickém jazyce Pascalovského typu implemenovány jako
 ** procedury (v jazyce C procedurám odpovídají funkce vracející typ void).
 **/

#include "c201.h"

int errflg;
int solved;

void Error() {
    /*
     ** Vytiskne upozornění na to, že došlo k chybě.
     ** Tato funkce bude volána z některých dále implementovaných operací.
     **/
    printf ("*ERROR* The program has performed an illegal operation.\n");
    errflg = TRUE;                      /* globální proměnná -- příznak chyby */
}

void InitList (tList *L) {
    /*
     ** Provede inicializaci seznamu L před jeho prvním použitím (tzn. žádná
     ** z následujících funkcí nebude volána nad neinicializovaným seznamem).
     ** Tato inicializace se nikdy nebude provádět nad již inicializovaným
     ** seznamem, a proto tuto možnost neošetřujte. Vždy předpokládejte,
     ** že neinicializované proměnné mají nedefinovanou hodnotu.
     **/
    
    L->Act = NULL; //inicializácia aktívneho prvku na NULL
    L->First = NULL; //inicializácia prvého prvku na NULL
    
}

void DisposeList (tList *L) {
    /*
     ** Zruší všechny prvky seznamu L a uvede seznam L do stavu, v jakém se nacházel
     ** po inicializaci. Veškerá paměť používaná prvky seznamu L bude korektně
     ** uvolněna voláním operace free.
     ***/
    
    while (L->First != NULL) //dokiaľ je zoznam ešte stále neprázdny
    {
        L->Act = L->First; //prvý prvok sa stáva aktívnym
        L->First = L->First->ptr; //vyviaže sa prvá položka zo zoznamu
        free(L->Act); //volaním tejto operácie je pamäť, ktorú používali prvky, korektne uvoľnená
    }
    L->Act = NULL; //zoznam prestáva byť aktívny
}

void InsertFirst (tList *L, int val) {
    /*
     ** Vloží prvek s hodnotou val na začátek seznamu L.
     ** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
     ** volá funkci Error().
     **/
    
    tElemPtr newElem = malloc(sizeof(struct tElem)); //vytvorenie nového prvku
    if (newElem == NULL) //v prípade, že alokácia neprebehla v poriadku
    {
        Error();
        return;
    }
    newElem->data = val; //nastavenie dátovej zložky na hodnotu val
    newElem->ptr = L->First; //nastavenie ukazateľa tam, kam momentálne ukazuje začiatok
    L->First = newElem;
}

void First (tList *L) {
    /*
     ** Nastaví aktivitu seznamu L na jeho první prvek.
     ** Funkci implementujte jako jediný příkaz, aniž byste testovali,
     ** zda je seznam L prázdný.
     **/
    
    L->Act = L->First; //prvý prvok sa stane aktivným
}

void CopyFirst (tList *L, int *val) {
    /*
     ** Prostřednictvím parametru val vrátí hodnotu prvního prvku seznamu L.
     ** Pokud je seznam L prázdný, volá funkci Error().
     **/
    
    if (L->First == NULL) //v prípade, že zoznam je prázdny
    {
	Error(); //volá Error
    }
    else
    {
	(*val) = L->First->data;
        return;
    }
}

void DeleteFirst (tList *L) {
    /*
     ** Zruší první prvek seznamu L a uvolní jím používanou paměť.
     ** Pokud byl rušený prvek aktivní, aktivita seznamu se ztrácí.
     ** Pokud byl seznam L prázdný, nic se neděje.
     **/
    
    if (L->First == NULL) //v prípade, že je zoznam prázdny
    {
	return; //funkcia nevykonáva nič
    }
    else
    {
        tElemPtr elem = L->First;
        if (L->Act == L->First) //v prípade, že prvý prvok je aktívny
        {
            L->Act = NULL; //zoznam prestáva byť aktivným
        }
        L->First = L->First->ptr; //nasledujúci prvok sa stáva prvým
        free(elem);
    }
}

void PostDelete (tList *L) {
    /*
     ** Zruší prvek seznamu L za aktivním prvkem a uvolní jím používanou paměť.
     ** Pokud není seznam L aktivní nebo pokud je aktivní poslední prvek seznamu L,
     ** nic se neděje.
     **/
    
    tElemPtr elem_ptr;
    if (L->Act != NULL) //v prípade, že zoznam je aktívny
    {
        if (L->Act->ptr != NULL) //v prípade, že "je čo rušiť" == že posledný prvok zoznamu je aktívny
        {
            elem_ptr = L->Act->ptr; //ukazateľ na prvok, ktorý sa ruší
            L->Act->ptr = elem_ptr->ptr;
            free(elem_ptr);
        }
    }
}

void PostInsert (tList *L, int val) {
    /*
     ** Vloží prvek s hodnotou val za aktivní prvek seznamu L.
     ** Pokud nebyl seznam L aktivní, nic se neděje!
     ** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
     ** zavolá funkci Error().
     **/
    
    if (L->Act == NULL) // v prípade, že je zoznam neaktívny
    {
	return; // funkcia nevykoná nič
    }
    else
    {
        tElemPtr newElem = malloc(sizeof(struct tElem));
        if (newElem == NULL) //v prípade, že nastala chyba pri alokácii pamäte
        {
            Error();
            return;
        }
        newElem->data = val;
        newElem->ptr = L->Act->ptr; //ukazateľ ukazuje tam, kam aktívny
        L->Act->ptr = newElem; //aktívny ukazuje na nového
    }
}

void Copy (tList *L, int *val) {
    /*
     ** Prostřednictvím parametru val vrátí hodnotu aktivního prvku seznamu L.
     ** Pokud seznam není aktivní, zavolá funkci Error().
     **/
    
    if (L->Act == NULL) //v prípade, že zoznam je neaktívny
    {
	Error(); // zavolá Error
    }
    else
    {
        (*val) = L->Act->data;
        return;
    }
}

void Actualize (tList *L, int val) {
    /*
     ** Přepíše data aktivního prvku seznamu L hodnotou val.
     ** Pokud seznam L není aktivní, nedělá nic!
     **/
    
    if (L->Act == NULL) //v prípade, že zoznam je neaktívny
    {
        return; //funkcia nevykonáva nič
    }
    else
    {
	L->Act->data = val; //prepíše dáta aktívneho prvku na hodnotu val
    }
}

void Succ (tList *L) {
    /*
     ** Posune aktivitu na následující prvek seznamu L.
     ** Všimněte si, že touto operací se může aktivní seznam stát neaktivním.
     ** Pokud není předaný seznam L aktivní, nedělá funkce nic.
     **/
    
    if (L->Act == NULL) //v prípade, že je zoznam neaktívny
    {
        return; //funkcia nevykonáva nič
    }
    else
    {
	L->Act = L->Act->ptr; //aktívnym prvkom sa stáva nasledujúci prvok
    }
}

int Active (tList *L) {
    /*
     ** Je-li seznam L aktivní, vrací nenulovou hodnotu, jinak vrací 0.
     ** Tuto funkci je vhodné implementovat jedním příkazem return.
     **/
    
    return L->Act != NULL; //vráti FALSE (0), v prípade, ak L->Act nadobúda hodnotu NULL

}

/* Konec c201.c */
