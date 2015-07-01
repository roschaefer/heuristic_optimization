#include "Evaluator.h"

///////////////////////////////
/// HARD-WIRED SCENARIO DATA //
///////////////////////////////
size_t Evaluator::nEvals = 0;
double Evaluator::CT=0.8;
double Evaluator::PRated=1500.0;
double Evaluator::R=38.5;
double Evaluator::eta=-500.0;
double Evaluator::k=0.0750;
double Evaluator::lambda=140.86;
double Evaluator::vCin=3.5;
size_t Evaluator::vCout=20;
size_t Evaluator::vRated=14;
size_t Evaluator::vints_length = 2*vRated-7+1;
double* Evaluator::vints = 0x0;
double* Evaluator::sin_mid_theta = 0x0;
double* Evaluator::cos_mid_theta = 0x0;
size_t Evaluator::data_rows = 24;
double Evaluator::wind_data[][5]  = {
    {7.0, 2.0, 0.0002, 0, 15},
    {5.0, 2.0, 0.0080, 15, 30},
    {5.0, 2.0, 0.0227, 30, 45},
    {5.0, 2.0, 0.0242, 45, 60},
    {5.0, 2.0, 0.0225, 60, 75},
    {4.0, 2.0, 0.0339, 75, 90},
    {5.0, 2.0, 0.0423, 90, 105},
    {6.0, 2.0, 0.0290, 105, 120},
    {7.0, 2.0, 0.0617, 120, 135},
    {7.0, 2.0, 0.0813, 135, 150},
    {8.0, 2.0, 0.0994, 150, 165},
    {9.5, 2.0, 0.1394, 165, 180},
    {10.0, 2.0, 0.1839, 180, 195},
    {8.5, 2.0, 0.1115, 195, 210},
    {8.5, 2.0, 0.0765, 210, 225},
    {6.5, 2.0, 0.0080, 225, 240},
    {4.6, 2.0, 0.0051, 240, 255},
    {2.6, 2.0, 0.0019, 255, 270},
    {8.0, 2.0, 0.0012, 270, 285},
    {5.0, 2.0, 0.0010, 285, 300},
    {6.4, 2.0, 0.0017, 300, 315},
    {5.2, 2.0, 0.0031, 315, 330},
    {4.5, 2.0, 0.0097, 330, 345},
    {3.9, 2.0, 0.0317, 345, 360}};


////////////////////////////////////////////////
/// Evaluator constructors, member functions ///
////////////////////////////////////////////////
Evaluator::Evaluator() {
  tspe=NULL;
  tpositions=NULL;
  wakeFreeEnergy=7315.38;
  energyCapture=0;
  if (tspe) delete tspe;
  if (tpositions) delete tpositions;
  tspe=NULL;
  tpositions=NULL;
  nEvals=0;
  energyCost = std::numeric_limits<double>::max();
 

  vints = new double[vints_length];
  for (size_t i=0; i<vints_length; i++){
    vints[i] = 3.5+i*0.5;
  }

  cos_mid_theta = new double[data_rows];
  sin_mid_theta = new double[data_rows];
#define FAC M_PI/180
  for (size_t i=0; i<data_rows; i++){
    cos_mid_theta[i] = cos((wind_data[i][THETA1]+wind_data[i][THETA2])/2.0*(FAC));
    sin_mid_theta[i] = sin((wind_data[i][THETA1]+wind_data[i][THETA2])/2.0*(FAC));
  }

}

Evaluator::~Evaluator() {
  if (tspe) delete tspe;
  if (tpositions) delete tpositions;
}

double Evaluator::evaluate(Matrix<double>* layout) {
  static double ct  = 750000;
  static double cs  = 8000000;
  static double m   = 30;
  static double r   = 0.03;
  static double y   = 20;
  static double com = 20000;

  double wfr = evaluate_2014(layout);
  if (wfr <= 0) return std::numeric_limits<double>::max();
  size_t n = layout->rows;

  energyCost = ((ct*n+cs*std::floor(n/m)*(0.666667+0.333333*std::exp(-0.00174*n*n))+com*n)/
                ((1.0-std::pow(1.0+r, -y))/r)/(8760.0*wakeFreeEnergy*wfr*n))+0.1/n;

  return energyCost;
}

double Evaluator::evaluate_2014(Matrix<double>* layout) {
  nEvals++;
  if (tpositions) delete tpositions;
  tpositions=new Matrix<double>(layout);
  if (tspe) delete tspe;
  energyCapture=0;
  wakeFreeRatio=0;
  if (checkConstraint()) {
    tspe=new Matrix<double>(data_rows, tpositions->rows);
    // Wind resource per turbine => stored temporaly in tspe
    for (size_t turb=0; turb<tpositions->rows; turb++) {
      // for each turbine
      for (size_t i=0; i<data_rows; i++) {
        // for each direction
        // calculate wake
        double totalVdef=calculateWakeTurbine(turb, i); 
        double cTurb=wind_data[i][C]*(1.0-totalVdef);

	// annual power output per turbine and per direction
        double tint=wind_data[i][THETA2] - wind_data[i][THETA1];
        double w=wind_data[i][OMEGA];
        double ki=wind_data[i][K];
        double totalPow=0;
        for (size_t ghh=1; ghh<vints_length; ghh++) {
          double v=(vints[ghh]+vints[ghh-1])/2.0;
          double P=powOutput(v);
          double prV=wblcdf(vints[ghh], cTurb, ki)-wblcdf(vints[ghh-1],cTurb,ki);
          totalPow+=prV*P;
        }
        totalPow+=PRated*(1.0-wblcdf(vRated, cTurb, ki));
        totalPow*=tint*w;
        tspe->set(i, turb, totalPow);
        energyCapture+=totalPow;
      }
    }
    wakeFreeRatio=energyCapture/(wakeFreeEnergy*tpositions->rows);
    return wakeFreeRatio;
  } else {
    return 0;
  }
}

Matrix<double>* Evaluator::getEnergyOutputs() {
  if (!tspe) return NULL;
  Matrix<double>* res = new Matrix<double>(tspe);
  return res;
}

Matrix<double>* Evaluator::getTurbineFitnesses() {
  if (!tspe) return NULL;
  Matrix<double>* res = new Matrix<double>(tpositions->rows, 1);
  for (size_t i=0; i<res->rows; i++) {
    double val=0.0;
    for (size_t j=0; j<tspe->rows; j++) {
      val+=tspe->get(j,i);
    }
    res->set(i,0,val/wakeFreeEnergy);
  }
  return res;
}


double Evaluator::powOutput(double v) {
  if (v<vCin) {
    return 0;
  } else if (v>=vCin && v<=vRated) {
    return lambda*v+eta;
  } else if (vCout>v && v>vRated) {
    return PRated;
  } else {
    return 0;
  }
}


double Evaluator::calculateWakeTurbine(size_t turb, size_t index) {
  double x=tpositions->get(turb, 0);
  double y=tpositions->get(turb, 1);
  static const double alpha=atan(k);
  double velDef=0;
  for (size_t oturb=0; oturb<tpositions->rows; oturb++) {
    if (oturb!=turb) {
      double xo=tpositions->get(oturb, 0);
      double yo=tpositions->get(oturb, 1);
      double beta=calculateBeta(x, y, xo, yo, index);
      if (beta<alpha) {
        double dij=calculateProjectedDistance(x, y, xo, yo, index);
        double curDef=calculateVelocityDeficit(dij);
        velDef+=curDef*curDef;
      }
    }
  }
  return sqrt(velDef);
}

double Evaluator::calculateVelocityDeficit(double dij) {
  static const double a=1.0-sqrt(1.0-CT);
  static const double rkRatio=k/R;
  return a/((1.0+rkRatio*dij)*(1.0+rkRatio*dij));
}


double Evaluator::calculateProjectedDistance(double xi, double yi, double xj, double yj, size_t index) {
  return std::abs((xi-xj)*cos_mid_theta[index]+(yi-yj)*sin_mid_theta[index]);
}

// calculate the angle between to turbines using xi, xj, yi, yj, R, k and theta
double Evaluator::calculateBeta(double xi, double yi, double xj, double yj, size_t index) {
  static const double rkRatio=R/k;
  double num=((xi-xj)*cos_mid_theta[index]+(yi-yj)*sin_mid_theta[index]+rkRatio);
  double a=xi-xj+rkRatio*cos_mid_theta[index];
  double b=yi-yj+rkRatio*sin_mid_theta[index];
  double denom=sqrt(a*a+b*b);
  return acos(num/denom);
}

// check to see if the candidate solution is feasible
bool Evaluator::checkConstraint() {
  static const double minDist=64.0*R*R; //min security distance squared
  for (size_t i=0; i<tpositions->rows; i++) {
    // check for obstacles
    // for (int j=0; j<scenario.obstacles.rows; j++) {
    //   if (tpositions->get(i, 0) > scenario.obstacles.get(j, 0) &&
    //        tpositions->get(i, 0) < scenario.obstacles.get(j, 2) &&
    //        tpositions->get(i, 1) > scenario.obstacles.get(j, 1) &&
    //        tpositions->get(i, 1) < scenario.obstacles.get(j, 3)) {
    //      printf("Obstacle %d [%f, %f, %f, %f] violated by turbine %d (%f, %f)\n",
    //             j, scenario.obstacles.get(j, 0), scenario.obstacles.get(j, 1),
    //             scenario.obstacles.get(j, 2), scenario.obstacles.get(j, 3), i);
    //      return false;
    //   }
    // }

    // Check if all turbines are on the field.
    double x = tpositions->get(i,0);
    double y = tpositions->get(i,1);    
    if (x < 0 || x >= 10000) {
      std::cerr << "*** CONSTRAINT VIOLATION: bounding box x ***" << std::endl;
      return false;
    }
    if (y < 0 || y >= 10000) {
      std::cerr << "*** CONSTRAINT VIOLATION: bounding box y ***" << std::endl;
      return false;
    }
    if ( (y < 2000 || y > 8000) && (x > 4000 && x < 6000) ){
      std::cerr << "*** CONSTRAINT VIOLATION: bounding box ***" << std::endl;
      return false;
    }
    
    /// Check security distance constraint
    for (size_t j=0; j<tpositions->rows; j++) {
      if (i!=j) {
        // calculate the squared distance between both turbs
        double dist=(tpositions->get(i, 0)-tpositions->get(j, 0))*(tpositions->get(i, 0)-tpositions->get(j, 0))+
          (tpositions->get(i, 1)-tpositions->get(j, 1))*(tpositions->get(i, 1)-tpositions->get(j, 1));
        if (dist<minDist) {
	  std::cerr << "*** CONSTRAINT VIOLATION: security distance";
	  std::cerr << "(" << dist << " < " << minDist << ") ***" << std::endl;
          //printf("dist:\t%f\t<\t%f\t(%d,%d)\n",dist,minDist,i,j);
          return false;
        }
      }
    }
  }
  return true;
}
