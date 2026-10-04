import shutil
import os
from datetime import datetime


source = "instance/forum.db"

backup_folder = "backups"

os.makedirs(
    backup_folder,
    exist_ok=True
)


date = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)


destination = (
    f"{backup_folder}/forum_{date}.db"
)


shutil.copy2(
    source,
    destination
)


print("Backup created:")
print(destination)