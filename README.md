# Books and Authors Database with SQLAlchemy

This project implements a database of books and authors using SQLAlchemy with a **many-to-many** relationship between `Book` and `Author`. The database is populated with randomly
generated data, and several queries are performed to analyze the data.

## Project Structure

- `books_authors.db`: The SQLite database file where the data is stored.
- `main.py`: The main Python file containing the SQLAlchemy models, data generation logic, and queries.
- `README.md`: This documentation file.

## Models

### Author Model
The `Author` model represents an author in the database and has the following fields:
- `id`: Primary key
- `first_name`: Author's first name
- `last_name`: Author's last name
- `date_of_birth`: Author's date of birth
- `place_of_birth`: Author's place of birth

### Book Model
The `Book` model represents a book in the database and has the following fields:
- `id`: Primary key
- `name`: Name of the book
- `category_name`: Category of the book (e.g., Fiction, Non-fiction)
- `number_of_pages`: Number of pages in the book
- `date_of_issue`: Date when the book was issued

### Book-Author Association Table
An **association table** `book_author_association` is used to represent the many-to-many relationship between `Book` and `Author`.

## Random Data Generation

- **500 authors** are randomly generated using the `Faker` library.
- **1000 books** are randomly generated and each book is associated with 1 to 3 random authors.

## Queries

The following queries are performed in the project:

1. **Find and print all fields of the book with the most pages.**
2. **Find and print the average number of pages in books.**
3. **Print the youngest author.**
4. **Print authors who do not have a book yet.**
5. **Bonus task:** Find 5 authors who have more than 3 books.

## Getting Started

### Prerequisites

You need to have Python installed and the following libraries:
- `SQLAlchemy`
- `Faker`

You can install these libraries using `pip`:

```bash
pip install SQLAlchemy Faker
