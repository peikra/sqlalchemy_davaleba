import random
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from faker import Faker


Base = declarative_base()
fake = Faker()


book_author_association = Table(
    'book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)

    books = relationship("Book", secondary=book_author_association, back_populates="authors")



class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_name = Column(String)
    number_of_pages = Column(Integer)
    date_of_issue = Column(Date)

    authors = relationship("Author", secondary=book_author_association, back_populates="books")



engine = create_engine('sqlite:///books_authors.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



def random_date_of_birth():
    return fake.date_of_birth(minimum_age=25, maximum_age=85)



def generate_authors(num_authors=500):
    for _ in range(num_authors):
        author = Author(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=random_date_of_birth(),
            place_of_birth=fake.city()
        )
        session.add(author)
    session.commit()


def generate_books(num_books=1000):
    author_ids = [author.id for author in session.query(Author).all()]
    for _ in range(num_books):
        book = Book(
            name=fake.sentence(nb_words=3),
            category_name=random.choice(['Fiction', 'Non-fiction', 'Fantasy', 'History', 'Science']),
            number_of_pages=random.randint(100, 1000),
            date_of_issue=fake.date_this_century()
        )


        random_author_ids = random.sample(author_ids, random.randint(1, 3))
        book.authors = session.query(Author).filter(Author.id.in_(random_author_ids)).all()
        session.add(book)

    session.commit()



def book_with_most_pages():
    book = session.query(Book).order_by(Book.number_of_pages.desc()).first()
    print(f"ყველაზე მეტ გვერდიანი წიგნი: {book.name}, {book.number_of_pages} გვერდი")



def average_number_of_pages():
    avg_pages = session.query(func.avg(Book.number_of_pages)).scalar()
    print(f"გვერდების საშუალო რაოდენობა: {avg_pages:.2f}")



def youngest_author():
    youngest = session.query(Author).order_by(Author.date_of_birth.desc()).first()
    print(f"ყველაზე ახალგაზრდა ავტორი: {youngest.first_name} {youngest.last_name}, {youngest.date_of_birth}")



def authors_without_books():
    authors = session.query(Author).outerjoin(book_author_association).filter(
        book_author_association.c.book_id == None).all()
    print("ავტორები წიგნის გარეშე:")
    for author in authors:
        print(f"{author.first_name} {author.last_name}")



def authors_with_more_than_three_books():
    authors = session.query(Author).join(book_author_association).group_by(Author.id).having(
        func.count(book_author_association.c.book_id) > 3).limit(5).all()
    print("ავტორები 3-ზე მეტი წიგნით:")
    for author in authors:
        print(f"{author.first_name} {author.last_name}")



generate_authors()
generate_books()


book_with_most_pages()
average_number_of_pages()
youngest_author()
authors_without_books()
authors_with_more_than_three_books()
