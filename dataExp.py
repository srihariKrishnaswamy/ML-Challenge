import glob
import os
# Path to the output file
output_file = 'output.txt'
# Path to the directory containing the output files
output_path = 'runs/detect/exp'

# Open the output file for writing
with open(output_file, 'w') as f_out:
    f_out.write('ACCESSING OUTPUT FILE')
    # Loop through all the output files
    for txt_file in glob.glob(os.path.join(output_path, '*.txt')):
        # Read the contents of the file
        with open(txt_file, 'r') as f_in:
            line = f_in.readlines()

            class_id, *bbox = line.strip().split()

            # Convert the class ID and bounding box coordinates to the desired format
            class_id = int(class_id)
            bbox = list(map(float, bbox))

            # Write the class and bounding box information to the output file
            f_out.write(f'Class ID: {class_id}, Bounding box: {bbox}\n')
