#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include "./test_utils.h"
#include <iostream>

#include <map2d.h>
#include <rsdnfconnecter.h>
#include <cellrsdnf.h>
#include <router.h>

using namespace std;
TEST_CASE("map2d error 1"){
    int size = 11;

    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);

    int nbBit = map2d.getTotalRegSize();

    bool * array = construct_array<bool>(1,nbBit);
    for(int i = 0 ; i < nbBit ; ++i){
        array[i] = 0;
    }
    array[1]= 1; 
    map2d.setErrorMaskFromArray(array,Register::TRANSIENT);
    map2d.compute(); //this load 0 in activated
    map2d.synch();

    int* state = construct_array<int>(size,size);
    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    REQUIRE(state[0] == 512);

    map2d.compute(); //this load 0 in activated
    map2d.synch();

    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    REQUIRE(state[0] == 0);

    map2d.compute(); //this load 0 in activated
    map2d.synch();

    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    REQUIRE(state[0] == 512);


}


TEST_CASE("map2d setErrorMaskFromArray"){
    int size = 11;

    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);

    int nbBit = map2d.getTotalRegSize();
    REQUIRE(nbBit == 6655);

    bool * array = construct_array<bool>(1,nbBit);
    for(int i = 0 ; i < nbBit ; ++i){
        array[i] = 0;
    }
    array[0]= 1; //should activate the first cell 
    map2d.setErrorMaskFromArray(array,Register::TRANSIENT);

    map2d.synch();
    REQUIRE(map2d.getCellReg(0,0,CellRsdnf::ACTIVATED) == 1);
    map2d.compute(); //this load 0 in activated
    map2d.synch();
    REQUIRE(map2d.getCellReg(0,0,CellRsdnf::ACTIVATED) == 1);
    map2d.compute(); //this load 0 in activated
    map2d.synch(); //next state is 0 by default
    REQUIRE(map2d.getCellReg(0,0,CellRsdnf::ACTIVATED) == 1);
    map2d.compute(); //this load 0 in activated
    map2d.synch(); //next state is 0 by default
    REQUIRE(map2d.getCellReg(0,0,CellRsdnf::ACTIVATED) == 1);
}

TEST_CASE("map2d getTotalRegSize "){
    int size = 11;

    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);

    REQUIRE(map2d.getTotalRegSize() == 6655);
}


TEST_CASE("map2d setArraySubParam"){
    int size = 11;
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);


    REQUIRE(map2d.getCellSubParam<float>(0,0,0,Router::PROBA) == 1.0);
    map2d.setArraySubParam<float>(Router::PROBA,0.5);
    REQUIRE(map2d.getCellSubParam<float>(0,0,0,Router::PROBA) == 0.5);
    

}



TEST_CASE("map2d setArrayParam"){
    int size = 11;
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);


    REQUIRE(map2d.getCellParam<int>(0,0,CellRsdnf::NB_SPIKE) == 20);
    map2d.setArrayParam<int>(CellRsdnf::NB_SPIKE,1);
    REQUIRE(map2d.getCellParam<int>(0,0,CellRsdnf::NB_SPIKE) == 1);
    

}

TEST_CASE("map2d of rsdnf spike accumulation"){

    int size = 11;
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);
    map2d.setCellReg(5,5,CellRsdnf::ACTIVATED,true);

    int* state = construct_array<int>(size,size);

    map2d.synch();
    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    int sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);


    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 4);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,size,size);
    cout << endl;
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 16);




}



TEST_CASE("map2d of rsdnf spike diffusion"){
    int size = 11;
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);
    // map2d.setParam(CellRsdnf::PROBA,new double(0.9));
    map2d.setCellReg(5,5,CellRsdnf::ACTIVATED,true);

    int* state = construct_array<int>(size,size);

    map2d.synch();
    map2d.getArrayState(CellRsdnf::ACTIVATED,state);


    int * sp_out = construct_array3d<int>(size,size,4);
    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(Router::SPIKE_OUT,sp_out);

    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(Router::SPIKE_OUT,sp_out);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+0] == 1);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+1] == 1);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+2] == 1);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+3] == 1);


    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(Router::SPIKE_OUT,sp_out);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+0] == 1);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+1] == 1);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+2] == 1);
    REQUIRE(sp_out[size/2*size*4 + size/2*4+3] == 1);

    //North
    REQUIRE(sp_out[(size/2-1)*size*4 + size/2*4+0] == 1);
    REQUIRE(sp_out[(size/2-1)*size*4 + size/2*4+2] == 1);
    REQUIRE(sp_out[(size/2-1)*size*4 + size/2*4+3] == 1);

    //South
    REQUIRE(sp_out[(size/2+1)*size*4 + size/2*4+1] == 1);
    REQUIRE(sp_out[(size/2+1)*size*4 + size/2*4+2] == 1);
    REQUIRE(sp_out[(size/2+1)*size*4 + size/2*4+3] == 1);

    //East
    REQUIRE(sp_out[size/2*size*4 + (size/2+1)*4+2] == 1);
    //West
    REQUIRE(sp_out[size/2*size*4 + (size/2-1)*4+3] == 1);
}

TEST_CASE("map2d of rsdnf initialisation and actication"){
    int size = 11;
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);
    // map2d.setParam(CellRsdnf::PROBA,new double(0.9));
    map2d.setCellReg(5,5,CellRsdnf::ACTIVATED,true);

    int* state = construct_array<int>(size,size);
    map2d.getArrayState(CellRsdnf::ACTIVATED,state);
    int sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

    map2d.synch();
    map2d.getArrayState(CellRsdnf::ACTIVATED,state);
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 1);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellRsdnf::ACTIVATED,state);
    sum = sum_array<int>(state,size*size);
    REQUIRE(sum == 0);

}
