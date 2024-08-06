# Imports
import os
import tkinter as tk
from entry import *
from tkinter import filedialog
from PIL import ImageTk, Image

# Initialization
root = tk.Tk()
root.title("FileFanner")
root.resizable(False, False)

root_path = ""
root_entries = []

def run_program() -> None:
    """
    Begins the program.

    Parameters
    ----------
    none
    
    Returns
    -------
    none
    
    """
    global root_path
    root_path = filedialog.askdirectory()

    if root_path:
        l_filename.config(text=root_path)

        global root_entries
        root_entries = get_entries_in_path(root_path)
        arrange_entries()    

def arrangeby_display(entries: list[EntryObject]) -> list:
    """
    Filters entries based on the Display value.

    Parameters
    ----------
    entries: list[EntryObject]
        List of EntryObjects to be filtered.

    Returns
    -------
    entry_list: list[tuples]
        List of tuples representing entry properties; passed into arrangeby_sort()
        
    """

    # If Display is set to "Folders", only include folders.
    # If Display is set to "Files", only include files.
    # No change otherwise.
    filtered_entries = []
    display_state = display_choice.get()
    if display_state == "Folders":
        for e in entries:
            if e.get_type() == "Folder":
                filtered_entries.append(e)
    elif display_state == "Files":
        for e in entries:
            if e.get_type() != "Folder":
                filtered_entries.append(e)
    else:
        filtered_entries = entries

    # Creates list of tuples representing relevant properties of the EntryObjects.
    # Makes displaying each item in the frame easier by allowing iteration.
    entry_list = []
    for e in filtered_entries:
        entry_item = (e.get_name(),
                      e.get_type(), 
                      e.get_groupedsize(),
                      e.get_size_group(),
                      e.get_bytesize()
                      )
        entry_list.append(entry_item)

    return entry_list

def arrangeby_sort(entry_tuples: list):
    """
    Sorts entries in place based on the Sort Choice and Sort Order values.

    Parameters
    ----------
    entry_tuples: list[tuple]
        List of tuples representing entry properties to be sorted.

    Returns
    -------
    entry_tuples: list[tuple]
        The same, sorted list of tuples
    
    """

    # If Sort Choice is set to "Type", sort tuples by their type property.
    # If Sort Choice is set to "Size", sort tuples by their bytesize property.
    # If sort Choice is set to "Name", sort tuples by their name property.
    sort_choice_state = sort_choice.get()
    sort_order_state = sort_order.get()
    reverse_type = -1
    if sort_choice_state == "Type":
        entry_tuples.sort(key = lambda x: x[1])
        reverse_type = 1
    elif sort_choice_state == "Size":
        entry_tuples.sort(key = lambda x: x[4])
        reverse_type = 4
    else:
        entry_tuples.sort(key = lambda x: x[0])
        reverse_type = 0

    # If Sort Order is set to "Ascending", reverse the list with Sort Choice as the key.
    if sort_order_state == "Ascending":
        entry_tuples.sort(reverse = True, key = lambda x: x[reverse_type])

    return entry_tuples

def arrange_entries():
    """
    A wrapper function that handles sorting and displaying entries.

    Parameters
    ----------
    none

    Returns
    -------
    none
    
    """

    # Filter root entries through sorting algorithms, then display them in the frame.
    new_tuples = arrangeby_display(root_entries)
    new_list = arrangeby_sort(new_tuples)
    display_entries(new_list)

# Select File button
b_selectfile = tk.Button(root, 
                         text="Select Folder",
                         bg="khaki",
                         command=run_program
                         )
b_selectfile.grid(row=0, 
                  column=0, 
                  padx=10, 
                  pady=10
                  )

# Filename label
l_filename = tk.Label(root, 
                      text=":(No file)",  
                      anchor="w", 
                      relief="groove"
                      )
l_filename.grid(row=0, 
                column=1, 
                padx=10, 
                pady=10
                )

# Display dropdown
display_options = [
    "Files",
    "Folders",
    "Both"
]
display_choice = tk.StringVar()
display_choice.set(display_options[2])

l_display = tk.Label(root, text="Display:"
                     ).grid(row=0, column=2)
d_display = tk.OptionMenu(root, display_choice, *display_options,
                          ).grid(row=0, column=3)

# Sort dropdown
sort_type_options = [
    "Name",
    "Type",
    "Size"
]
sort_order_options = [
    "Ascending",
    "Descending"
]

sort_choice = tk.StringVar()
sort_choice.set(sort_type_options[0])

sort_order = tk.StringVar()
sort_order.set(sort_order_options[1])

l_sort = tk.Label(root, text="Sort:"
                  ).grid(row=0, column=4, padx=(10, 0))
d_sort = tk.OptionMenu(root, sort_choice, *sort_type_options,
                       ).grid(row=0, column=5, padx=(0, 10))

# Sort Order buttons
b_sort_order_down = tk.Button(root, text="v",
                              command=lambda:set_sort_order(1),
                              state='disabled')
b_sort_order_up = tk.Button(root, text="^",
                            command=lambda:set_sort_order(0)
                            )
b_sort_order_down.grid(row=0, column=6)
b_sort_order_up.grid(row=0, column=7, padx=(0, 10))



def set_sort_order(order: int):
    """
    Enables/disables the Sort Order buttons depending on which one is selected.

    Parameters
    ----------
    order: int
        The value representing the state of the sort order.

    Returns
    -------
    none
    
    """

    # If "Ascending" button is clicked, disable it and enable the "Descending" button.
    # Vice versa.
    sort_order.set(sort_order_options[order])
    if sort_order.get() == sort_order_options[0]:
        b_sort_order_up.config(state="disabled")
        b_sort_order_down.config(state="active")
    else:
        b_sort_order_up.config(state="active")
        b_sort_order_down.config(state="disabled")

def divert_to_arrangement(*args):
    """
    A wrapper function that calls arrange_entries() from each sorting variable's observer.
    (Can likely be optimized; only exists because variables passed by trace.add() make it
    difficult to call arrange_entries(), which takes no arguments.)

    Parameters
    ----------
    *args
        arguments passed from trace.add()

    Returns
    -------
    none
    
    """
    arrange_entries()

# Add observers to Sort variables
display_choice.trace_add("write", divert_to_arrangement)
sort_choice.trace_add("write", divert_to_arrangement)
sort_order.trace_add("write", divert_to_arrangement)

# Item frame
f_items = tk.LabelFrame(root, text="Items")
f_items.grid(row=1, column=0, columnspan=8, padx=10, pady=10, sticky="we")

l_defaultitem = tk.Label(f_items, text="Select a folder to display its contents.")
l_defaultitem.grid(row=1, column=0)

# Configure frame grid
for i in range(3):
    tk.Grid.columnconfigure(f_items, i, weight=1)



def clear_frame(frame: tk.LabelFrame) -> None:
    """
    Destroys all Widgets inside the Frame.

    Parameters
    ----------
    frame: tk.LabelFrame Widget
        The Frame to clear of all its Widgets.
    
    Returns
    -------
    none

    """
    for widget in frame.winfo_children():
        widget.destroy()

def get_entries_in_path(path):
    """
    Creates a list of EntryObjects from a path containing files.

    Parameters
    ----------
    path: str
        The path containing files.

    Returns
    -------
    entry_list: list[EntryObject]
        A list containing EntryObjects.
        
    """

    # Make each DirEntry into an EntryObject.
    entry_list = []
    for direntry in os.scandir(path):
        entry = make_entry_object(direntry)
        entry_list.append(entry)
    return entry_list

def display_entries(entry_tuples: list[tuple]) -> None:
    """
    Places Labels representing files in the path into the Frame.
    Also updates the Label representing the chosen directory.

    Parameters
    ----------
    path: str
        String representing a file path.
    
    Returns
    -------
    none

    """
    clear_frame(f_items)
    
    anchor_list = ["w", "center", "e", "w"]
    color_list = ["white", "light grey"]

    # Displays Labels of each property of each item.
    # Alternates bg color of labels.
    for i in range(len(entry_tuples)):
        for j in range(4):
            l_entry = tk.Label(f_items,
                               text=f"{entry_tuples[i][j]}",
                               anchor=anchor_list[j],
                               bg=color_list[i % 2]
                               )
            l_entry.grid(row=i, column=j, sticky="we")
  
def make_entry_object(direntry: os.DirEntry) -> EntryObject:
    '''
    Returns an EntryObject object from a DirEntry object.
    
    Parameters
    ----------
    direntry: os.DirEntry object
        The DirEntry to turn into an EntryObject.
    
    Returns
    -------
    EntryObject
        The EntryObject modeled after the DirEntry.

    '''
    size = 2
    type = ""

    # If file, type becomes its extension + "File". If directory, type becomes "Folder".
    if direntry.is_file():
        size = direntry.stat().st_size
        type = f"{os.path.splitext(direntry.name)[1].upper().strip(".")} File"
    elif direntry.is_dir():
        size = get_dir_size(direntry.path)
        type = "Folder"

    return EntryObject(direntry.name, size, type)

def get_dir_size(main_path: str) -> int:
    """
    Returns total size of the directory in bytes.
    
    Parameters
    ----------
    main_path: str
        The path of the directory whose size to calculate.
        
    Returns
    -------
    total_size: int
        The total size of the directory in bytes.
        
    """
    total_size = 0

    # If file, adds its size to total. If folder, recurs into that folder
    for dir in os.scandir(main_path):
        if dir.is_file():
            total_size += dir.stat().st_size
        elif dir.is_dir():
            total_size += get_dir_size(dir.path)
    return total_size

root.mainloop()
