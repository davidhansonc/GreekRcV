import sqlite3

class FootnoteManager:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def update_footnote_text(self, book, chapter, verse, footnote_number, new_footnote_text):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # First, find the verse_id for the given book, chapter, and verse
        c.execute('''
            SELECT id FROM Verses
            WHERE book_name = ? AND chapter_number = ? AND verse_number = ?
        ''', (book, chapter, verse))
        verse_id_record = c.fetchone()
        if verse_id_record is None:
            print("Verse not found.")
            return
        verse_id = verse_id_record[0]

        # Update the footnote text for the specified verse_id and footnote_number
        c.execute('''
            UPDATE Footnotes
            SET footnote = ?
            WHERE verse_id = ? AND footnote_number = ?
        ''', (new_footnote_text, verse_id, footnote_number))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def add_new_footnote(self, book, chapter, verse, footnote_number, word_index, footnote_text):
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

    def update_book_subject(self, book_name, subject):
        """
        Update the subject for a given book.

        :param book_name: The name of the book to update.
        :param subject: The new subject to set for the book.
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()  # Create a cursor object

        query = """
        UPDATE Books
        SET subject = ?
        WHERE name = ?
        """
        cursor.execute(query, (subject, book_name))
        conn.commit()  # Commit the changes
        conn.close()  # Close the connection
        print(f"Subject updated for book '{book_name}'.")


if __name__ == "__main__":
    manager = FootnoteManager('new_testament.db')

    # subject = "Χριστὸν ἐμπειράζοντες - Λαμβάνοντες Χριστὸν ὡς τὴν ζωὴν ἡμῶν, τύπον, σκοπόν, δύναμιν, καὶ μυστήριον."
    book = "Philippians"
    chapter = 1
    verse = 5
    footnote_number = 1
    # word_index = 7
    footnote = """
    οἱ ἅγιοι ἐν Φιλίπποις κοινωνίαν εἶχον εἰς τὸ εὐαγγέλιον, μετέχοντες εἰς τὴν προκοπὴν τοῦ εὐαγγελίου διὰ τῆς διακονίας τοῦ ἀποστόλου Παύλου. ἡ μετοχὴ αὕτη συμπεριελάμβανε οἰκονομικὰς συνεισφορὰς αὐτῶν πρὸς τὸν ἀπόστολον (4:10, 15-16), αἵτινες ἐξήλθεν εἰς τὸν προκόπτειν τοῦ εὐαγγελίου. τοιαύτη κοινωνία, ἥ ἐφύλαξεν αὐτοῦς μὴ εἶναι ἰδιωτικοῦς καὶ ποικίλον νοῦν ἔχοντας, δηλοῖ ὅτι ἕν ἐγένοντο μετὰ τοῦ ἀποστόλου Παύλου καὶ μετὰ ἀλλήλων. τούτο ἔδωκεν αὐτοῖς ἔδαφος εἰς ἐμπειρίαν καὶ χάραν τοῦ Χριστοῦ, ὅ ἐστιν τὸ κυριώτατον τοῦ βιβλίου τοῦτου. ἡ ζωή ἡ ἐμπειρῶσα καὶ χαίρουσα τὸν Χρίστον ἔστιν ζωή ἐν τῷ προκοπτεῖν τοῦ εὐαγγελίου, ἐν τῷ ἀπαγγέλλειν τοῦ εὐαγγελίου, μὴ ἰδιωτική ἀλλά κοινή. ὅσον πλείον ἔχωμεν κοινωνίαν ἐν τῷ προκοπτεῖν τοῦ εὐαγγελίου, ὅσον πλείον τὸν Χρίστον ἐμπειρῶμεν καὶ χαιρόμεν. τοῦτο ἀποκτείνει τὸν ἐαυτόν ἡμῶν τε καὶ τὴν φιλοτιμίαν ἡμῶν καὶ τὴν αἵρεσιν τοῦ νοῦ ἡμῶν καὶ τὸν ἐκλογήν ἡμῶν.
    """

    # manager.update_book_subject('Philippians', subject)
    # manager.add_new_footnote(book, chapter, verse, footnote_number, word_index, footnote) 
    manager.update_footnote_text(book, chapter, verse, footnote_number, footnote)
    # manager.update_fn_index("Philippians 1:1", footnote_number=1, new_word_index=16)
    # manager.update_fn_index("Philippians 1:1", footnote_number=2, new_word_index=17)
    print(manager.get_footnote(book, chapter, verse, footnote_number))
