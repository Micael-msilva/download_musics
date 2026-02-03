
def generate_zip(files_path="../musics", zip_name="musics.zip"):
    import os
    import zipfile

    zip_path = os.path.join(files_path, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(files_path):
            for file in files:
                if file != zip_name: 
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, files_path)
                    zipf.write(file_path, arcname)
    # delete_musics(files_path)
    return zip_path

def delete_musics(files_path="../musics"):
    import os
    import shutil
    # Removes all music files less the zip file
    for item in os.listdir(files_path):
        item_path = os.path.join(files_path, item)
        if os.path.isfile(item_path) and item != "musics.zip":
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
