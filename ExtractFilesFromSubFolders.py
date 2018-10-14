import os

klist = []
vlist = []
dirslist = []

restore_py_file = "restore.py"

# ################## SET UP SOURCE AND DESTINATION FOLDER ##################
# example: source_folder = "D:\dummy\folder"    # note: backslashes are single and none at end
# source_folder = "Z:\Learning"
destination_folder = source_folder

# ################## LOCATION TO STORE RECOVERY FILES(leave unchanged) ##################
restore_folder = "....restore"
default_restore_folder = os.path.join(destination_folder, restore_folder)

# ################## READ FILE ##################
def read_list_from_file(filename):
  mylist = []
  try:
    my_file = open(filename, "r")
    mylist = my_file.read().split()
    my_file.close
  except Exception as e:
    print(e)
  return mylist

# ################## OVERWRITE FILE ##################
def overrite_list_in_file(my_list, filename):
  try:
    my_file = open(filename, "w")
    for item in my_list:
      my_file.write(str(item)+ "\n")
    my_file.close
  except Exception as e:
    print(e)

# ################## FIND DEEP DIRECTORIES ##################
def find_long_dirs(src, des):
  directory_items = os.listdir(src)
  no_dir = True
  for item in directory_items:
    if (os.path.isdir(os.path.join(src, item))):
      find_long_dirs(os.path.join(src, item), des)
      no_dir = False
  if (no_dir):
    dirslist.append(src)

# ################## MOVE FILES OUT OF FOLDERS ##################
def extract_files(src, des):
  directory_items = os.listdir(src)
  for item in directory_items:
    if (os.path.isfile(os.path.join(src, item))):
      klist.append(os.path.join(destination_folder, item))
      vlist.append(os.path.join(src, item))
      try:
        os.rename(os.path.join(src, item), os.path.join(des, item))
      except Exception as e:
        klist.pop
        vlist.pop
        print(e)
    if (os.path.isdir(os.path.join(src, item))):
      extract_files(os.path.join(src, item), des)

# ################## DELETE EMPTY DIRECTORIES ##################
def delete_dirs(my_list):
  for item in my_list:
    if (len(os.listdir(item)) == 0):
      try:
        os.removedirs(item)
      except Exception as e:
        print(e)

if __name__ == '__main__':
  
  try:
    if (os.path.isdir(default_restore_folder)):
      print("Restore folder found. Skipping execution\nDelete folder "+
      restore_folder+" at "+default_restore_folder+" and try again")
    else:
      find_long_dirs(source_folder, destination_folder)
      extract_files(source_folder, destination_folder)
      delete_dirs(dirslist)
      
      os.mkdir(default_restore_folder)
      overrite_list_in_file(klist, os.path.join(default_restore_folder, "klist.txt"))
      overrite_list_in_file(vlist, os.path.join(default_restore_folder, "vlist.txt"))
      overrite_list_in_file(dirslist, os.path.join(default_restore_folder, "dirslist.txt"))

      try:
        restore = open(os.path.join(default_restore_folder, restore_py_file), "w")
        restore.write("import os" + "\n\n" +

        "klist = []" + "\n" +
        "vlist = []" + "\n" +
        "dirslist = []" + "\n\n" +

        "# ################## SET UP SOURCE AND DESTINATION FOLDER ##################" + "\n" +
        "source_folder = \"" + str(source_folder) + "\"\n" +
        "destination_folder = \"" + str(destination_folder) + "\"\n\n" +

        "default_restore_folder = \""+ str(default_restore_folder) +"\"\n\n"

        "# ################## READ FILE ##################" + "\n" +
        "def read_list_from_file(filename):" + "\n" +
        "  mylist = []" + "\n" +
        "  try:" + "\n" +
        "    my_file = open(filename, \""+"r"+"\")" + "\n" +
        "    mylist = my_file.read().split()" + "\n" +
        "    my_file.close" + "\n" +
        "  except Exception:" + "\n" +
        "    print(\"something went wrong reading \" + filename)" + "\n" +
        "  return mylist" + "\n\n" +

        "# ################## CREATE EMPTY DIRECTORIES ##################" + "\n" +
        "def create_dirs(my_list):" + "\n" +
        "  for item in my_list:" + "\n" +
        "    try:" + "\n" +
        "      if (not (os.path.isdir(item))):" + "\n" +
        "        os.makedirs(item)" + "\n" +
        "    except Exception:" + "\n" +
        "      print(\"something went wrong creating \" + item)" + "\n\n" +

        "# ################## RESTORE FILES ##################" + "\n" +
        "def restore_files():" + "\n" +
        "  for item1, item2 in zip(klist, vlist):" + "\n" +
        "    try:" + "\n" +
        "      os.rename(item1, item2)" + "\n" +
        "    except Exception:" + "\n" +
        "      print(\"something went wrong restoring \" + item2 + \" to \" + item1 + \" place\")" + "\n\n" +

        "if __name__ == '__main__':" + "\n\n" +
          
        "  dirslist = read_list_from_file(os.path.join(default_restore_folder, \"dirslist.txt\"))" + "\n" +
        "  klist = read_list_from_file(os.path.join(default_restore_folder, \"klist.txt\"))" + "\n" +
        "  vlist = read_list_from_file(os.path.join(default_restore_folder, \"vlist.txt\"))" + "\n\n" +

        "  if (len(dirslist) != 0) :" + "\n" +
        "    create_dirs(dirslist)" + "\n" +
        "    if ((len(klist) != 0) and (len(vlist) != 0)):" + "\n" +
        "      restore_files()" + "\n\n" +
        "  print(\"\\nFinished!\")"
        )
        restore.close
      except Exception as e:
        print("something went wrong writing restore file\n"+e)
        
      print("\nYou can restore your files by running " + restore_py_file +
      " at location " + default_restore_folder + "\n\nFinished!")
      
  except Exception as e:
    print("Operation failed.\n"+e)
