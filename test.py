import tkinter as tk

from simpledatatabletk import Table
from simpledatatabletk.utilities.adapters import SQliteAdapter, Adapter, ManualAdapter


root = tk.Tk()

test_table_adapter: Adapter = ManualAdapter() # type: ignore
test_table_adapter.add("Nombre",["Manuel","Fernando","Susana","Beto"])
test_table_adapter.add("Telefono",["7713212","77321321","77312321234","774324324325","77432432","7732432432","77432432432"])
test_table_adapter.add("Edad",[20,24,50,12])
test_table_adapter.add("Pais",["Mexico","España","Honduras"])

tb = Table(root)
tb.create(test_table_adapter,(10,10))
tb.pack(fill="both", expand=True)

root.mainloop()