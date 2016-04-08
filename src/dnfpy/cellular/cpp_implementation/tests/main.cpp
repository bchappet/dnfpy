#include <router.h>
#include <module.h>



int main(){
        
    Module::ModulePtr router = Module::ModulePtr(new Router());
    router.get()->setRegState(Router::BUFFER,1);
    router.get()->synch();
    router.get()->compute();
    router.get()->synch();



}
