
/* c016.c: **********************************************************}
 {* Téma:  Tabulka s Rozptýlenými Položkami
 **                      První implementace: Petr Přikryl, prosinec 1994
 **                      Do jazyka C prepsal a upravil: Vaclav Topinka, 2005
 **                      Úpravy: Karel Masařík, říjen 2014
 **                              Radek Hranický, 2014-2018
 **
 ** Vytvořete abstraktní datový typ
 ** TRP (Tabulka s Rozptýlenými Položkami = Hash table)
 ** s explicitně řetězenými synonymy. Tabulka je implementována polem
 ** lineárních seznamů synonym.
 **
 ** Implementujte následující procedury a funkce.
 **
 **  HTInit ....... inicializuje tabulku před prvním použitím
 **  HTInsert ..... vložení prvku
 **  HTSearch ..... zjištění přítomnosti prvku v tabulce
 **  HTDelete ..... zrušení prvku
 **  HTRead ....... přečtení hodnoty prvku
 **  HTClearAll ... zrušení obsahu celé tabulky (inicializace tabulky
 **                 poté, co již byla použita)
 **
 ** Definici typů naleznete v souboru c016.h.
 **
 ** Tabulka je reprezentována datovou strukturou typu tHTable,
 ** která se skládá z ukazatelů na položky, jež obsahují složky
 ** klíče 'key', obsahu 'data' (pro jednoduchost typu float), a
 ** ukazatele na další synonymum 'ptrnext'. Při implementaci funkcí
 ** uvažujte maximální rozměr pole HTSIZE.
 **
 ** U všech procedur využívejte rozptylovou funkci hashCode.  Povšimněte si
 ** způsobu předávání parametrů a zamyslete se nad tím, zda je možné parametry
 ** předávat jiným způsobem (hodnotou/odkazem) a v případě, že jsou obě
 ** možnosti funkčně přípustné, jaké jsou výhody či nevýhody toho či onoho
 ** způsobu.
 **
 ** V příkladech jsou použity položky, kde klíčem je řetězec, ke kterému
 ** je přidán obsah - reálné číslo.
 */

#include "c016.h"

int HTSIZE = MAX_HTSIZE;
int solved;

/*          -------
 ** Rozptylovací funkce - jejím úkolem je zpracovat zadaný klíč a přidělit
 ** mu index v rozmezí 0..HTSize-1.  V ideálním případě by mělo dojít
 ** k rovnoměrnému rozptýlení těchto klíčů po celé tabulce.  V rámci
 ** pokusů se můžete zamyslet nad kvalitou této funkce.  (Funkce nebyla
 ** volena s ohledem na maximální kvalitu výsledku). }
 */

int hashCode ( tKey key ) {
    int retval = 1;
    int keylen = strlen(key);
    for ( int i=0; i<keylen; i++ )
        retval += key[i];
    return ( retval % HTSIZE );
}

/*
 ** Inicializace tabulky s explicitně zřetězenými synonymy.  Tato procedura
 ** se volá pouze před prvním použitím tabulky.
 */

void htInit ( tHTable* ptrht ) {
    int cnt = 0; //pomocný counter na indexovanie tabuľky
    while (cnt < HTSIZE) //prejde celú tabuľku
    {
        (*ptrht)[cnt] = NULL; //inicializuje na NULL
        cnt++; //inkrementácia countera
    }
}

/* TRP s explicitně zřetězenými synonymy.
 ** Vyhledání prvku v TRP ptrht podle zadaného klíče key.  Pokud je
 ** daný prvek nalezen, vrací se ukazatel na daný prvek. Pokud prvek nalezen není,
 ** vrací se hodnota NULL.
 **
 */

tHTItem* htSearch ( tHTable* ptrht, tKey key ) {
    
    tHTItem *searchin_one = NULL; //pomocná položka pomocou ktorej budeme prehľadávať tabuľku
    int idx;
    idx = hashCode(key); //vypočítanie umiestnenia položky
    searchin_one = (*ptrht)[idx];  //uložíme adresu prvej položky synoným
    while ((searchin_one != NULL) && (strcmp(key, searchin_one->key)))
           searchin_one = searchin_one->ptrnext; //postupujeme na ďalší synonym
    return searchin_one;
}

/*
 ** TRP s explicitně zřetězenými synonymy.
 ** Tato procedura vkládá do tabulky ptrht položku s klíčem key a s daty
 ** data.  Protože jde o vyhledávací tabulku, nemůže být prvek se stejným
 ** klíčem uložen v tabulce více než jedenkrát.  Pokud se vkládá prvek,
 ** jehož klíč se již v tabulce nachází, aktualizujte jeho datovou část.
 **
 ** Využijte dříve vytvořenou funkci htSearch.  Při vkládání nového
 ** prvku do seznamu synonym použijte co nejefektivnější způsob,
 ** tedy proveďte.vložení prvku na začátek seznamu.
 **/

void htInsert ( tHTable* ptrht, tKey key, tData data ) {
    if (ptrht != NULL)
    {
        tHTItem *searchin_one; //pomocná premenná slúžiaca na uchovanie adresy položky
        searchin_one = htSearch(ptrht,key); //vyhľadáme položku s daným kľúčom key
        int idx;
        idx = hashCode(key);
        if (searchin_one == NULL) //ak sme ju zatiaľ nenašli
        {
            tHTItem *new_item = malloc(sizeof(tHTItem)); //vytvoríme novú položku
            new_item->key = key; //uložíme kľúč do novej položky
            new_item->data = data; //uložíme dáta do novej položky
            new_item->ptrnext = (*ptrht)[idx]; //vložíme ukazateľ na nasledujúcu položku
            (*ptrht)[idx] = new_item; //vložíme ju ako prvé synonymum
        }
        else //ak sa položka našla
        {
            searchin_one->data = data; //aktualizujeme dáta danej položky
        }
    }
}

/*
 ** TRP s explicitně zřetězenými synonymy.
 ** Tato funkce zjišťuje hodnotu datové části položky zadané klíčem.
 ** Pokud je položka nalezena, vrací funkce ukazatel na položku
 ** Pokud položka nalezena nebyla, vrací se funkční hodnota NULL
 **
 ** Využijte dříve vytvořenou funkci HTSearch.
 */

tData* htRead ( tHTable* ptrht, tKey key ) {
    tHTItem *searchin_one; //pomocná premenná
    searchin_one = htSearch(ptrht,key); //hladáme položku s kľúčom key
    if (searchin_one == NULL) //ak sa nenašla
        return NULL;
    else //inak
        return &searchin_one->data; //vrátime adresu
}


/*
 ** TRP s explicitně zřetězenými synonymy.
 ** Tato procedura vyjme položku s klíčem key z tabulky
 ** ptrht.  Uvolněnou položku korektně zrušte.  Pokud položka s uvedeným
 ** klíčem neexistuje, dělejte, jako kdyby se nic nestalo (tj. nedělejte
 ** nic).
 **
 ** V tomto případě NEVYUŽÍVEJTE dříve vytvořenou funkci HTSearch.
 */

void htDelete ( tHTable* ptrht, tKey key ) {
    if ((*ptrht) != NULL)
    {
        int idx;
        idx = hashCode(key);

        tHTItem *pom1; //pomocná premenná
        tHTItem *pom2; //pomocná premenná
        pom1 = (*ptrht)[idx]; //prvý prvok zoznamu
        pom2 = (*ptrht)[idx]; //prvý prvok zoznamu
        
        while (pom1 != NULL) //prechádzame celý zoznam
        {
            if (pom1->key == key) //ak nájde kľúč
            {
                if (pom1 != (*ptrht)[idx])
                {
                    pom2->ptrnext = pom1->ptrnext;
                }
                else
                {
                    (*ptrht)[idx] = pom1->ptrnext;
                }
                free(pom1);
            }
            pom2 = pom1; //ak nenájde kľúč, postupujeme ďalej
            pom1 = pom1->ptrnext;
        }
    }
}

/* TRP s explicitně zřetězenými synonymy.
 ** Tato procedura zruší všechny položky tabulky, korektně uvolní prostor,
 ** který tyto položky zabíraly, a uvede tabulku do počátečního stavu.
 */

void htClearAll ( tHTable* ptrht ) {
    tHTItem *actual; //pomocná premenná
    tHTItem *next_one; //pomocná premenná
    actual = NULL; //nastavíme na NULL
    next_one = NULL; //nastavíme na NULL
    int cnt = 0; //pomocný counter
    while (cnt < HTSIZE) //prechádzame celý zoznam
    {
        actual = (*ptrht)[cnt];
        while (actual != NULL){
            next_one = actual->ptrnext;
            free(actual);
            actual = next_one;
        }
        (*ptrht)[cnt] = NULL;
        cnt++;
    }
}
