import shutil
import zipfile
from pathlib import Path
import os
import random


class EpubProcessor:
    """Class for processing epub. This class is supposed to be the parent of another class that
    overrides make_changes_to_temp method.

    Create instance of your class that extends EpubProcessor and overrides make_changes_to_temp().
    Then running process_epub() method of instance of your class will do the implemeted processing
    in make_changes_to_temp() and save new .epub file with name "processed_{name of your old epub}".

    Attributes
    ----------
    _fname : str
        path to the ebup file
    _temp_directory : str
        name of folder where the contents of epub are extracted
    _new_fname : str
        path to new epub file that will be created while running process_epub()

    Methods
    -------
    extract_to_temp()
        Extract contents of .epub file to temporary folder.
    make_changes_to_temp()
        Override this method in the subclass of this class.
    temp_to_epub()
        Zip contents of temporaty folder to .epub file.
    process_epub()
        You should run this method on the intance of the class extending this class.
    """
    
    def __init__(self, fname: str) -> None:
        """Initialize EpubProcessor instance with path to epub and name of temporary folder.

        Parameters
        ----------
        fname : str
            path to the .epub file
        """
        assert fname.endswith('.epub')
        self._fname = fname
        self._temp_directory = f"temp_extracted_{random.randint(10**19, 10**20-1)}"
        splited_fname = fname.rsplit(os.path.sep, maxsplit=2)
        splited_fname[-1] = "processed_" + splited_fname[-1]
        self._new_fname = os.path.sep.join(splited_fname)

    def extract_to_temp(self):
        """Extract the contents of .epub file to _temp_directory
        """
        shutil.unpack_archive(self._fname, self._temp_directory, format='zip')

    def make_changes_to_temp(self):
        """Has to be overriding by child class.
        """
        pass

    def temp_to_epub(self):
        """Zip _temp_directory into .epub
        The created epub file has the following name: "processed_" + initial name of epub 
        """
        with zipfile.ZipFile(self._new_fname, 'w') as zip_arc:
            for directory, _, files in os.walk(self._temp_directory):
                arc_directory = os.path.relpath(directory, self._temp_directory)
                zip_arc.write(directory, arc_directory)
                for file_ in files:
                    path = os.path.join(directory, file_)
                    zip_arc.write(path, os.path.relpath(path, self._temp_directory))

        shutil.rmtree(str(self._temp_directory))

    def process_epub(self):
        """Extract process and zip contents of .epub file.
        """
        self.extract_to_temp()
        self.make_changes_to_temp()
        self.temp_to_epub()
