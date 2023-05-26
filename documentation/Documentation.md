# SeaScout: An underwater organisim detector and classifier

Student Contributors

- Srihari Krishnaswamy: Model Training, User Interface, App Functionality
- Vivian Wang: Annotation, Model Training

## Table of Contents
- Problem Description
- Data Description
- Object Detection Model 
- UI Description
- Architecture Diagram
- Results
- Limitations
- Ackowledgements and Resources
- Video Demo/Explaination

## Problem Description
We built our model and the sorrounding scripts to fulfill [MATE's 2023 Computer Coding Challenge](https://files.materovcompetition.org/2023/2023-OER-MATE-ROV-Computer-Coding-Challenge_FINAL.pdf).
This tasked us with identifiying marine organisims in seafloor footage collected by Remotely Operated Vehicles.

The competition was divided into two levels
- Level 1: Classify and place bounding boxes around organisms in the NOAA ship Okeanos Explorer remotely operated clips provided
- Level 2: Identify the organisims in (a provided) broad morphological category and draw a bounding box for each instance

## Data Description
The classes that our project identifies are summarized below: 

| Class | Description |
| -------- | -------- |
| Annelids | Segmented worms |
| Arthropods | Crustaceans (shrimp, crabs, copepods, etc.), pycnogonids (sea spiders) |
| Cnidarians | Sea jellies, corals, anemones, siphonophores |
| Echinoderms | Sea stars, brittle stars, basket stars, urchins, sea cucumbers, sea lilies, sand dollars |
| Mollusca | Cephalopods (squid, octopi, cuttlefish), gastropods (sea snails and slugs), bivalves, aplacophorans (worm-like mollusks) |
| Porifera | Sponges, glass sponges |
| Other Invertebrates | Includes tunicates (sea squirts and larvaceans), ctenophores, many worm phyla |
| Vertebrates: Fishes | Cartilaginous, bony, and jawless fishes |
| Unidentified Biology | Unidentified Biology |

We based our dataset off last year's deepsea-detector project's dataset. We ended up adding a lot of images since at first, our model would label almost everything as fish. This was because of the large concentration of the species in the previous dataset. We added images from the [World Register of Marine Species](www.marinespecies.org), and had to relabel some of their annotations using Robolfow. 
Our model was overfitting for a while during our training iterations, and would still label almost everything as fish or cnidaria, but we were able to solve this issue by tweaking some training parameters, as discussed in the next section.

## Object Detection Model 
Our project uses a Yolov5 object detection model due to its popularity in the CV field and accuracy. We decided to train a pre-trained yolov5 model from FathomNet, specifically the [MBARI Monterey Bay Benthic YOLOv5x model](https://zenodo.org/record/5539915). This was because of the relatively small size of our dataset compared to those of other similar objectives, so we wanted to leverage the fact that the weights of the base model would already be tuned to detect underwater organisims. 

The most accurate model we produced (located in the iterations folder of our project) was the result of us freezing (keeping the weights of) 18 layers of the MBARI model, and traing the rest of the layers with our data. It was important to find a good balance of layers to freeze and unfreeze, since unfreezing all of the layers could detract from accuracy since we would have abandonded the weights from the MBARI model. On the flip side, unfreezing less layers would allow our dataset to create less of an impact on the model's weights.

Our model was trained for 14 epochs, and all of our training specs are available in our [Model Training Colab Notebook](https://github.com/srihariKrishnaswamy/ML-Challenge/blob/main/notebooks/SeaScout_Model_Train.ipynb). 

As mentioned, we faced some issues with overfitting while trying to find the optimal model with our dataset, but this was mitigated mainly by changing our number of epochs in training. We strived to create the most accurate model we could with the data we could find, but there are still some inconsistencies with the model's accuracy. Regardless, we still hold that it provides value with its detections and labels. 

## UI Description
The UI for SeaScout was written with Tkinter. The UI for our project allows the user to enter multiple videos to process, and logs the results for the detections for each video on one spreadsheet. After a sequence of videos are processed, the processed videos with bounding boxes are available in the latest folder in the output folder, along with the spreadsheet. The user can cancel video processing at any time, but if this is done, no spreadsheet or videos with bounding boxes will be generated. It is worth noting that the same detection and logging process can be run via the Terminal/CLI, and that the UI is simply a wrapper for this.

<img width="984" alt="image" src="https://github.com/srihariKrishnaswamy/ML-Challenge/assets/86600946/e3675a26-b0ac-4e41-9f90-6772d0339726">

After inference finishes, the detections are outputted to a spreadsheet located in the latest folder inside the output folder: 

<img width="1727" alt="image" src="https://github.com/srihariKrishnaswamy/ML-Challenge/assets/86600946/608be8b5-1cf0-4b07-823f-46dc9025fcff">

Processed video files will also be available in the same folder:

<img width="1093" alt="image" src="https://github.com/srihariKrishnaswamy/ML-Challenge/assets/86600946/39b7cc93-5871-48bc-9509-633246c5c0ef">

## Architecture Diagram
<img width="660" alt="image" src="https://github.com/srihariKrishnaswamy/ML-Challenge/assets/86600946/9b4a7eb6-c888-4eb4-8183-6ec44661e2ec">
