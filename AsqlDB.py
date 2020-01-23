import sqlite3
import os

class MicroserviceDB: 
    def __init__(self):
        
        # Set up DB filename
        self.__db_filename = "microserviceDB.db"
        
        # If DB file exists remove it for clean start
        if os.path.isfile("microserviceDB.db"):
            os.remove("microserviceDB.db")
        
        # Create DB and tables
        # Set up conection
        self.connect()
        print("Creating DB and tables.")
        # Create tables
            # Create Products table
        self.__conn.execute(("""
                create table products (
            id          integer primary key autoincrement not null,
            name        text,
            description text
            )
                """))
        # Create Offers table
        self.__conn.execute(("""
                create table offers (
            id      integer primary key,  
            price   integer, 
            items_in_stock   integer,
            product_id integer
            )
                """))
        # Close connection
        self.__conn.close()

        # Set up conection
    def connect(self):
        self.__conn = sqlite3.connect(self.__db_filename, check_same_thread=False)
        
        # Insert Product
    def insertProduct(self, name: str, description: str):
        # Set up conneciton and cursor
        self.connect()
        cursor = self.__conn.cursor()
        # Define insert query
        sql =  ''' INSERT INTO products (name,description)
              VALUES(?,?) '''
        row = (name, description)
        # Execute statement
        cursor.execute(sql, row)

        # Commit and close connection
        self.__conn.commit()
        self.__conn.close()

        # Return product ID
        return cursor.lastrowid

        # Update product
    def updateProduct(self, id: int, name:str = '', description:str = ''):
        # Set up conneciton and coursor
        self.connect()
        cursor = self.__conn.cursor()

        # Statement for updating desctiption only 
        if name == '' and description != '':

            sql =  ''' UPDATE products
                SET description = ?
                WHERE id = ? '''
            row = (description, id)
        # Statement for updating name only 
        elif name != '' and description == '':
            sql =  ''' UPDATE products
                SET name = ?
                WHERE id = ? '''
            row = (name, id)
        # Statement for updating both name and desctiption  
        elif name != '' and description != '':
            sql =  ''' UPDATE products
                SET name = ?,
                description = ?
                WHERE id = ? '''
            row = (name, description, id)
        # Execute statement
        cursor.execute(sql, row)

        # Print confirmation after the process is done
        if name == '' and description == '':
            print("Product " + "'" + str(id) +  "'"+ " not updated.")
        else:
            print("Product " + "'" + str(id) +  "'"+ " updated.")
        # Commit and close connection
        self.__conn.commit()
        self.__conn.close()

        # Delete Product
    def deleteProduct(self, id):
        # Connect and set cursor
        self.connect()
        cursor = self.__conn.cursor()
        # Delete from Products table
        sql = '''DELETE from products WHERE id = ?''' 
        cursor.execute(sql, [id])
        # Delete from Offers table
        sql = '''DELETE from offers WHERE product_id = ?'''
        cursor.execute(sql, [id])
        #Commit and close connection
        self.__conn.commit()
        self.__conn.close()

        # Insert Offer
    def insertOffer(self, id: int, price: int, items_in_stock: int, product_id: int):
        # Set up connection and cursor
        self.connect()
        cursor = self.__conn.cursor()
        # Define statement
        sql =  ''' INSERT INTO offers (id,price,items_in_stock,product_id)
             VALUES(?,?,?,?) '''

        row = (id, price, items_in_stock, product_id)
        # Execute statement
        cursor.execute(sql, row)
        #Commit and close connection
        self.__conn.commit()
        self.__conn.close()

        # Update Offer
    def updateOffer(self, id: int, price: int, items_in_stock: int):
        # Set up connection and cursor
        self.connect()
        cursor = self.__conn.cursor()
        # Define statement
        sql =  ''' UPDATE offers
            SET price = ?,
                items_in_stock = ?
            WHERE id = ? '''

        row = (price, items_in_stock, id)
        # Execute statement
        cursor.execute(sql, row)
        
        #Commit and close connection
        self.__conn.commit()
        self.__conn.close()
                
        # Get Products
    def getProducts(self):
        # Set up connection and cursor
        self.connect()
        cursor = self.__conn.cursor()        
        # Define statement        
        sql =  ''' SELECT * from products '''
        # Execute statement
        cursor.execute(sql)
        # Store output
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        # Close connection
        self.__conn.close()
        # Return output
        return output

        # Get one product
    def getProduct(self, id):
        # Set up connection and cursor
        self.connect()
        cursor = self.__conn.cursor()        
        # Define statement  
        sql =  ''' SELECT * from products WHERE id = ? '''
        # Execute statement 
        cursor.execute(sql, [id])
        # Store output
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        # Close connection
        self.__conn.close()
        # Return output
        return output

        # Get offers for one product
    def getOffer(self, id):
        # Set up connection and cursor
        self.connect()
        cursor = self.__conn.cursor()        
        # Define statement
        sql =  ''' SELECT * from offers WHERE product_id = ? '''
        # Execute statement
        cursor.execute(sql, [id])
        # Store output
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        # Close connection
        self.__conn.close()
        # Return output
        return output

        # Get Offers
    def getOffers(self):
        # Set up connection and cursor
        self.connect()
        cursor = self.__conn.cursor()        
        # Define statement
        sql =  ''' SELECT * from offers '''
        # Execute statement
        cursor.execute(sql)
        # Store output
        output = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        # Close connection
        self.__conn.close()
        # Return output
        return output