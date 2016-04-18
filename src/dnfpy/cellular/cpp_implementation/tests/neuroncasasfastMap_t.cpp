#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include "./test_utils.h"
#include <iostream>

#include <map2d.h>
#include <neuroncasasfast.h>
#include <bsrouter.h>
#include <rsdnfconnecter2layer.h>
#include <module.h>

using namespace std;
#define SIZE 11

Map2D initTest(int size){
    initSeed(255);
    RsdnfConnecter2layer c;
    Map2D map2d(size,size);
    map2d.initCellArray<NeuronCasasFast>();
    map2d.connect(c);
    return map2d;
}
//TEST_CASE("BsRsdnf  spike accumulation"){
//
//    Map2D map2d = initTest(SIZE);
//    map2d.setCellReg(5,5,CellBsRsdnf::ACTIVATED,true);
//
//    int* state = construct_array<int>(SIZE,SIZE);
//
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
//    int sum = sum_array<int>(state,SIZE*SIZE);
//    REQUIRE(sum == 0);
//
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
//    print_2D_array(state,SIZE,SIZE);
//    cout << endl;
//    sum = sum_array<int>(state,SIZE*SIZE);
//    REQUIRE(sum == 0);
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
//    print_2D_array(state,SIZE,SIZE);
//    cout << endl;
//    sum = sum_array<int>(state,SIZE*SIZE);
//    REQUIRE(sum == 0);
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
//    print_2D_array(state,SIZE,SIZE);
//    cout << endl;
//    sum = sum_array<int>(state,SIZE*SIZE);
//    REQUIRE(sum == 4);
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
//    print_2D_array(state,SIZE,SIZE);
//    cout << endl;
//    sum = sum_array<int>(state,SIZE*SIZE);
//    REQUIRE(sum == 16);
//    
//    map2d.compute();
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
//    print_2D_array(state,SIZE,SIZE);
//    cout << endl;
//    sum = sum_array<int>(state,SIZE*SIZE);
//    REQUIRE(sum == 40);
//
//
//
//
//
//}
//
//
//
//
//
//TEST_CASE("map2d of rsdnf spike diffusion"){
//    Map2D map2d = initTest(SIZE);
//    // map2d.setParam(CellRsdnf::PROBA,new double(0.9));
//    map2d.setCellReg(5,5,CellBsRsdnf::ACTIVATED,true);
//
//    int* state = construct_array<int>(SIZE,SIZE);
//
//    map2d.synch();
//    map2d.getArrayState(CellBsRsdnf::ACTIVATED,state);
//
//
//    int * sp_out = construct_array3d<int>(SIZE,SIZE,4);
//    map2d.compute();
//    map2d.synch();
////    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
////    print_3D_array<int>(sp_out,SIZE,SIZE,4);
////    cout << endl;
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
//    //print_3D_array<int>(sp_out,SIZE,SIZE,4);
//    //cout << endl;
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+0] == 1);
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+1] == 1);
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+2] == 1);
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+3] == 1);
//
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
//    //print_3D_array<int>(sp_out,SIZE,SIZE,4);
//    //cout << endl;
//    //CENTER
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+0] == 1);
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+1] == 1);
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+2] == 1);
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+3] == 1);
//
//    //North
//    REQUIRE(sp_out[(SIZE/2-1)*SIZE*4 + SIZE/2*4+0] == 1);
//    REQUIRE(sp_out[(SIZE/2-1)*SIZE*4 + SIZE/2*4+2] == 1);
//    REQUIRE(sp_out[(SIZE/2-1)*SIZE*4 + SIZE/2*4+3] == 1);
//
//    //South
//    REQUIRE(sp_out[(SIZE/2+1)*SIZE*4 + SIZE/2*4+1] == 1);
//    REQUIRE(sp_out[(SIZE/2+1)*SIZE*4 + SIZE/2*4+2] == 1);
//    REQUIRE(sp_out[(SIZE/2+1)*SIZE*4 + SIZE/2*4+3] == 1);
//
//    //East
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + (SIZE/2+1)*4+2] == 1);
//    //West
//    REQUIRE(sp_out[SIZE/2*SIZE*4 + (SIZE/2-1)*4+3] == 1);
//
//    map2d.compute();
//    map2d.synch();
//    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
//    //print_3D_array<int>(sp_out,SIZE,SIZE,4);
//    //cout << endl;
//}
//


TEST_CASE("map2d of neuroncasasfast diffusion"){
    Map2D map2d = initTest(SIZE);
    Module::ModulePtr cell = map2d.getCell(5,5);
    map2d.setArrayParam<int>(NeuronCasasFast::THRESHOLD,28);

    float stim = 0.99;
    map2d.setCellAttribute(5,5,NeuronCasasFast::STIM,&stim);

    float* potential = construct_array<float>(SIZE,SIZE);
    int* act = construct_array<int>(SIZE,SIZE);
    int* exc = construct_array<int>(SIZE,SIZE);
    map2d.preCompute();
    map2d.compute();
    map2d.getArrayAttribute<float>(NeuronCasasFast::POTENTIAL,potential);
    print_2D_array<float>(potential,SIZE,SIZE);
    map2d.preCompute();
    map2d.getArrayAttribute<int>(NeuronCasasFast::NB_ACT,act);
    print_2D_array<int>(act,SIZE,SIZE);
    cout << endl;

    map2d.compute();
    map2d.getArrayAttribute<int>(NeuronCasasFast::NB_BIT_EXC,exc);
    print_2D_array<int>(exc,SIZE,SIZE);
    cout << endl;


    map2d.preCompute();
    map2d.compute();
    map2d.getArrayAttribute<float>(NeuronCasasFast::POTENTIAL,potential);
    print_2D_array<float>(potential,SIZE,SIZE);
    cout << endl;


}

//TEST_CASE("map2d of neuroncasasfast initialisation and actication"){
//    Map2D map2d = initTest(SIZE);
//    map2d.setArrayParam<int>(NeuronCasasFast::SIZE_POTENTIAL_STREAM,1000);
//    Module::ModulePtr cell = map2d.getCell(5,5);
//    cout << ((NeuronCasasFast*)cell.get())->getSBS()->size << endl;
//    // map2d.setParam(CellBsRsdnf::PROBA,new double(0.9));
//    float stim = 0.98;
//    map2d.setCellAttribute(5,5,NeuronCasasFast::STIM,&stim);
//
//    float* potential = construct_array<float>(SIZE,SIZE);
//    map2d.preCompute();
//    map2d.compute();
//    map2d.getArrayAttribute<float>(NeuronCasasFast::POTENTIAL,potential);
//    print_2D_array<float>(potential,SIZE,SIZE);
//    cout << endl;
//
//
//}
