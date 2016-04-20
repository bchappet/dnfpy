#define CATCH_CONFIG_MAIN
#include "test_utils.h"
#include <catch.hpp>
#include <router.h>
#include <module.h>
#include <cellrsdnf.h>


using namespace std;
TEST_CASE("fisrt register error"){

    Module::ModulePtr cell = Module::ModulePtr(new CellRsdnf());
    cell->initParams();
    int nbBit = cell->getTotalRegSize();
    bool * errors = construct_array<bool>(1,nbBit);
    errors[0] = 1;
    cell->setErrorMaskFromArray(errors);
    
    cell->setRegState(CellRsdnf::ACTIVATED,true);
    int reg = cell->getRegState(CellRsdnf::ACTIVATED);
    REQUIRE(reg== false);
    cell->synch();
    reg = cell->getRegState(CellRsdnf::ACTIVATED);
    cout << reg << endl;
    REQUIRE(reg== false);
    cell->synch();
    reg = cell->getRegState(CellRsdnf::ACTIVATED);
    cout << reg << endl;
    REQUIRE(reg == true);



}

//TEST_CASE("cell populate router on activation","[cellrsdnf]"){
//    Module::ModulePtr cell = Module::ModulePtr(new CellRsdnf());
//    cell->initParams();
//    
//    cell->setRegState(CellRsdnf::ACTIVATED,true);
//    cell->synch();
//
//
//    cell->compute();
//    cell->synch();
//
//
//    REQUIRE(cell->getRegState(CellRsdnf::ACTIVATED) == false);
//    REQUIRE(cell->getSubModuleState(0,Router::BUFFER) == 20);
//    
//}
//
//
//TEST_CASE("cell receive predecessor SPIKES and increase NB_BIT_RECEIVED","[cellrsdnf]"){
//
//    Module::ModulePtr cell = Module::ModulePtr(new CellRsdnf());
//    cell->initParams();
//    Module::ModulePtr router = Module::ModulePtr(new Router());
//    cell->addNeighbour(router);
//
//    router->setRegState(Router::SPIKE_OUT,true);
//    router->synch();
//    REQUIRE(cell->getRegState(CellRsdnf::NB_BIT_RECEIVED) == 0);
//    cell->compute();
//    cell->synch();
//
//    REQUIRE(cell->getRegState(CellRsdnf::NB_BIT_RECEIVED) == 1);
//    
//
//}
//


