from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('The New Testament')):
        doc.append('Introduction to the New Testament text.')

        with doc.create(Subsection('Matthew 1:1')):
            doc.append('The book of the generation of Jesus Christ, the son of David, the son of Abraham.')
            doc.append(NoEscape(r'\footnote{Footnote text goes here.}'))

if __name__ == '__main__':
    # Basic document
    doc = Document('basic')
    fill_document(doc)

    doc.generate_pdf(clean_tex=False)