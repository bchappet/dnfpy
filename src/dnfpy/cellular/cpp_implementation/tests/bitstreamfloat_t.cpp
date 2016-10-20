#define CATCH_CONFIG_MAIN
#include <limits>
#include <catch.hpp>
#include <bitstreamfloat.h>
using namespace std;

TEST_CASE("print"){
    BitStreamFloat uut = BitStreamFloat(0.8f,100);
    cout << uut << endl;
}

TEST_CASE("and"){
    int size = 100;
    BitStreamFloat a = BitStreamFloat(0.8f,size);
    BitStreamFloat b = BitStreamFloat(0.2f,size);
    
    a &= b;
    REQUIRE(a.mean() == Approx(0.16));
}

TEST_CASE("or"){
    int size = 100;
    BitStreamFloat a = BitStreamFloat(0.8f,size);
    BitStreamFloat b = BitStreamFloat(0.2f,size);
    
    a |= b;
    REQUIRE(a.mean() == Approx(0.84));
}




TEST_CASE("precision"){
    BitStreamFloat uut = BitStreamFloat(0.8f,100,0b100);
    REQUIRE(uut.mean() == 0.75f);
}

TEST_CASE("precision2"){
    BitStreamFloat uut = BitStreamFloat(1.0f,100,0x7fffffff);
    REQUIRE(uut.mean() == 1.0f);
}
