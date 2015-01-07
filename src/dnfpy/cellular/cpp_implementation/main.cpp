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
using namespace std;

void test_register();
void test_cellgof();
void test_Map2D(int size);
void test_neumann_connecter(int size);
void test_rsdnf_map(int size);
void test_rsdnf_cell();
void test_soft_simu(int size);
void test_cell_nspike();
void test_map_nspike(int size);
int main()
{
    cout << "Hello World!" << endl;
    test_register();
    cout << "test register passed" << endl;
    test_cellgof();
    cout << "test cell gof passed" << endl;
    test_Map2D(10);
    cout << "test Map2D passed" << endl;
    test_neumann_connecter(10);
    cout << "test neumann connecter passed" << endl;
    test_rsdnf_cell();
    cout << "test router passed" << endl;
    test_rsdnf_map(11);
    cout << "test rsdnf map passed" << endl;

    test_cell_nspike();
    cout<< "test cell n spike passed" << endl;
    test_map_nspike(11);
    cout << "test map nspike passed" << endl;
    test_soft_simu(11);
    cout<< "test soft simu passed" <<endl;
    return 0;
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

void test_map_nspike(int size){
    NSpikeConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellNSpike>();
    map2d.connect(c);
    bool activated = true;
    map2d.setCellAttribute(size/2,size/2,CellNSpike::ACTIVATED,&activated);
    map2d.compute();
    int* nb_sp = construct_array<int>(size,size);

    map2d.getArrayAttribute<int>(CellNSpike::NB_SPIKE_RECEIVED,nb_sp);
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
    map2d.getArrayAttribute<int>(CellNSpike::NB_SPIKE_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);



}

void test_cell_nspike(){
    CellNSpike* cell = new CellNSpike();
    int nb = 10;

    cell->setAttribute(CellNSpike::NB_SPIKE_RECEIVED,&nb);
    int res;
    cell->getAttribute(CellNSpike::NB_SPIKE_RECEIVED,&res);
    assert(res == 10);
    nb = 2;
    cell->getAttribute(CellNSpike::NB_SPIKE_RECEIVED,&res);
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
    int nb_spike_received = -99;
    cn->getAttribute(CellNSpike::NB_SPIKE_RECEIVED,&nb_spike_received);
    assert(nb_spike_received == nb_spike);
    cs->getAttribute(CellNSpike::NB_SPIKE_RECEIVED,&nb_spike_received);
    cout << "nb spike received : " << nb_spike_received << endl;
    //assert(nb_spike_received == nb_spike);
    ce->getAttribute(CellNSpike::NB_SPIKE_RECEIVED,&nb_spike_received);
    assert(nb_spike_received == 0);
    cw->getAttribute(CellNSpike::NB_SPIKE_RECEIVED,&nb_spike_received);
    assert(nb_spike_received == nb_spike);


}

void test_soft_simu(int size)
{
    initSimu(size,size,"cellrsdnf","rsdnfconnecter");
    int* stateInt = construct_array<int>(size,size);
    setCellBool(5,5,CellRsdnf::ACTIVATED_OUT,true);
    //simu.map.synch();
    for(int i = 0 ; i < 20 ; i++){
        step();
    }
    getArrayInt(CellRsdnf::POTENTIAL,stateInt);
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

    neigh->setRegState<bool>(CellRsdnf::ACTIVATED_OUT,true);
    neigh->synch();
    assert(neigh->getRegState<bool>(CellRsdnf::ACTIVATED_OUT));

    neigh->compute();
    neigh->synch();
    //cout << "router neigh buffer : " << neigh->getSubModule(0)->getRegState<int>(Router::BUFFER) << endl;
    assert(neigh->getSubModule(0)->getRegState<int>(Router::BUFFER) == 19);

    cell->compute();
    cell->synch();
    assert(cell->getSubModule(0)->getRegState<bool>(Router::SPIKE_OUT));
    assert(cell->getRegState<int>(CellRsdnf::POTENTIAL) == 1);


}

void test_rsdnf_map(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);
    map2d.setMapParam<float>(Router::PROBA,0.9,"./*");


    map2d.setCellState<bool>(5,5,CellRsdnf::ACTIVATED_OUT,true);
    map2d.synch();
    bool* state = construct_array<bool>(size,size);
    map2d.getArrayState<bool>(CellRsdnf::ACTIVATED_OUT,state);
    print_2D_array<bool>(state,size,size);
    cout << endl;

    map2d.compute();
    map2d.synch();
    int* stateInt = construct_array<int>(size,size);
    map2d.getArrayState<int>(CellRsdnf::POTENTIAL,stateInt);
    print_2D_array<int>(stateInt,size,size);
    cout << endl;


    time_t before = time(0);
    for(int i = 0 ; i < 200 ; i ++){
        map2d.compute();
        map2d.synch();
    }
    time_t after = time(0);
    map2d.getArrayState<int>(CellRsdnf::POTENTIAL,stateInt);
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

