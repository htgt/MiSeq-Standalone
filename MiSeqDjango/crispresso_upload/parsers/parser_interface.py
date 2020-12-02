"""Interface for the extraction of data from the inputted file."""
import tarfile

from concurrent.futures import ThreadPoolExecutor

class ParserInterface:
    """Interface for the extraction of data from the inputted file."""
    def load_directory(self, file: tarfile, uploaded_file_path) -> dict:
        """Load in the tar file for extracting well information."""

    def extract_well_information(self, file, tar_info) -> dict:
        """Extract the tar file into memory and load the information into a dict"""

    def chunkify_tar_file(self, file: tarfile) -> dict:
        """Split the tar file up into chunks to parallelise access to the data"""

        with ThreadPoolExecutor(5) as executor:
            futures = [
                executor.submit(self.extract_well_information, file, member)
                for member in file.getmembers()
                ]

        array = [f.result() for f in futures]

        return self.reconstruct_file_structure(array)

    def reconstruct_file_structure(self, array) -> dict:
        """Takes in an array and reconstructs it into the
        expected format depending on the specific implementation"""
