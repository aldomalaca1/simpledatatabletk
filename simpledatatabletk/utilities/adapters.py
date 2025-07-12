from typing import Any
from abc import abstractmethod
from typing import override
from sqlite3 import Cursor
from sqlite3 import OperationalError
import sqlite3
import os

#Father class for Adapters
class Adapter():
      def __init__(self):
        self._total_rows,self._total_columns = 0,0

      @abstractmethod
      def create_structure(self)-> list[list[str]]:
        pass

      def get_size(self) -> tuple[int, int]:
        return self._total_rows, self._total_columns


class ManualAdapter(Adapter):
    def __init__(self):
        super().__init__()
        self.__table_data: list[list[str]] = []

    def add(self, header: str, values: list[Any]) -> None:
        # Pass the list to a variable and add to the first index the header conserving the other values in the list
        rows: list[str] = list(values)
        rows.insert(0, header)
        self.__table_data.append(rows) # type: ignore


    # Returns the Normalized data for 'SimpleTable' class
    @override
    def create_structure(self) -> list[list[str]]:
        #Saves the normalized __data of table
        normalized_data: list[list[str]] = []
        #Saves the reoganiced list of table for their implementation
        reformatted_table: list[list[str]] = []
      
        #Check if none of the headers are empty
        if any(rows[0]!= "" for rows in self.__table_data ):
            
            #Turn all not str values inside each list into a str
            table_data_str: list[list[str]] = [[str(value) for value in row] for row in self.__table_data] # type: ignore
            
            for row in table_data_str:
                normalized:list[str] = row + [""] * (
                max(len(row) for row in table_data_str) - len(row))#Fill missing rows with blanks ''
                normalized_data.append(normalized)

                reformatted_table = list(map(list, zip(*normalized_data))) #Reformats this ["header1,1,2"], ["header2,3,4"] into this ["header1","header2"],[1,3],[2,4]
            
            #Saves the real size of the table in '__total__rows' and '__total_columns' variables
            self._total_rows=len(reformatted_table)
            self._total_columns=len(reformatted_table[0])
        
        else:
           #Change 'reformatted_table' data for [["Error"],["No header"]] and change the size of rows and cols for 1 x 2 table if and header is empty
           reformatted_table = [["Error"],["No header"]]
           self._total_rows,self._total_columns=2,1
        
        return reformatted_table
    
#This adapter is for SQLite data
class SQliteAdapter(Adapter):
    def __init__(self,db_dir:str="",query:str=""):
        super().__init__()
        self.__db_dir:str = db_dir
        self.__query:str = query

    #You can set the dir of the database using this funciton
    def set_database_dir(self,db_dir:str="")->None:
        self.__db_dir = db_dir

    #You can use this function to set a query of the data of specic request of the tables in db 
    def set_query(self,query:str=""):
        self.__query = query
    
    #Returns the results of query of the data
    @override
    def create_structure(self) -> list[list[str]]:
        query_data:list[list[str]]=[] #Declare a varible that gets the result of the query for the 'SimpleTable' class
        
        try:
            connector= sqlite3.connect(os.path.abspath(self.__db_dir))
            cursor:Cursor = connector.cursor()

            cursor.execute(self.__query)

            #Get the headers of the query table
            headers:list[str] = [header[0] for header in cursor.description]
            
            #Get requested table values
            rows:list[list[str]]= cursor.fetchall()

            #Add the headers and rows to 'query_data' list variable
            query_data.append(headers)
            query_data += [[str(value) for value in row] for row in rows]

            #Close the database connection
            cursor.close()
            
            #Set rows and cols size using the requested data as a reference
            self._total_rows = len(query_data)
            self._total_columns = len(query_data[0])
        except (OperationalError,TypeError):
            #Change 'query_data data' for [["Error"],["No query"]] and change the size of rows and cols for 1 x 2 table if and header is empty
            query_data=[["Error"],["No query"]]
            self._total_rows,self._total_columns=2,1

        return query_data

#<------------------------------------------------------------You can create your own adapters here----------------------------------------------->