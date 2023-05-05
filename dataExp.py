import glob
import os
import xlsxwriter
from os.path import normcase

frame_width = 640
frame_height = 328
first_output_file = 'raw_output.txt'
second_output_file = 'processed_output_1.txt'
output_path = 'runs/detect/exp/labels/'
classes = ['annelida', 'arthropoda', 'cnidaria', 'echinodermata', 'fish', 'mollusca', 'other-invertebrates', 'porifera', 'unidentified-biology']
sourceVid = ""
with open("sourceVid.txt", "r") as sv:
    sourceVid = sv.readline()
with open(first_output_file , 'w') as f_out:
    for txt_file in glob.glob(output_path + '*.txt'):
        title = os.path.basename(txt_file)
        title = title[8:]
        title = title[:len(title)-4]
        with open(txt_file, 'r') as f_in:
            lines = f_in.readlines()
            for line in lines:
                if line != "":
                    f_out.write(sourceVid + " " + title + " " + line)
with open(second_output_file, 'w') as ff_out:
    with open(first_output_file, 'r') as pf_in:
      lines = pf_in.readlines()
      for line in lines:
        tokens = line.split()
        source = tokens[0]
        frame = str(int(tokens[1]))
        animal = classes[int(tokens[2])]
        x_bound_left = str(tokens[3]) #x1
        y_bound_top = str(tokens[4]) #y1
        x_bound_right = str(float(tokens[5]) + float(tokens[3])) #x2
        y_bound_bottom = str(float(tokens[6]) + float(tokens[4])) #y2
        ff_out.write(source + " " + frame + " " + animal + " " + x_bound_left + " " + x_bound_right + " " + y_bound_top + " " + y_bound_bottom + "\n")
os.remove(first_output_file)
os.remove("sourceVid.txt")

# write to excel from txt
data = []
excelName = "detections.xlsx"
with open(second_output_file, 'r') as sf_in:
    lines = sf_in.readlines()
    for line in lines:
        dict = {}
        tokens = line.split()
        dict['vid'] = tokens[0]
        dict['frame'] = tokens[1]
        dict['class'] = tokens[2]
        dict['x_left'] = tokens[3]
        dict['x_right'] = tokens[4]
        dict['y_up'] =  tokens[5]
        dict['y_low'] = tokens[6]
        data.append(dict)

workbook = xlsxwriter.Workbook(excelName)
worksheet = workbook.add_worksheet("detections")
worksheet.write(0,0,"Source Video")
worksheet.write(0,1,"Classification")
worksheet.write(0,2,"X Bound, Left")
worksheet.write(0,3,"X Bound, Right")
worksheet.write(0,4,"Y Bound, Upper")
worksheet.write(0,5,"Y Bound, Lower")
for index, entry in enumerate(data):
    worksheet.write(index+1, 0, entry["vid"])
    worksheet.write(index+1, 1, entry["frame"])
    worksheet.write(index+1, 2, entry["class"])
    worksheet.write(index+1, 3, entry["x_left"])
    worksheet.write(index+1, 4, entry["x_right"])
    worksheet.write(index+1, 5, entry["y_up"])
    worksheet.write(index+1, 6, entry["y_low"])
workbook.close()