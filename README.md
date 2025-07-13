# simpledatatabletk

This package is designed to meet the needs of having a data table for both manually entering values ​​and obtaining them from databases. Since Tkinter doesn't have a table widget as such, I was forced to create my own to meet the needs of future projects related to CRUD programs and forms that require database connections.

```text
simpledatatabledtk/
├── test/
│   └── Testdb/
│       └── Base-de-pruebas.db
│       └── __init__.py
│       └── simpledatatabledtk_test.py
├── utilities/
│   └── __init__.py
│   └── adapters.py
└── __init__.py
└── datatable.py
```
## Installation
```text
pip install . #Local installation␣
pip install e . #Local installation in dev mode
```
##Implementantion examples

#Library declaration
```python
import tkinter as tk
from simpledatatabletk import Table #Import Table
from simpledatatabletk import Adapter,ManualAdapter,SQliteAdapter #Import Adapters for Table
```
```python
root = tk.Tk()

#ManualAdapter use
test_table_adapter: Adapter = ManualAdapter() #Declare ManualAdapter (Adapter object type)

#Add headers as a text chain and the data related to the header in the form of list
test_table_adapter.add("Nombre",["Manuel","Fernando","Susana","Beto"])
test_table_adapter.add("Telefono",["7713212","77321321","77312321234","774324324325","77432432","7732432432","77432432432"])
test_table_adapter.add("Edad",[20,24,50,12])
test_table_adapter.add("Pais",["Mexico","España","Honduras"])

tb = Table(root)
tb.create(adapter=test_table_adapter,limit-bounds=(10,10))
tb.pack(fill="both", expand=True) #<---- very importat if you want that the table shows itself

root.mainloop()
```
#Output
<img width="269" height="197" alt="image" src="https://github.com/user-attachments/assets/9917db31-66ff-4b18-8824-18a864eabb82" />

```python
#SQliteAdapter use
adpSQL = SQliteAdapter(db_dir="test\\Base-de-pruebas.db",query="you can use this too") #declare dir of the database
adpSQL.set_database_dir("<put your db dir here>") #<--- You can use this alternative to set de db dir too
adpSQL.set_query("select * from personas") #execute query
adpSQL.create_structure()

table.create(adapter=adpSQL,limit_bounds=(5,5))

table.pack(fill=tk.BOTH, expand=True)

root.mainloop()
```
#Output
<img width="265" height="144" alt="image" src="https://github.com/user-attachments/assets/687430b9-3c75-493c-b586-dc1a8026ef2e" />





