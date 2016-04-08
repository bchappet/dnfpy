#define CATCH_CONFIG_MAIN
#include <catch.hpp>
#include <register.h>


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
