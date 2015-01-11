#include <iostream>
#include "register.h"
#include <assert.h>
#include "cellgof.h"
#include <vector>
#include "map2d.h"
#include "mooreconnecter.h"
#include "cellrsdnf.h"
#include "rsdnfconnecter.h"
#include "router.h"
#include "cellrsdnf.h"
#include <ctime>
#include "softsimu.h"
#include "cellnspike.h"
#include "nspikeconnecter.h"
#include "cellbsrsdnf.h"
#include "bsrouter.h"
using namespace std;
#define PRECISION 1000000


template <typename T>
void print_2D_array(T* array,int width,int height);

template <typename T>
T* construct_array(int width,int height);

void assertAlmostEquals(float a,float b);

void test_register();
void test_cellgof();
void test_Map2D(int size);
void test_neumann_connecter(int size);
void test_rsdnf_map(int size);
void test_rsdnf_cell();
void test_soft_simu(int size);
void test_cell_nspike();
void test_map_nspike(int size);
void test_stochastic_rsdnf_map(int size);
void test_stochastic_rsdnf_map2(int size);
void test_stochastic_rsdnf();
void test_stochastic_rsdnf_map_carry_router(int size);

int main()
{
//    cout << "Hello World!" << endl;
//    test_register();
//    cout << "test register passed" << endl;
//    test_cellgof();
//    cout << "test cell gof passed" << endl;
//    test_Map2D(10);
//    cout << "test Map2D passed" << endl;
//    test_neumann_connecter(10);
//    cout << "test neumann connecter passed" << endl;
//    test_rsdnf_cell();
//    cout << "test rsdnf passed" << endl;
//    test_rsdnf_map(11);
//    cout << "test rsdnf map passed" << endl;

//    test_cell_nspike();
//    cout<< "test cell n spike passed" << endl;
//    test_map_nspike(11);
//    cout << "test map nspike passed" << endl;
//    test_soft_simu(11);
//    cout<< "test soft simu passed" <<endl;
//    test_stochastic_rsdnf_map2(11);
//    cout << "test stochastic rsdnf map passed" << endl;
//    test_stochastic_rsdnf();
//    cout << "test stochastic rsdnf passed" << endl;
    test_stochastic_rsdnf_map_carry_router(11);
    cout << "test stochastic rsdnf map carry router passed" << endl;
    return 0;
}

void test_stochastic_rsdnf_map_carry_router(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellBsRsdnf>("carryRouter");
    map2d.connect(c);


    map2d.initMapSeed();

    int hSize = size/2;
    map2d.compute();
    map2d.synch();
    int* nb_sp = construct_array<int>(size,size);

    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);

    bool activate = true;
    map2d.setCellAttribute(hSize,hSize,CellBsRsdnf::ACTIVATED,&activate);
    map2d.setCellAttribute(hSize+2,hSize+2,CellBsRsdnf::ACTIVATED,&activate);
    map2d.setCellAttribute(hSize-2,hSize,CellBsRsdnf::ACTIVATED,&activate);

    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);
//    assert(map2d.getCellState<bool>(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
//    assert(nb_sp[hSize*size+hSize-1]==1);
//    assert(nb_sp[hSize*size+hSize+1]==1);
//    assert(nb_sp[(hSize+1)*size+hSize]==1);
//    assert(nb_sp[(hSize-1)*size+hSize]==1);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
//    assert(nb_sp[hSize*size+hSize-1]==2);
//    assert(nb_sp[hSize*size+hSize+1]==2);
//    assert(nb_sp[(hSize+1)*size+hSize]==2);
//    assert(nb_sp[(hSize-1)*size+hSize]==2);



    for(int i = 0 ; i < 10 ; i ++){
        cout << "compute" << endl;


        map2d.compute();
        map2d.synch();
        map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
        print_2D_array<int>(nb_sp,size,size);
    }
//    assert(nb_sp[0]==20);
//    assert(nb_sp[size]==20);


}

void test_stochastic_rsdnf(){
    CellBsRsdnf *cell = new CellBsRsdnf();
    CellBsRsdnf *rn,*rs,*re,*rw;
    RsdnfConnecter c;
    rn = new CellBsRsdnf();
    rs = new CellBsRsdnf();
    re = new CellBsRsdnf();
    rw = new CellBsRsdnf();

    c.cellConnection(cell,rn,c.N);
    c.cellConnection(cell,rs,c.S);
    c.cellConnection(cell,re,c.E);
    c.cellConnection(cell,rw,c.W);

    c.cellConnection(rn,cell,c.S);
    c.cellConnection(rs,cell,c.N);
    c.cellConnection(re,cell,c.W);
    c.cellConnection(rw,cell,c.E);
    cell->setParam<float>(CellBsRsdnf::PROBA_SYNAPSE,0.9);
    assertAlmostEquals(cell->getSubModule(0)->getParam<float>(BSRouter::PROBA_SYNAPSE),0.9);
    cell->setParam<float>(CellBsRsdnf::PROBA_SYNAPSE,1.);
    bool activated = true;
    cell->setAttribute(CellBsRsdnf::ACTIVATED,&activated);

    cell->compute();
    cell->synch();
    assert(cell->getRegState<bool>(CellBsRsdnf::SPIKE_BS)==1);

    cell->compute();
    cell->synch();
    assert(cell->getSubModule(0)->getRegState<bool>(BSRouter::BS_OUT)==1);
    assert(cell->getSubModule(1)->getRegState<bool>(BSRouter::BS_OUT)==1);

    cell->compute();
    rn->compute();
    cell->synch();
    rn->synch();
    int nbB;
    rn->getAttribute(CellBsRsdnf::NB_BIT_RECEIVED,&nbB);
    assert(nbB == 1);
    assert(rn->getSubModule(0)->getRegState<bool>(BSRouter::BS_OUT)==1);
    assert(rn->getSubModule(2)->getRegState<bool>(BSRouter::BS_OUT)==1);

}

void test_stochastic_rsdnf_map2(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellBsRsdnf>();
    map2d.connect(c);


    map2d.initMapSeed();

    int hSize = size/2;
    map2d.compute();
    map2d.synch();
    int* nb_sp = construct_array<int>(size,size);

    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);

    bool activate = true;
    map2d.setCellAttribute(hSize,hSize,CellBsRsdnf::ACTIVATED,&activate);
    map2d.setCellAttribute(hSize+2,hSize+2,CellBsRsdnf::ACTIVATED,&activate);
     map2d.setCellAttribute(hSize-2,hSize,CellBsRsdnf::ACTIVATED,&activate);

    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);
//    assert(map2d.getCellState<bool>(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
//    assert(nb_sp[hSize*size+hSize-1]==1);
//    assert(nb_sp[hSize*size+hSize+1]==1);
//    assert(nb_sp[(hSize+1)*size+hSize]==1);
//    assert(nb_sp[(hSize-1)*size+hSize]==1);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
//    assert(nb_sp[hSize*size+hSize-1]==2);
//    assert(nb_sp[hSize*size+hSize+1]==2);
//    assert(nb_sp[(hSize+1)*size+hSize]==2);
//    assert(nb_sp[(hSize-1)*size+hSize]==2);



    for(int i = 0 ; i < 10 ; i ++){
        cout << "compute" << endl;


        map2d.compute();
        map2d.synch();
        map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
        print_2D_array<int>(nb_sp,size,size);
    }
//    assert(nb_sp[0]==20);
//    assert(nb_sp[size]==20);



}


void test_stochastic_rsdnf_map(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellBsRsdnf>();
    map2d.connect(c);

    int hSize = size/2;
    map2d.compute();
    map2d.synch();
    int* nb_sp = construct_array<int>(size,size);

    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);

    bool activate = true;
    map2d.setCellAttribute(hSize,hSize,CellBsRsdnf::ACTIVATED,&activate);

    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);
    assert(map2d.getCellState<bool>(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[hSize*size+hSize-1]==1);
    assert(nb_sp[hSize*size+hSize+1]==1);
    assert(nb_sp[(hSize+1)*size+hSize]==1);
    assert(nb_sp[(hSize-1)*size+hSize]==1);
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[hSize*size+hSize-1]==2);
    assert(nb_sp[hSize*size+hSize+1]==2);
    assert(nb_sp[(hSize+1)*size+hSize]==2);
    assert(nb_sp[(hSize-1)*size+hSize]==2);



    for(int i = 0 ; i < 30 ; i ++){
        map2d.compute();
        map2d.synch();
        map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
        print_2D_array<int>(nb_sp,size,size);
    }
    assert(nb_sp[0]==20);
    assert(nb_sp[size]==20);



}

void test_map_nspike(int size){
    NSpikeConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellNSpike>();
    map2d.connect(c);
    bool activated = true;
    map2d.setCellAttribute(size/2,size/2,CellNSpike::ACTIVATED,&activated);
    map2d.compute();
    int* nb_sp = construct_array<int>(size,size);

    map2d.getArrayAttribute<int>(CellNSpike::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);

    cout << endl;

    map2d.setMapParam<float>(CellNSpike::PROBA_N,0.5);
    map2d.setMapParam<float>(CellNSpike::PROBA_S,0.5);
    map2d.setMapParam<float>(CellNSpike::PROBA_E,0.5);
    map2d.setMapParam<float>(CellNSpike::PROBA_W,0.5);
    float probaN = map2d.getCell(0,0)->getParam<float>(CellNSpike::PROBA_N);
    cout << "probaN : " << probaN << endl;
    assert(probaN == 0.5);

    map2d.setCellAttribute(size/2,size/2,CellNSpike::ACTIVATED,&activated);
    map2d.compute();
    map2d.getArrayAttribute<int>(CellNSpike::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    float proba = 0.99;
    map2d.setMapParam<float>(CellNSpike::PROBA_N,proba);
    map2d.setMapParam<float>(CellNSpike::PROBA_S,proba);
    map2d.setMapParam<float>(CellNSpike::PROBA_E,proba);
    map2d.setMapParam<float>(CellNSpike::PROBA_W,proba);
    for(int i = 0 ; i < 5 ; i++){
        map2d.setCellAttribute(size/2,size/2,CellNSpike::ACTIVATED,&activated);
        map2d.compute();
        map2d.getArrayAttribute<int>(CellNSpike::NB_BIT_RECEIVED,nb_sp);
        map2d.reset();
        print_2D_array<int>(nb_sp,size,size);

    }



}

void test_cell_nspike(){
    CellNSpike* cell = new CellNSpike();
    int nb = 10;

    cell->setAttribute(CellNSpike::NB_BIT_RECEIVED,&nb);
    int res;
    cell->getAttribute(CellNSpike::NB_BIT_RECEIVED,&res);
    assert(res == 10);
    nb = 2;
    cell->getAttribute(CellNSpike::NB_BIT_RECEIVED,&res);
    assert(res == 10);

    bool act = true;
    bool dead = true;
    cell->setAttribute(CellNSpike::ACTIVATED,&act);
    cell->setAttribute(CellNSpike::DEAD,&dead);
    cell->compute();

    CellNSpike* cn,*cs,*ce,*cw;
    cn = new CellNSpike();
    cs = new CellNSpike();
    ce = new CellNSpike();
    cw = new CellNSpike();
    cell->addNeighbour(cn);cn->setAttribute(CellNSpike::DEAD,&dead);
    cell->addNeighbour(cs);cs->setAttribute(CellNSpike::DEAD,&dead);
    cell->addNeighbour(ce);ce->setAttribute(CellNSpike::DEAD,&dead);
    cell->addNeighbour(cw);cw->setAttribute(CellNSpike::DEAD,&dead);

    dead = false;
    int nb_spike = 100;
    cell->setAttribute(CellNSpike::DEAD,&dead);
    cell->setAttribute(CellNSpike::ACTIVATED,&act);
    cell->setParam<int>(CellNSpike::NB_SPIKE,nb_spike);
    cell->setParam<float>(CellNSpike::PROBA_E,0.);
    cell->setParam<float>(CellNSpike::PROBA_S,0.5);
    cell->compute();
    int NB_BIT_RECEIVED = -99;
    cn->getAttribute(CellNSpike::NB_BIT_RECEIVED,&NB_BIT_RECEIVED);
    assert(NB_BIT_RECEIVED == nb_spike);
    cs->getAttribute(CellNSpike::NB_BIT_RECEIVED,&NB_BIT_RECEIVED);
    cout << "nb spike received : " << NB_BIT_RECEIVED << endl;
    //assert(NB_BIT_RECEIVED == nb_spike);
    ce->getAttribute(CellNSpike::NB_BIT_RECEIVED,&NB_BIT_RECEIVED);
    assert(NB_BIT_RECEIVED == 0);
    cw->getAttribute(CellNSpike::NB_BIT_RECEIVED,&NB_BIT_RECEIVED);
    assert(NB_BIT_RECEIVED == nb_spike);


}

void test_soft_simu(int size)
{
    int idMap = initSimu(size,size,"cellrsdnf","rsdnfconnecter");
    useMap(idMap);
    int* stateInt = construct_array<int>(size,size);
    bool act = true;
    setCellAttribute(5,5,CellRsdnf::ACTIVATED,&act);
    //simu.map.synch();
    for(int i = 0 ; i < 20 ; i++){
        step();
    }
    getArrayAttributeInt(CellRsdnf::NB_BIT_RECEIVED,stateInt);
    print_2D_array<int>(stateInt,size,size);

    initSimu(size,size,"cellnspike","nspikeconnecter");
    int i = 10;
    setCellAttribute(0,0,0,&i);
    int res = 0;
    getCellAttribute(0,0,0,&res);
    assert(res = 10);




}

void test_rsdnf_cell(){
    CellRsdnf* cell;
    CellRsdnf* neigh;
    cell = new CellRsdnf();
    neigh = new CellRsdnf();
    cell->getSubModule(0)->addNeighbour(neigh->getSubModule(0));
    cell->addNeighbour(neigh->getSubModule(0));
    bool activated = true;
    neigh->setAttribute(CellRsdnf::ACTIVATED,&activated);
    bool resB;
    neigh->getAttribute(CellRsdnf::ACTIVATED,&resB);
    assert(resB);

    neigh->compute();
    neigh->synch();
    //cout << "router neigh buffer : " << neigh->getSubModule(0)->getRegState<int>(Router::BUFFER) << endl;
    assert(neigh->getSubModule(0)->getRegState<int>(Router::BUFFER) == 19);

    cell->compute();
    cell->synch();
    assert(cell->getSubModule(0)->getRegState<bool>(Router::SPIKE_OUT));
    int resI;
    cell->getAttribute(CellRsdnf::NB_BIT_RECEIVED,&resI);
    assert(resI == 1);


}

void test_rsdnf_map(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);
    map2d.setMapParam<float>(Router::PROBA,0.9,"./*");

    bool activated = true;
    map2d.setCellAttribute(5,5,CellRsdnf::ACTIVATED,&activated);

    bool* state = construct_array<bool>(size,size);
    map2d.getArrayAttribute<bool>(CellRsdnf::ACTIVATED,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;

    map2d.compute();
    map2d.synch();
    int* stateInt = construct_array<int>(size,size);
    map2d.getArrayAttribute<int>(CellRsdnf::NB_BIT_RECEIVED,stateInt);
    print_2D_array<int>(stateInt,size,size);
    cout << endl;


    time_t before = time(0);
    for(int i = 0 ; i < 10 ; i ++){
        map2d.compute();
        map2d.synch();
    }
    time_t after = time(0);
    map2d.getArrayAttribute<int>(CellRsdnf::NB_BIT_RECEIVED,stateInt);
    print_2D_array<int>(stateInt,size,size);
    cout <<"time diff : " << difftime(after,before)/200 << endl;


}

void test_neumann_connecter(int size){
    MooreConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellGof>();
    map2d.connect(c);
    bool* new_state = construct_array<bool>(size,size);
      for(int i = 0 ; i < size ; i++){
        for(int j = 0 ; j < size ; j++){
            new_state[i*size+j] = false;
        }
    }
    new_state[3*size+3] = true;
    new_state[3*size+4] = true;
    new_state[3*size+5] = true;
    new_state[4*size+3] = true;
    new_state[4*size+4] = true;
    new_state[4*size+2] = true;

    map2d.setArrayState<bool>(0,new_state);
    map2d.synch();
    bool* state = construct_array<bool>(size,size);
    map2d.getArrayState<bool>(0,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(2,4,0));

    map2d.compute();
    map2d.synch();
    map2d.getArrayState<bool>(0,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(3,5,0));

    map2d.compute();
    map2d.synch();
    map2d.getArrayState<bool>(0,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(2,4,0));

}

void test_Map2D(int size){
    Map2D map2d(size,size);
    map2d.initCellArray<CellGof>();
    bool* state = construct_array<bool>(size,size);
    map2d.getArrayState<bool>(0,state);

    print_2D_array<bool>(state,size,size);
    cout << endl;
    map2d.setCellState<bool>(3,3,0,true);
    map2d.synch();
    map2d.getArrayState<bool>(0,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(3,3,0));

    bool* new_state;
    new_state = construct_array<bool>(size,size);
    new_state[3*size+3] = true;
    new_state[3*size+4] = true;
    new_state[3*size+5] = true;
    new_state[4*size+3] = true;
    new_state[4*size+4] = true;
    new_state[4*size+2] = true;

    map2d.setArrayState<bool>(0,new_state);
    map2d.synch();
    map2d.getArrayState<bool>(0,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(3,3,0));
    assert(map2d.getCellState<bool>(3,4,0));
    assert(map2d.getCellState<bool>(4,4,0));
}

void test_register(){
    Register<int> regInt(10);
    assert(regInt.get() == 10);
    regInt.set(20);
    assert(regInt.get() == 10);
    regInt.synch();
    assert(regInt.get() == 20);
}

void test_cellgof(){
    CellGof cell;
    assert(!cell.getRegState<bool>(0));
    CellGof cell1,cell2;
    cell1.setRegState<bool>(0,true);
    cell2.setRegState<bool>(0,true);
    cell1.synch();
    cell2.synch();
    assert(cell1.getRegState<bool>(0));
    assert(cell2.getRegState<bool>(0));

    CellGof cell3(true);
    assert(cell3.getRegState<bool>(0));

    vector<Module*> neighs;
    neighs.push_back(&cell1);
    neighs.push_back(&cell2);

    cell.addNeighbours(neighs);
    cell.compute();
    cell.synch();
    assert(!cell.getRegState<bool>(0));//2 neigh is not enough to be alive

    neighs.clear();
    neighs.push_back(&cell3);
    cell.addNeighbours(neighs);
    cell.compute();
    cell.synch();
    assert(cell.getRegState<bool>(0));//3 neigh is  enough to be alive

}


template <typename T>
void print_2D_array(T* array,int width,int height){
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            cout << array[i*width + j] << ",";
        }
        cout << endl;
    }
}

template <typename T>
T* construct_array(int width,int height){
    T * array;
    array = new T[height*width];
    return array;
}

void assertAlmostEquals(float a,float b){
    assert( a-b <= 1/PRECISION);
}

