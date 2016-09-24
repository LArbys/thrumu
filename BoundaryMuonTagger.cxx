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

    boundaryalgo::ConfigBoundaryMuonTaggerAlgo config;

    fInputImageProducer   = cfg.get<std::string>("InputImageProducer");
    config.neighborhoods = cfg.get< std::vector<int> >("Neighborhoods");
    config.thresholds    = cfg.get< std::vector<float> >( "Thresholds" );
    
    // match tagged images
    fSaveMatchImage          = cfg.get<bool>("SaveMatchImage",false);
    fOutputMatchedPixelImage = cfg.get<std::string>("OutputMatchedPixelImage","");

    _algo.configure( config );

  }

  void BoundaryMuonTagger::initialize()
  {}

  bool BoundaryMuonTagger::process(IOManager& mgr)
  {
    larcv::EventImage2D* input = (larcv::EventImage2D*)mgr.get_data(larcv::kProductImage2D,fInputImageProducer);
    larcv::EventImage2D* output = nullptr;
    if ( fSaveMatchImage ) output = (larcv::EventImage2D*)mgr.get_data(larcv::kProductImage2D,fOutputMatchedPixelImage);

    const std::vector< larcv::Image2D >& imgs = input->Image2DArray();
    std::vector< larcv::Image2D > matchedpixels;
    
    _algo.searchforboundarypixels( imgs, matchedpixels );
    
    if ( fSaveMatchImage ) {
      output->Emplace( std::move( matchedpixels ) );
    }

    return true;
  }

  void BoundaryMuonTagger::finalize()
  {
  }

  // -------------------------------------------------------------------------------------------------------
  // Tagger Code: modularized so that we can separate it out as an algo at some point
  


  // -------------------------------------------------------------------------------------------------------

}
#endif
