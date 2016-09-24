/**
 * \file BoundaryMuonTagger.h
 *
 * \ingroup Package_Name
 * 
 * \brief Class def header for a class BoundaryMuonTagger
 *
 * @author twongjirad
 */

/** \addtogroup Package_Name

    @{*/
#ifndef __BOUNDARYMUONTAGGER_H__
#define __BOUNDARYMUONTAGGER_H__

#include "Processor/ProcessBase.h"
#include "Processor/ProcessFactory.h"

#include <vector>
#include <string>
#include "BoundaryMatchArrays.h"

namespace larcv {

  /**
     \class ProcessBase
     User defined class BoundaryMuonTagger ... these comments are used to generate
     doxygen documentation!
  */
  class BoundaryMuonTagger : public ProcessBase {

  public:
    
    /// Default constructor
    BoundaryMuonTagger(const std::string name="BoundaryMuonTagger");
    
    /// Default destructor
    ~BoundaryMuonTagger(){}

    void configure(const PSet&);

    void initialize();

    bool process(IOManager& mgr);

    void finalize();

  protected:

    boundaryalgo::BoundaryMatchArrays m_matches;
    std::string fInputImageProducer;
    int fNeighborhood;
    std::vector<int> fThreshold;
    bool fSaveMatchImage;
    std::string fOutputMatchedPixelImage;

  };

  /**
     \class larcv::BoundaryMuonTaggerFactory
     \brief A concrete factory class for larcv::BoundaryMuonTagger
  */
  class BoundaryMuonTaggerProcessFactory : public ProcessFactoryBase {
  public:
    /// ctor
    BoundaryMuonTaggerProcessFactory() { ProcessFactory::get().add_factory("BoundaryMuonTagger",this); }
    /// dtor
    ~BoundaryMuonTaggerProcessFactory() {}
    /// creation method
    ProcessBase* create(const std::string instance_name) { return new BoundaryMuonTagger(instance_name); }
  };

}

#endif
/** @} */ // end of doxygen group 

