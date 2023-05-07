import subprocess
import os
vids = []
choice = ""
model = "seventh.pt"
while choice != "quit":
    print("Enter video to process, enter quit to quit (must be valid video in folder)")
    choice = input()
    if choice == "quit":
        break
    elif os.path.exists(os.path.join("./videos", choice)) == False:
        print("path does not exist")
    else:
        vids.append(choice)
print(vids)

for video in vids:
    print("curr vid: " + video)
    subprocess.run('python', 'detect.py', '--model', model, '--source', video, '--save-txt')
    subprocess.run('python', 'dataExp.py')