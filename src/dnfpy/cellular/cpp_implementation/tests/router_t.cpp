#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <router.h>
#include <module.h>




TEST_CASE( "router update SPIKE_OUT", "[router]" ) {
    Module::ModulePtr router = Module::ModulePtr(new Router());
    router->initParams();
    router.get()->setRegState(Router::BUFFER,1);
    router.get()->synch();
    router.get()->compute();
    router.get()->synch();
    REQUIRE(router->getRegState(Router::SPIKE_OUT) == 1);
}


TEST_CASE("router send spike until buffer is 0","[router]"){
    

    Module::ModulePtr router = Module::ModulePtr(new Router());
    router->initParams();
    router.get()->setRegState(Router::BUFFER,9);
    router->synch();
    for(int i = 0 ; i < 9 ; ++i){
        router->compute();
        router->synch();
        REQUIRE(router->getRegState(Router::SPIKE_OUT) == 1);
        REQUIRE(router->getRegState(Router::BUFFER) == 9-i-1);
    }
    router->compute();
    router->synch();

    REQUIRE(router->getRegState(Router::SPIKE_OUT) == 0);
    REQUIRE(router->getRegState(Router::BUFFER) == 0);
} 


TEST_CASE("router receive spike from neighbors","[router]"){
    Module::ModulePtr router = Module::ModulePtr(new Router());
    router->initParams();
    Module::ModulePtr router2 = Module::ModulePtr(new Router());
    router2->initParams();

    router->addNeighbour(NULL);//the first neighbor sould be the cell
    router->addNeighbour(router2);
    router2->setRegState(Router::BUFFER,2);
    router2->synch();
    REQUIRE(router2->getRegState(Router::BUFFER)==2);

    //the order of computation does not matter
    router->compute();
    router2->compute();
    router->synch();
    router2->synch();
    REQUIRE(router2->getRegState(Router::SPIKE_OUT) == 1);
    REQUIRE(router->getRegState(Router::SPIKE_OUT) == 0);

    router->compute();
    router2->compute();
    router->synch();
    router2->synch();
    REQUIRE(router2->getRegState(Router::SPIKE_OUT) == 1);
    REQUIRE(router->getRegState(Router::SPIKE_OUT) == 1);

    router->compute();
    router2->compute();
    router->synch();
    router2->synch();
    REQUIRE(router2->getRegState(Router::SPIKE_OUT) == 0);
    REQUIRE(router->getRegState(Router::SPIKE_OUT) == 1);

    router->compute();
    router2->compute();
    router->synch();
    router2->synch();
    REQUIRE(router2->getRegState(Router::SPIKE_OUT) == 0);
    REQUIRE(router->getRegState(Router::SPIKE_OUT) == 0);


}
