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

FILEEXTENSIONS = [["jpeg","jpg","png","svg","gif","psd"],["mp4","mpeg","mpeg4","3gp","avi","mkv"],["xlsx","docx","pptx","txt"],["pdf"],["rar","iso","7z","aar","jar","gz","xz","deb"],["mp3","wav"],["opdownload"]]
dictionaryFolder = {0:"Images",1:"Videos",2:"Docs",3:"PDFs",4:"CompressedFiles",5:"Audio",7:"Miscellaneous"}
temp_list = []
user_download_folder_path = ""

def move_file(source_path,destination_path):
    shutil.move(source_path,destination_path)


def give_category(filename):
    index_of = filename.rfind('.')
    extension = filename[index_of+1:]

    for index,filetypes in enumerate(FILEEXTENSIONS):
        for indi_extensions in filetypes:
            if indi_extensions == extension:
                return index
    return 7


class MyHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        path_file = event.src_path
        print(path_file)
        if path_file not in temp_list:
            temp_list.append(path_file)
            filename = path_file[path_file.rfind('/')+1:]
            newFilename = filename.replace(" ","_")
            print(filename,newFilename)
            extension = give_category(path_file)
            if extension!=6:
                foldername = dictionaryFolder[extension]
                move_file(os.path.join(user_download_folder_path,filename), os.path.join(user_download_folder_path,foldername,newFilename))

if __name__ == "__main__":

    user_download_folder_path = input("Please enter the path of the download folder in your pc: ")

    # code to create the basic categories of folders that we need. 
    try:
        for categories in dictionaryFolder:
            os.makedirs(os.path.join(user_download_folder_path,dictionaryFolder[categories]))
    except:
        pass

    # function that works on the aldready present files in the folder. 
    files = []
    for (dirpath, dirnames, filenames) in walk(user_download_folder_path):
        files.extend(filenames)
        break
    
    for single_file in files:
        destination_folder_type = give_category(single_file)
        foldername = dictionaryFolder[destination_folder_type]
        move_file(os.path.join(user_download_folder_path,single_file), os.path.join(user_download_folder_path,foldername,single_file))

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