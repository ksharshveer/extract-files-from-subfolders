import os, shutil
from pathlib import Path

# To store program execution details
logs = [] 


def get_str_of_backslash_escaped_path_object(path):
  """Returns a string of file/folder path replacing each backslash with 2 backslashes"""
  return str(Path(path)).replace("\\", "\\\\")


def read_list_from_file(filename):
  """Returns a list of lines read given a file"""
  filename = get_str_of_backslash_escaped_path_object(filename)
  mylist = []

  my_file = open(filename, "r")
  mylist = my_file.read().split("\n")
  mylist.pop()
  my_file.close

  return mylist


def write_list_in_file(my_list, filename, mode="a+"):
  """Appends/Overwrites list items as lines given a list, file, and 
  write mode (use a+ to append, or w+ to overwrite)"""
  filename = get_str_of_backslash_escaped_path_object(filename)

  my_file = open(filename, mode)

  for item in my_list:
    my_file.write(str(item)+ "\n")

  my_file.close

 
def find_long_dirs(src, des, dirslist):
  """Returns list of chained """
  src = Path(src)
  des = Path(des)
  directory_items = os.listdir(src)
  is_dir_empty = True

  for item in directory_items:

    if (os.path.isdir(src.joinpath(item))):
      find_long_dirs(src.joinpath(item), des, dirslist)
      is_dir_empty = False

  if (is_dir_empty):
    dirslist.append(src)

  return dirslist


def extract_files(src, des, current_dir):
  """Moves files from given source folder to given destination folder"""
  src = Path(src)
  des = Path(des)
  current_dir = Path(current_dir)
  directory_items = os.listdir(src)

  for item in directory_items:
    joined_src = src.joinpath(item)
    joined_des = des.joinpath(item)

    if (os.path.isfile(joined_src)):
      klist.append(current_dir.joinpath(item))
      vlist.append(joined_src)

      try:
        os.rename(joined_src, joined_des)
        logs.append("Moved "+str(joined_src)+" to "+str(joined_des))

      except Exception as e:
        klist.pop
        vlist.pop
        logs.append("Failed to move "+str(joined_src)+" to "+str(joined_des))

    if (os.path.isdir(joined_src)):
      extract_files(joined_src, des, current_dir)


def delete_dirs(my_list):
  """Deletes directories from a given list of directories if no files exist in them"""
  for item in my_list:
    path_item = Path(item)

    if (len(os.listdir(path_item)) == 0):
    
      try:
        os.removedirs(path_item)
        logs.append("Deleting "+str(path_item))
    
      except Exception as e:
        logs.append(str(e))
    
    else:
      logs.append("Could not delete folder "+str(item)+" because it has file(s)")


def create_dirs(my_list):
  """Creates directories from a list of paths of directories"""
  for item in my_list:
    path_item = Path(item)

    try:
      if (not (os.path.isdir(path_item))):
        os.makedirs(path_item)
        logs.append("Creating "+str(path_item))
    
    except Exception as e:
      logs.append(str(e))


def restore_files():
  for item1, item2 in zip(klist, vlist):

    try:
      os.rename(get_str_of_backslash_escaped_path_object(item1), get_str_of_backslash_escaped_path_object(item2))
      logs.append("Moved "+str(item1)+" to "+str(item2))

    except Exception as e:
      logs.append("Failed to move "+str(item1)+" to "+str(item2)+str(e))


if __name__ == '__main__':
  
  # lists to contain information of files moved and deleted folders
  klist = []
  vlist = []
  dirslist = []

  # Restore folder and file name
  restore_folder = "....restore"
  restore_py_file = "restore.py"
  
  # Set current folder as source for program execution, all files
  #  in this folder/subfolders will be extracted to this folder
  current_file_path = Path(os.path.realpath(__file__))

  source_folder = current_file_path.parent
  logs.append("\nSource folder : "+str(source_folder))

  destination_folder = source_folder
  logs.append("Destination folder : "+str(destination_folder))

  # Set restore folder location
  default_restore_folder = source_folder.joinpath(restore_folder)
  logs.append("Restore folder : "+str(default_restore_folder))

  # proper filenames to be used for reading/writing files
  chained_directories_list_file = get_str_of_backslash_escaped_path_object(default_restore_folder.joinpath("dirslist.txt"))
  keys_list_file = get_str_of_backslash_escaped_path_object(default_restore_folder.joinpath("klist.txt"))
  values_list_file = get_str_of_backslash_escaped_path_object(default_restore_folder.joinpath("vlist.txt"))
  logs_file = get_str_of_backslash_escaped_path_object(source_folder.joinpath("logs.txt"))

  try:

    if (os.path.isdir(default_restore_folder)):
      logs.append("\nRestore folder found. Starting restoration...")
      
      try:
        logs.append("\nReading data from restore files...")

        dirslist = read_list_from_file(chained_directories_list_file)
        klist = read_list_from_file(keys_list_file)
        vlist = read_list_from_file(values_list_file)

        if ((len(dirslist) == 0) or (len(klist) == 0) or (len(vlist) == 0)):
          raise Exception("\nExpected at lease one item in restoration file(s), but found"+
          "\nItems in "+chained_directories_list_file+" : "+len(dirslist)+
          "\nItems in "+keys_list_file+" : "+len(klist)+
          "\nItems in "+values_list_file+" : "+len(vlist))

        logs.append("Data has been read from restore files.")

      except Exception as e:
        halt_msg = "Halting execution, insufficient restoration data."
        logs.append(halt_msg+str(e))
        raise Exception(halt_msg,e)

      
      logs.append("\nCreating directories for files restoration...")
      create_dirs(dirslist)
      logs.append("Directories created.")
      
      logs.append("\nMoving files for restoration...")
      restore_files()
      logs.append("Files are now restored.")

      logs.append("\nDeleting restore folder...")
      shutil.rmtree(default_restore_folder)
      logs.append("Done.")

    else:

      logs.append("Scanning directories...")
      dirslist = find_long_dirs(source_folder, destination_folder, dirslist)

      logs.append("Scanning directories complete.\n\nExtracting files...")
      extract_files(source_folder, destination_folder, source_folder)

      logs.append("Files extraction complete.\n\nDeleting empty remaining directories...")
      delete_dirs(dirslist)

      logs.append("Empty directories deletion complete.\nCreating restore files")
      
      try:
        os.makedirs((default_restore_folder))

      except Exception as e:
        logs.append(str(e))

      write_list_in_file(dirslist, chained_directories_list_file, "w+")
      write_list_in_file(klist, keys_list_file, "w+")
      write_list_in_file(vlist, values_list_file, "w+")

      logs.append("Restore files created. Do not delete or move restore files/folder and program file")
      logs.append("\nYou can restore your files by executing the program again.")
      
  except Exception as e:
    logs.append("Severe error.\n"+str(e))

  finally:
    write_list_in_file(logs,logs_file)
