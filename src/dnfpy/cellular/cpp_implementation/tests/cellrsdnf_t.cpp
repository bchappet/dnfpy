#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <router.h>
#include <module.h>
#include <cellrsdnf.h>

TEST_CASE("cell populate router on activation","[cellrsdnf]"){
    Module::ModulePtr cell = Module::ModulePtr(new CellRsdnf());
    cell->initParams();
    
    cell->setRegState(CellRsdnf::ACTIVATED,true);
    cell->synch();


    cell->compute();
    cell->synch();


    REQUIRE(cell->getRegState(CellRsdnf::ACTIVATED) == false);
    REQUIRE(cell->getSubModuleState(0,Router::BUFFER) == 20);
    
}


TEST_CASE("cell receive predecessor SPIKES and increase NB_BIT_RECEIVED","[cellrsdnf]"){

    Module::ModulePtr cell = Module::ModulePtr(new CellRsdnf());
    cell->initParams();
    Module::ModulePtr router = Module::ModulePtr(new Router());
    cell->addNeighbour(router);

    router->setRegState(Router::SPIKE_OUT,true);
    router->synch();
    REQUIRE(cell->getRegState(CellRsdnf::NB_BIT_RECEIVED) == 0);
    cell->compute();
    cell->synch();

    REQUIRE(cell->getRegState(CellRsdnf::NB_BIT_RECEIVED) == 1);
    

}



