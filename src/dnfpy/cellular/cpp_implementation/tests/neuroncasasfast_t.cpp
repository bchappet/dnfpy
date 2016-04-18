#define CATCH_CONFIG_MAIN
#include <limits>
#include <catch.hpp>
#include <neuroncasasfast.h>
#include <bitstreamutils.h>
using namespace std;

TEST_CASE("stimulu"){

    initSeed(255);
    //TODO
    Module::ModulePtr cell = Module::ModulePtr(new NeuronCasasFast());
    cell->initParams();
    cell->setParam<int>(NeuronCasasFast::THRESHOLD,25);
    cell->setParam<int>(NeuronCasasFast::SIZE_POTENTIAL_STREAM,100);
    cell->reset(); //necessart to change SIZE_POTENTIAL_STREAM

    float stim = 0.9f;
    cell->setAttribute(NeuronCasasFast::STIM,&stim);
    float pot;
    cell->preCompute();
    cell->compute();
    cell->getAttribute(NeuronCasasFast::POTENTIAL,&pot) ;
    cout << "pot1 : " << pot << endl;
    cell->preCompute();
    int act;
    cell->getAttribute(NeuronCasasFast::NB_ACT,&act);
    cout << "act  : " << act << endl;
    cell->compute();
    cell->getAttribute(NeuronCasasFast::POTENTIAL,&pot) ;
    cout << "pot2 : " << pot << endl;
    cell->preCompute();
    cell->getAttribute(NeuronCasasFast::NB_ACT,&act);
    cout << "act2  : " << act << endl;
    cell->compute();
    cell->getAttribute(NeuronCasasFast::POTENTIAL,&pot) ;
    cout << "pot3 : " << pot << endl;
    cell->preCompute();
    cell->getAttribute(NeuronCasasFast::NB_ACT,&act);
    cout << "act3  : " << act << endl;
    stim = 0.0f;
    cell->setAttribute(NeuronCasasFast::STIM,&stim);
    cell->compute();
    cell->getAttribute(NeuronCasasFast::POTENTIAL,&pot) ;
    cout << "pot4 : " << pot << endl;
    cell->preCompute();
    cell->getAttribute(NeuronCasasFast::NB_ACT,&act);
    cout << "act4  : " << act << endl;


}


TEST_CASE("change params"){
    initSeed(255);
    //TODO
    Module::ModulePtr cell = Module::ModulePtr(new NeuronCasasFast());
    cell->initParams();

    cell->setParam<int>(NeuronCasasFast::SIZE_POTENTIAL_STREAM,100);
    cell->reset(); //necessart to change SIZE_POTENTIAL_STREAM
    cell->preCompute();
    cell->compute();
    REQUIRE( ((NeuronCasasFast*)cell.get())->getSBS()->size  == 100);
    REQUIRE( ((NeuronCasasFast*)cell.get())->getPotSBS()->size  == 100);

    cell->preCompute();
    cell->compute();

    cell->setParam<int>(NeuronCasasFast::SIZE_POTENTIAL_STREAM,100000);
    cell->reset(); //necessart to change SIZE_POTENTIAL_STREAM
    cell->preCompute();
    cell->compute();
    cell->preCompute();
    cell->compute();
    REQUIRE( ((NeuronCasasFast*)cell.get())->getSBS()->size  == 100000);
    REQUIRE( ((NeuronCasasFast*)cell.get())->getPotSBS()->size  == 100000);
}

TEST_CASE("compute pot stable"){
    initSeed(255);

    Module::ModulePtr cell = Module::ModulePtr(new NeuronCasasFast());
    cell->initParams();
    float* pot = new float;
    for (int i = 0 ; i < 10000 ; ++i){
        cell->preCompute();
        cell->compute();
        cell->getAttribute(NeuronCasasFast::POTENTIAL,pot) ;
    }
    REQUIRE(*pot == Approx(0.513));
}


TEST_CASE("precompute"){
    initSeed(255);

    Module::ModulePtr cell = Module::ModulePtr(new NeuronCasasFast());
    cell->initParams();
    cell->preCompute();
    float* pot = new float;
    cell->getAttribute(NeuronCasasFast::POTENTIAL,pot) ;
    REQUIRE(*pot == Approx(0.506));
    int* nbAct = new int;
    cell->getAttribute(NeuronCasasFast::NB_ACT,nbAct);
    REQUIRE(*nbAct == 0);

}
