# Imports
import os
import tkinter as tk
from entry import *
from tkinter import filedialog
from PIL import ImageTk, Image

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

    if sort_order_state == "Ascending":
        entry_tuples.sort(reverse = True, key = lambda x: x[reverse_type])

    return entry_tuples

def arrange_entries():
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
    sort_order.set(sort_order_options[order])
    if sort_order.get() == sort_order_options[0]:
        b_sort_order_up.config(state="disabled")
        b_sort_order_down.config(state="active")
    else:
        b_sort_order_up.config(state="active")
        b_sort_order_down.config(state="disabled")

# Detect Options funcitonality
def divert_to_arrangement(*args):
    arrange_entries()

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

    for i in range(len(entry_tuples)):
        for j in range(4):
            l_entry = tk.Label(f_items,
                               text=f"{entry_tuples[i][j]}",
                               anchor=anchor_list[j],
                               bg=color_list[i % 2]
                               )
            l_entry.grid(row=i, column=j, sticky="we")
    # for e in entry_tuples:
    #     for i in range(4):
    #         new_label = tk.Label(f_items, 
    #                              text=f"{entry_tuples[i]}", 
    #                              anchor=anchor_list[i], 
    #                              bg=color_list[entry_num % 2]
    #                              )
    #         new_label.grid(row=entry_num, 
    #                        column=i, 
    #                        sticky="we"
    #                        )
    #     entry_num += 1





    # for direntry in os.scandir(path):
    #     entry = make_entry_object(direntry)
    #     entry_tuple = (entry.get_name(),
    #                    entry.get_type(), 
    #                    entry.get_size(),
    #                    entry.get_size_group()
    #                    )
    #     anchor_list = ["w", "center", "e", "w"]
    #     color_list = ["white", "light grey"]
    #     for i in range(4):
    #         new_label = tk.Label(f_items, 
    #                              text=f"{entry_tuple[i]}", 
    #                              anchor=anchor_list[i], 
    #                              bg=color_list[entry_num % 2]
    #                              )
    #         new_label.grid(row=entry_num, 
    #                        column=i, 
    #                        sticky="we"
    #                        )
    #     entry_num += 1
  
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

    if direntry.is_file():
        size = direntry.stat().st_size
        type = f"{os.path.splitext(direntry.name)[1].upper().strip(".")} File"
    elif direntry.is_dir():
        size = get_dir_size(direntry.path)
        type = "Folder"

    return EntryObject(direntry.name, size, type)

# Gets combined size of all files in the directory
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

# class FileFanner:

#     def __init__(self, root):
#         self.root = root
#         self.root_path = ""
        
#     def set_root_path(self) -> None:
#         '''
#         Selects the root folder in which to look
#         :return: None
#         '''
#         self.root_path = filedialog.askdirectory()
#         print(self.root_path)        

#     def update_select_file_button(self) -> None:
#         b_select_file = tk.Button(
#             self.root, 
#             text="Select Folder",
#             command=self.set_root_path
#             )
#         b_select_file.grid(
#             row=0, 
#             column=0,)
    
#     def update_labels(self, direntry) -> None:
#         tk.Label(self.root, text=f"{direntry.name}").pack()


# def main():

#     root = tk.Tk()
#     root.title("FileFanner")
#     root.geometry("800x600")
    
#     app = FileFanner(root)
#     app.update_select_file_button()

#     while app.root_path:
#         print("Got path")
#         direntry_list = os.scandir(app.root_path)
#         for direntry in direntry_list:
#             print(direntry)
#             app.update_label(direntry)

#     root.mainloop()

# if __name__ == "__main__":
#     main()
    
# Include dropdown
# include_options = [
#     "This folder",
#     "This folder + All subfolders"
# ]
# include_choice = tk.StringVar()
# include_choice.set(include_options[0])

# l_include = tk.Label(root, text="   Include:"
#                      ).grid(row=0, column=2, padx=(10, 0))
# d_include = tk.OptionMenu(root, include_choice, *include_options,
#                           ).grid(row=0, column=3)