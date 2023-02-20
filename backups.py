import shutil
import tarfile
import os
import datetime

# Define backup settings
source = '/path/to/your/source'  # Replace with the path to your source file or directory
destination = '/path/to/your/backup'  # Replace with the path to your backup directory
filename = 'backup-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.tar.gz'

# Create a backup archive
with tarfile.open(os.path.join(destination, filename), "w:gz") as tar:
    tar.add(source, arcname=os.path.basename(source))

# Copy the backup archive to a remote destination (optional)
shutil.copy(os.path.join(destination, filename), 'user@yourserver:/path/to/remote/destination')
