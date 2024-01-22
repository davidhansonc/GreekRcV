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
                verse_id INTEGER,
                footnote TEXT,
                FOREIGN KEY(verse_id) REFERENCES Verses(id)
            )
        ''')

    def create_cross_references_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS CrossReferences (
                verse_id INTEGER,
                cross_ref_id INTEGER,
                FOREIGN KEY(verse_id) REFERENCES Verses(id),
                FOREIGN KEY(cross_ref_id) REFERENCES Verses(id)
            )
        ''')

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