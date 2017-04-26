import os
import shutil
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import pip

WORKING_DIR = '/code/morecode'

IGNORE_FILES_AND_FOLDERS = ['ve', '.git']
IGNORE_EXTENSION = ['.pyc']


def ignore_folders(path, contents):
    if os.path.basename(path) in IGNORE_FILES_AND_FOLDERS:
        return contents
    else:
        files_to_ignore = []
        for filename in contents:
            if filename in IGNORE_FILES_AND_FOLDERS:
                files_to_ignore.append(filename)
            if os.path.splitext(filename)[1] in IGNORE_EXTENSION:
                files_to_ignore.append(filename)

        return files_to_ignore

# Create release directory
with TemporaryDirectory() as temp_dir:
    release_dir = os.path.join(temp_dir, 'release')

    print(release_dir)
# Copy everything into it
    shutil.copytree(WORKING_DIR, release_dir, ignore=ignore_folders)

# Run requirements putting it into the release directory
    print(pip.__file__)
    pip.main(['install', '-t', release_dir, '-r', os.path.join(release_dir, 'requirements.txt')])


# Zip up the release directory
    with ZipFile(os.path.join(WORKING_DIR, 'release.zip'), 'w') as zfile:

        file_list = os.walk(release_dir)
        for path, folders, files in file_list:

            for file in files:

                truncated_path = path.replace(release_dir, '')

                source_file = os.path.join(path, file)
                arc_file = os.path.join(truncated_path, file)

                if arc_file[0] == os.sep:
                    arc_file = arc_file[1:]

                zfile.write(source_file, arc_file)




# shove it up on Lambda
