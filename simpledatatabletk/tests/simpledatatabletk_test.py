import unittest
from unittest import TestCase
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from simpledatatabletk.utilities.adapters import Adapter, ManualAdapter, SQliteAdapter

#Test the adapters
class TestAdapters(TestCase):
    #Test if the 'ManualAdapter' can create an legible estructure for the class 'SimpleTable' with incomplete values
    def test_manual_ad_asymetic(self):

        test_table_adapter: Adapter = ManualAdapter() # type: ignore
        test_table_adapter.add("Nombre",["Manuel","Fernando","Susana","Beto"])
        test_table_adapter.add("Telefono",["7713212","77321321","77312321234","774324324325","77432432","7732432432","77432432432"])
        test_table_adapter.add("Edad",[20,24,50,12])
        test_table_adapter.add("Pais",["Mexico","España","Honduras"])

        compare_to:list[list[str]] =[ ["Nombre","Telefono","Edad","Pais"],
                                      ["Manuel","7713212","20", "Mexico"],
                                      ["Fernando","77321321","24", "España"],
                                      ["Susana","77312321234","50", "Honduras"],
                                      ["Beto","774324324325","12", ""],
                                      ["","77432432","", ""],
                                      ["","7732432432","", ""],
                                      ["","77432432432","", ""]

        ]
        
        table_structure:list[list[str]] =test_table_adapter.create_structure()

        rows,cols = test_table_adapter.get_size()
        
        assert (rows,cols)==(8,4) and table_structure == compare_to
    
    #Check if the normalization process do not doing anything to the data if is symetric
    def test_manual_ad_symetic(self):

        test_table_adapter: Adapter = ManualAdapter()
        test_table_adapter.add("Nombre",["Manuel","Fernando","Susana","Beto"])
        test_table_adapter.add("Telefono",["7713212","77321321","77312321234","774324324325"])
        test_table_adapter.add("Edad",[20,24,50,12])
        test_table_adapter.add("Pais",["Mexico","España","Honduras","Canada"])

        compare_to: list[list[str]] = [["Nombre","Telefono","Edad","Pais"],
                                       ["Manuel","7713212","20","Mexico"],
                                       ["Fernando","77321321","24","España"],
                                       ["Susana","77312321234","50","Honduras"],
                                       ["Beto","774324324325","12","Canada"]
                                       ]
        
        table_structure:list[list[str]]=test_table_adapter.create_structure()

        rows,cols = test_table_adapter.get_size()

        assert (rows,cols)==(5,4) and table_structure == compare_to
    
    #Check if the connection with database and the results are correct
    def test_sqlite_ad_with_correct_dir(self):

        test_table_adapter: Adapter = SQliteAdapter(db_dir="tests\\Testdb\\Base-de-pruebas.db",query="select * from personas")

        table_structure:list[list[str]] = test_table_adapter.create_structure()

        compare_to:list[list[str]]=[ ["id","nombre","edad","ciudad"],
                                     ["1","Juan","25","Ciudad de MÃ©xico"],
                                     ["2","Ana","30","Guadalajara"],
                                     ["3","Pedro","22","Monterrey"],
                                     ["4","LucÃ­a","28","Puebla"],
                                     ["5","Carlos","35","Tijuana"]
                                    ]

        assert table_structure != [["Error"],["No query"]] and table_structure == compare_to

    #Check if the algorithm throws expected errors if the direction of database is wrong
    def test_sqlite_ad_with_wrong_dir(self):

        test_table_adapter: Adapter = SQliteAdapter(db_dir="Test\\Testdb\\Base-de-pruebas.db",query="select * from personas")

        table_structure:list[list[str]] = test_table_adapter.create_structure()

        assert table_structure == [["Error"],["No query"]]

if __name__ == "__main__":
   unittest.main()

        