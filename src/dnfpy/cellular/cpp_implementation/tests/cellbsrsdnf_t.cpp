#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <bsrouter.h>
#include <module.h>
#include <cellbsrsdnf.h>


TEST_CASE("nb bir reg"){

    Module::ModulePtr cell = Module::ModulePtr(new CellBsRsdnf());
    cell->initParams();
    int nbBit = cell->getTotalRegSize();
    REQUIRE(nbBit == 26);
}

TEST_CASE("cell populate router on activation"){
    Module::ModulePtr cell = Module::ModulePtr(new CellBsRsdnf());
    cell->initParams();
    
    cell->setRegState(CellBsRsdnf::ACTIVATED,true);
    cell->synch();


    cell->compute();
    cell->synch();


    REQUIRE(cell->getRegState(CellBsRsdnf::ACTIVATED) == false);
    
}


TEST_CASE("cell receive predecessor SPIKES and increase NB_BIT_RECEIVED"){

    Module::ModulePtr cell = Module::ModulePtr(new CellBsRsdnf());
    cell->initParams();
    Module::ModulePtr router = Module::ModulePtr(new BSRouter());
    cell->addNeighbour(router);

    router->setRegState(BSRouter::BS_OUT,true);
    router->synch();
    REQUIRE(cell->getRegState(CellBsRsdnf::NB_BIT_RECEIVED) == 0);
    cell->compute();
    cell->synch();

    REQUIRE(cell->getRegState(CellBsRsdnf::NB_BIT_RECEIVED) == 1);
    

}



