## Test scripts for boundary through-going muon tagger

### Processing Chain Notes

* gen_wire_matches.py: produces list of match triplets for top, bottom, upstream, and downstream. These are saved in pickle files for the use in later stages.
* tag_boundary_hits.py: takes in LArCV image and applies match triplets to find boundary crossings.  produces a hit image marking pixels that have enough charge and are consistent with a boundary crossing. hit image saved as numpy array in saves numpy binary file or next stage.
* cluster_imghits.py: uses scikit-learn to do clustering. DBSCAN seemed to work well enough.
* find_tracks.py: connects combination of clusters to find tracks in a plane. saves candidate tracks.
* [next: filter through candidate tracks, checking consistency between planes.  comes up with final candidate 3D tracks.]