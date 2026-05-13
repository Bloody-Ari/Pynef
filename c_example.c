#ifndef printf
#include <stdio.h>
#endif

#ifndef Py_Object
#include <Python.h>
#endif

#include "c_binds/include/pynef_types.h"
#include "c_binds/include/pynef_functions.h"

int main(){
  // should be arguments!
  float new_nozzle[] = {8.0, 5.0, 2.0, 6.0, 7.0};
  char file_name[] = {"EwEwE"};
  char file_type[] = {"3mf"};
  char target_dir[] = {"/tmp/"};

  // default directory usage
  if(pynefWrapper(new_nozzle, file_name, file_type, NULL) == 0){
    printf("[FROM C] All good using default directory!");
  } else {
    printf("[FROM C] Something failed...");
    return -1;
  }

  // using custom directory
  if(pynefWrapper(new_nozzle, file_name, file_type, target_dir) == 0){
    printf("[FROM C] All good using custom directory!");
  } else {
    printf("[FROM C] Something failed...");
    return -1;
  }
  return 0;
}
