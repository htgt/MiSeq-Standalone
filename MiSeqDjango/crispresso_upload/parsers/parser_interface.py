"""Interface for the extraction of data from the inputed file."""
import os

from concurrent.futures import ThreadPoolExecutor


class ParserInterface:
    """Interface for the extraction of data from the inputed directory."""
   
    DEFAULT_DIR = '/home/ubuntu/dev/miseq-standalone/testFiles/Plate_test/'
   
    def load_directory(self, file_path) -> dict:
        """Load in the files for extracting well information."""

    def extract_well_information(self, filename) -> dict:
        """Extract the tar file into memory and load the information into a dict"""

    def chunkify_files(self, file_path) -> dict:
        """Split the tar file up into chunks to parallelise access to the data"""

        with ThreadPoolExecutor(5) as executor:
            futures = [
                executor.submit(self.extract_well_information, well_dir)
                for well_dir in self.get_file_paths(file_path)
                ]

        array = [f.result() for f in futures]

        return self.reconstruct_file_structure(array)

    def reconstruct_file_structure(self, array) -> dict:
        """Takes in an array and reconstructs it into the
        expected format depending on the specific implementation"""

    def get_file_paths(self, file_path):

        for d in os.listdir(file_path):
            yield os.path.join(file_path, d)
