#ifndef SOFTSIMU_H
#define SOFTSIMU_H
#include "hardsimu.h"
#include <string>
#include "map2d.h"
class SoftSimu : public HardSimu
{
public:
    SoftSimu(int width,int height,std::string cellName,std::string connecterName);

    virtual void step() override;

    virtual void getArrayInt(int index,int** array) override;
    virtual void getArrayBool(int index,bool ** array) override;
    virtual void getArrayFloat(int index,float ** array) override;

    virtual void setArrayInt(int index, int** array) override;
    virtual void setArrayBool(int index, bool** array) override;
    virtual void setArrayFloat(int index, float** array) override;

    virtual void setCellInt(int x,int y,int index,int val) override;
    virtual void setCellBool(int x,int y,int index,bool val) override;
    virtual void setCellFloat(int x,int y,int index,float val) override;




protected:
    Map2D map;

};

#endif // SOFTSIMU_H
