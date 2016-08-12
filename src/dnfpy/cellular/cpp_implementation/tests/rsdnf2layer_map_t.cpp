#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include "./test_utils.h"
#include <iostream>

#include <map2d.h>
#include <rsdnfconnecter2layer.h>
#include <cellrsdnf2.h>
#include <router.h>

using namespace std;

Map2D initMap(int size){
    RsdnfConnecter2layer c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf2>();
    map2d.connect(c);
    return map2d;
}

TEST_CASE("map2d of rsdnf2 initialisation and actication"){
    int size = 11;
    Map2D map2d = initMap(size);
    // map2d.setParam(CellRsdnf2::PROBA,new double(0.9));
    map2d.setCellReg(5,5,CellRsdnf2::ACTIVATED,true);

    int* state = construct_array<int>(size,size);
    map2d.getArrayState(CellRsdnf2::ACTIVATED,state);
    int sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.synch();
    map2d.getArrayState(CellRsdnf2::ACTIVATED,state);
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 1);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::ACTIVATED,state);
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

}

TEST_CASE("map2d of rsdnf2 spike diffusion"){
    int size = 11;
    int nbRouter = 8;
    Map2D map2d = initMap(size);
   // map2d.setParam(CellRsdnf2::PROBA,new double(0.9));
    map2d.setCellReg(5,5,CellRsdnf2::ACTIVATED,true);

    int* state = construct_array<int>(size,size);

    map2d.synch();
    map2d.getArrayState(CellRsdnf2::ACTIVATED,state);
    print_2D_array(state, size,size);


    int * sp_out = construct_array3d<int>(size,size,nbRouter);
    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(Router::SPIKE_OUT,sp_out);

    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(Router::SPIKE_OUT,sp_out);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+0] == 1);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+1] == 1);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+2] == 1);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+3] == 1);


    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(Router::SPIKE_OUT,sp_out);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+0] == 1);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+1] == 1);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+2] == 1);
    REQUIRE(sp_out[size/2*size*nbRouter + size/2*nbRouter+3] == 1);

    //North
    REQUIRE(sp_out[(size/2-1)*size*nbRouter + size/2*nbRouter+0] == 1);
    REQUIRE(sp_out[(size/2-1)*size*nbRouter + size/2*nbRouter+2] == 1);
    REQUIRE(sp_out[(size/2-1)*size*nbRouter + size/2*nbRouter+3] == 1);

    //South
    REQUIRE(sp_out[(size/2+1)*size*nbRouter + size/2*nbRouter+1] == 1);
    REQUIRE(sp_out[(size/2+1)*size*nbRouter + size/2*nbRouter+2] == 1);
    REQUIRE(sp_out[(size/2+1)*size*nbRouter + size/2*nbRouter+3] == 1);

    //East
    REQUIRE(sp_out[size/2*size*nbRouter + (size/2+1)*nbRouter+2] == 1);
    //West
    REQUIRE(sp_out[size/2*size*nbRouter + (size/2-1)*nbRouter+3] == 1);



    print_3D_array(sp_out,size,size,nbRouter);
}

TEST_CASE("map2d of rsdnf2 spike accumulation exc"){

    int size = 11;
    Map2D map2d = initMap(size);
    map2d.setCellReg(5,5,CellRsdnf2::ACTIVATED,true);

    int* state = construct_array<int>(size,size);

    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_RECEIVED,state);
    int sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);


    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 4);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 16);




}

TEST_CASE("map2d of rsdnf2 spike accumulation inh"){

    int size = 11;
    Map2D map2d = initMap(size);
    map2d.setCellReg(5,5,CellRsdnf2::ACTIVATED,true);

    int* state = construct_array<int>(size,size);

    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_INH_RECEIVED,state);
    int sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);


    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_INH_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_INH_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_INH_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 4);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf2::NB_BIT_INH_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 16);

}


TEST_CASE("map2d setArrayParam"){
    int size = 11;
    Map2D map2d = initMap(size);
    REQUIRE(map2d.getCellParam<int>(0,0,CellRsdnf2::NB_SPIKE) == 20);
    map2d.setArrayParam<int>(CellRsdnf2::NB_SPIKE,1);
    REQUIRE(map2d.getCellParam<int>(0,0,CellRsdnf2::NB_SPIKE) == 1);
    
    REQUIRE(map2d.getCellParam<float>(0,0,CellRsdnf2::PROBA) == 1.0);
    map2d.setArrayParam<float>(CellRsdnf2::PROBA,0.5);
    REQUIRE(map2d.getCellParam<float>(0,0,CellRsdnf2::PROBA) == 0.5);

    REQUIRE(map2d.getCellParam<float>(0,0,CellRsdnf2::PROBA_INH) == 1.0);
    map2d.setArrayParam<float>(CellRsdnf2::PROBA_INH,0.5);
    REQUIRE(map2d.getCellParam<float>(0,0,CellRsdnf2::PROBA_INH) == 0.5);

}


