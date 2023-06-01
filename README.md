# ML-Challenge: SeaScout

This progam is a deepsea organisim detector and classifier for the 2023 MATE Machine Learning Challenge.

Developed by Srihari Krishnaswamy and Vivian Wang, part of the Underwater Remotely Operated Vehicles Team at the University of Washington.

### Project Overview
SeaScout uses a Yolov5 object detection model for detections and classifications. Specifically, training was done based on the [MBARI Monterey Bay Benthic Object Detector](https://zenodo.org/record/5539915), also found in FathomNet's [Model Zoo](https://github.com/fathomnet/models).
In Training, some layers of the Neural Network were left frozen, but enough layers were unfrozen to get optimal model performance. The model was trained on data from last year's [Deepsea-Detector](https://github.com/ShrimpCryptid/deepsea-detector) project, but the dataset was expanded to include more data from [Fathomnet](https://fathomnet.org/fathomnet/#/).
The training data for our model can be found in our [Roboflow](https://universe.roboflow.com/uwrov-2023-ml-challenge/2023-mate-ml-challenge) project.

### Getting Started
#### Downloading the Project
This project requires python 3.10 or higher. It also uses Git LFS to store files such as our models and base videos.

Run the following lines in a command terminal to clone the repository, initialize LFS and install requirements:
```git clone https://github.com/srihariKrishnaswamy/ML-Challenge.git
cd ML-Challenge
git lfs install; git lfs fetch; git lfs pull
pip3 install -qr requirements.txt
```

#### Running the UI
To run the project's UI, run this command: 

```python ui.py```

<img width="920" alt="image" src="https://github.com/srihariKrishnaswamy/ML-Challenge/assets/86600946/e9427705-4b30-42de-8040-52ae43e50524">

After the UI starts, you are free to process videos. In order for videos to be processed, they have to be moved into the videos folder inside the project folder. Similarly, in order for a model to be used, it has to be in the iterations folder inside the main project folder. 
The user can process multiple videos and log them onto the same excel file, which will appear in the latest folder inside the output folder after processing is finished. Processed videos will appear here as well. The user is free to kill the video processing at any point, but if this happens, no excel file or processed videos will be generated for the user to see.

#### Running in the Command Line/Terminal or Google Colab
The UI for our project is a wrapper for a python script which invokes object detection and detection logging. In order to run this script on its own, run the following command:

```python master_detect_data.py --videos FIRST_VIDEO_HERE.mp4 SECOND_VIDEO_HERE.mp4 --model MODEL_HERE.pt```

Just as in the UI, the entered videos and model must be valid and in the videos or iterations (NOT MODELS) folder respectively. For instance, a valid statement running the script would be:

```python master_detect_data.py --videos descent.mp4 seafloor.mp4 --model SeaScout.pt```

since the file SeaScout.pt is in the iterations folder, and each of the .mp4 files are in the videos folder.

### Resources:
Dataset: [Roboflow project](https://universe.roboflow.com/uwrov-2023-ml-challenge/2023-mate-ml-challenge)

Model Training Notebook: [Colab Notebook](https://github.com/srihariKrishnaswamy/ML-Challenge/blob/main/notebooks/SeaScout_Model_Train.ipynb)

Additional in-Depth Documentation: [Documentation](https://github.com/srihariKrishnaswamy/ML-Challenge/blob/main/documentation/Documentation.md)
### Acknowledgements: 
We would like to thank the following people and organizations: 
- [MATE](https://materovcompetition.org/) and [NOAA Ocean Exploration](https://oceanexplorer.noaa.gov/) for hosting this competition
- The [World Register of Marine Species (WoRMS)](https://www.marinespecies.org/), [Fathomnet](https://fathomnet.org/fathomnet/#/) and [NOAA Ocean Exploration](https://oceanexplorer.noaa.gov/) for providing additional data
- Peyton Lee, Neha Nagvekar and last year's [Deepsea-Detector](https://github.com/ShrimpCryptid/deepsea-detector) project for advice and a large portion of our dataset
