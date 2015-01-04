#ifndef SOFTWARESIMU_H
#define SOFTWARESIMU_H
#include "map.h"
#include "hardsimu.h"

class SoftwareSimu : public HardSimu
{
public:
    SoftwareSimu();
private:
    class clazz;
    Map* map;
};

#endif // SOFTWARESIMU_H
