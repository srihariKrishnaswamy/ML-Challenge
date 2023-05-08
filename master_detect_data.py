import subprocess
import os
import shutil
vids = []
choice = ""
model = "./iterations/seventh.pt"
output_folder = "./output"
def_output_folder = "out"
full_output_path = ""
yolo_output_path_log = "output_path_log.txt"
def determine_output_folder(): #assumes that the base output folder exists, creates new output folder
  output_list = os.listdir(output_folder)
  max = 0
  for folder in output_list:
      if len(folder) == len(def_output_folder):
          max = 2
      else:
          folder_num = int(folder[3:len(folder)])
          if folder_num >= max:
              max = folder_num + 1
  if max == 0:
      new_output_folder = os.path.join(output_folder,def_output_folder + "/")
  else:
      new_output_folder = os.path.join(output_folder,def_output_folder + str(max) + "/")
  return new_output_folder
while choice != "quit":
  print("Enter video to process, enter quit to quit (must be valid video in folder)")
  choice = input()
  if choice == "quit":
      break
  elif os.path.exists(os.path.join("./videos", choice)) == False:
      print("path does not exist")
  else:
      vids.append(os.path.join("./videos", choice))
print(vids)
for video in vids:
  print("curr vid: " + video)
  proc1 = subprocess.Popen(['python', 'detect.py', '--weights', model, '--source', video, '--save-txt'])
  proc1.communicate()
  proc2 = subprocess.Popen(['python', 'dataExp.py'])
  proc2.communicate()
#video processing done and videos & excel file generated
if os.path.exists(output_folder) == False:
  os.mkdir(output_folder)
full_output_path = determine_output_folder()
os.mkdir(full_output_path)
print("OUTPUT FOLDER: " + full_output_path)
# moving appropriate files
shutil.move("detections.xlsx", full_output_path)
folders = []
with open(yolo_output_path_log, 'r') as yolo_output:
  for line in yolo_output.readlines():
      folders.append(line.strip())
os.remove(yolo_output_path_log)
print("FOLDERS: ")
print(folders)
for i in range(len(folders)):
  vid = os.path.join(folders[i], os.listdir(folders[i])[0])
  shutil.move(vid, full_output_path)
  os.rmdir(folders[i])