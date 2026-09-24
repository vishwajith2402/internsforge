import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- DATABASE ----------------

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# create tables (old structure)
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
author TEXT,
year INTEGER,
publisher TEXT,
isbn TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS libraries(
id INTEGER PRIMARY KEY AUTOINCREMENT,
library_name TEXT,
city TEXT,
country TEXT,
isbn TEXT
)
""")

# add category column if database already exists
try:
    cursor.execute("ALTER TABLE books ADD COLUMN category TEXT")
    conn.commit()
except:
    pass

conn.commit()
# ---------------- SAMPLE DATA (40+ BOOKS) ----------------

def insert_sample_data():

    books=[

    ("The Alchemist","Paulo Coelho",1988,"HarperOne","ISBN001","Fiction"),
    ("Harry Potter","J.K Rowling",1997,"Bloomsbury","ISBN002","Fiction"),
    ("The Hobbit","J.R.R Tolkien",1937,"Allen & Unwin","ISBN003","Fiction"),
    ("Game of Thrones","George R.R Martin",1996,"Bantam","ISBN004","Fiction"),
    ("Sherlock Holmes","Arthur Conan Doyle",1892,"George Newnes","ISBN005","Classic"),

    ("Wings of Fire","A.P.J Abdul Kalam",1999,"Universities Press","ISBN006","Indian"),
    ("Ignited Minds","A.P.J Abdul Kalam",2002,"Penguin","ISBN007","Indian"),
    ("Five Point Someone","Chetan Bhagat",2004,"Rupa","ISBN008","Indian"),
    ("2 States","Chetan Bhagat",2009,"Rupa","ISBN009","Indian"),
    ("The Guide","R.K Narayan",1958,"Indian Thought","ISBN010","Indian"),

    ("Spider Man Comic","Marvel",2005,"Marvel Comics","ISBN011","Comics"),
    ("Batman Comic","DC",1987,"DC Comics","ISBN012","Comics"),
    ("Superman Comic","DC",1990,"DC Comics","ISBN013","Comics"),
    ("Avengers Comic","Marvel",2012,"Marvel Comics","ISBN014","Comics"),
    ("Iron Man Comic","Marvel",2008,"Marvel Comics","ISBN015","Comics"),

    ("Interstellar","Kip Thorne",2014,"W.W Norton","ISBN016","Movie"),
    ("Jurassic Park","Michael Crichton",1990,"Knopf","ISBN017","Movie"),
    ("Star Wars","George Lucas",1977,"Lucas Books","ISBN018","Movie"),
    ("The Dark Knight Script","Christopher Nolan",2008,"Warner","ISBN019","Movie"),
    ("Avengers Movie Book","Marvel Studios",2012,"Marvel","ISBN020","Movie"),

    ("Python Crash Course","Eric Matthes",2015,"No Starch","ISBN021","Programming"),
    ("Learning Python","Mark Lutz",2013,"OReilly","ISBN022","Programming"),
    ("Hands on ML","Aurelien Geron",2017,"OReilly","ISBN023","Programming"),
    ("Deep Learning","Ian Goodfellow",2016,"MIT Press","ISBN024","Programming"),
    ("AI Modern Approach","Stuart Russell",2010,"Pearson","ISBN025","Programming"),

    ("Atomic Habits","James Clear",2018,"Penguin","ISBN026","Self Development"),
    ("Think and Grow Rich","Napoleon Hill",1937,"Ralston","ISBN027","Self Development"),
    ("Rich Dad Poor Dad","Robert Kiyosaki",1997,"Warner","ISBN028","Self Development"),
    ("Ikigai","Hector Garcia",2016,"Penguin","ISBN029","Self Development"),
    ("Think Like Monk","Jay Shetty",2020,"Simon","ISBN030","Self Development"),

    ("Dune","Frank Herbert",1965,"Chilton","ISBN031","Sci-Fi"),
    ("The Martian","Andy Weir",2011,"Crown","ISBN032","Sci-Fi"),
    ("Foundation","Isaac Asimov",1951,"Gnome","ISBN033","Sci-Fi"),
    ("Enders Game","Orson Scott",1985,"Tor","ISBN034","Sci-Fi"),
    ("Ready Player One","Ernest Cline",2011,"Crown","ISBN035","Sci-Fi"),

    ("Pride and Prejudice","Jane Austen",1813,"Egerton","ISBN036","Classic"),
    ("Great Expectations","Charles Dickens",1861,"Chapman","ISBN037","Classic"),
    ("Moby Dick","Herman Melville",1851,"Harper","ISBN038","Classic"),
    ("War and Peace","Leo Tolstoy",1869,"The Russian Messenger","ISBN039","Classic"),
    ("Hamlet","William Shakespeare",1603,"Nicolas Ling","ISBN040","Classic"),

    ("Naruto Manga","Masashi Kishimoto",1999,"Shueisha","ISBN041","Comics"),
    ("Dragon Ball","Akira Toriyama",1984,"Shueisha","ISBN042","Comics"),
    ("One Piece","Eiichiro Oda",1997,"Shueisha","ISBN043","Comics")

    ]

    libraries=[

    ("British Library","London","UK"),
    ("New York Public Library","New York","USA"),
    ("Delhi Public Library","Delhi","India"),
    ("Anna Centenary Library","Chennai","India"),
    ("State Library Victoria","Melbourne","Australia"),
    ("Toronto Public Library","Toronto","Canada"),
    ("National Library","Singapore","Singapore"),
    ("Dubai Public Library","Dubai","UAE")

    ]

    for book in books:

        try:

            cursor.execute(
            "INSERT INTO books(title,author,year,publisher,isbn,category) VALUES(?,?,?,?,?,?)",
            book
            )

            for lib in libraries:

                cursor.execute(
                "INSERT INTO libraries(library_name,city,country,isbn) VALUES(?,?,?,?)",
                (lib[0],lib[1],lib[2],book[4])
                )

        except:
            pass

    conn.commit()

# run once
insert_sample_data()
# ---------------- COLORS ----------------

black="#0f0f0f"
olive="#6b8e23"
dark_olive="#556b2f"
gold="#d4af37"
light_bg="#f4f6f0"

# ---------------- WINDOW ----------------

window=tk.Tk()
window.title("Global Library Intelligence System")
window.geometry("1280x730")
window.configure(bg=light_bg)

sidebar=tk.Frame(window,bg=black,width=240)
sidebar.pack(side="left",fill="y")

main_area=tk.Frame(window,bg=light_bg)
main_area.pack(side="right",fill="both",expand=True)

# ---------------- CLEAR ----------------

def clear_main():
    for widget in main_area.winfo_children():
        widget.destroy()

# ---------------- DASHBOARD ----------------

def dashboard():

    clear_main()

    banner=tk.Frame(main_area,bg=dark_olive,height=140)
    banner.pack(fill="x")

    tk.Label(
        banner,
        text="Global Library Intelligence System",
        font=("Segoe UI",26,"bold"),
        bg=dark_olive,
        fg=gold
    ).pack(pady=10)

    tk.Label(
        banner,
        text="Smart Book Tracking Across Multiple Libraries",
        font=("Segoe UI",12),
        bg=dark_olive,
        fg="white"
    ).pack()

    tk.Frame(banner,bg=gold,height=3,width=420).pack(pady=10)

    stats=tk.Frame(main_area,bg=light_bg)
    stats.pack(pady=40)

    cursor.execute("SELECT COUNT(*) FROM books")
    books=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM libraries")
    libraries=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT category) FROM books")
    categories=cursor.fetchone()[0]

    def card(title,value):

        f=tk.Frame(stats,bg=dark_olive,width=260,height=120)
        f.pack(side="left",padx=20)

        tk.Label(
            f,
            text=title,
            bg=dark_olive,
            fg=gold,
            font=("Segoe UI",13)
        ).pack(pady=10)

        tk.Label(
            f,
            text=value,
            bg=dark_olive,
            fg="white",
            font=("Segoe UI",20,"bold")
        ).pack()

    card("Total Books",books)
    card("Categories",categories)
    card("Library Records",libraries)

# ---------------- SEARCH BOOKS ----------------

def search_books():

    clear_main()

    tk.Label(
        main_area,
        text="Search Books",
        font=("Segoe UI",20,"bold"),
        bg=light_bg,
        fg=dark_olive
    ).pack(pady=10)

    tk.Label(main_area,text="Book Title",bg=light_bg).pack()

    search_entry=tk.Entry(main_area,width=35)
    search_entry.pack()

    tk.Label(main_area,text="Category",bg=light_bg).pack()

    category_box=ttk.Combobox(main_area,
    values=[
    "All",
    "Fiction",
    "Comics",
    "Movie",
    "Programming",
    "Self Development",
    "Indian",
    "Sci-Fi",
    "Classic"
    ])

    category_box.current(0)
    category_box.pack(pady=5)

    columns=("Title","Author","Year","Publisher","ISBN","Category")

    tree=ttk.Treeview(
        main_area,
        columns=columns,
        show="headings",
        height=15
    )

    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,width=150)

    tree.pack()

    scrollbar=ttk.Scrollbar(main_area,command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack()

    def clear():
        for r in tree.get_children():
            tree.delete(r)

    def search():

        clear()

        category=category_box.get()

        if category=="All":

            cursor.execute(
            "SELECT title,author,year,publisher,isbn,category FROM books WHERE LOWER(title) LIKE LOWER(?)",
            ('%'+search_entry.get()+'%',)
            )

        else:

            cursor.execute(
            "SELECT title,author,year,publisher,isbn,category FROM books WHERE LOWER(title) LIKE LOWER(?) AND category=?",
            ('%'+search_entry.get()+'%',category)
            )

        for row in cursor.fetchall():
            tree.insert("",tk.END,values=row)

    def show_all():

        clear()

        cursor.execute(
        "SELECT title,author,year,publisher,isbn,category FROM books"
        )

        for row in cursor.fetchall():
            tree.insert("",tk.END,values=row)

    def track():

        clear()

        cursor.execute(
        "SELECT isbn FROM books WHERE LOWER(title) LIKE LOWER(?)",
        ('%'+search_entry.get()+'%',)
        )

        for book in cursor.fetchall():

            cursor.execute(
            "SELECT library_name,city,country,isbn FROM libraries WHERE isbn=?",
            (book[0],)
            )

            for row in cursor.fetchall():
                tree.insert("",tk.END,values=row)

    btn_frame=tk.Frame(main_area,bg=light_bg)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame,text="Search",
    bg=dark_olive,fg="white",
    width=15,command=search).pack(side="left",padx=5)

    tk.Button(btn_frame,text="Show All",
    bg=dark_olive,fg="white",
    width=15,command=show_all).pack(side="left",padx=5)

    tk.Button(btn_frame,text="Track Libraries",
    bg=dark_olive,fg="white",
    width=18,command=track).pack(side="left",padx=5)

# ---------------- ADD BOOK ----------------

def add_books():

    clear_main()

    fields=["Title","Author","Year","Publisher","ISBN"]

    entries=[]

    for f in fields:

        tk.Label(main_area,text=f,bg=light_bg).pack()

        e=tk.Entry(main_area,width=40)
        e.pack()

        entries.append(e)

    tk.Label(main_area,text="Category",bg=light_bg).pack()

    category=ttk.Combobox(main_area,
    values=[
    "Fiction",
    "Comics",
    "Movie",
    "Programming",
    "Self Development",
    "Indian",
    "Sci-Fi",
    "Classic"
    ])

    category.pack()

    def save():

        cursor.execute(
        "INSERT INTO books(title,author,year,publisher,isbn,category) VALUES(?,?,?,?,?,?)",
        (
        entries[0].get(),
        entries[1].get(),
        entries[2].get(),
        entries[3].get(),
        entries[4].get(),
        category.get()
        )
        )

        conn.commit()

        messagebox.showinfo("Saved","Book added")

    tk.Button(main_area,text="Add Book",
    bg=dark_olive,fg="white",
    command=save).pack(pady=10)

# ---------------- UPDATE BOOK ----------------

def update_details():

    clear_main()

    labels=["ISBN","Author","Year","Publisher","Category"]

    entries=[]

    for l in labels:

        tk.Label(main_area,text=l,bg=light_bg).pack()

        e=tk.Entry(main_area,width=40)
        e.pack()

        entries.append(e)

    def update():

        cursor.execute(
        "UPDATE books SET author=?,year=?,publisher=?,category=? WHERE isbn=?",
        (
        entries[1].get(),
        entries[2].get(),
        entries[3].get(),
        entries[4].get(),
        entries[0].get()
        )
        )

        conn.commit()

        messagebox.showinfo("Updated","Book Updated")

    tk.Button(main_area,text="Update",
    bg=dark_olive,fg="white",
    command=update).pack(pady=10)

# ---------------- DELETE BOOK ----------------

def delete_books():

    clear_main()

    tk.Label(main_area,text="Enter ISBN",bg=light_bg).pack()

    isbn=tk.Entry(main_area,width=40)
    isbn.pack()

    def delete():

        cursor.execute("DELETE FROM books WHERE isbn=?",(isbn.get(),))
        cursor.execute("DELETE FROM libraries WHERE isbn=?",(isbn.get(),))

        conn.commit()

        messagebox.showinfo("Deleted","Book removed")

    tk.Button(main_area,text="Delete",
    bg="#8b0000",fg="white",
    command=delete).pack(pady=10)

# ---------------- ADVANCED SEARCH ----------------

def advanced_search():

    clear_main()

    labels=["Title","Author","Year","Category"]

    entries=[]

    for l in labels:

        tk.Label(main_area,text=l,bg=light_bg).pack()

        e=tk.Entry(main_area,width=40)
        e.pack()

        entries.append(e)

    tree=ttk.Treeview(main_area,
    columns=("Title","Author","Year","Publisher","ISBN","Category"),
    show="headings",
    height=15)

    for col in ("Title","Author","Year","Publisher","ISBN","Category"):
        tree.heading(col,text=col)

    tree.pack()

    def search():

        for r in tree.get_children():
            tree.delete(r)

        cursor.execute(
        "SELECT title,author,year,publisher,isbn,category FROM books WHERE title LIKE ? AND author LIKE ? AND year LIKE ? AND category LIKE ?",
        (
        '%'+entries[0].get()+'%',
        '%'+entries[1].get()+'%',
        '%'+entries[2].get()+'%',
        '%'+entries[3].get()+'%'
        )
        )

        for r in cursor.fetchall():
            tree.insert("",tk.END,values=r)

    tk.Button(main_area,text="Search",
    bg=dark_olive,fg="white",
    command=search).pack(pady=10)

# ---------------- ABOUT PAGE ----------------

def about_page():

    clear_main()

    canvas=tk.Canvas(main_area,bg=light_bg)

    scroll=ttk.Scrollbar(main_area,command=canvas.yview)

    frame=tk.Frame(canvas,bg=light_bg)

    frame.bind("<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0,0),window=frame,anchor="nw")

    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(side="left",fill="both",expand=True)

    scroll.pack(side="right",fill="y")

    tk.Label(frame,text="About Project",
    font=("Segoe UI",22,"bold"),
    bg=light_bg,fg=dark_olive).pack(pady=10)

    text="""

Global Library Intelligence System manages books across multiple libraries.

Features:
Dashboard
Search books
Category filter
Add books
Update details
Delete books
Advanced search
Track libraries

Technologies:
Python
Tkinter
SQLite

Concepts:
DBMS
CRUD operations
Primary key
Foreign key

"""

    tk.Label(frame,text=text,
    bg="white",
    justify="left",
    wraplength=850).pack(padx=20,pady=20)

# ---------------- SIDEBAR ----------------

menu=[

("Dashboard",dashboard),
("Search Books",search_books),
("Add Books",add_books),
("Update Details",update_details),
("Delete Books",delete_books),
("Advanced Search",advanced_search),
("About Page",about_page)

]

tk.Label(sidebar,text="LIBRARY",
bg=black,fg=gold,
font=("Segoe UI",18,"bold")).pack(pady=20)

for text,cmd in menu:

    tk.Button(sidebar,text=text,
    bg=black,fg="white",
    activebackground=olive,
    bd=0,font=("Segoe UI",12),
    command=cmd).pack(fill="x",pady=8)

dashboard()

window.mainloop()