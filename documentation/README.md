# SeaScout: An underwater organisim detector and classifier

Student Contributors

| Name | Role |
| Srihari Krishnaswamy | Model Training, User Interface, App Functionality |
| Vivian Wang | Annotation, Model Training |

## Table of Contents
- Problem Description
- Data Description
- Model 
- UI
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

## Model 
