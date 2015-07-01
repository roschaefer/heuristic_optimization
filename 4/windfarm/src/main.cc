//
//  main.cc
//

#include <iostream>
#include <stdio.h>
#include <string>

#include "Evaluator.h"
#include "Matrix.h"


Matrix<double>* readLayout(std::istream& is)
{
  size_t nturbines;
  Matrix<double>* layout;
  is >> nturbines;
  layout = new Matrix<double>(nturbines,2);
  for (size_t i=0; i<nturbines; i++){
    double xpos, ypos;
    is >> xpos >> ypos;
    layout->set(i,0,xpos);
    layout->set(i,1,ypos);
  }
  return layout;
}

static void writeLayout(Matrix<double>* layout, std::ostream& os)
{
  os << layout->rows << std::endl;
  os << layout->toString();
}

int main(int argc, const char * argv[])
{
  Evaluator wfle;
  Matrix<double>* layout = readLayout(std::cin);
  //writeLayout(layout,std::cout);
  std::cout << wfle.evaluate(layout) << std::endl;
  delete layout;
}
