import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()  # Grafo semplice e pesato

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getAllCategories()

    def buildGraph(self, categoria,start_date,end_date):
        # Recupero i costruttori del periodo selezionato
        prodotti = DAO.getProductsbyCategory(categoria)

        # Svuoto il grafo prima di ricostruirlo
        self._graph.clear()

        # Aggiungo i costruttori come nodi
        self._graph.add_nodes_from(prodotti)
        # Creo una mappa: ID -> oggetto Product
        pMap = {}
        for p in prodotti:
            pMap[p.product_id] = p

        # Recupero gli archi
        archi = DAO.getP1P2(categoria,start_date, end_date)

        #esamino tutte le colonne in input da DAO.getP1P2
        for p1, p2, v1,v2,q1,q2 in archi:

            # AASEGNO/RECUPERO GLI OGGETTI CORRISPONDENTI AGLI ID
            p1 = pMap[p1]
            p2 = pMap[p2]

            # IL PESO È LA SOMMA DEI PEZZI VENDUTI (TotPezzi/QuantitaTot)
            peso= q1+q2

            #DIREZIONE DA VENDITE MINORI A VENDITE MAGGIORI (per TotOrdini/NuMvendite considero v1,v2)

            if q1<q2:
                # P1 HA MENO ORDINI: ARCO DA P1 A P2
                self._graph.add_edge(p1, p2, weight=peso)
            elif q1>q2:
                # P2 HA MENO ORDINI: ARCO DA P2 A P1
                self._graph.add_edge(p2, p1, weight=peso)
            else:
                # PARITÀ: AGGIUNGO ENTRAMBI GLI ARCHI
                self._graph.add_edge(p1, p2, weight=peso)
                self._graph.add_edge(p2, p1, weight=peso)

    def getNumNodi(self):
        # Restituisco il numero di nodi
        return len(self._graph.nodes())

    def getNumArchi(self):
        # Restituisco il numero di archi
        return len(self._graph.edges())