import glob
import os
from os.path import normcase
frame_width = 640
frame_height = 328
first_output_file = 'raw_output.txt'
final_output_file = 'processed_output.txt'
output_path = 'runs/detect/exp/labels/'
classes = ['annelida', 'arthropoda', 'cnidaria', 'echinodermata', 'fish', 'mollusca', 'other-invertebrates', 'porifera', 'unidentified-biology']
with open(first_output_file , 'w') as f_out:
    for txt_file in glob.glob(output_path + '*.txt'):
        title = os.path.basename(txt_file)
        title = title[8:]
        title = title[:len(title)-4]
        with open(txt_file, 'r') as f_in:
            lines = f_in.readlines()
            f_out.write(title + " " + lines[0])
with open(final_output_file, 'w') as ff_out:
    with open(first_output_file, 'r') as pf_in:
      lines = pf_in.readlines()
      for line in lines:
        tokens = line.split()
        frame = str(int(tokens[0]))
        animal = classes[int(tokens[1])]
        x_bound_left = str(tokens[2]) #x1
        y_bound_top = str(tokens[3]) #y1
        x_bound_right = str(float(tokens[4]) + float(tokens[2])) #x2
        y_bound_bottom = str(float(tokens[5]) + float(tokens[3])) #y2
        ff_out.write(frame + " " + animal + " " + x_bound_left + " " + x_bound_right + " " + y_bound_top + " " + y_bound_bottom + "\n")