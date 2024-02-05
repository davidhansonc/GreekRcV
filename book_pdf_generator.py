import subprocess
import os
import sqlite3

class PDFGenerator:
    # Initialization and Database Connection
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.last_printed_verse = None

    def close(self):
        self.cursor.close()
        self.conn.close()

    # Data Fetching Methods
    def fetch_greek_title(self, book_name):
        query = """
        SELECT greek_title
        FROM Books
        WHERE name = ?
        """
        self.cursor.execute(query, (book_name,))
        result = self.cursor.fetchone()
        return result[0] if result else book_name

    def fetch_book_details(self, book_name):
        query = """
        SELECT greek_title, subject
        FROM Books
        WHERE name = ?
        """
        self.cursor.execute(query, (book_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            return book_name, ""

    def fetch_outline_points(self, book_name):
        query = """
        SELECT verse_range, outline_point
        FROM Outlines
        WHERE book = ?
        ORDER BY CAST(SUBSTR(verse_range, 1, INSTR(verse_range, ':') - 1) AS INTEGER),
                 CAST(SUBSTR(verse_range, INSTR(verse_range, ':') + 1, INSTR(verse_range, '-') - INSTR(verse_range, ':') - 1) AS INTEGER)
        """
        self.cursor.execute(query, (book_name,))
        return self.cursor.fetchall()

    def fetch_verses_and_footnotes(self, book_name):
        query = """
        SELECT V.chapter_number, V.verse_number, V.verse_text, F.footnote_number, F.word_index, F.footnote
        FROM Verses V
        LEFT JOIN Footnotes F ON V.id = F.verse_id
        WHERE V.book_name = ?
        ORDER BY V.chapter_number, V.verse_number, F.footnote_number
        """
        self.cursor.execute(query, (book_name,))
        return self.cursor.fetchall()

    # Content Generation Methods
    def generate_latex_content(self, book_name, results):
        content = []
        current_chapter = None
        current_verse = None
        verse_text = ""
        footnotes = []
        outline_points = self.fetch_outline_points(book_name)  # Fetch outline points for the book

        outline_iterator = iter(outline_points)
        current_outline = next(outline_iterator, None)

        for chapter, verse, text, footnote_number, word_index, footnote in results:
            # Check if there's an outline point to insert before this verse
            while current_outline and (int(current_outline[0].split(':')[0]) < chapter or (int(current_outline[0].split(':')[0]) == chapter and int(current_outline[0].split(':')[1].split('-')[0]) <= verse)):
                # Insert the outline point into the content
                content.append(f'{current_outline[1]}\n')
                current_outline = next(outline_iterator, None)

            if current_verse != verse or current_chapter != chapter:
                if current_verse is not None:
                    # Add the collected verse and its footnotes to content
                    self.add_verse_to_content(current_chapter, current_verse, verse_text, content, footnotes)
                # Reset for the new verse
                current_chapter = chapter
                current_verse = verse
                verse_text = text
                footnotes = []
            else:
                # Same verse as before, append text if it's not the first entry
                if text != verse_text:
                    verse_text += " " + text

            if footnote:
                footnotes.append((word_index, footnote))

        # Add the last verse and its footnotes to content
        if current_verse is not None:
            self.add_verse_to_content(current_chapter, current_verse, verse_text, content, footnotes)

        # Check for any remaining outline points after the last verse
        while current_outline:
            content.append(f'\\textbf{{Outline Point:}} {current_outline[1]}\n')
            current_outline = next(outline_iterator, None)

        if self.last_printed_verse is not None:
            content.append('\\end{verse}')  # End the last verse environment
        return '\n'.join(content)

    def add_verse_to_content(self, chapter, verse, text, content, footnotes):
        # Check if we are starting a new chapter or verse
        if self.last_printed_verse is None or chapter != self.last_printed_verse[0] or verse != self.last_printed_verse[1]:
            if self.last_printed_verse is not None:
                # End the previous verse environment if it exists
                content.append('\\end{verse}\n')  # End the previous verse environment
            # Start a new chapter if necessary
            if self.last_printed_verse is None or chapter != self.last_printed_verse[0]:
                content.append(f'\\section*{{ΚΕΦΑΛΑΙΟΝ {chapter}}}\n')  # Start a new chapter
            # Start a new verse environment
            content.append('\\begin{verse}\n')  # Start the verse environment
            # Set the current verse number for footnotes
            content.append(f'\\setcurrentverse{{{verse}}}\n')  # Update the current verse number

        # Reset the footnote counter for each new verse
        content.append('\\setcounter{footnote}{0}\n')

        # Apply footnotes to verse text
        verse_with_footnotes = self.apply_footnotes_to_verse(text, footnotes)
        # Add the verse number and text to the content, followed by a space to separate from the next verse
        content.append(f'\\textsuperscript{{{verse}}}~{verse_with_footnotes}\n')
        self.last_printed_verse = (chapter, verse)

    def apply_footnotes_to_verse(self, text, footnotes):
        words = text.split()
        for word_index, footnote in sorted(footnotes, key=lambda x: int(x[0])):
            index = int(word_index) - 1
            if 0 <= index < len(words):
                words[index] = f'\\footnote{{{footnote}}}{words[index]}'
        return ' '.join(words)

    # File and Compilation Management
    def write_latex_file(self, book_title, book_subject, content, output_filename):
        with open('book_template.tex', 'r') as file:
            template = file.read()
        # Include the book subject as a secondary title, formatted to be smaller and centered below the main title
        title_content = f"\\title{{{book_title}\\\\[1ex] \\Large {book_subject}}}\n\\date{{}}\n\\maketitle\n" + content
        latex_document = template.replace('{{ content }}', title_content)
        with open(f'{output_filename}.tex', 'w') as file:
            file.write(latex_document)

    def compile_latex_to_pdf(self, output_filename):
        subprocess.run(['pdflatex', f'{output_filename}.tex'])

    def cleanup_aux_files(self, output_filename):
        aux_files = ['.aux', '.log', '.out']
        for ext in aux_files:
            try:
                os.remove(f'{output_filename}{ext}')
            except OSError:
                pass

    # Main Method to Generate PDF
    def generate_pdf_with_verses_and_footnotes(self, book_name, output_filename='ΦΙΛΙΠΠΗΣΙΟΥΣ'):
        greek_title, book_subject = self.fetch_book_details(book_name)  # Fetch both title and subject
        results = self.fetch_verses_and_footnotes(book_name)
        latex_content = self.generate_latex_content(book_name, results)  # Now passing book_name here
        self.write_latex_file(greek_title, book_subject, latex_content, output_filename)
        self.compile_latex_to_pdf(output_filename)
        self.cleanup_aux_files(output_filename)

# Usage example
pdf_generator = PDFGenerator('new_testament.db')
pdf_generator.generate_pdf_with_verses_and_footnotes('Philippians')
pdf_generator.close()