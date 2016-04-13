#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <module.h>


TEST_CASE("incr reg"){

    Module::ModulePtr module = Module::ModulePtr(new Module());
    module->addReg(7,8);
    module->incrReg(0,10);
    module->synch();
    REQUIRE(module->getRegState(0) == 17);

}

TEST_CASE("setErrorMaskFromArray"){
 
    Module::ModulePtr module = Module::ModulePtr(new Module());
    module->addReg(7,8);
    REQUIRE(module->getTotalRegSize() == 8);

    module->addReg(8);
    REQUIRE(module->getTotalRegSize() == 24);

    Module::ModulePtr module2 = Module::ModulePtr(new Module());
    module2->addReg(1,1);
    module2->addReg(4,3);

    module->addSubModule(module2);
    REQUIRE(module->getTotalRegSize() == 28);

    bool array[28] = {0,0,0,0,0,0,0,1,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
        1,
        0,0,1};
    module->setErrorMaskFromArray(array);
    module->synch();

    REQUIRE(module->getRegState(0) == 6);
    REQUIRE(module->getRegState(1) == 9);
    REQUIRE(module->getSubModuleState(0,0) == 0);
    REQUIRE(module->getSubModuleState(0,1) == 5);
   
}

TEST_CASE("getTotalRegSize"){

    Module::ModulePtr module = Module::ModulePtr(new Module());
    module->addReg(7,8);
    REQUIRE(module->getTotalRegSize() == 8);

    module->addReg(7);
    REQUIRE(module->getTotalRegSize() == 24);

    Module::ModulePtr module2 = Module::ModulePtr(new Module());
    module2->addReg(1,1);
    module2->addReg(4,3);

    module->addSubModule(module2);
    REQUIRE(module->getTotalRegSize() == 28);
}
