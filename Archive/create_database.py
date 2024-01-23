import sqlite3
import csv

class DatabaseCreator:
    def __init__(self):
        self.conn = sqlite3.connect('new_testament.db')
        self.c = self.conn.cursor()
        

    def create_verses_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Verses (
                id INTEGER PRIMARY KEY,
                book_name TEXT,
                chapter_number INTEGER,
                verse_number INTEGER,
                verse_text TEXT
            )
        ''')


    def create_footnotes_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Footnotes (
                id INTEGER PRIMARY KEY,
                verse_id INTEGER NOT NULL,
                footnote_number INTEGER NOT NULL,
                footnote TEXT NOT NULL,
                FOREIGN KEY(verse_id) REFERENCES Verses(id),
                UNIQUE(verse_id, footnote_number)
            )
        ''')
        self.conn.commit()


    def create_cross_references_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS CrossReferences (
                verse_id INTEGER,
                cross_ref_id INTEGER,
                FOREIGN KEY(verse_id) REFERENCES Verses(id),
                FOREIGN KEY(cross_ref_id) REFERENCES Verses(id)
            )
        ''')


    def create_books_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                chapter_count INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
        

    def populate_books_table(self):
        # Assuming you have a list of tuples with book names and their chapter counts
        books_with_chapters = [
            ('Matthew', 28), ('Mark', 16), ('Luke', 24), ('John', 21), ('Acts', 28), ('Romans', 16),
            ('1 Corinthians', 16), ('2 Corinthians', 13), ('Galatians', 6), ('Ephesians', 6), 
            ('Philippians', 4), ('Colossians', 4), ('1 Thessalonians', 5), ('2 Thessalonians', 3), 
            ('1 Timothy', 6), ('2 Timothy', 4), ('Titus', 3), ('Philemon', 1), ('Hebrews', 13), 
            ('James', 5), ('1 Peter', 5), ('2 Peter', 3), ('1 John', 5), ('2 John', 1), ('3 John', 1), 
            ('Jude', 1), ('Revelation', 22)
        ]
        self.c.executemany('''
            INSERT INTO Books (name, chapter_count) VALUES (?, ?)
        ''', books_with_chapters)
        self.conn.commit()


    def populate_verses_table(self, csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter="|")
            next(csv_reader)  # Skip the header row if there is one
            for row in csv_reader:
                # Assuming the CSV columns are ordered as book_name, chapter_number, verse_number, verse_text
                book_name, chapter_number, verse_number, verse_text = row
                self.c.execute('''
                    INSERT INTO Verses (book_name, chapter_number, verse_number, verse_text)
                    VALUES (?, ?, ?, ?)
                ''', (book_name, chapter_number, verse_number, verse_text))
            self.conn.commit()


if __name__ == "__main__":
    creator = DatabaseCreator()
    creator.create_verses_table()
    creator.populate_verses_table('./nestle1904/nestle1904.csv')
    creator.create_footnotes_table()    
    creator.create_books_table()  # Create the Books table
    creator.populate_books_table()  # Populate the Books table with the names of the books