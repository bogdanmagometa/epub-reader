from epub_processor import EpubProcessor
from collections import Counter
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re


class WordHighlighter(EpubProcessor):
    contents_folder = 'OEBPS'

    def __init__(self, fname: str) -> None:
        super().__init__(fname)
        self.all_words = Counter()

    def process_epub(self) -> Counter:
        super().process_epub()
        return self.all_words

    def make_changes_to_temp(self):
        content_files = Path(os.path.join(self._temp_directory, self.contents_folder)).iterdir()
        for file_ in content_files:
            if file_.suffix == '.xhtml':
                bs = BeautifulSoup(open(file_).read(), features="html5lib")
                text = bs.body.get_text()
                words = re.findall(r'''([a-zA-Z\-’]+(?=[…:\s\.,;"\?!])|[a-zA-Z\-’]+$)''', text)
                words = [word.lower() for word in words]
                # if 'cover-' in words:
                #     print(text)
                self.all_words.update(words)



def find_unknown_words(all_words) -> list:
    unknown_words = []
    for word in all_words:
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
    all_words = WordHighlighter("/home/bohdanm/Desktop/harry-potter-book-1.epub").process_epub()
    print("Number of total unique words found:", len(all_words))

    unknown_words = find_unknown_words(filter(lambda x: 100 >= all_words[x] >= 49, all_words))

    print('\n\n\nAll unknown words:', *unknown_words, sep='\t')
