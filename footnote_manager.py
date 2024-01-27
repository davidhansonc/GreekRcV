import sqlite3

class FootnoteManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_footnote(self, book, chapter, verse, footnote_number, word_index, footnote_text):
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
            INSERT INTO Footnotes (verse_id, footnote_number, word_index, footnote)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(verse_id, footnote_number) DO UPDATE SET
            footnote = excluded.footnote,
            word_index = excluded.word_index
        ''', (verse_id, footnote_number, word_index, footnote_text))

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

    def parse_book_chapter_verse(self, book_chapter_verse):
        # Split the string by spaces to separate the components
        parts = book_chapter_verse.split()

        # Extract book, chapter, and verse
        book = parts[0]
        chapter_and_verse = parts[1].split(':')
        chapter = int(chapter_and_verse[0])
        verse = int(chapter_and_verse[1])

        return book, chapter, verse

    def update_fn_index(self, book_chapter_verse, footnote_number, new_word_index):
        # Parse the book name, chapter, and verse from the input string
        book, chapter, verse = self.parse_book_chapter_verse(book_chapter_verse)

        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Find the verse_id for the given book, chapter, and verse
        c.execute('''
            SELECT id FROM Verses
            WHERE book_name = ? AND chapter_number = ? AND verse_number = ?
        ''', (book, chapter, verse))
        verse_id_record = c.fetchone()
        if verse_id_record is None:
            print("Verse not found.")
            return
        verse_id = verse_id_record[0]

        # Update the word_index for the specified footnote
        c.execute('''
            UPDATE Footnotes
            SET word_index = ?
            WHERE verse_id = ? AND footnote_number = ?
        ''', (new_word_index, verse_id, footnote_number))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

if __name__ == "__main__":
    manager = FootnoteManager('new_testament.db')

    book = "Philippians"
    chapter = 1
    verse = 5
    footnote_number = 1
    word_index = 3
    footnote = "Ἴδε τὴν πρωτὴν γραφήν τοῦ εἰκοστοῦ ἑκτοῦ στιχοῦ ἐν τῷ πεντεκαιδεκάτῳ κεφαλαίῳ τῆς ἐπιστολῆς· Πρὸς Ῥωμαίους. Οἵ ἅγιοι κοινονίαν εἰς τὸ εὐαγγέλιον εἰχον, μετεχόντες ἐν τῷ"

    # manager.add_footnote(book, chapter, verse, footnote_number, word_index, footnote) 
    print(manager.get_footnote(book, chapter, verse, footnote_number))

    # Update the word index for a specific footnote
    manager.update_fn_index("Philippians 1:5", footnote_number=1, new_word_index=word_index)