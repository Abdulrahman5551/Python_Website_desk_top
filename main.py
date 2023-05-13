from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import webbrowser

"""
This App Save Websites in List
"""

root = Tk()
root.geometry('440x480+390+90')
root.resizable(False, False)
root.title('Bookmark WebSite: 1.1')
root.iconbitmap('C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\images\\icons\\web.ico')
root.config(bg='#00D7AD')

# All Variables
show_url_var = StringVar()
combox_var = StringVar()
name_var = StringVar()
url_var = StringVar()


# Add data
def addUrl():
    db = sqlite3.connect("C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\DB_files\\webs.db")  # Connect with database file
    cursor = db.cursor()  # Create cursor

    name = name_var.get().title()  # Get text from entry name and save in variables [ name ]
    url = url_var.get().lower()  # Get URL from entry URL and save in variables [ url ]

    if len(name) > 0 and len(url) > 5:  # Check Length String name and URL
        sql = f"INSERT INTO web_fav(name_web, url_web) VALUES('{name}', '{url}')"
        cursor.execute(sql)
        db.commit()
        db.close()
        fetchUrl()
        messagebox.showinfo('Done', f'Add {name} Succeed ..')

    else:
        pass


# Delete data
def deleteUrl():
    db = sqlite3.connect("C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\DB_files\\webs.db")
    cursor = db.cursor()

    try:
        cursor_row = table_tree.focus()
        contents = table_tree.item(cursor_row)
        data = contents['values']

        name_del = data[0].title()

        if len(data) == 1:
            sql = f"DELETE FROM web_fav WHERE name_web = '{name_del}'"
            cursor.execute(sql)
            db.commit()
            db.close()
            fetchUrl()
        else:
            pass

    except IndexError:
        messagebox.showerror('Sorry', 'No Selected !!')


# Update data
def updateUrl():
    db = sqlite3.connect("C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\DB_files\\webs.db")
    cursor = db.cursor()

    try:

        cursor_row = table_tree.focus()
        contents = table_tree.item(cursor_row)
        data = contents['values']

        name_up = data[0]

        cursor.execute(f"SELECT name_web, url_web FROM web_fav WHERE name_web = '{name_up}'")
        rows = cursor.fetchall()

        getName = name_var.get()
        getUrl = url_var.get()
        countName = 0
        countUrl = 0

        if getName != rows[0][0]:
            sql = f"UPDATE web_fav SET name_web = '{getName}' WHERE url_web = '{url_var.get().lower()}'"
            cursor.execute(sql)
            db.commit()
            fetchUrl()
            countName += 1

        if getUrl != rows[0][1]:
            sql = f"UPDATE web_fav SET url_web = '{getUrl}' WHERE name_web = '{name_var.get()}'"
            cursor.execute(sql)
            db.commit()
            fetchUrl()
            countUrl += 1
        db.close()

        if countName == 1 and countUrl == 1:
            messagebox.showinfo("Done", "Edit Name and URL")

        elif countName == 1 and countUrl == 0:
            messagebox.showinfo("Done", "Edit Name")

        elif countName == 0 and countUrl == 1:
            messagebox.showinfo("Done", "Edit URL")

    except IndexError:
        pass


# Get All Data and insert in table
def fetchUrl():
    db = sqlite3.connect("C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\DB_files\\webs.db")
    cursor = db.cursor()

    # This code remove items in table before fetch
    for items in table_tree.get_children():
        table_tree.delete(items)

    cursor.execute("SELECT name_web FROM web_fav")
    rows = cursor.fetchall()

    if len(rows) != 0:
        table_tree.delete(*table_tree.children)
        for row in rows:
            table_tree.insert("", END, values=row)
        db.commit()
        db.close()


def setCursor(event):
    db = sqlite3.connect("C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\DB_files\\webs.db")
    cursor = db.cursor()

    cursor_row = table_tree.focus()
    contents = table_tree.item(cursor_row)
    data = contents['values']
    nameWeb = data[0]

    try:

        cursor.execute(f"SELECT name_web, url_web FROM web_fav WHERE name_web = '{nameWeb}'")
        rows = cursor.fetchall()
        name_var.set(rows[0][0])
        url_var.set(rows[0][1])
        show_url_var.set(rows[0][1])
        db.close()

    except IndexError:
        pass


def sortList(event):
    db = sqlite3.connect("C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\DB_files\\webs.db")
    cursor = db.cursor()

    for items in table_tree.get_children():
        table_tree.delete(items)

    if combox_var.get() == "Ascending":
        sql = "SELECT name_web FROM web_fav ORDER BY name_web"
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            table_tree.insert("", END, values=row)
        db.commit()

    elif combox_var.get() == "Descending":
        sql = "SELECT name_web FROM web_fav ORDER BY name_web DESC"
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            table_tree.insert("", END, values=row)
        db.commit()
    db.close()


def openBrowser():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    url = show_url_var.get()
    if url:
        webbrowser.get(chrome_path).open(url)
    else:
        pass


def cleanEntry():
    show_url_var.set("")
    name_var.set("")
    url_var.set("")


# Frame Table
tree_frame = Frame(root, bg="black")
tree_frame.place(x=0, y=0, width=200, height=480)
# Table
table_tree = ttk.Treeview(tree_frame, columns="1", height=60)
table_tree.heading("1", text="Name WebSite")
table_tree.column("1", width=140, anchor="center")
table_tree["show"] = "headings"
table_tree.place(x=0, y=0, width=200)

# Entry Show URL
entry_url = Entry(root, width=20, font=('Calibre', 10), justify='left', state='readonly', textvariable=show_url_var)
entry_url.place(x=210, y=24, width=220)

# Button open in Browser
butt_open_browser = Button(root, text="Open", bd=2, command=openBrowser)
butt_open_browser.place(x=210, y=49, width=66)

# Icon clear
ico_clear = PhotoImage(
    file="C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\images\\icons\\broom.png")

# Label Icon clear
butt_clear = Button(root, image=ico_clear, bg="Orange", border=1, command=cleanEntry).place(x=400, y=49)

# Combobox with label combobox
label_sort = Label(root, text="Sort :", bg="#00D7AD", font=('Calibre', 12))
label_sort.place(x=210, y=99)

combobox_sort = ttk.Combobox(root, textvariable=combox_var)
combobox_sort['values'] = ("Ascending", "Descending")
combobox_sort.place(x=255, y=101)

# Entry and Label Name Web
label_name = Label(root, text="Name Website :", bg="#00D7AD", font=('Calibre', 13))
label_name.place(x=210, y=160)

entry_name = Entry(root, font=('Calibre', 13), justify='center', border=2, textvariable=name_var)
entry_name.place(x=210, y=185)

# Entry and Label Url Web
label_url = Label(root, text="URL :", bg="#00D7AD", font=('Calibre', 13))
label_url.place(x=210, y=230)

entry_url_2 = Entry(root, font=('Calibre', 13), justify='center', border=2, textvariable=url_var)
entry_url_2.place(x=210, y=255)

# Icon Add
ico_add = PhotoImage(
    file="C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\images\\icons\\plus.png")

# Icon Delete
ico_delete = PhotoImage(
    file="C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\images\\icons\\delete.png")

# Icon Edit
ico_edit = PhotoImage(
    file="C:\\Users\\abdul\\Downloads\\My-Github\\Python_project\\Websites_project\\images\\icons\\edit.png")

# Label Icon add
butt_add = Button(root, image=ico_add, bg="White", border=2, command=addUrl).place(x=210, y=300)

# Label Icon delete
butt_delete = Button(root, image=ico_delete, bg="#00D7AD", border=1, command=deleteUrl).place(x=210, y=340)

# Label Icon edit
butt_edit = Button(root, image=ico_edit, bg="#00D7AD", border=1, command=updateUrl).place(x=210, y=380)

fetchUrl()
table_tree.bind("<ButtonRelease-1>", setCursor)
combobox_sort.bind('<<ComboboxSelected>>', sortList)

root.mainloop()
