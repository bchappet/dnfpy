#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include "./test_utils.h"
#include <iostream>

#include <map2d.h>
#include <rsdnfconnecter.h>
#include <cellbsrsdnf.h>
#include <bsrouter.h>

using namespace std;
#define SIZE 11

Map2D initTest(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellBsRsdnf>();
    map2d.connect(c);
    return map2d;
}
TEST_CASE("BsRsdnf  spike accumulation"){

    Map2D map2d = initTest(SIZE);
    map2d.setCellReg(5,5,CellBsRsdnf::ACTIVATED,true);

    int* state = construct_array<int>(SIZE,SIZE);

    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
    int sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 0);


    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,SIZE,SIZE);
    cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,SIZE,SIZE);
    cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 0);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,SIZE,SIZE);
    cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 4);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,SIZE,SIZE);
    cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 16);
    
    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::NB_BIT_RECEIVED,state);
    print_2D_array(state,SIZE,SIZE);
    cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 40);





}





TEST_CASE("map2d of rsdnf spike diffusion"){
    Map2D map2d = initTest(SIZE);
    // map2d.setParam(CellRsdnf::PROBA,new double(0.9));
    map2d.setCellReg(5,5,CellBsRsdnf::ACTIVATED,true);

    int* state = construct_array<int>(SIZE,SIZE);

    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::ACTIVATED,state);


    int * sp_out = construct_array3d<int>(SIZE,SIZE,4);
    map2d.compute();
    map2d.synch();
//    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
//    print_3D_array<int>(sp_out,SIZE,SIZE,4);
//    cout << endl;

    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
    //print_3D_array<int>(sp_out,SIZE,SIZE,4);
    //cout << endl;
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+0] == 1);
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+1] == 1);
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+2] == 1);
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+3] == 1);


    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
    //print_3D_array<int>(sp_out,SIZE,SIZE,4);
    //cout << endl;
    //CENTER
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+0] == 1);
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+1] == 1);
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+2] == 1);
    REQUIRE(sp_out[SIZE/2*SIZE*4 + SIZE/2*4+3] == 1);

    //North
    REQUIRE(sp_out[(SIZE/2-1)*SIZE*4 + SIZE/2*4+0] == 1);
    REQUIRE(sp_out[(SIZE/2-1)*SIZE*4 + SIZE/2*4+2] == 1);
    REQUIRE(sp_out[(SIZE/2-1)*SIZE*4 + SIZE/2*4+3] == 1);

    //South
    REQUIRE(sp_out[(SIZE/2+1)*SIZE*4 + SIZE/2*4+1] == 1);
    REQUIRE(sp_out[(SIZE/2+1)*SIZE*4 + SIZE/2*4+2] == 1);
    REQUIRE(sp_out[(SIZE/2+1)*SIZE*4 + SIZE/2*4+3] == 1);

    //East
    REQUIRE(sp_out[SIZE/2*SIZE*4 + (SIZE/2+1)*4+2] == 1);
    //West
    REQUIRE(sp_out[SIZE/2*SIZE*4 + (SIZE/2-1)*4+3] == 1);

    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(BSRouter::BS_OUT,sp_out);
    //print_3D_array<int>(sp_out,SIZE,SIZE,4);
    //cout << endl;
}



TEST_CASE("map2d of rsdnf initialisation and actication"){
    Map2D map2d = initTest(SIZE);
    // map2d.setParam(CellBsRsdnf::PROBA,new double(0.9));
    map2d.setCellReg(5,5,CellBsRsdnf::ACTIVATED,true);

    int* state = construct_array<int>(SIZE,SIZE);
    map2d.getArrayState(CellBsRsdnf::ACTIVATED,state);
    //print_2D_array<int>(state,SIZE,SIZE);
    //cout << endl;
    int sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 0);

    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::ACTIVATED,state);
    //print_2D_array<int>(state,SIZE,SIZE);
    //cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 1);

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(CellBsRsdnf::ACTIVATED,state);
    //print_2D_array<int>(state,SIZE,SIZE);
    //cout << endl;
    sum = sum_array<int>(state,SIZE*SIZE);
    REQUIRE(sum == 0);

}
