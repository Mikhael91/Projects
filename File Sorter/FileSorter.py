# Import modules
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import csv
import threading
import re


# Inserts sorting list to dictionary
def insert_list():
    with open("SortingList.txt") as csv_file:
        new_list = []
        file_read = csv.reader(csv_file, delimiter="-")
        try:
            for lines in file_read:
                new_list.append([lines[0], lines[1], lines[2]])
        except IndexError:
            pass
    return new_list


# Writes a file containing dictionary keys, values, and extensions
def write_file(final_list):
    with open("SortingList.txt", "w", newline="") as csv_file:
        file_write = csv.writer(csv_file, delimiter="-")
        for keys, destination, extension in final_list:
            file_write.writerow([keys, destination, extension])


# Adding the sort dictionary
def add_sort():

    # Browse file destination
    def browse_dir():
        move_dir = filedialog.askdirectory(initialdir=r"C:\Users\User\Desktop")
        if move_dir:
            file_dir_entry.config(state=NORMAL)
            file_dir_entry.delete(0, END)
            file_dir_entry.insert(0, move_dir)
            file_dir_entry.config(state=DISABLED)

    # Adding Key and folder location to dictionary
    def add_list():
        if key_entry.get() == "":
            messagebox.showwarning(title="Error", message="You must input a key")
        elif file_dir_entry.get() == "File Destination":
            messagebox.showwarning(title="Error", message="You must insert a file destination")
        elif [key_entry.get(), file_dir_entry.get(), extension_var.get()] in sort_list:
            messagebox.showwarning(title="Error", message="Key, Direction, and Extension already saved")
        else:
            for index, saved in enumerate(sort_list):

                # If Key has been saved with "All files" as extension
                if saved[0] == key_entry.get() and saved[2] == "All files":
                    messagebox.showwarning(title="Warning", message="This key has been saved with the extension\n"
                                                                    "'All files'")
                    return

                # If key has been saved with another extension and the same key is added with "All files" as extension
                if saved[0] == key_entry.get() and saved[2] != "All files" and extension_var.get() == "All files":
                    messagebox.showwarning(title="Warning", message="Key has been saved with another extension\n"
                                                                    "Cannot add 'All files' as an extension")
                    return

                # If a duplicate key and extension is found in the sort list
                if saved[0] == key_entry.get() and saved[2] == extension_var.get():
                    if messagebox.askyesno(title="Warning",
                                           message="Key and extension is registered to another folder\n"
                                                   "Do you want to change?", icon="warning"):
                        sort_list.insert(index, [key_entry.get(), file_dir_entry.get(), extension_var.get()])
                        sort_list.pop(index)
                        messagebox.showinfo(title="Info",
                                            message=f"Keyword: {key_entry.get()}\nDestination: {file_dir_entry.get()}\n"
                                                    f"Extension: {extension_var.get()}\nHas been changed")
                        return
                    else:
                        return

            # Adds sort list
            sort_list.append([key_entry.get(), file_dir_entry.get(), extension_var.get()])
            messagebox.showinfo(title="Info",
                                message=f"Keyword: {key_entry.get()}\nDestination: {file_dir_entry.get()}\n"
                                        f"Extension: {extension_var.get()}\nHas been added")

    # Manage window
    manage_window = Toplevel()
    manage_window.title("Manage Sorting")
    manage_window.geometry(f"{NEW_WIDTH}x{NEW_HEIGHT}+{x}+{y}")
    manage_window.resizable(False, False)

    # Configure columns
    manage_window.columnconfigure(0, weight=1)
    manage_window.columnconfigure(1, weight=5)
    manage_window.columnconfigure(2, weight=1)

    # Lists of extensions
    extension_var = StringVar()
    extension_list = ('All files', '264', '3dm', '3ds', '3g2', '3ga', '3gp', '3gpp', '4mp', '7z', '8bi', 'aa', 'aac',
                      'aae', 'aax', 'accdb', 'ace', 'acsm', 'act', 'adoc', 'adpcm', 'adt', 'aep', 'afpub', 'ai', 'aif',
                      'aifc', 'aiff', 'aimppl', 'air', 'amr', 'amv', 'ani', 'apa', 'ape', 'api', 'apk', 'apnx', 'app',
                      'approj', 'arf', 'art', 'arw', 'asc', 'asf', 'asm', 'asp', 'aspx', 'ass', 'asw', 'asx', 'au',
                      'aup', 'avi', 'avif', 'awb', 'azw', 'azw3', 'b', 'bak', 'bas', 'bashrc', 'bat', 'bbl', 'bet',
                      'bfc', 'bib', 'bibtex', 'bik', 'bin', 'bluej', 'bmp', 'bok', 'braw', 'bud', 'bup', 'bz2', 'c',
                      'cab', 'caf', 'caj', 'camproj', 'camrec', 'cat', 'cbl', 'cbr', 'cbt', 'cbz', 'ccc', 'cd', 'cda',
                      'cdo', 'cdr', 'cdt', 'ced', 'cel', 'cer', 'cff', 'cfg', 'cfm', 'cfml', 'cgi', 'chm', 'class',
                      'clp', 'cma', 'cmd', 'cmf', 'cmproj', 'cmrec', 'cod', 'com', 'cpi', 'cpl', 'cpp', 'cr2',
                      'crdownload', 'crw', 'crx', 'crypt', 'cs', 'csk', 'csr', 'css', 'csv', 'cue', 'cur', 'cvs', 'd',
                      'dao', 'dat', 'dav', 'db', 'dbf', 'dbx', 'dcm', 'dd', 'dds', 'deb', 'def', 'dem', 'deskthemepack',
                      'dev', 'dic', 'dif', 'dir', 'dit', 'divx', 'djvu', 'dll', 'dmg', 'dmp', 'dng', 'do', 'doc',
                      'docm', 'docx', 'dot', 'dotx', 'drv', 'ds', 'dtd', 'dtp', 'dun', 'dvd', 'dvsd', 'dwg', 'dxf',
                      'ebd', 'eddx', 'efx', 'emf', 'eml', 'emz', 'enc', 'enl', 'ens', 'enw', 'epc', 'eps', 'epub',
                      'erb', 'esp3', 'exe', 'exr', 'f4v', 'fb2', 'fcpevent', 'fdxt', 'ffl', 'ffo', 'fla', 'flac',
                      'flif', 'flipchart', 'flo', 'flp', 'flt', 'flv', 'fm3', 'fnt', 'fon', 'fota', 'fpx', 'fsproj',
                      'fxc', 'g64', 'gadget', 'gam', 'gbr', 'gcw', 'ged', 'gho', 'gid', 'gif', 'gms', 'gpx', 'grp',
                      'gsm', 'gvdesign', 'gz', 'gzip', 'h', 'h264', 'hdmp', 'hdr', 'heic', 'hex', 'hht', 'hiv', 'hlp',
                      'hpp', 'hqx', 'ht', 'htm', 'html', 'htt', 'hwp', 'i5z', 'ibooks', 'icl', 'icm', 'icns', 'ico',
                      'iconpackage', 'ics', 'idx', 'iff', 'ifo', 'img', 'imoviemobile', 'indd', 'inf', 'ini', 'ion',
                      'ip', 'ipa', 'iptheme', 'ise', 'iso', 'ithmb', 'itl', 'iwb', 'jad', 'jar', 'java', 'jp2', 'jpeg',
                      'jpg', 'js', 'json', 'jsp', 'jxr', 'kar', 'kdc', 'key', 'keychain', 'kfx', 'kml', 'kmz', 'koz',
                      'kv', 'lbl', 'lit', 'lnk', 'log', 'lrf', 'lua', 'm', 'm2ts', 'm3u', 'm3u8', 'm4', 'm4a', 'm4b',
                      'm4p', 'm4r', 'm4v', 'mac', 'map', 'marc', 'max', 'mbp', 'md', 'mdb', 'mdf', 'mdi', 'mdmp',
                      'mepx', 'mht', 'mhtml', 'mid', 'midi', 'mim', 'mime', 'mind', 'mix', 'mkv', 'mlc', 'mmf', 'mobi',
                      'mod', 'modd', 'mov', 'mp2', 'mp3', 'mp4', 'mpa', 'mpc', 'mpeg', 'mpg', 'mpga', 'mpkg', 'mproj',
                      'mrc', 'mse', 'msg', 'msi', 'mswmm', 'mtb', 'mts', 'mtw', 'mui', 'mxf', 'nb0', 'nef', 'nes',
                      'nfa', 'nfi', 'nfo', 'nfs', 'nfv', 'nib', 'nrw', 'nt', 'numbers', 'nzb', 'o', 'obj', 'odg', 'odm',
                      'odp', 'ods', 'odt', 'oga', 'ogg', 'ogv', 'oma', 'one', 'opf', 'opis', 'orf', 'ori', 'osp', 'otf',
                      'otg', 'ova', 'ovf', 'owl', 'oxps', 'p', 'p65', 'pages', 'part', 'pas', 'pb', 'pbj', 'pbxuser',
                      'pcd', 'pck', 'pct', 'pcx', 'pd', 'pdb', 'pdf', 'pds', 'pef', 'pes', 'pgm', 'php', 'pict',
                      'pictclipping', 'pif', 'pika', 'pkg', 'pl', 'plist', 'plugin', 'pmd', 'pnf', 'png', 'pol', 'pps',
                      'ppsx', 'ppt', 'pptm', 'pptx', 'prc', 'prf', 'prop', 'ps', 'psd', 'pspimage', 'pub', 'pup', 'pwn',
                      'py', 'pyw', 'pz', 'qb2011', 'qcp', 'qpr', 'qt', 'quickendata', 'qvm', 'qxd', 'qxp', 'r01', 'ra',
                      'raf', 'ram', 'rar', 'raw', 'rc', 'rcproject', 'rdf', 'reg', 'rels', 'rem', 'resources', 'ris',
                      'rm', 'rmvb', 'rom', 'rpm', 'rss', 'rta', 'rte', 'rtf', 'rvt', 'rwl', 's19', 'sav', 'sb', 'sb2',
                      'scr', 'sdf', 'sdt', 'sfw', 'sh', 'shs', 'sit', 'sitx', 'sln', 'sma', 'snb', 'sql', 'sr2', 'srt',
                      'ss', 'std', 'stp', 'suo', 'svg', 'svgz', 'swf', 'swift', 'sxw', 'sys', 't65', 'tar', 'tax',
                      'tax2012', 'tax2014', 'tax2016', 'tbz', 'tcr', 'tec', 'tex', 'tga', 'tgz', 'thm', 'thp', 'tif',
                      'tiff', 'tmp', 'toast', 'torrent', 'trec', 'trx', 'ts', 'tscproj', 'ttf', 'tvs', 'txt', 'url',
                      'uue', 'vb', 'vbk', 'vbp', 'vbproj', 'vbx', 'vc', 'vcd', 'vcf', 'vcs', 'vcxproj', 'veg', 'vep',
                      'vmg', 'vnt', 'vob', 'vpj', 'vproj', 'vqf', 'vro', 'vsd', 'wav', 'wbmp', 'webarchive', 'webloc',
                      'webm', 'webp', 'wk3', 'wks', 'wlmp', 'wma', 'wmf', 'wmv', 'wp5', 'wpd', 'wpg', 'wps', 'wsf',
                      'wwp', 'xap', 'xcf', 'xcodeproj', 'xesc', 'xfdl', 'xhtml', 'xib', 'xll', 'xlr', 'xls', 'xlsb',
                      'xlsm', 'xlsx', 'xmind', 'xml', 'xps', 'xq', 'xspf', 'xt', 'yml', 'yuv', 'zip', 'zipx')
    extension_var.set(extension_list[0])

    # Labels, Entries, ComboBox, and buttons
    sort_label = Label(manage_window, text="Add Sorting", height=2, font=("Arial", 20))
    sort_label.grid(row=0, column=0, columnspan=3)

    key_label = Label(manage_window, text="File Key :", font=("Arial", 10))
    key_label.grid(row=1, column=0)

    key_entry = Entry(manage_window, font=("Arial", 15))
    key_entry.grid(row=1, column=1, sticky=W + E)

    file_dir_label = Label(manage_window, text="Move file to :", font=("Arial", 10))
    file_dir_label.grid(row=2, column=0)

    file_dir_entry = Entry(manage_window, font=("Arial", 15))
    file_dir_entry.grid(row=2, column=1, sticky=W + E)
    file_dir_entry.insert(0, "File Destination")
    file_dir_entry.config(state=DISABLED)

    browse_button = Button(manage_window, text="Browse", command=browse_dir)
    browse_button.grid(row=2, column=2, sticky=W)

    file_extension_label = Label(manage_window, text="Extension :", font=("Arial", 10))
    file_extension_label.grid(row=3, column=0)

    file_extension_box = ttk.Combobox(manage_window, textvariable=extension_var, values=extension_list)
    file_extension_box.grid(row=3, column=1, sticky=W)
    file_extension_box.configure(state="readonly")

    add_button = Button(manage_window, text="Add", width=20, command=add_list)
    add_button.grid(row=4, column=1)


# See sorting list
def see_list():

    # Changes directory and extension according to key chosen by user
    def change():
        show_dir.set(sort_list[int(show_key.get().split("-")[1]) - 1][1])
        show_extension.set(sort_list[int(show_key.get().split("-")[1]) - 1][2])

    # Deletes the key chosen by user
    def delete_list():
        sort_list.pop(sort_list.index([show_key.get().split("-")[0], show_dir.get(), show_extension.get()]))
        if sort_list:
            sort_menu["values"] = [sort_list[key][0] + "-" + str(key + 1) for key in range(len(sort_list))]
            show_key.set([sort_list[key][0] + "-" + str(key + 1) for key in range(len(sort_list))][0])
            show_dir.set(sort_list[0][1])
            show_extension.set(sort_list[0][2])
        else:
            list_window.destroy()

    # Clears list
    def clear_list():
        sort_list.clear()
        list_window.destroy()

    # List Window
    if sort_list:
        list_window = Toplevel()
        list_window.title("Sorting List")
        list_window.geometry(f"{MANAGE_WIDTH}x{MANAGE_HEIGHT}+{x}+{y}")
        list_window.resizable(False, False)

        show_key = StringVar()
        show_dir = StringVar()
        show_extension = StringVar()
        show_key.set([sort_list[key][0] + "-" + str(key + 1) for key in range(len(sort_list))][0])
        show_dir.set(sort_list[0][1])
        show_extension.set(sort_list[0][2])
        show_key.trace("w", lambda *args: change())

        # Frames, labels, buttons, and ComboBox
        list_title = Label(list_window, text="View List", height=2, font=("Arial", 20))
        list_title.pack()

        list_frame = Frame(list_window)
        list_frame.pack(anchor=W)

        list_label = Label(list_frame, text="Key list :", font=("Arial", 10))
        list_label.grid(row=0, column=0)

        sort_menu = ttk.Combobox(list_frame, textvariable=show_key,
                                 values=[sort_list[key][0] + "-" + str(key + 1) for key in range(len(sort_list))])
        sort_menu.grid(row=0, column=1, sticky=W)

        del_button = Button(list_frame, text="Delete", command=delete_list)
        del_button.grid(row=1, column=2, sticky=W)

        dir_text = Label(list_frame, text="Destination :", font=("Arial", 10))
        dir_text.grid(row=1, column=0)

        dir_label = Label(list_frame, textvariable=show_dir, width=65, bg="light grey")
        dir_label.grid(row=1, column=1)

        clear_button = Button(list_frame, text="Clear", command=clear_list)
        clear_button.grid(row=2, column=2, sticky=W)

        extension_text = Label(list_frame, text="File type :", font=("Arial", 10))
        extension_text.grid(row=2, column=0)

        extension_label = Label(list_frame, textvariable=show_extension, width=30, bg="light grey")
        extension_label.grid(row=2, column=1, sticky=W)

    # If list empty, use add_sort function to add sort
    else:
        messagebox.showinfo(title="List Empty", message="You must add key first")
        add_sort()


# Sort by file function
def sort_by_file():
    # Sort file thread
    def sort_file():
        sort_dir = Path(directory)

        # Loops through every file in the desired directory
        for file in sort_dir.iterdir():

            # If the file is a file
            if file.is_file():

                # Creates variables needed
                file_name = file.name
                old_path = file.parent
                extension = file.suffix
                new_path = old_path.joinpath(extension[1:])

                # Creates a folder if folder needed doesn't exist
                if not new_path.exists():
                    new_path.mkdir()

                # Creates new file path
                new_file_path = new_path.joinpath(file_name)

                # If file exists in destination
                if new_file_path.exists():

                    # If user wants to replace the existing file
                    if messagebox.askyesno(title="Warning",
                                           message=f"{file_name} already exists in destination\nContinue?",
                                           icon="warning"):
                        file.replace(new_file_path)

                # If file doesn't exist
                else:
                    file.replace(new_file_path)

        # Destroys the window and shows info if sorting has finished
        sort_window.destroy()
        messagebox.showinfo(title="Sorting Info", message="Sorting has finished")

    # asks for folder to sort
    choose_dir = False
    while not choose_dir:
        directory = filedialog.askdirectory(initialdir=r"C:\Users\User\Desktop")
        if directory:
            choose_dir = messagebox.askyesno(title="Directory", message=f"You will sort file in {directory}\nContinue?")
        else:
            return

    # Sort window loop
    sort_window = Toplevel()
    sort_window.geometry(f"{SORT_WIDTH}x{SORT_HEIGHT}")
    sort_window.resizable(False, False)
    wait_label = Label(sort_window, text="Wait while we sort your files...\n(Do not close this window)",
                       font=("Arial", 10))
    wait_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    sorting = threading.Thread(target=sort_file, args=())
    sorting.start()


# Sort files according to keys, values in dictionary
def sort_by_dic():
    # Sort file thread
    def sort_dic():
        sort_dir = Path(directory)

        # Loops through key, location, and extension in sort_list
        for key, location, extension in sort_list:

            # Loops through file in the desired directory
            for file in sort_dir.iterdir():

                # Creates variables needed
                file_name = file.stem
                file_extension = file.suffix
                split_file = re.split(r"[\s_,-]", file_name)

                # If the file is a file and the extension is "All files"
                if file.is_file() and key in split_file and extension == "All files":

                    # Creates variables needed to move file
                    full_file_name = file.name
                    file_destination = Path(location).joinpath(full_file_name)

                    # If file exists in destination
                    if file_destination.exists():

                        # If user wants to replace the existing file
                        if messagebox.askyesno(title="Warning",
                                               message=f"{full_file_name} already exists in destination\nContinue?",
                                               icon="warning"):
                            file.replace(file_destination)

                    # If file doesn't exist
                    else:
                        file.replace(file_destination)

                # If the file is a file and it is the desired file
                elif file.is_file() and key in split_file and extension == file_extension[1:]:

                    # Creates variables needed to move file
                    full_file_name = file.name
                    file_destination = Path(location).joinpath(full_file_name)

                    # If file exists in destination
                    if file_destination.exists():

                        # If user wants to replace the existing file
                        if messagebox.askyesno(title="Warning",
                                               message=f"{full_file_name} already exists in destination\nContinue?",
                                               icon="warning"):
                            file.replace(file_destination)

                    # If file doesn't exist
                    else:
                        file.replace(file_destination)

        # Destroys window and shows info if sorting has finished
        sort_window.destroy()
        messagebox.showinfo(title="Sorting Info", message="Sorting has finished")

    # If sort dictionary is not empty
    if sort_list:

        # asks for folder to sort
        choose_dir = False
        while not choose_dir:
            directory = filedialog.askdirectory(initialdir=r"C:\Users\User\Desktop")
            if directory:
                choose_dir = messagebox.askyesno(title="Directory", message=f"You will sort files in {directory}\n"
                                                                            f"Continue?")
            else:
                return

        # Sort window
        sort_window = Toplevel()
        sort_window.geometry(f"{SORT_WIDTH}x{SORT_HEIGHT}")
        sort_window.resizable(False, False)
        wait_label = Label(sort_window, text="Wait while we sort your files...\n(Do not close this window)",
                           font=("Arial", 10))
        wait_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        sorting = threading.Thread(target=sort_dic, args=())
        sorting.start()

    # Sort list is empty
    else:
        messagebox.showinfo(title="List Empty", message="You must add key first")
        add_sort()


# How to Use the Program
def how_to_use():
    # How to use window
    about_window = Toplevel()
    about_window.geometry(f"{ABOUT_WIDTH}x{ABOUT_HEIGHT}")

    # How to use text
    about_text = Text(about_window, font=("Arial", 15))
    scroll_bar = Scrollbar(about_text)
    about_window.grid_rowconfigure(0, weight=1)
    about_window.grid_columnconfigure(0, weight=1)
    about_text.grid(sticky=N + E + S + W)
    scroll_bar.pack(side=RIGHT, fill=Y)
    about_text.config(yscrollcommand=scroll_bar.set)

    # Insert words to text area
    with open("HowToUse.txt") as file:
        about_text.insert(1.0, file.read())

    # Text is read only
    about_text.config(state=DISABLED)


# sort_list
sort_list = insert_list()

# Constants needed
WIDTH = 400
HEIGHT = 225
NEW_WIDTH = 800
NEW_HEIGHT = 225
MANAGE_WIDTH = 600
MANAGE_HEIGHT = 175
SORT_WIDTH = 300
SORT_HEIGHT = 50
ABOUT_WIDTH = 500
ABOUT_HEIGHT = 500

# Inserts saved sorting
insert_list()

# Main window loop
window = Tk()
window.title("File Sorting")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (WIDTH / 2))
y = int((screen_height / 2) - (HEIGHT / 2))
window.geometry(f"{WIDTH}x{HEIGHT}")
window.resizable(False, False)

# Title
title_label = Label(window, text="File Sorting Program", height=2, font=("Arial", 20))
title_label.pack()

# Buttons
see_list_button = Button(window, text="Manage Sorting", width=30, command=see_list)
see_list_button.pack()

add_sort_button = Button(window, text="Add sorting", width=30, command=add_sort)
add_sort_button.pack()

file_type_button = Button(window, text="Run sort by file type", width=30, command=sort_by_file)
file_type_button.pack()

run_button = Button(window, text="Run Sorting", width=30, command=sort_by_dic)
run_button.pack()

about_button = Button(window, text="How to Use", width=30, command=how_to_use)
about_button.pack()

window.mainloop()

# Writes the list into a file for next use
write_file(sort_list)

