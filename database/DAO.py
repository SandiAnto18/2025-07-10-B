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
        query = """select distinct p.product_id as p1 ,p2.product_id as p2 , count(distinct o.order_id) as NumOrdiniP1,
count(distinct o2.order_id) as NumOrdiniP2,sum(distinct oi.quantity) as TotQuantitaP1, sum( distinct oi2.quantity) as TotQuantitaP2
from products p ,order_items oi, categories c , orders o,
products p2 ,order_items oi2, categories c2 , orders o2
where p.category_id =c.category_id 
and c.category_name = %s
and o.order_date between %s and %s
and p.product_id =oi.product_id 
and oi.order_id =o.order_id 
and p2.category_id =c2.category_id 
and c2.category_name = %s
and o2.order_date between %s and %s
and p2.product_id =oi2.product_id 
and oi2.order_id =o2.order_id
and p.product_id < p2.product_id 
group by p1,p2

                    """

        cursor.execute(query, (categoria,start_date,end_date,categoria,start_date,end_date))

        for row in cursor:
            results.append((row["p1"],row["p2"],row["NumOrdiniP1"],row["NumOrdiniP2"],row["TotQuantitaP1"],row["TotQuantitaP2"]))

        cursor.close()
        conn.close()
        return results



