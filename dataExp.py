import glob
import os

# Path to the directory containing the output files
output_path = 'runs/detect/exp'

# Loop through all the output files
for txt_file in glob.glob(os.path.join(output_path, '*.txt')):
    # Read the contents of the file
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    
    # Extract the class and bounding box information for each object
    for line in lines:
        # Split the line into class ID and bounding box coordinates
        class_id, *bbox = line.strip().split()
        
        # Convert the class ID and bounding box coordinates to the desired format
        class_id = int(class_id)
        bbox = list(map(float, bbox))
        
        # Print the class and bounding box information
        print(f'Class ID: {class_id}, Bounding box: {bbox}')