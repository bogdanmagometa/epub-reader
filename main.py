from epub_processor import EpubProcessor
from collections import Counter

class WordHighlighter(EpubProcessor):
    def do_changes_to_temp(self):
        pass


if __name__ == "__main__":
    EpubProcessor("/home/bohdanm/Desktop/harry-potter-book-1.epub").process_epub()
