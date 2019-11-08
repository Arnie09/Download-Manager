import os
from os import walk
import sys
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


'''

0. Image files: jpeg,jpg,png,svg,gif
1. Videos: mp4,mpeg4,3gp,avi,mkv,
2. Docs: xlsx,docx
3. PDF
4. Compressed files: rar,iso
5. Audio: mp3,wav
6. Miscellaneous

'''

FILEEXTENSIONS = [["jpeg","jpg","png","svg","gif"],["mp4","mpeg","mpeg4","3gp","avi","mkv"],["xlsx","docx","pptx"],["pdf"],["rar","iso","7z"],["mp3","wav"]]
dictionaryFolder = {0:"Images",1:"Videos",2:"Docs",3:"PDFs",4:"CompressedFiles",5:"Audio",6:"Miscellaneous"}

def give_category(filename):
    index_of = filename.rfind('.')
    extension = filename[index_of+1:]

    for index,filetypes in enumerate(FILEEXTENSIONS):
        for indi_extensions in filetypes:
            if indi_extensions == extension:
                return index
    return 6


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        event_type = {event.event_type}
        path = {event.src_path}



if __name__ == "__main__":

    user_download_folder_path = input("Please enter the path of the download folder in your pc. ")

    # code to create the basic categories of folders that we need. 
    for categories in dictionaryFolder:
        os.makedirs(os.path.join(user_download_folder_path,dictionaryFolder[categories]))

    # function that works on the aldready present files in the folder. 
    files = []
    for (dirpath, dirnames, filenames) in walk(user_download_folder_path):
        files.extend(filenames)
        break
    
    for single_file in files:
        destination_folder_type = give_category(single_file)
        foldername = dictionaryFolder[destination_folder_type]
        shutil.move(os.path.join(user_download_folder_path,single_file), os.path.join(user_download_folder_path,foldername,single_file))

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=user_download_folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()