#define CATCH_CONFIG_MAIN
#include <limits>
#include <catch.hpp>
#include <bitstreamfloat.h>
#include <cellsbsfloat.h>

using namespace std;


TEST_CASE("precompute"){
    CellSBSFloat uut = CellSBSFloat(0,0);
    uut.initParams();
    uut.preCompute();
    REQUIRE(uut.getSBS()->mean() == 0.0f);
    REQUIRE(((BitStreamFloatGenerator*)uut.getSubModule(0).get())->getSBS()->mean() == 0.0f);
}

 
