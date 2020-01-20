import sqlite3
import os

class MicroserviceDB: 
    def __init__(self):
        
        self.db_filename = "microserviceDB.db"
        
        # If DB file exists remove it for clean start
        if os.path.isfile("microserviceDB.db"):
            os.remove("microserviceDB.db")
        
        # Create DB and tables
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        print("Creating DB and tables.")
        # Create tables
            # Create Products table
        conn.execute(("""
                create table products (
            id          integer primary key autoincrement not null,
            name        text,
            description text
            )
                """))
        # Create Offers table
        conn.execute(("""
                create table offers (
            id      integer primary key,  
            price   integer, 
            items_in_stock   integer,
            product_id integer
            )
                """))

        conn.close()

        # Insert Product
    def insertProduct(self, name: str, description: str):
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        
        sql =  ''' INSERT INTO products (name,description)
              VALUES(?,?) '''
        row = (name, description)

        cursor.execute(sql, row)
        productId = cursor.lastrowid

        conn.commit()
        conn.close()

        return productId

        # Update product
    def updateProduct(self, id: int, name:str = '', description:str = ''):
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        if name == '' and description != '':

            sql =  ''' UPDATE products
                SET description = ?
                WHERE id = ? '''
            row = (description, id)

        elif name != '' and description == '':
            sql =  ''' UPDATE products
                SET name = ?
                WHERE id = ? '''
            row = (name, id)

        elif name != '' and description != '':
            sql =  ''' UPDATE products
                SET name = ?,
                description = ?
                WHERE id = ? '''
            row = (name, description, id)
        
        cursor.execute(sql, row)

        if name == '' and description == '':
            print("Product " + "'" + str(id) +  "'"+ " not updated.")
        else:
            print("Product " + "'" + str(id) +  "'"+ " updated.")

        conn.commit()
        conn.close()

        # Delete Product
    def deleteProduct(self, id):
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        # Delete from Products table
        sql = '''DELETE from products WHERE id = ?''' 
        cursor.execute(sql, [id])
        # Delete from Offers table
        sql = '''DELETE from offers WHERE product_id = ?'''
        cursor.execute(sql, [id])

        conn.commit()
        conn.close()

        # Insert Offer
    def insertOffer(self, id: int, price: int, items_in_stock: int, product_id: int):

        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()

        sql =  ''' INSERT INTO offers (id,price,items_in_stock,product_id)
             VALUES(?,?,?,?) '''

        row = (id, price, items_in_stock, product_id)

        cursor.execute(sql, row)

        conn.commit()
        conn.close()

        # Update Offer
    def updateOffer(self, id: int, price: int, items_in_stock: int):

        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()

        sql =  ''' UPDATE offers
            SET price = ?,
                items_in_stock = ?
            WHERE id = ? '''

        row = (price, items_in_stock, id)

        cursor.execute(sql, row)
        
        conn.commit()
        conn.close()
                
        # Get Products
    def getProducts(self):
        
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        
        sql =  ''' SELECT * from products '''

        cursor.execute(sql)
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

        conn.close()
        return output

        # Get one product
    def getProduct(self, id):
        
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        
        sql =  ''' SELECT * from products WHERE id = ? '''

        cursor.execute(sql, [id])
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

        conn.close()
        return output

        # Get offers for one product
    def getOffer(self, id):
        
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        
        sql =  ''' SELECT * from offers WHERE product_id = ? '''

        cursor.execute(sql, [id])
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

        conn.close()
        return output

        # Get Offers
    def getOffers(self):
        
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        cursor = conn.cursor()
        
        sql =  ''' SELECT * from offers '''

        cursor.execute(sql)
        
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

        conn.close()
        return output