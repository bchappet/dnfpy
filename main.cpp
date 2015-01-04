#include <iostream>
#include "register.h"
#include <assert.h>
#include "cellgof.h"
#include <vector>
#include "map2d.h"
#include "mooreconnecter.h"
#include "cellrsdnf.h"
#include "rsdnfconnecter.h"
#include "test.h"
#include "router.h"
#include "cellrsdnf.h"
using namespace std;

void test_register();
void test_cellgof();
void test_Map2D(int size);
void test_neumann_connecter(int size);
void test_rsdnf_map(int size);
void test_rsdnf_cell();
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
    test_rsdnf_map(101);
    cout << "test rsdnf map passed" << endl;
    return 0;
}

template <typename T>
void print_2D_array(T** array,int width,int height){
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            cout << array[i][j] << ",";
        }
        cout << endl;
    }
}

void test_rsdnf_cell(){
    CellRsdnf* cell;
    CellRsdnf* neigh;
    cell = new CellRsdnf();
    neigh = new CellRsdnf();
    cell->getSubModule(0)->addInput(neigh->getSubModule(0));
    cell->addInput(neigh->getSubModule(0));

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



    map2d.setCellState<bool>(5,5,CellRsdnf::ACTIVATED_OUT,true);
    map2d.synch();
    bool** state = map2d.getArrayState<bool>(CellRsdnf::ACTIVATED_OUT);
    print_2D_array<bool>(state,size,size);
    cout << endl;

    map2d.compute();
    map2d.synch();
    print_2D_array<int>(map2d.getArrayState<int>(CellRsdnf::POTENTIAL),size,size);
    cout << endl;

    for(int i = 0 ; i < 200 ; i ++){
        map2d.compute();
        map2d.synch();
    }
    print_2D_array<int>(map2d.getArrayState<int>(CellRsdnf::POTENTIAL),size,size);
    cout << endl;


}

void test_neumann_connecter(int size){
    MooreConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellGof>();
    map2d.connect(c);
    bool** new_state;
    new_state = new bool*[size];
    for(int i = 0 ; i < size ;i ++)
        new_state[i] = new bool[size];
    for(int i = 0 ; i < size ; i++){
        for(int j = 0 ; j < size ; j++){
            new_state[i][j] = false;
        }
    }
    new_state[3][3] = true;
    new_state[3][4] = true;
    new_state[3][5] = true;
    new_state[4][3] = true;
    new_state[4][4] = true;
    new_state[4][2] = true;

    map2d.setArrayState<bool>(0,new_state);
    map2d.synch();
    print_2D_array<bool>(map2d.getArrayState<bool>(0),size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(2,4,0));

    map2d.compute();
    map2d.synch();
    print_2D_array<bool>(map2d.getArrayState<bool>(0),size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(3,5,0));

    map2d.compute();
    map2d.synch();
    print_2D_array<bool>(map2d.getArrayState<bool>(0),size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(2,4,0));

}

void test_Map2D(int size){
    Map2D map2d(size,size);
    map2d.initCellArray<CellGof>();
    bool** state = map2d.getArrayState<bool>(0);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    map2d.setCellState<bool>(3,3,0,true);
    map2d.synch();
    state = map2d.getArrayState<bool>(0);
    print_2D_array<bool>(state,size,size);
    cout << endl;
    assert(map2d.getCellState<bool>(3,3,0));

    bool** new_state;
    new_state = new bool*[size];
    for(int i = 0 ; i < size ;i ++)
        new_state[i] = new bool;
    new_state[3][3] = true;
    new_state[3][4] = true;
    new_state[3][5] = true;
    new_state[4][3] = true;
    new_state[4][4] = true;
    new_state[4][2] = true;

    map2d.setArrayState<bool>(0,new_state);
    map2d.synch();
    print_2D_array<bool>(map2d.getArrayState<bool>(0),size,size);
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

    cell.addInputs(neighs);
    cell.compute();
    cell.synch();
    assert(!cell.getRegState<bool>(0));//2 neigh is not enough to be alive

    neighs.clear();
    neighs.push_back(&cell3);
    cell.addInputs(neighs);
    cell.compute();
    cell.synch();
    assert(cell.getRegState<bool>(0));//3 neigh is  enough to be alive

}

