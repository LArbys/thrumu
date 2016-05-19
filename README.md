# ThruMu

This repo is a test bed for a low-level, image-based through-going muon selection.

The goal is isolating through-going muons that will provide a way to study data vs. MC agreement of ADC values.  The sample will allow a comparison versus different parameters such as wire plane and track angle.

With such metrics in hand, hopefully we can begin the path towards data/mc agreement that will lead to better network performances on data.

## Dependencies

* numpy
* ROOT
* LArCV
* larlite/larsoft eventually when dealing with MC and reco. parameters


## Setup

Going to build this as a submodule of LArCV, to be located in the app folder of LArCV.

First, get a copy of LArCV, set it up and build it.

Next clone this repository in the LArCV/app folder.

Then build it. (Nothing in it right now)