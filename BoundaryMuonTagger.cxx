#ifndef __BOUNDARYMUONTAGGER_CXX__
#define __BOUNDARYMUONTAGGER_CXX__

#include "BoundaryMuonTagger.h"
#include "DataFormat/EventImage2D.h"

namespace larcv {

  static BoundaryMuonTaggerProcessFactory __global_BoundaryMuonTaggerProcessFactory__;

  BoundaryMuonTagger::BoundaryMuonTagger(const std::string name)
    : ProcessBase(name)
  {}
    
  void BoundaryMuonTagger::configure(const PSet& cfg)
  {
    fInputImageProducer  = cfg.get<std::string>("InputImageProducer");
    fNeighborhood        = cfg.get<int>("Neighborhood");
    fThreshold           = cfg.get< std::vector<int> >( "Thresholds" );
    
    // match tagged images
    fSaveMatchImage          = cfg.get<bool>("SaveMatchImage",false);
    fOutputMatchedPixelImage = cfg.get<std::string>("OutputMatchedPixelImage","");

  }

  void BoundaryMuonTagger::initialize()
  {}

  bool BoundaryMuonTagger::process(IOManager& mgr)
  {
    larcv::EventImage2D* input = (larcv::EventImage2D*)mgr.get_data(larcv::kProductImage2D,fInputImageProducer);
    larcv::EventImage2D* output = nullptr;
    if ( fSaveMatchImage ) output = (larcv::EventImage2D*)mgr.get_data(larcv::kProductImage2D,fOutputMatchedPixelImage);

    // get meta for input image
    const larcv::ImageMeta& meta = input->Image2DArray().at(0).meta();

    // create Image2D objects to store the result of boundary matching
    // we use meta to make the same sized image as the input
    std::vector<larcv::Image2D> matchedpixels;
    for (int i=0; i<12; i++) { // top, bottom, upstream, downstream x 3 planes
      larcv::Image2D matchimage( meta );
      matchimage.paint(0.0);
      matchedpixels.emplace_back( std::move(matchimage) );
    }

    // we need the wire downsampling factor
    int dsfactor = int( meta.pixel_width()+0.1 ); 

    // now loop over over the time of the images
    for (int r=0; r<meta.rows(); r++) {
      // loop through boundary type
      for (int b=0; b<4; b++) {
	// loop through combinations
	for (int imatch=0; imatch<m_matches.nmatches( (boundaryalgo::BoundaryMatchArrays::Boundary_t)b ); imatch++) {
	  
	  int triple[3];
	  m_matches.getMatch( (boundaryalgo::BoundaryMatchArrays::Boundary_t)b, imatch, triple[0], triple[1], triple[2] );

	  // now we have a match combo
	  // look if the image has charge above some threshold, within some neighborhood

	  bool hascharge[3] = { false, false, false };
	  std::vector<int> abovethresh[3]; // we save col number of pixels above threshold in each plane with this

	  for (int p=0; p<3; p++) {
	    const Image2D& img = input->Image2DArray().at(p);
	    int col = triple[p]/dsfactor;
	    for (int n=-fNeighborhood; n<=fNeighborhood; n++) {
	      if (col + n <0 || col + n>=meta.cols() )  continue; // skip out of bound columns
		   
	      if ( img.pixel( r, col + n ) > fThreshold[p] ) {
		hascharge[p] = true;
		abovethresh[p].push_back(col+n);
	      }
	    }
	    // small optimization, if we see that one plane does not have charge, the match will fail. move on.
	    if ( !hascharge[p] ) break;
	  }
	  
	  if ( hascharge[0] & hascharge[1] & hascharge[2] ) {
	    // match!  we write the match to the output
	    for (int p=0; p<3; p++) {
	      for ( int ipixel=0; ipixel<(int)abovethresh[p].size(); ipixel++) {
		//matchedpixels.at( p*4 + b ).set_pixel( r, abovethresh[p].at(ipixel), imatch ); // give it the match index
		matchedpixels.at( p*4 + b ).set_pixel( r, abovethresh[p].at(ipixel), 256.0 ); // give it the match index
	      }
	    }
	  }
	}//end of match loop
      }//end of boundary loop
    }//end of row loop

    if ( fSaveMatchImage ) {
      output->Emplace( std::move( matchedpixels ) );
    }

    return true;
  }

  void BoundaryMuonTagger::finalize()
  {
  }

}
#endif
