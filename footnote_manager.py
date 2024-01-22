import sqlite3

class FootnoteManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_footnote(self, book, chapter, verse, footnote_number, footnote_text):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Find the verse_id for the given book, chapter, and verse
        c.execute('''
            SELECT id FROM Verses
            WHERE book_name = ? AND chapter_number = ? AND verse_number = ?
        ''', (book, chapter, verse))
        verse_id = c.fetchone()
        if verse_id is None:
            print("Verse not found.")
            return
        verse_id = verse_id[0]

        # Insert or replace a footnote for the specified verse
        c.execute('''
            INSERT INTO Footnotes (verse_id, footnote_number, footnote)
            VALUES (?, ?, ?)
            ON CONFLICT(verse_id, footnote_number) DO UPDATE SET
            footnote = excluded.footnote
        ''', (verse_id, footnote_number, footnote_text))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def get_footnote(self, book, chapter, verse, footnote_number):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Find the verse_id for the given book, chapter, and verse
        c.execute('''
            SELECT id FROM Verses
            WHERE book_name = ? AND chapter_number = ? AND verse_number = ?
        ''', (book, chapter, verse))
        verse_id = c.fetchone()
        if verse_id is None:
            print("Verse not found.")
            return None
        verse_id = verse_id[0]

        # Retrieve the footnote text for the specified verse and footnote number
        c.execute('''
            SELECT footnote FROM Footnotes
            WHERE verse_id = ? AND footnote_number = ?
        ''', (verse_id, footnote_number))
        footnote = c.fetchone()
        conn.close()

        if footnote is None:
            print("Footnote not found.")
            return None
        return footnote[0]

# Usage example
manager = FootnoteManager('new_testament.db')
# manager.add_footnote('John', 2, 4, 5, "This is a test footnote!")
print(manager.get_footnote('John', 2, 4, 5))