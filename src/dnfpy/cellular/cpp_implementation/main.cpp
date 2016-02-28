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
#include "bitstreamutils.h"
#include "bitstreamchar.h"
#include "bitstreamuint.h"
#include "cellsbsfast.h"
#include "cellsbsfast2.h"
#include <boost/ptr_container/ptr_vector.hpp>
#include <boost/shared_ptr.hpp>
#include <assert.h>
#include <bitset>
#include "bitstreamuint.h"
#include "sequenceConnecter.h"

typedef boost::shared_ptr<Module> ModulePtr;

using namespace std;
#define PRECISION 1000000


template <typename T>
void print_2D_array(T* array,int width,int height);
template <typename T>
void print_3D_array(T* array,int width,int height,int third);

template <typename T>
T* construct_array(int width,int height);
template <typename T>
T* construct_array3d(int width,int height,int third);

void assertAlmostEquals(float a,float b,float precision=PRECISION);

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
void test_stochastic_rsdnf_carry_router();
void test_stochastic_rsdnf_precision();
void test_stochastic_soft_simu_nstep(int size);
void test_SBS();
void test_SBSChar();
void test_SBSUint();
void test_SBSUint_precision();
void  test_SBSFastMap();
void test_SBSFastMap_precision();
void test_SBSFastMap_2layer();
void test_stoch_bitStream();
Module::ParamsPtr newParams();
void test_sequence_rsdnf_map(int size);

int main()
{
    //            cout << "Hello World!" << endl;
    //            test_register();
    //            cout << "test register passed" << endl;
    //            test_cellgof();
    //            cout << "test cell gof passed" << endl;
    //            test_Map2D(10);
    //            cout << "test Map2D passed" << endl;
    //            test_neumann_connecter(10);
    //            cout << "test neumann connecter passed" << endl;
    //            test_rsdnf_cell();
    //            cout << "test rsdnf passed" << endl;
    //            test_rsdnf_map(11);
    //            cout << "test rsdnf map passed" << endl;

//                test_cell_nspike();
//                cout<< "test cell n spike passed" << endl;
//                test_map_nspike(11);
//                cout << "test map nspike passed" << endl;
    //            test_soft_simu(11);
    //            cout<< "test soft simu passed" <<endl;
    //            test_stochastic_rsdnf_map2(11);
    //            cout << "test stochastic rsdnf map passed" << endl;
    //            test_stochastic_soft_simu_nstep(49);
    //            cout << "test test_stochastic_soft_simu_nstep passed " << endl;
    //            test_stochastic_rsdnf();
    //            cout << "test stochastic rsdnf passed" << endl;
    //            test_stochastic_rsdnf_map_carry_router(11);
    //            cout << "test stochastic rsdnf map carry router passed" << endl;
    //            test_stochastic_rsdnf_carry_router();
    //            cout << "test stochastic rsdnf carry router passed" << endl;

    //                test_stochastic_rsdnf_precision();
    //                cout << "test stochastic rsdnf precision passed" << endl;
    //                test_SBS();
    //                cout << " test SBS passed " << endl;
    //                test_SBSChar();
    //                cout << " test SBS char passed " << endl;
//    test_SBSUint();
//    cout << " test SBS Uint passed " << endl;
//    test_SBSUint_precision();
//    cout << "test SBS uint precision passed " << endl;
//    test_SBSFastMap();
//    cout << " test sbs fast map passed" << endl;
//    test_SBSFastMap_precision();
//    cout << "test sbsfastmap precision passed" << endl;
//    test_SBSFastMap_2layer();
//    cout << "test sbsFast map 2 layer passed " << endl;
//    test_stoch_bitStream();
//    cout << "test stoch bit stream passed" << endl;

    test_sequence_rsdnf_map(11);
    cout << "test map sequence rsdnf passed" << endl;


    //    cout << "ALL TEST PASSED " << endl;
    return 0;
}
Module::ParamsPtr newParams(){
    return Module::ParamsPtr(new std::vector<void*>());
}


void test_sequence_rsdnf_map(int size){
    RsdnfConnecter c;
    SequenceConnecter c2;
    cout << "start " << endl;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>("sequence");
    map2d.connect(c);
    map2d.connect(c2);

    int* randState = construct_array3d<int>(size,size,4);

    map2d.getArraySubState(2,randState);
    print_3D_array<int>(randState,size,size,4); 

    randState[0] = 1;
    randState[size*4-2] = 1;
    randState[size*size*4-1] = 1;
    map2d.setArraySubState(2,randState);
    map2d.synch();
    map2d.compute();
    map2d.synch();
    map2d.compute();
    map2d.synch();
    map2d.getArraySubState(2,randState);
    print_3D_array<int>(randState,size,size,4); 
    assert(randState[8]==1);//check propagation of random numbers simple
    assert(randState[7]==1);//check propagation of random numbers end of array
    assert(randState[size*4+6]==1);//check propagation of random numbers end of row
    
    //generate random map with only one
    for(size_t i =0 ; i < size*size*4 ; ++i)
        randState[i] = 1;
    map2d.setArraySubState(2,randState);
    map2d.synch();
    map2d.getArraySubState(2,randState);
    print_3D_array<int>(randState,size,size,4); 

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
    assert(stateInt[0] == 1);
    assert(stateInt[1] == 2);
    assert(stateInt[2] == 3);
    cout <<"time diff : " << difftime(after,before)/200 << endl;

    //generate random map with P = 0.9
    for(size_t i =0 ; i < size*size*4 ; ++i)
        randState[i] = rand() % 0x3FFFFFFF < 0.8 * 0x3FFFFFFF;
    print_3D_array<int>(randState,size,size,4);
    map2d.reset();
    map2d.setArraySubState(2,randState);
    map2d.setCellAttribute(5,5,CellRsdnf::ACTIVATED,&activated);
    map2d.synch();
    for(int i = 0 ; i < 10 ; i ++){
        map2d.compute();
        map2d.synch();
    }
    map2d.getArrayAttribute<int>(CellRsdnf::NB_BIT_RECEIVED,stateInt);
    print_2D_array<int>(stateInt,size,size);
    map2d.getArraySubState(2,randState);
    print_3D_array<int>(randState,size,size,4);



}

void test_stoch_bitStream(){
    unsigned int nbChunck = 10;
    vector<float> probaVec(nbChunck);
    for(unsigned int i = 0 ; i < nbChunck ; ++i)
        probaVec[i] = 0.5;


    std::vector<u_int32_t> chuncks = generateRotatedBitChunck32(nbChunck,probaVec,20,31,0x7fffffff,0x000000ff);
    for(unsigned int i = 0 ; i < nbChunck ; ++i){
        cout << i<<": " << std::bitset<32>(chuncks[i]) << " popcount : " << __builtin_popcount(chuncks[i]) << endl;
    }


    chuncks = generateRotatedBitChunck32(nbChunck,probaVec,0,31,0x7fffffff,0x000000ff);
    for(unsigned int i = 0 ; i < nbChunck ; ++i){
        cout << i<<": " << std::bitset<32>(chuncks[i]) << " popcount : " << __builtin_popcount(chuncks[i]) << endl;
    }

    chuncks = generateRotatedBitChunck32(nbChunck,probaVec,1,9,0x000001ff,0x000000ff);
    //    for(unsigned int i = 0 ; i < nbChunck ; ++i){
    //        cout << i<<": " << std::bitset<32>(chuncks[i]) << " popcount : " << __builtin_popcount(chuncks[i]) << endl;
    //    }

    //As we have only 9 random bit the chunck #0 and #9 are the same
    assert(chuncks[0] == chuncks[9]);

    std::vector<BitStreamUint::BSBPtr> sbsVec = genRotatedSBS(nbChunck,probaVec,100,1,9,0x000000ff);
    //    for(unsigned int i = 0 ; i < nbChunck ; ++i){
    //        cout << i<<": " << " mean : " << sbsVec[i]->mean() << endl;
    //    }
    assert(sbsVec[0]->mean() == sbsVec[9]->mean());

    sbsVec = genRotatedSBS(nbChunck,probaVec,10000,7,31,0x7fffffff);
    //    for(unsigned int i = 0 ; i < nbChunck ; ++i){
    //        cout << i<<": " << " mean : " << sbsVec[i]->mean() << endl;
    //    }

    //The special proba are encoded as it. But it doesnot affect the random bit rotation
    probaVec[0] = 1;
    probaVec[1] = 0;
    sbsVec = genRotatedSBS(nbChunck,probaVec,10000,7,31,0x7fffffff);
    //    for(unsigned int i = 0 ; i < nbChunck ; ++i){
    //        cout << i<<": " << " mean : " << sbsVec[i]->mean() << endl;
    //    }
    assert(sbsVec[0]->mean() == 1);
    assert(sbsVec[1]->mean() == 0);

    for(unsigned int i = 0 ; i < nbChunck ; ++i)
        probaVec[i] = 0.;
    sbsVec = genRotatedSBS(nbChunck,probaVec,10000,7,31,0x7fffffff);
    //    for(unsigned int i = 0 ; i < nbChunck ; ++i){
    //        cout << i<<": " << " mean : " << sbsVec[i]->mean() << endl;
    //    }


}


void test_SBSFastMap_2layer(){
    int size = 11;
    int hSize = size/2;

    int mapId = initSimu(size,size,"cellsbsfast2","rsdnfconnecter2layer");
    useMap(mapId);
    setMapParamInt(CellSBSFast::SIZE_STREAM,10);
    setMapParamFloat(CellSBSFast::PROBA_SYNAPSE,1.);
    setMapParamFloat(CellSBSFast2::PROBA_SYNAPSE_INH,1.);
    assert(getMapParamFloat(CellSBSFast2::PROBA_SYNAPSE_INH) == 1.);


    initMapSeed(255);//reproductibility
    bool activate = true;
    int* nb_sp = construct_array<int>(size,size);
    int* nb_spInh = construct_array<int>(size,size);

    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);

    preCompute();
    step();
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    getArrayAttributeInt(CellSBSFast2::NB_BIT_INH_RECEIVED,nb_spInh);
    cout << "Exc : " << endl;
    print_2D_array<int>(nb_sp,size,size);
    cout << "Inh : " << endl;
    print_2D_array<int>(nb_spInh,size,size);
    assert(nb_sp[hSize*size+hSize] == 10);
    assert(nb_spInh[hSize*size+hSize] == 10);

    reset();
    setMapParamInt(CellSBSFast::SIZE_STREAM,100);
    setMapParamFloat(CellSBSFast::PROBA_SYNAPSE,0.9);
    setMapParamFloat(CellSBSFast2::PROBA_SYNAPSE_INH,0.1);
    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);
    preCompute();
    step();
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    getArrayAttributeInt(CellSBSFast2::NB_BIT_INH_RECEIVED,nb_spInh);
    cout << "Exc : " << endl;
    print_2D_array<int>(nb_sp,size,size);
    cout << "Inh : " << endl;
    print_2D_array<int>(nb_spInh,size,size);
    // assert(nb_sp[hSize*size+hSize] == 94);
    //assert(nb_spInh[hSize*size+hSize] == 1);

    size = 11;
    hSize = size/2;
    mapId = initSimu(size,size,"cellsbsfast2","rsdnfconnecter2layer");
    useMap(mapId);
    setMapParamInt(CellSBSFast::SIZE_STREAM,1000);
    setMapParamFloat(CellSBSFast::PROBA_SPIKE,0.01);
    setMapParamFloat(CellSBSFast::PROBA_SYNAPSE,1);
    setMapParamFloat(CellSBSFast2::PROBA_SYNAPSE_INH,1);
    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);
    preCompute();
    step();
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    getArrayAttributeInt(CellSBSFast2::NB_BIT_INH_RECEIVED,nb_spInh);
    cout << "Exc : " << endl;
    print_2D_array<int>(nb_sp,size,size);
    cout << "Inh : " << endl;
    print_2D_array<int>(nb_spInh,size,size);
    assert(nb_sp[hSize*size+hSize] == 19);
    assert(nb_spInh[hSize*size+hSize] == 19);



}

void test_SBSFastMap_precision(){
    int size = 11;
    int hSize = size/2;

    int mapId = initSimu(size,size,"cellsbsfast","rsdnfconnecter");
    useMap(mapId);
    setMapParamInt(CellSBSFast::SIZE_STREAM,10);
    setMapParamInt(CellSBSFast::PRECISION_PROBA,1);
    assert(getMapParamInt(CellSBSFast::PRECISION_PROBA) == 1);
    //A proba of 0.99 should be equivalent to 0.5
    setMapParamFloat(CellSBSFast::PROBA_SYNAPSE,0.99);


    initMapSeed(255);//reproductibility
    bool activate = true;
    int* nb_sp = construct_array<int>(size,size);

    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);

    preCompute();
    step();
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    //    assert(nb_sp[hSize*size+hSize] == 1);
    //    assert(nb_sp[hSize*size+hSize+1] == 8);
    //    assert(nb_sp[hSize*size+hSize-1] == 7);
    reset();

    setMapParamInt(CellSBSFast::PRECISION_PROBA,3);
    assert(getMapParamInt(CellSBSFast::PRECISION_PROBA) == 3);
    //A proba of 0.99 should be equivalent to 0.75
    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);
    preCompute();
    step();
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    //    assert(nb_sp[hSize*size+hSize] == 5);
    //    assert(nb_sp[hSize*size+hSize+1] == 9);
    //    assert(nb_sp[hSize*size+hSize-1] == 8);
    reset();
}

void test_SBSFastMap(){
    int size = 101;
    int hSize = size/2;

    int mapId = initSimu(size,size,"cellsbsfast","rsdnfconnecter");
    useMap(mapId);
    setMapParamInt(CellSBSFast::SIZE_STREAM,10);
    //    setMapParamFloat(CellSBSFast::PROBA_SYNAPSE,0.9,".");

    initMapSeed(255);//reproductibility
    bool activate = true;
    int* nb_sp = construct_array<int>(size,size);

    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);

    preCompute();
    step();
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    // print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[hSize*size+hSize] == 10);
    reset();

    setMapParamInt(CellSBSFast::SIZE_STREAM,1000);
    setMapParamFloat(CellSBSFast::PROBA_SPIKE,0.05);
    setMapParamFloat(CellSBSFast::PROBA_SYNAPSE,0.9);
    clock_t start = clock(), diff;
    // Time taken 2 seconds 277 milliseconds 3 * SS=1000 res = 101 release
    // Time taken 1 seconds 801 milliseconds after opti (use of simpleVal)
    for(unsigned int i = 0 ; i < 3 ; ++i){
        reset();
        setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
        setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
        setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);
        preCompute();
        step();
        cout << "step " << i << endl;

    }
    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    //print_2D_array<int>(nb_sp,size,size);
    diff = clock() - start;
    int msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);



    //    reset();
    //    setMapParamInt(CellSBSFast::SIZE_STREAM,255,".");
    //    setCellAttribute(hSize,hSize,CellSBSFast::ACTIVATED,&activate);
    //    setCellAttribute(hSize+2,hSize+2,CellSBSFast::ACTIVATED,&activate);
    //    setCellAttribute(hSize-2,hSize,CellSBSFast::ACTIVATED,&activate);

    //    start = clock();
    //    // Time taken 4 seconds 638 milliseconds 500 step
    //    step();
    //    diff = clock() - start;
    //    msec = diff * 1000 / CLOCKS_PER_SEC;
    //    printf("Time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);
    //    getArrayAttributeInt(CellSBSFast::NB_BIT_RECEIVED,nb_sp);
    //    print_2D_array<int>(nb_sp,size,size);
    //    assert(nb_sp[hSize*size+hSize] == 255);

    delete[] nb_sp;
}
void test_SBSUint_precision(){
    unsigned int sizeStream = 100000;
    BitStreamUint a = BitStreamUint(0.99,sizeStream,1);
    assertAlmostEquals(a.mean(),0.5,100);

    a = BitStreamUint(0.99,sizeStream,3);
    assertAlmostEquals(a.mean(),0.75,100);

    a = BitStreamUint(0.02,sizeStream,3);
    assertAlmostEquals(a.mean(),0.25,100);

    a = BitStreamUint(0.99999,sizeStream,PRECISION_MAX);
    assertAlmostEquals(a.mean(),1.,100);

    a = BitStreamUint(0.5,sizeStream,PRECISION_MAX);
    assertAlmostEquals(a.mean(),0.5,100);
}

void test_SBSUint(){

    BitStreamUint sbs = BitStreamUint(0.5,10000);
    assertAlmostEquals(sbs.mean(),0.5037);
    BitStreamUint copy = BitStreamUint(1,10);
    copy.copy(sbs);
    assert(copy.mean() == sbs.mean());

    sbs = BitStreamUint(0,100);
    copy = BitStreamUint(0.1,100);
    copy.copy(sbs);
    assert(copy.mean() == sbs.mean());
    //cout << " copy should be 0 : " <<  copy << endl;

    sbs = BitStreamUint(1,100);
    assert(sbs.mean() == 1);
    copy = BitStreamUint(0,10);
    copy.copy(sbs);
    assert(copy.mean() == sbs.mean());
    //cout << " copy should be 1 : "  << copy << endl;

    unsigned int sizeStream = 10000;
    BitStreamUint a = BitStreamUint(0.9,sizeStream,0x7fffffff);
    //cout << "a . mean " << a.mean() << endl;
    assertAlmostEquals(a.mean() == 0.9,100);


    sizeStream = 255;
    BitStreamUint* ap = new BitStreamUint(sizeStream);
    BitStreamUint* bp = new BitStreamUint(sizeStream);
    assert(ap->count_ones() == 0);
    assert(bp->count_ones() == 0);
    assert((*(ap)&=*(bp)).count_ones() == 0);
    assert((*(ap)|=*(bp)).count_ones() == 0);


    ap = new BitStreamUint(0.5,20);
    bp = new BitStreamUint(0.5,20);
    *(ap)&=(*bp);


    //check that no prob = p== 0
    sbs = BitStreamUint(10000);
    assert(sbs.mean() == 0.);
    assert(sbs.count_ones() == 0 );

    initSeed(0);
    a = BitStreamUint(1,100);
    BitStreamUint b = BitStreamUint(0,1);
    //cout  << "a : " << a << endl;
    //cout  << "b : " << b << endl;
    assert((a&=b).mean()==0);
    a = BitStreamUint(1,100);
    b = BitStreamUint(0,100);
    assert((b&=a).mean()==0);
    a = BitStreamUint(1,100);
    b = BitStreamUint(0,100);
    //cout << "b|a : " << (b|=a).mean() << endl;
    assert((b|=a).mean()==1);
    a = BitStreamUint(1,100);
    b = BitStreamUint(0,100);
    assert((a|=b).mean()==1);

    a = BitStreamUint(0,100);
    b = BitStreamUint(1,1);
    assert((a&=b).mean()==0);
    a = BitStreamUint(0,100);
    b = BitStreamUint(1,1);
    assert((b&=a).mean()==0);
    a = BitStreamUint(0,100);
    b = BitStreamUint(1,1);
    assert((b|=a).mean()==1);
    a = BitStreamUint(0,100);
    b = BitStreamUint(1,1);
    assert((a|=b).mean()==1);



    sizeStream = 1;
    sbs = BitStreamUint(1,sizeStream);
    assert(sbs.mean() == 1.);
    assert(sbs.count_ones() ==1);
    //cout << (BitStreamUint)sbs << endl;

    sizeStream = 20;
    sbs = BitStreamUint(1,sizeStream);
    assert(sbs.count_ones() ==20);
    //cout << (BitStreamUint)sbs << " means " << sbs.mean() <<  endl;



    sizeStream = 10000;
    sbs = BitStreamUint(1,sizeStream);
    assert(sbs.mean() == 1.);
    //cout << sbs.mean() << endl;

    sbs = BitStreamUint (0,sizeStream);
    assert(sbs.mean() == 0.);

    sizeStream = 1000000;
    initSeed(255);

    clock_t start = clock(), diff;
    //Time construction 2 seconds 297 milliseconds
    //1 second and 195 milisecond
    for(unsigned int i = 0 ; i < 100 ; ++i){
        sbs = BitStreamUint (0.5,sizeStream);
    }
    diff = clock() - start;
    int msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time construction %d seconds %d milliseconds. Was 1.195 before.\n", msec/1000, msec%1000);

    start = clock();
    //Time mean 16 seconds 505 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        sbs.mean();
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time mean %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << sbs.mean() << endl;


    a = BitStreamUint (0.5,sizeStream);
    b = BitStreamUint (0.5,sizeStream);
    //BitStreamUint  res = BitStreamUint (sizeStream);

    //    start = clock();
    //    //Time | 32 seconds 379 milliseconds
    //    for(unsigned int i = 0 ; i < 10000 ; ++i){

    //        res = a | b;
    //    }
    //    diff = clock() - start;
    //    msec = diff * 1000 / CLOCKS_PER_SEC;
    //    printf("Time | %d seconds %d milliseconds\n", msec/1000, msec%1000);
    //    cout << res.mean() << endl;


    //    start = clock();
    //    //Time & 32 seconds 31 milliseconds
    //    for(unsigned int i = 0 ; i < 10000 ; ++i){
    //        res = a & b;
    //    }
    //    diff = clock() - start;
    //    msec = diff * 1000 / CLOCKS_PER_SEC;
    //    printf("Time & %d seconds %d milliseconds\n", msec/1000, msec%1000);
    //    cout << res.mean() << endl;


    //TEST &=
    for(unsigned int i = 0 ; i < 10 ; ++i){
        a &= b;
    }
    cout << "a &= b" <<  a.mean() << endl;

    //TEST &=
    for(unsigned int i = 0 ; i < 10 ; ++i){
        a |= b;
    }
    cout <<"a |= b" <<  a.mean() << endl;

}


void test_SBSChar(){
    initSeed(0);
    unsigned int sizeStream = 10000;
    BitStreamChar sbs = BitStreamChar(1,sizeStream);
    assert(sbs.mean() == 1.);
    cout << sbs.mean() << endl;

    sbs = BitStreamChar(0,sizeStream);
    assert(sbs.mean() == 0.);

    sizeStream = 1000000;
    initSeed(255);

    clock_t start = clock(), diff;
    //Time construction 2 seconds 297 milliseconds
    for(unsigned int i = 0 ; i < 100 ; ++i){
        sbs = BitStreamChar(0.5,sizeStream);
    }
    diff = clock() - start;
    int msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time construction %d seconds %d milliseconds\n", msec/1000, msec%1000);

    start = clock();
    //Time mean 16 seconds 505 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        sbs.mean();
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time mean %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << sbs.mean() << endl;


    BitStreamChar a = BitStreamChar(0.5,sizeStream);
    BitStreamChar b = BitStreamChar(0.5,sizeStream);
    BitStreamChar res = BitStreamChar(sizeStream);

    start = clock();
    //Time | 32 seconds 379 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        res = a | b;
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time | %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << res.mean() << endl;


    start = clock();
    //Time & 32 seconds 31 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        res = a & b;
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time & %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << res.mean() << endl;
}


void test_SBS(){
    initSeed(0);
    unsigned int sizeStream = 10000;
    vector<u_int64_t> sbs = newSBS(1,sizeStream);
    assert(sbs.size() == 157); //157*64 = 10048
    assert(sbs[0] == 0xffffffffffffffff);
    assert(sbs[sbs.size()-1] == 0xffffffffffffffff);
    assert(count_ones(sbs) == 10048);
    assert(meanSBS(sbs) == 1.);

    sbs = newSBS(0,sizeStream);
    assert(sbs[0] == 0x0);
    assert(sbs[sbs.size()-1] == 0x0);
    assert(count_ones(sbs) == 0);
    assert(meanSBS(sbs) == 0.);

    sizeStream = 1000000;
    initSeed(255);

    clock_t start = clock(), diff;
    //1 seconds 379 milliseconds
    for(unsigned int i = 0 ; i < 100 ; ++i){
        sbs = newSBS(0.5,sizeStream);
    }
    diff = clock() - start;
    int msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time construction %d seconds %d milliseconds\n", msec/1000, msec%1000);

    start = clock();
    //Time mean 1 second 379 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        meanSBS(sbs);
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time mean %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << meanSBS(sbs) << endl;
    assert_perror(meanSBS(sbs) == 0.500042);



    vector<u_int64_t> a = newSBS(0.5,sizeStream);
    vector<u_int64_t> b = newSBS(0.5,sizeStream);
    vector<u_int64_t> res;

    start = clock();
    //Time | 1 seconds 379 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        res = a | b;
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time | %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << meanSBS(res) << endl;


    start = clock();
    //Time & 1 seconds 31 milliseconds
    for(unsigned int i = 0 ; i < 10000 ; ++i){
        res = a & b;
    }
    diff = clock() - start;
    msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time & %d seconds %d milliseconds\n", msec/1000, msec%1000);
    cout << meanSBS(res) << endl;
}

void test_stochastic_rsdnf_carry_router(){
    ModulePtr cell = ModulePtr(new CellBsRsdnf("carryRouter"));
    ModulePtr rn,rs,re,rw;
    RsdnfConnecter c;
    rn = ModulePtr(new CellBsRsdnf());
    rs = ModulePtr(new CellBsRsdnf());
    re = ModulePtr(new CellBsRsdnf());
    rw = ModulePtr(new CellBsRsdnf());

    c.cellConnection(cell);
    c.cellNeighbourConnection(cell,rn,c.N);
    c.cellNeighbourConnection(cell,rs,c.S);
    c.cellNeighbourConnection(cell,re,c.E);
    c.cellNeighbourConnection(cell,rw,c.W);

    c.cellConnection(rn);
    c.cellNeighbourConnection(rn,cell,c.S);
    c.cellConnection(rs);
    c.cellNeighbourConnection(rs,cell,c.N);
    c.cellConnection(re);
    c.cellNeighbourConnection(re,cell,c.W);
    c.cellConnection(rw);
    c.cellNeighbourConnection(rw,cell,c.E);
    Module::ParamsPtr params = newParams();
    cell->setDefaultParams(params);
    cell->setParams(params);
    rn->setParams(params);
    rs->setParams(params);
    re->setParams(params);
    rw->setParams(params);
    cell->setParam<float>(CellBsRsdnf::PROBA_SYNAPSE,1);


    bool activated = true;
    cell->setAttribute(CellBsRsdnf::ACTIVATED,&activated);

    cell->compute();
    cell->synch();
    assert(cell->getRegState(CellBsRsdnf::SPIKE_BS)==1);

    cell->compute();
    cell->synch();
    assert(cell->getSubModule(0).get()->getRegState(BSRouter::BS_OUT)==1);
    assert(cell->getSubModule(1).get()->getRegState(BSRouter::BS_OUT)==1);

    cell->compute();
    rn->compute();
    cell->synch();
    rn->synch();
    int nbB;
    rn->getAttribute(CellBsRsdnf::NB_BIT_RECEIVED,&nbB);
    assert(nbB == 1);
    assert(rn->getSubModule(0)->getRegState(BSRouter::BS_OUT)==1);
    assert(rn->getSubModule(2)->getRegState(BSRouter::BS_OUT)==1);

}


void test_stochastic_rsdnf_map_carry_router(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellBsRsdnf>("carryRouter");
    map2d.connect(c);

    map2d.initMapSeed(0);

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
    //    assert(map2d.getCellState(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);
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
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);

    for(int i = 0 ; i < 1000 ; i ++){
        map2d.compute();
        map2d.synch();
    }
    cout << "compute" << endl;
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    //    assert(nb_sp[0]==20);
    //    assert(nb_sp[size]==20);


}

void test_stochastic_rsdnf(){
    ModulePtr cell = ModulePtr(new CellBsRsdnf());
    ModulePtr rn,rs,re,rw;
    RsdnfConnecter c;
    rn = ModulePtr(new CellBsRsdnf());
    rs = ModulePtr(new CellBsRsdnf());
    re = ModulePtr(new CellBsRsdnf());
    rw = ModulePtr(new CellBsRsdnf());

    c.cellConnection(cell);
    c.cellNeighbourConnection(cell,rn,c.N);
    c.cellNeighbourConnection(cell,rs,c.S);
    c.cellNeighbourConnection(cell,re,c.E);
    c.cellNeighbourConnection(cell,rw,c.W);

    c.cellConnection(rn);
    c.cellNeighbourConnection(rn,cell,c.S);
    c.cellConnection(rs);
    c.cellNeighbourConnection(rs,cell,c.N);
    c.cellConnection(re);
    c.cellNeighbourConnection(re,cell,c.W);
    c.cellConnection(rw);
    c.cellNeighbourConnection(rw,cell,c.E);

    Module::ParamsPtr params = newParams();
    cell->setDefaultParams(params);
    cell->setParams(params);
    rn->setParams(params);
    rs->setParams(params);
    re->setParams(params);
    rw->setParams(params);
    cell->setParam<float>(CellBsRsdnf::PROBA_SYNAPSE,1);




    bool activated = true;
    cell->setAttribute(CellBsRsdnf::ACTIVATED,&activated);

    cell->compute();
    cell->synch();
    assert(cell->getRegState(CellBsRsdnf::SPIKE_BS)==1);

    cell->compute();
    cell->synch();
    assert(cell->getSubModule(0)->getRegState(BSRouter::BS_OUT)==1);
    assert(cell->getSubModule(1)->getRegState(BSRouter::BS_OUT)==1);

    cell->compute();
    rn->compute();
    cell->synch();
    rn->synch();
    int nbB;
    rn->getAttribute(CellBsRsdnf::NB_BIT_RECEIVED,&nbB);
    assert(nbB == 1);
    assert(rn->getSubModule(0)->getRegState(BSRouter::BS_OUT)==1);
    assert(rn->getSubModule(2)->getRegState(BSRouter::BS_OUT)==1);

}

void test_stochastic_rsdnf_precision(){
    initSeed(0);
    ModulePtr cell = ModulePtr(new CellBsRsdnf());
    ModulePtr rn,rs,re,rw;
    RsdnfConnecter c;
    rn = ModulePtr(new CellBsRsdnf());
    rs = ModulePtr(new CellBsRsdnf());
    re = ModulePtr(new CellBsRsdnf());
    rw = ModulePtr(new CellBsRsdnf());

    c.cellConnection(cell);
    c.cellNeighbourConnection(cell,rn,c.N);
    c.cellNeighbourConnection(cell,rs,c.S);
    c.cellNeighbourConnection(cell,re,c.E);
    c.cellNeighbourConnection(cell,rw,c.W);

    c.cellConnection(rn);
    c.cellNeighbourConnection(rn,cell,c.S);
    c.cellConnection(rs);
    c.cellNeighbourConnection(rs,cell,c.N);
    c.cellConnection(re);
    c.cellNeighbourConnection(re,cell,c.W);
    c.cellConnection(rw);
    c.cellNeighbourConnection(rw,cell,c.E);
    Module::ParamsPtr params = newParams();
    cell->setDefaultParams(params);
    cell->setParams(params);
    rn->setParams(params);
    rs->setParams(params);
    re->setParams(params);
    rw->setParams(params);

    cell->setParam<unsigned long int>(CellBsRsdnf::PRECISION_PROBA,1);
    //With a precision of 1, we cannot encode a proba of 0.9999

    cell->setParam<float>(CellBsRsdnf::PROBA_SYNAPSE,0.9999);
    cell->setParam<float>(CellBsRsdnf::PROBA_SPIKE,1);


    bool activated = true;
    cell->setAttribute(CellBsRsdnf::ACTIVATED,&activated);

    cell->compute();
    cell->synch();
    assert(cell->getRegState(CellBsRsdnf::SPIKE_BS)==1);

    cell->compute();
    cell->synch();
    assert(cell->getSubModule(0)->getRegState(BSRouter::BS_OUT)==0);
    assert(cell->getSubModule(1)->getRegState(BSRouter::BS_OUT)==1);

    cell->compute();
    rn->compute();
    cell->synch();
    rn->synch();
    int nbB;
    rn->getAttribute(CellBsRsdnf::NB_BIT_RECEIVED,&nbB);
    assert(nbB == 0);
    assert(rn->getSubModule(0)->getRegState(BSRouter::BS_OUT)==0);
    assert(rn->getSubModule(2)->getRegState(BSRouter::BS_OUT)==0);

}

Map2D initMap2D(int size){
    RsdnfConnecter c;
    Map2D map2d(size,size);
    map2d.initCellArray<CellBsRsdnf>();
    map2d.connect(c);
    map2d.initMapSeed(0);//reproductibility
    return map2d;
}

void activateMap2D(Map2D &map2d,int size){
    int hSize = size/2;
    bool activate = true;
    //00000
    //00000
    //10x00
    //00000
    //00001
    map2d.setCellAttribute(hSize,hSize,CellBsRsdnf::ACTIVATED,&activate);
    map2d.setCellAttribute(hSize+2,hSize+2,CellBsRsdnf::ACTIVATED,&activate);
    map2d.setCellAttribute(hSize-2,hSize,CellBsRsdnf::ACTIVATED,&activate);
}

void test_stochastic_soft_simu_nstep(int size){
    int hSize = size/2;
    int mapId = initSimu(size,size,"cellbsrsdnf","rsdnfconnecter");
    useMap(mapId);
    initMapSeed(255);//reproductibility
    bool activate = true;
    int* nb_sp = construct_array<int>(size,size);

    setCellAttribute(hSize,hSize,CellBsRsdnf::ACTIVATED,&activate);
    setCellAttribute(hSize+2,hSize+2,CellBsRsdnf::ACTIVATED,&activate);
    setCellAttribute(hSize-2,hSize,CellBsRsdnf::ACTIVATED,&activate);

    clock_t start = clock(), diff;
    // Time taken 4 seconds 638 milliseconds 500 step
    nstep(500);
    diff = clock() - start;
    int msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);
    getArrayAttributeInt(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[hSize*size+hSize-1]==24);
    assert(nb_sp[hSize*size+hSize+1]==22);
    assert(nb_sp[(hSize-1)*size+hSize]==24);
    assert(nb_sp[(hSize+1)*size+hSize]==22);


}

void test_stochastic_rsdnf_map2(int size){
    int hSize = size/2;
    Map2D map2d = initMap2D(size);
    map2d.compute();
    map2d.synch();
    int* nb_sp = construct_array<int>(size,size);

    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[0] == 0 && nb_sp[size] == 0);
    activateMap2D(map2d,size);

    //On the first activation a spike bit is generated
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);

    //We assert that 2 cell didnot received spike
    assert(nb_sp[hSize*size+hSize+1] == 0 && nb_sp[(hSize+1)*size+hSize] == 0);
    //We assert the spike out of the central cell is 1
    assert(map2d.getCellState(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);

    //On the second iteration the router of the central cell emmit a spike
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    //We assert that 2 cell didnot received spike
    assert(nb_sp[hSize*size+hSize+1] == 0 && nb_sp[(hSize+1)*size+hSize] == 0);
    //We assert the spike out of the central cell is 1
    assert(map2d.getCellState(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);

    //On the third iteration this spike is at last received by the neighbours
    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[(hSize)*size+hSize-1]==1);
    assert(nb_sp[hSize*size+hSize+1]==1);
    assert(nb_sp[(hSize-1)*size+hSize]==1);
    assert(nb_sp[(hSize+1)*size+hSize]==1);

    cout << "compute" << endl;
    map2d.compute();
    map2d.synch();
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[(hSize)*size+hSize-1]==2);
    assert(nb_sp[hSize*size+hSize+1]==2);
    assert(nb_sp[(hSize-1)*size+hSize]==2);
    assert(nb_sp[(hSize+1)*size+hSize]==2);

    //1 seconds 985 milliseconds
    clock_t start = clock(), diff;
    for(int i = 0 ; i < 1000 ; i ++){
        map2d.compute();
        map2d.synch();

    }
    diff = clock() - start;

    int msec = diff * 1000 / CLOCKS_PER_SEC;
    printf("Time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);
    map2d.getArrayAttribute<int>(CellBsRsdnf::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);
    assert(nb_sp[hSize*size+hSize-1]==24);
    assert(nb_sp[hSize*size+hSize+1]==22);
    assert(nb_sp[(hSize-1)*size+hSize]==24);
    assert(nb_sp[(hSize+1)*size+hSize]==22);



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
    assert(map2d.getCellState(hSize,hSize,CellBsRsdnf::SPIKE_BS) == 1);
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

    float proba = 0.5;
    map2d.setParam<float>(CellNSpike::PROBA_N,proba);
    map2d.setParam<float>(CellNSpike::PROBA_S,proba);
    map2d.setParam<float>(CellNSpike::PROBA_E,proba);
    map2d.setParam<float>(CellNSpike::PROBA_W,proba);
    assert(*((float*)map2d.getMapParam(CellNSpike::PROBA_N)) == 0.5);

    map2d.setCellAttribute(size/2,size/2,CellNSpike::ACTIVATED,&activated);
    map2d.compute();
    map2d.getArrayAttribute<int>(CellNSpike::NB_BIT_RECEIVED,nb_sp);
    print_2D_array<int>(nb_sp,size,size);


    proba = 0.99;
    map2d.setParam<float>(CellNSpike::PROBA_N,proba);
    map2d.setParam<float>(CellNSpike::PROBA_S,proba);
    map2d.setParam<float>(CellNSpike::PROBA_E,proba);
    map2d.setParam<float>(CellNSpike::PROBA_W,proba);
    assertAlmostEquals(*((float*)map2d.getMapParam(CellNSpike::PROBA_N)), 0.99);
    for(int i = 0 ; i < 5 ; i++){
        map2d.setCellAttribute(size/2,size/2,CellNSpike::ACTIVATED,&activated);
        map2d.compute();
        map2d.getArrayAttribute<int>(CellNSpike::NB_BIT_RECEIVED,nb_sp);
        map2d.reset();
        print_2D_array<int>(nb_sp,size,size);

    }



}

void test_cell_nspike(){
    ModulePtr cell = ModulePtr(new CellNSpike());
    srand(0);
    int nb = 10;
    Module::ParamsPtr params = newParams();
    cell->setDefaultParams(params);
    assert(params->size() ==5);
    cell->setParams(params);

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

    ModulePtr cn,cs,ce,cw;
    cn = ModulePtr(new CellNSpike());
    cn->setParams(params);
    cs = ModulePtr(new CellNSpike());
    cs->setParams(params);
    ce = ModulePtr(new  CellNSpike());
    ce->setParams(params);
    cw = ModulePtr(new CellNSpike());
    cw->setParams(params);
    cell->addNeighbour(cn);cn->setAttribute(CellNSpike::DEAD,&dead);
    cell->addNeighbour(cs);cs->setAttribute(CellNSpike::DEAD,&dead);
    cell->addNeighbour(ce);ce->setAttribute(CellNSpike::DEAD,&dead);
    cell->addNeighbour(cw);cw->setAttribute(CellNSpike::DEAD,&dead);


    dead = false;
    int nb_spike = 100;
    cell->setAttribute(CellNSpike::DEAD,&dead);
    cell->setAttribute(CellNSpike::ACTIVATED,&act);

    cell->setParam<int>(CellNSpike::NB_SPIKE,nb_spike);
    assert(cn->getParam<int>(CellNSpike::NB_SPIKE) == nb_spike);
    assert(cs->getParam<int>(CellNSpike::NB_SPIKE) == nb_spike);
    assert(ce->getParam<int>(CellNSpike::NB_SPIKE) == nb_spike);
    assert(cw->getParam<int>(CellNSpike::NB_SPIKE) == nb_spike);
    cell->setParam<float>(CellNSpike::PROBA_E,0.);
    cell->setParam<float>(CellNSpike::PROBA_S,0.5);
    assert(cn->getParam<float>(CellNSpike::PROBA_S) == 0.5);
    assert(cs->getParam<float>(CellNSpike::PROBA_S) == 0.5);
    assert(ce->getParam<float>(CellNSpike::PROBA_S) == 0.5);
    assert(cw->getParam<float>(CellNSpike::PROBA_S) == 0.5);


    cell->compute();
    int NB_BIT_RECEIVED = -99;
    cn->getAttribute(CellNSpike::NB_BIT_RECEIVED,&NB_BIT_RECEIVED);
    assert(NB_BIT_RECEIVED == nb_spike);
    cs->getAttribute(CellNSpike::NB_BIT_RECEIVED,&NB_BIT_RECEIVED);
    //cout << "nb spike received : " << NB_BIT_RECEIVED << endl;
    assert(NB_BIT_RECEIVED == 54);
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

    ModulePtr cell = ModulePtr(new CellRsdnf());
    ModulePtr neigh = ModulePtr(new CellRsdnf());
    //Set the params
    Module::ParamsPtr params = newParams();
    cell->setDefaultParams(params);
    cell.get()->setParams(params);
    neigh.get()->setParams(params);

    //Connect the cells
    cell->getSubModule(0)->addNeighbour(cell);
    cell.get()->getSubModule(0)->addNeighbour(neigh.get()->getSubModule(0));
    cell.get()->addNeighbour(neigh.get()->getSubModule(0));
    bool activated = true;

    //activate neigh
    neigh.get()->setAttribute(CellRsdnf::ACTIVATED,&activated);
    bool resB;
    neigh.get()->getAttribute(CellRsdnf::ACTIVATED,&resB);
    assert(resB);

    neigh.get()->compute();
    neigh.get()->synch();
    //cout << "router neigh buffer : " << neigh->getSubModule(0)->getRegState(Router::BUFFER) << endl;
    assert(neigh.get()->getSubModule(0)->getRegState(Router::BUFFER) == 19);

    //The cell should get the spike from neigh
    //cout << "compute cell" << endl;
    cell.get()->compute();
    cell.get()->synch();
    assert(cell.get()->getSubModule(0)->getRegState(Router::SPIKE_OUT) == 1);
    int resI;
    cell.get()->getAttribute(CellRsdnf::NB_BIT_RECEIVED,&resI);
    assert(resI == 1);


}

void test_rsdnf_map(int size){
    RsdnfConnecter c;
    cout << "start " << endl;
    Map2D map2d(size,size);
    map2d.initCellArray<CellRsdnf>();
    map2d.connect(c);
    map2d.setParam(CellRsdnf::PROBA,new double(0.9));

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
    int* new_state = construct_array<int>(size,size);
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

    map2d.setArrayState(0,new_state);
    map2d.synch();
    int* state = construct_array<int>(size,size);
    map2d.getArrayState(0,state);
    print_2D_array<int>(state,size,size);
    cout << endl;
    assert(map2d.getCellState(2,4,0));

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(0,state);
    print_2D_array<int>(state,size,size);
    cout << endl;
    assert(map2d.getCellState(3,5,0));

    map2d.compute();
    map2d.synch();
    map2d.getArrayState(0,state);
    print_2D_array<int>(state,size,size);
    cout << endl;
    assert(map2d.getCellState(2,4,0));

}

void test_Map2D(int size){
    Map2D map2d(size,size);
    map2d.initCellArray<CellGof>();
    int* state = construct_array<int>(size,size);
    map2d.getArrayState(0,state);

    print_2D_array<int>(state,size,size);
    cout << endl;
    map2d.setCellState(3,3,0,true);
    map2d.synch();
    map2d.getArrayState(0,state);
    print_2D_array<int>(state,size,size);
    cout << endl;
    assert(map2d.getCellState(3,3,0));

    int* new_state;
    new_state = construct_array<int>(size,size);
    new_state[3*size+3] = true;
    new_state[3*size+4] = true;
    new_state[3*size+5] = true;
    new_state[4*size+3] = true;
    new_state[4*size+4] = true;
    new_state[4*size+2] = true;

    map2d.setArrayState(0,new_state);
    map2d.synch();
    map2d.getArrayState(0,state);
    print_2D_array<int>(state,size,size);
    cout << endl;
    assert(map2d.getCellState(3,3,0));
    assert(map2d.getCellState(3,4,0));
    assert(map2d.getCellState(4,4,0));
}

void test_register(){
    Register regInt(10);
    assert(regInt.get() == 10);
    regInt.set(20);
    assert(regInt.get() == 10);
    regInt.synch();
    assert(regInt.get() == 20);
}

void test_cellgof(){
    CellGof cell;
    assert(!cell.getRegState(0));
    ModulePtr ptr1 = ModulePtr(new CellGof);
    ModulePtr ptr2 = ModulePtr(new CellGof);

    ptr1.get()->setRegState(0,true);
    ptr2.get()->setRegState(0,true);
    ptr1.get()->synch();
    ptr2.get()->synch();
    assert(ptr1.get()->getRegState(0));
    assert(ptr2.get()->getRegState(0));

    ModulePtr ptr3 = ModulePtr(new CellGof(true));
    assert(ptr3.get()->getRegState(0) == 1);


    std::vector<boost::shared_ptr<Module>> neighs;
    neighs.push_back(ptr1);
    neighs.push_back(ptr2);

    cell.addNeighbours(neighs);
    cell.compute();
    cell.synch();
    assert(!cell.getRegState(0));//2 neigh is not enough to be alive

    neighs.clear();
    neighs.push_back(ptr3);
    cell.addNeighbours(neighs);
    cell.compute();
    cell.synch();
    assert(cell.getRegState(0));//3 neigh is  enough to be alive

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
void print_3D_array(T* array,int width,int height,int third){
    for(int i = 0 ; i < height ; i++){
        for(int j = 0 ; j < width ; j++){
            cout << "(";
            for(int k = 0 ; k < third ; k++){
                cout << array[i*(width*third) + j*third +k] << ",";
            }
            cout << ")," ;
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

template <typename T>
T* construct_array3d(int width,int height,int third){
    T * array;
    array = new T[height*width*third];
    return array;
}

void assertAlmostEquals(float a,float b,float precision){
    assert(a-b <= 1./precision);
}

