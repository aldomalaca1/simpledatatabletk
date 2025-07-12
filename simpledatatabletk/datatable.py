from tkinter import Frame
from tkinter import Scrollbar
from tkinter import Entry
from tkinter import END
from tkinter import Tk
from typing import Callable
from typing import Optional
from typing import Any
from tkinter import Event
from functools import partial
from .utilities.adapters import Adapter

class Table(Frame):
    
    def __init__(self, parent: Tk):  # type: ignore
        super().__init__(parent)
 
       # Declare total rows and columns variables that saves de real size of the table
        self.__total_rows, self.__total_cols = 0,0

        #Saves the visible aspect of the table
        self.__visible_rows: int = 0
        self.__visible_columns: int = 0

        #Set variable for table data
        self.__data:list[list[str]] = []

        # Set the initial position of the table both horizontally and vertically
        self.start_point_h, self.start_point_v = 0, 0

        # Declare grid container object
        self.__grid_frame: Frame = NotImplemented
       

        self.__entries: list[list[Entry]] = [] #List that stores the Entry rows in RAM as lists

        #------------------------------------------Scroll bars------------------------------------------------------------------
    
        # Set Scrollbars
      
        self.__v_scroll: Scrollbar = NotImplemented
        self.__h_scroll: Scrollbar = NotImplemented


    #Init vars to facilitate the refresh __data values
    def __init_vars(self, adapter:Adapter, limit_bounds:tuple[int,int]=(0,0)):
        
        #Delete the current list of entries to prevent that new entries can break the program if the function is reutilized
        self.__entries = []

        #Get the __data of table from TableStructure object
        self.__data = adapter.create_structure()

        # Set grid container object
        self.__grid_frame: Frame = Frame(self)
        self.__grid_frame.grid(row=0, column=0, sticky="nsew")

        #------------------------------------------Scroll bars configuration------------------------------------------------------------------
    
        # Set Scrollbars
        __on_vscroll: Callable[..., None] = self.__on_vscroll
        self.__v_scroll: Scrollbar = Scrollbar(
            self, orient="vertical", command=__on_vscroll
        )
        self.__v_scroll.grid(row=0, column=1, sticky="ns")

        __on_hscroll: Callable[..., None] = self.__on_hscroll
        self.__h_scroll: Scrollbar = Scrollbar(
            self, orient="horizontal", command=__on_hscroll
        )
        self.__h_scroll.grid(row=1, column=0, sticky="we")

        # Get table size from TableStructure
        self.__total_rows, self.__total_cols = adapter.get_size()


        #Saves the visible aspect of the table
        self.__visible_rows: int = (
            self.__total_rows if self.__total_rows < limit_bounds[0] else limit_bounds[0]
        )
        self.__visible_columns: int = (
            self.__total_cols if self.__total_cols < limit_bounds[1] else limit_bounds[1]
        )

        # Variables that targets the headers or rows
        self.target_headers: tuple[int, int] = (-1, 1)
        self.target_rows: tuple[int, int] = (0, self.__visible_rows)

        #Set maximum scrolling values
        max_v_value: int = int(self.__visible_rows / self.__total_rows)
        max_h_value: int = int(self.__visible_columns / self.__total_cols)
        self.__v_scroll.set(0, max_v_value)
        self.__h_scroll.set(0, max_h_value)


    #Create the entris and set into it the values of the table
    def create(self, adapter:Adapter, limit_bounds:tuple[int,int]=(0,0))->None:
        self.__init_vars(adapter=adapter,limit_bounds=limit_bounds)

        for row in range(self.__visible_rows):
            row_entries: list[Entry] = []
            for column in range(self.__visible_columns):
                entry: Entry = Entry(self.__grid_frame, width=10, justify="center")
                entry.grid(row=row, column=column)
                if row > 0:
                    #Enable the event '<KeyRealease>' to change the __data of table when the user writes over the entries
                    entry.bind(
                        "<KeyRelease>",
                        lambda e, row=row, col=column: self.change_data_from_table(
                            row, col
                        ),
                    )
                row_entries.append(entry)
            self.__entries.append(row_entries)
        
         #Set maximum scrolling values
        max_v_value: int = int(self.__visible_rows / self.__total_rows)
        max_h_value: int = int(self.__visible_columns / self.__total_cols)
        self.__v_scroll.set(0, max_v_value)
        self.__h_scroll.set(0, max_h_value)

        #Fill the table with values
        self.update_rows()


    #Updates the entry values ​​within the headers table, giving the illusion of headers scrolling
    def update_headers(self) -> None:
        for column in range(self.__visible_columns):
            calibrated_column: int = self.start_point_v + column #Calculate the real column position of the __data
            entry = self.__entries[0][column] #Only loops inside __data in index 0 that is simulating the headers
            if calibrated_column < self.__total_cols:
                entry.delete(0, END) #Delete the content of the headers so that when the content is updated it does not overwrite the visual part of the table headers
                entry.insert(0, str(self.__data[0][calibrated_column]))
                entry.bind("<Key>", lambda e: "break") #Cancels the '<key>' event so that the user cannot edit the headers
            else:
                entry.delete(0, END)

    #Updates the entry values ​​within the table, giving the illusion of table scrolling.
    def update_rows(self) -> None:
        self.update_headers()

        for row in range(1, self.__visible_rows):
            value_row: int = self.start_point_h + row
            if value_row == 0: #Ingores the headers area
                continue
            for column in range(self.__visible_columns):
                value_column: int = self.start_point_v + column
                entry = self.__entries[row][column]
                if value_row < self.__total_rows and value_column < self.__total_cols:
                    entry.delete(0, END) #Any entry is deleted to prevent indiscriminate concatenation of __data
                    entry.insert(0, str(self.__data[value_row][value_column]))
                else:
                    entry.delete(0, END)

        # Update scroll bars
        calibrate_scroll_h: tuple[float, float] = (
            (self.start_point_h / self.__total_rows),
            ((self.start_point_h + self.__visible_rows) / self.__total_rows),
        )
        self.__v_scroll.set(calibrate_scroll_h[0], calibrate_scroll_h[1])

        calibrate_scroll_v: tuple[float, float] = (
            (self.start_point_v / self.__total_cols),
            ((self.start_point_v + self.__visible_columns) / self.__total_cols),
        )
        self.__h_scroll.set(calibrate_scroll_v[0], calibrate_scroll_v[1])


    #----------------------------------Table configuration fucntions------------------------------------------------------
    
    def __target_grid_area(self,area:str="headers")->tuple[int,int]:
        target:dict[str,tuple[int,int]]={"headers":(-1,1),"rows":(0, self.__visible_rows)}
        return target[area]

    #Table visual configuration
    def visual_conf(self, target_area: str, **conf: Any) -> None:
        target = self.__target_grid_area(area=target_area)
        for entries_list in self.__entries:
            for entry in entries_list:
                row: int = entry.grid_info()["row"]
                if row > target[0] and row < target[1]:
                   entry.configure(**conf)

    #Disable or re-enable the capability of the table to alow writing
    def read_only(self, state: bool = True)->None:
        target = self.__target_grid_area(area="rows")
        for entries_list in self.__entries:
            for entry in entries_list:
                row: int = entry.grid_info()["row"]
                if (row > target[0] and row < target[1]) and state:
                    entry.bind("<Key>", lambda e: "break") #Cancels the '<Key>' event to prevent writing
                    entry.bind("<KeyRelease>", lambda e: "break") #Cancels the '<KeyRealease>' event as a extra preventive measure

    #Specifies an event externally to trigger a function outside the table code
    def set_event(self,event: str = "<Return>",target_f: Optional[Callable[[Any], Any]] = None,**parameters: Any):

        #Create an internal function using Partial to be able to send self-referencing to the 'SimpleTable' object so that it can be accessed externally
        handler: Optional[Callable[..., Any]] = (
            partial(target_f, self, **parameters) if target_f else None
        )

        target = self.__target_grid_area("rows")
        for entries_list in self.__entries:
            for entry in entries_list:
                row:int = entry.grid_info()["row"]
                if row > target[0] and row < target[1]:
                   entry.bind(event, handler)
        
    #Change the __data inside '__data' variable that collects the values of the table synchronizing with the change of values ​​of the virtualized table
    def change_data_from_table(self, row: int, column: int) -> None:
        #Ignore the headers
        if row == 0:
            return

        #Calculate the real rows and cols index of the __data in table
        calibrate_row: int = self.start_point_h + row
        calibrate_column: int = self.start_point_v + column

        #Check if current rows and cols indexes not exceeds the real size (no virtual size) of table
        if calibrate_row < self.__total_rows and calibrate_column < self.__total_cols:
            value: str = self.__entries[row][column].get()
            self.__data[calibrate_row][calibrate_column] = value

    
    def _on_entry_edit(self, event: Event, row: int, col: int)->None:
        self.change_data_from_table(row, col)
    
    #--------------------------------------------------------Scrolling functions -----------------------------------------------------------------------
    
    #Update the logic table when the vertical scroll is moved
    def __on_vscroll(self, *args: str) -> None:
        if args[0] == "moveto":
            fractional_position: float = float(args[1]) #Absolute fractional position
            self.start_point_h = int(fractional_position * self.__total_rows) #Updates the starting point of the rows when the horizontal bar is moved
        elif args[0] == "scroll":
            step: int = int(args[1]) #Relative displacement
            self.start_point_h = max(
                0, min(self.start_point_h + step, self.__total_rows - self.__visible_rows)
            )
        self.update_rows()

    #Update the logic table when the horizontal scroll is moved
    def __on_hscroll(self, *args: str) -> None:
        if args[0] == "moveto":
            fraction: float = float(args[1])
            self.start_point_v = int(fraction * self.__total_cols)
        elif args[0] == "scroll":
            step: int = int(args[1])
            self.start_point_v = max(
                0, min(self.start_point_v + step, self.__total_cols - self.__visible_columns) #Updates the starting point of the cols when the vertical bar is moved
            )
        self.update_rows()

#--------------------------------------- Functions related with __data ----------------------------------------------------------------

    def get_values(self,target_headers:list[str]=[])-> dict[str,list[str]]:
        #Declaring a variable to save the values of table by key='header',rows=[0,1,2,3]
        values:dict[str,list[str]] = {}
        
        #Reorganize this ['header1','header2','header3'], [1,3,5],[2,4,6] into this [1,2],[3,4],[5,6]
        reformatted_in_columns:list[list[str]]=list(map(list, zip(*self.__data)))
        #Get the first element [header][index=0] of the each lists
        headers:list[str] = [header[0] for header in reformatted_in_columns]
        #Saves into the variable all headers in headers list if headers in 'target_headers' is empty or do not intersect with 'headers' list in other case gets the intersected headers
        intersected_headers:list[str] = headers if target_headers is  [] or  not(set(target_headers) & set(headers)) else list(set(target_headers) & set(headers))

    
        for column, header in enumerate(headers):
                if  header in intersected_headers: #If the header intersect with the list of 'intersected_headers' exsecute the nex line
                    values[header] = reformatted_in_columns[column][1:]#Saves the header as a key and the values of list except the first element of each one

        return values
