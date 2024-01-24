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

def parse_footnote_string(footnote_str):
    # Split the string by spaces to separate the components
    parts = footnote_str.split()

    # Extract book, chapter, and verse
    book = parts[0]
    chapter_and_verse = parts[1].split(':')
    chapter = int(chapter_and_verse[0])
    verse = int(chapter_and_verse[1])

    # Extract footnote number
    footnote_number = int(parts[3])

    return book, chapter, verse, footnote_number

# Usage example
manager = FootnoteManager('new_testament.db')

footnote_str = "Philippians 1:1 fn 2"
footnote = "Ὥδε οὐκ ἔστιν· τοῖς ἁγίοις...καὶ ἐπισκόποις καὶ διακόνοις, ἀλλά ἔστιν· τοῖς ἁγίοις...σὺν ἐπισκόποις καὶ διακόνοις. τοῦτο ἐστὶν ὑψηλῶς σημαντικόν, ὅτι δηλοῖ ὅτι ἐν τῇ τοπικῇ ἐκκλησία οἱ ἅγιοι καὶ οἱ ἐπίσκοποι καὶ οἱ διάκονοι οὐκ εἴσιν τρεῖς τάξεις. ἡ ἐκκλησία μόνην μίαν τάξιν τῶν ἁγίων σὺν τοῖς ἐπισκόποις καὶ τοις διακόνοις συσταθεῖσα ἔχει. τοῦτο προσδηλοῖ ἔτι ὅτι ἐν τινι τοπικῇ δεῖ εἴναι μονὴν μίαν ἐκκλεσίαν σὺν ἑνὶ τάξει λαοῦ ᾗ πάντας τῶν ἁγίων ἔν ταῦτῃ τοπικῇ συνέστηκεν."
book, chapter, verse, footnote_number = parse_footnote_string(footnote_str)
manager.add_footnote(book, chapter, verse, footnote_number, footnote) 
print(manager.get_footnote(book, chapter, verse, footnote_number))