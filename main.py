from epub_processor import EpubProcessor
from collections import Counter
import os
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re


class WordHighlighter(EpubProcessor):
    """A class for highlighting unknown words in .epub file.

    To use the class, you have to create its instance with passed in path to your .epub file.
    Then run .process_epub() method on the instance.
    You'll be asked whether you know the words. Adter that the instance will create new .epub file
    in the same folder with your old .epub file.

    >>> WordHighlighter("harry-potter-book.epub").process_epub()
    """
    #TODO: improve readability of the code in this class

    _contents_folder = 'OEBPS'

    def __init__(self, fname: str) -> None:
        super().__init__(fname)
        self._all_words = Counter()

    def make_changes_to_temp(self):
        content_files = Path(os.path.join(self._temp_directory, self._contents_folder)).iterdir()
        for file_ in content_files:
            if file_.suffix == '.xhtml':
                bs = BeautifulSoup(open(file_).read(), features="html5lib")
                text = bs.body.get_text()
                words = re.findall(r'''(?<=[…:\s\.,;"“\?!^\)\(])[a-zA-Z\-‘’]{2,}(?=[…:\s\.,;"”\?!$\)\(])''', text)
                words = [word.lower() for word in words]
                self._all_words.update(words)

        unknown_words = self.find_unknown_words(filter(lambda x: 1000 >= self._all_words[x] >= 100, self._all_words))
        self.highlight_unknown_words(unknown_words)


    def highlight_unknown_words(self, unknown_words):
        pattern = re.compile(
                r'(?<=[…:\s\.,;"“\?!^\)\(])('
              + '|'.join(map(re.escape, unknown_words))
              + r')(?=[…:\s\.,;"”\?!$\)\(])'
                )
        start_tag = "<b style='background-color: yellow'>"
        end_tag = '</b>'
        content_files = Path(os.path.join(self._temp_directory, self._contents_folder)).iterdir()
        for file_ in content_files:
            if file_.suffix == '.xhtml':
                bs = BeautifulSoup(open(file_).read(), features="html5lib")
                for desc in list(bs.body.descendants):
                    if isinstance(desc, NavigableString):
                        raw_string = str(desc)
                        new_text = pattern.sub(lambda x: start_tag + raw_string[x.start():x.end()] + end_tag, raw_string)
                        desc.replace_with(BeautifulSoup(new_text, 'html.parser'))

                with open(file_, 'w') as outfile:
                    outfile.write(str(bs))

    @staticmethod
    def find_unknown_words(words) -> list:
        unknown_words = []
        for word in words:
            while True:
                ans = input(f"\n{word}\nIs this word new to you? (Y/n) ")
                if ans == '' or ans.lower() == 'y':
                    unknown_words.append(word)
                    break
                elif ans.lower() == 'n':
                    break
            print('Current new words:', *unknown_words, sep='\t')

        return unknown_words


if __name__ == "__main__":
    WordHighlighter("/home/bohdanm/Desktop/harry-potter-book-1.epub").process_epub()
