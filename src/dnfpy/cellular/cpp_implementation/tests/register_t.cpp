#define CATCH_CONFIG_MAIN
#include "test_utils.h"
#include <catch.hpp>
#include <register.h>
#include <iostream>

using namespace std;
 

TEST_CASE("precision mask"){

    //init value
    Register* reg = new Register(257,8);
    REQUIRE(reg->get() == 1);
    //set value
    reg->set(258);
    reg->synch();
    REQUIRE(reg->get() == 2);
    //incr value
    reg->set(255);
    reg->synch();
    REQUIRE(reg->get() == 255);
    reg->incr(1);
    reg->synch();
    REQUIRE(reg->get() == 0);






}

TEST_CASE("increment register"){

    Register* reg = new Register(10,10);
    reg->incr(23);
    REQUIRE(reg->get() == 10);
    reg->synch();
    REQUIRE(reg->get() == 33);

    reg->incr(-3);
    reg->synch();
        REQUIRE(reg->get() == 30);

}


TEST_CASE("set big erro mask"){

    Register* reg1 = new Register(0,1);
    Register* reg2 = new Register(0,10);
    bool * errors = construct_array<bool>(1,11);
    for(int i =0 ; i<11 ; ++i){
        errors[i] = 0;
    }
    cout << endl;
    bool* pt = reg1->setErrorMaskFromArray(errors,Register::TRANSIENT);
    pt = reg2->setErrorMaskFromArray(pt,Register::TRANSIENT);
    REQUIRE(reg1->getErrorMask(Register::TRANSIENT) == 0);
    REQUIRE(reg2->getErrorMask(Register::TRANSIENT) == 0);


}

TEST_CASE("set error mask form bool"){

    Register* reg = new Register(0,10);
    reg->set(100);
    bool tab[10] = {0,0,0,1,1,1,1,1,0,0};//msb -> lsb
    reg->setErrorMaskFromArray(tab,Register::TRANSIENT);
    REQUIRE(reg->getErrorMask(Register::TRANSIENT) == 124);


}

TEST_CASE("register update"){

    Register* reg = new Register(0);
    reg->set(100);
    reg->synch();
    REQUIRE(reg->get() == 100);

}


TEST_CASE("register reset"){


    Register* reg = new Register(7);
    reg->set(100);
    reg->synch();
    REQUIRE(reg->get() == 100);
    reg->reset();
    REQUIRE(reg->get() == 7);
}


TEST_CASE("register size"){

    Register* reg = new Register(7,8);
    reg->set(100);
    reg->synch();
    REQUIRE(reg->getSize() == 8);
    REQUIRE(reg->get() == 100);

}

TEST_CASE("error mask transient "){

    Register* reg = new Register(0,8);
    reg->set(100);
    reg->setErrorMask(1,Register::TRANSIENT);
    reg->synch();
    REQUIRE(reg->get() == 101);
    reg->synch();
    REQUIRE(reg->get() == 100);
    reg->synch();
    REQUIRE(reg->get() == 101);
    reg->synch();
    REQUIRE(reg->get() == 100);

}


TEST_CASE("error mask high"){
    Register* reg = new Register(0,8);
    bool error[8] = {1,0,0,0,0,0,0,0};
    reg->setErrorMaskFromArray(error,Register::PERMANENT_HIGH);
    reg->synch();
    REQUIRE(reg->get() == 128);
    reg->set(199);
    reg->synch();
    REQUIRE(reg->get() == 199);
    reg->set(99);
    reg->synch();
    REQUIRE(reg->get() == 227);
    reg->synch();
    REQUIRE(reg->get() == 227);
}

TEST_CASE("error mask low"){
    Register* reg = new Register(0,8);
    bool error[8] = {1,0,0,0,0,0,0,0};
    reg->setErrorMaskFromArray(error,Register::PERMANENT_LOW);
    reg->set(255);
    reg->synch();
    REQUIRE(reg->get() == 128-1);

    reg->set(128);
    reg->synch();
    REQUIRE(reg->get() == 0);

    reg->set(127);
    reg->synch();
    REQUIRE(reg->get() == 127);
}
