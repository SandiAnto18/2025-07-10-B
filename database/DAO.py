from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    #GRAFO ORIENTATO/DIRETTO E PESATO

    @staticmethod
    def getAllCategories():
        # Recupero tutti gli anni disponibili nel database
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.category_name 
from categories c
            """

        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductsbyCategory(categoria):
        # Recupero tutti gli anni disponibili nel database
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.*
from products p , categories c
where p.category_id =c.category_id 
and c.category_name = %s
                """

        cursor.execute(query,(categoria,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getP1P2(categoria,start_date, end_date):
        # Recupero tutti gli anni disponibili nel database
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
-- RECUPERO LE STATISTICHE DEI DUE PRODOTTI
SELECT
    tot1.p1 as p1,
    tot1.numordini as NumOrdini1,
    tot1.totquantita as TotQuantita1,
    tot2.p2 as p2,
    tot2.numordini as NumOrdini2,
    tot2.totquantita as TotQuantita2

-- CREO DUE TABELLE TEMPORANEE (TOT1 E TOT2)
FROM
(
    
    SELECT
        p.product_id AS p1,
        COUNT(DISTINCT o.order_id) AS NumOrdini,
        SUM(oi.quantity) AS TotQuantita
    FROM products p, orders o, order_items oi, categories c
    WHERE p.product_id = oi.product_id
      AND oi.order_id = o.order_id
      AND c.category_id = p.category_id
      AND c.category_name = %s
      AND o.order_date BETWEEN %s
                           AND %s
    GROUP BY p1

) AS tot1,

(
    SELECT
        p.product_id AS p2,
        COUNT(DISTINCT o.order_id) AS NumOrdini,
        SUM(oi.quantity) AS TotQuantita

    FROM products p, orders o, order_items oi, categories c

    WHERE p.product_id = oi.product_id
      AND oi.order_id = o.order_id
      AND c.category_id = p.category_id
      AND c.category_name = %s
      AND o.order_date BETWEEN %s
                           AND %s
    GROUP BY p2

) AS tot2

-- ABBINO I PRODOTTI A DUE A DUE
-- CONSIDERO SOLO LE COPPIE NON INVERTITE, EVITANDO I DUPLICATI
WHERE tot1.p1 < tot2.p2
-- USO LE SOTTOQUERY PER AGGREGARE SEPARATAMENTE I DATI DEI DUE PRODOTTI,
-- EVITANDO CHE LE RIGHE SI MOLTIPLICHINO QUANDO CONFRONTO LE LORO VENDITE.
"""

        cursor.execute(query, (categoria,start_date,end_date,categoria,start_date,end_date))

        for row in cursor:
            results.append((row["p1"],row["p2"],row["NumOrdini1"],row["NumOrdini2"],row["TotQuantita1"],row["TotQuantita2"]))
        cursor.close()
        conn.close()
        return results



