#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <register.h>


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


TEST_CASE("set error mask form char"){

    Register* reg = new Register(0,10);
    reg->set(100);
    //char tab[10] = {'\0','\0','\0','\x01','\x01','\x01','\x01','\x01','\0','\0'};
    bool tab[10] = {0,0,0,1,1,1,1,1,0,0};//msb -> lsb
    reg->setErrorMaskFromArray(tab);
    REQUIRE(reg->getErrorMask() == 124);


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

TEST_CASE("error mask "){

    Register* reg = new Register(7,8);
    reg->set(100);
    reg->setErrorMask(1);
    reg->synch();

    REQUIRE(reg->get() == 101);

}
