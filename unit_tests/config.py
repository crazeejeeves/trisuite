import os
import tempfile
test_files_folder_in = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TestFiles")
#for tests that write files
test_files_folder_out = tempfile.gettempdir()
