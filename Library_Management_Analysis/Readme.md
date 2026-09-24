# 📚 Global Library Intelligence System

A desktop-based **Library Management and Book Tracking System** developed using **Python, Tkinter, and SQLite**. The application provides a graphical interface for managing books, organizing them by category, searching the collection, updating or deleting book records, and tracking the libraries associated with each book.

The project demonstrates practical implementation of **GUI development, database management, CRUD operations, SQL queries, search functionality, and relational data handling** in Python.

---

## 🚀 Project Overview

The **Global Library Intelligence System** is designed to manage a collection of books and their availability across multiple libraries.

The system maintains two primary database tables:

* **Books** – Stores information about books such as title, author, publication year, publisher, ISBN, and category.
* **Libraries** – Stores library information and associates libraries with books using ISBN.

The application provides a simple desktop dashboard where users can perform different library management operations without directly interacting with the database.

---

## ✨ Key Features

### 📊 Dashboard

Provides an overview of the library database, including:

* Total number of books
* Number of book categories
* Number of library records

### 🔎 Search Books

Users can search books using:

* Book title
* Category

The system also provides a **Show All** option to display the complete book collection.

### 🌍 Track Libraries

The **Track Libraries** feature searches for libraries associated with a book using its ISBN.

The system can display:

* Library name
* City
* Country
* ISBN

### ➕ Add Books

New books can be added to the database by entering:

* Title
* Author
* Publication year
* Publisher
* ISBN
* Category

### ✏️ Update Book Details

Existing book information can be updated using the ISBN.

The system allows updating:

* Author
* Year
* Publisher
* Category

### 🗑️ Delete Books

Books can be removed from the database using their ISBN.

When a book is deleted, its associated library records are also removed.

### 🔍 Advanced Search

The advanced search module allows users to search using multiple fields:

* Title
* Author
* Year
* Category

This provides more precise filtering compared with the normal search.

### ℹ️ About Page

Provides information about the project, its features, technologies, and database concepts used.

---

## 🛠️ Technologies Used

| Technology  | Purpose                              |
| ----------- | ------------------------------------ |
| **Python**  | Core programming language            |
| **Tkinter** | Desktop GUI development              |
| **ttk**     | Enhanced Tkinter widgets             |
| **SQLite**  | Local database management            |
| **SQL**     | Database queries and CRUD operations |

### Python Modules

```text
sqlite3
tkinter
tkinter.ttk
tkinter.messagebox
```

These modules are available as part of Python's standard library, so no external Python packages are required.

---

## 🗄️ Database Design

The application uses an SQLite database named:

```text
library.db
```

### Books Table

The `books` table contains:

| Column      | Description                      |
| ----------- | -------------------------------- |
| `id`        | Unique auto-incrementing book ID |
| `title`     | Book title                       |
| `author`    | Book author                      |
| `year`      | Publication year                 |
| `publisher` | Publisher name                   |
| `isbn`      | Unique ISBN identifier           |
| `category`  | Book category                    |

### Libraries Table

The `libraries` table contains:

| Column         | Description                   |
| -------------- | ----------------------------- |
| `id`           | Unique library record ID      |
| `library_name` | Name of the library           |
| `city`         | Library city                  |
| `country`      | Library country               |
| `isbn`         | ISBN associated with the book |

The **ISBN** is used to associate books with their corresponding library records.

---

## 📚 Book Categories

The current system supports the following categories:

* Fiction
* Comics
* Movie
* Programming
* Self Development
* Indian
* Sci-Fi
* Classic

The application also initializes the database with a sample collection of **43 books** and multiple library records.

---

## 🏛️ Sample Libraries

The sample database includes libraries such as:

* British Library – London, UK
* New York Public Library – New York, USA
* Delhi Public Library – Delhi, India
* Anna Centenary Library – Chennai, India
* State Library Victoria – Melbourne, Australia
* Toronto Public Library – Toronto, Canada
* National Library – Singapore
* Dubai Public Library – Dubai, UAE

---

## 🔄 CRUD Operations

The project demonstrates the four fundamental database operations:

### Create

Adding new book records to the database.

### Read

Searching, displaying, and tracking book and library information.

### Update

Modifying existing book details using ISBN.

### Delete

Removing books and their related library records.

---

## 🖥️ Application Structure

The application is organized into different functional sections:

```text
Global Library Intelligence System
│
├── Dashboard
│   ├── Total Books
│   ├── Categories
│   └── Library Records
│
├── Search Books
│   ├── Title Search
│   ├── Category Filter
│   ├── Show All
│   └── Track Libraries
│
├── Add Books
│
├── Update Details
│
├── Delete Books
│
├── Advanced Search
│   ├── Title
│   ├── Author
│   ├── Year
│   └── Category
│
└── About Page
```

---

## 🎨 User Interface

The application uses a dark and professional **black, olive, and gold** color scheme.

The interface consists of:

* Left-side navigation sidebar
* Dashboard
* Form-based data entry
* Search controls
* Table-based result display
* Scrollable About page
* Message boxes for database operations

The application window is configured for a desktop resolution of approximately:

```text
1280 × 730
```

---

## ⚙️ How the Application Works

When the application starts:

1. Python connects to the SQLite database.
2. Required database tables are created if they do not already exist.
3. The `category` column is added to older database structures when necessary.
4. Sample book and library data is inserted.
5. The Tkinter application window is created.
6. The Dashboard is displayed.
7. Users can navigate through the different modules using the sidebar.
8. Database operations are performed using SQL queries.
9. Changes are committed to `library.d
