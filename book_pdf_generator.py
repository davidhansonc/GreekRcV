import subprocess
import os
import sqlite3

class PDFGenerator:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.last_printed_verse = None

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

    def add_verse_to_content(self, chapter, verse, text, content):
        if self.last_printed_verse is None or chapter != self.last_printed_verse[0]:
            if self.last_printed_verse is not None:
                content.append('\\end{verse}')  # End the previous verse environment
            content.append(f'\\section*{{Chapter {chapter}}}')  # Start a new chapter
            content.append('\\begin{verse}')  # Start the verse environment
        content.append(f'\\textsuperscript{{{verse}}} {text}')
        self.last_printed_verse = (chapter, verse)

    def add_footnote_to_content(self, word_index, footnote, content):
        if word_index is None:
            return
        index = int(word_index) - 1  # Convert to zero-based index
        words = content[-1].split()  # Split the last line of content into words
        if 0 <= index < len(words):
            words[index] += f'\\footnote{{{footnote}}}'
            content[-1] = ' '.join(words)  # Rejoin the words into a single string

    def generate_latex_content(self, results):
        content = []
        for chapter, verse, text, footnote_number, word_index, footnote in results:
            self.add_verse_to_content(chapter, verse, text, content)
            if footnote:
                self.add_footnote_to_content(word_index, footnote, content)
        content.append('\\end{verse}')  # End the last verse environment
        return '\n'.join(content)

    def write_latex_file(self, content, output_filename):
        with open('book_template.tex', 'r') as file:
            template = file.read()
        latex_document = template.replace('{{ content }}', content)
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

    def generate_pdf_with_verses_and_footnotes(self, book_name, output_filename='verses_footnotes'):
        results = self.fetch_verses_and_footnotes(book_name)
        latex_content = self.generate_latex_content(results)
        self.write_latex_file(latex_content, output_filename)
        self.compile_latex_to_pdf(output_filename)
        self.cleanup_aux_files(output_filename)

    def close(self):
        self.cursor.close()
        self.conn.close()

# Usage example
pdf_generator = PDFGenerator('new_testament.db')
pdf_generator.generate_pdf_with_verses_and_footnotes('Philippians')
pdf_generator.close()
