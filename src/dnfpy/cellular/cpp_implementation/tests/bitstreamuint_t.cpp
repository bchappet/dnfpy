#define CATCH_CONFIG_MAIN
#include <limits>
#include <catch.hpp>
#include <bitstreamuint.h>
#include <bitstreamutils.h>

using namespace std;


TEST_CASE("generate rotated bitstrem"){
    //TODO check
    initSeed(253);
    int size =32;
    std::vector<float> probaVec;
    for(unsigned int i = 0 ; i < 10 ; i++){
        probaVec.push_back(0.5f);
    }
    vector<BitStreamUint::BSBPtr> bss = genRotatedSBS(10,probaVec,size,size-5,PRECISION_MAX);
    for(int i = 0 ; i < 10 ; ++i){
        cout << *(bss[i].get()) << endl;
    }

}

TEST_CASE("print"){
    initSeed(253);
    int size =100;
    BitStreamUint uut = BitStreamUint(0.8f,size);
    cout << uut << endl;


}


TEST_CASE("copy"){
    initSeed(255);
    int size = 10000;
    BitStreamUint a = BitStreamUint(0.4f,size);
    BitStreamUint b = BitStreamUint(size);
    b.copy(a);
    cout << b.mean() << endl;
    REQUIRE(b.mean() == Approx(0.4086));
}

TEST_CASE("+"){
    initSeed(255);
    int size = 10000;
    BitStreamUint a = BitStreamUint(0.3f,size);
    BitStreamUint b = BitStreamUint(0.4f,size);

    BitStreamUint res = a+b;
    REQUIRE(res.mean() == Approx(0.3575));
}

TEST_CASE("~"){
    initSeed(255);
    int size = 10000;
    BitStreamUint a = BitStreamUint(0.3f,size);

    BitStreamUint res = ~(a);
    REQUIRE(res.mean() == Approx(0.6938));

    a = BitStreamUint(1.0f,size);
    res = ~a;
    REQUIRE(res.mean() == 0);


    a = BitStreamUint(size);
    res = ~a;
    REQUIRE(res.mean() == 1);
}


TEST_CASE("^"){
    initSeed(255);
    int size = 10000;
    BitStreamUint a = BitStreamUint(0.3f,size);
    BitStreamUint b = BitStreamUint(0.4f,size);

    BitStreamUint res = a^b;
    REQUIRE(res.mean() == Approx(0.4582));

    a = BitStreamUint(1.0f,size);
    b = BitStreamUint(0.0f,size);
    res = a ^ b;
    REQUIRE(res.mean() == 1.0);

    a = BitStreamUint(size);
    b = BitStreamUint(size);
    res = a ^ b;
    REQUIRE(res.mean() == 0.0);

    a = BitStreamUint(1.0f,size);
    b = BitStreamUint(1.0f,size);
    res = a ^ b;
    REQUIRE(res.mean() == 0.0);

    a = BitStreamUint(0.0f,size);
    b = BitStreamUint(1.0f,size);
    res = a ^ b;
    REQUIRE(res.mean() == 1.0);

}

TEST_CASE("|"){
    initSeed(255);
    int size = 10000;
    BitStreamUint a = BitStreamUint(0.3f,size);
    BitStreamUint b = BitStreamUint(0.4f,size);

    BitStreamUint res = a|b;
    REQUIRE(res.mean() == Approx(0.585));

    a = BitStreamUint(1.0f,size);
    b = BitStreamUint(0.0f,size);
    res = a | b;
    REQUIRE(res.mean() == 1.0);

    a = BitStreamUint(size);
    b = BitStreamUint(size);
    res = a | b;
    REQUIRE(res.mean() == 0.0);

    a = BitStreamUint(1.0f,size);
    b = BitStreamUint(1.0f,size);
    res = a | b;
    REQUIRE(res.mean() == 1.0);

    a = BitStreamUint(0.0f,size);
    b = BitStreamUint(1.0f,size);
    res = a | b;
    REQUIRE(res.mean() == 1.0);
}



TEST_CASE("apply counter"){
    initSeed(255);
    int size = 100;
    BitStreamUint a = BitStreamUint(0.3f,size);

    BitStreamUint res = a.applyCounter(10,size);
    REQUIRE(res.count_ones() == 2);
}


