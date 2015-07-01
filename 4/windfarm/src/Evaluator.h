#ifndef __EVALUATOR_H__
#define __EVALUATOR_H__

#include "Matrix.h"
#include <cmath>
#include <limits>


class Evaluator {
 public:
  Evaluator();
  ~Evaluator();

  //virtual void initialize(WindScenario& scenario);

  double evaluate(Matrix<double>* layout);
  double evaluate_2014(Matrix<double>* layout);

  Matrix<double>* getEnergyOutputs();
  Matrix<double>* getTurbineFitnesses();
  double getEnergyOutput() {return energyCapture;};
  double getWakeFreeRatio() {return wakeFreeRatio;};
  double getEnergyCost() {return energyCost;};
  //  WindScenario scenario;

 protected:
  Matrix<double>* tspe;
  Matrix<double>* tpositions;
  double energyCapture;
  double wakeFreeEnergy;
  double wakeFreeRatio;
  double energyCost;

  bool checkConstraint();
  double calculateWakeTurbine(size_t index, double theta);
  double calculateWakeTurbine(size_t index, size_t thetindex);
  double calculateBeta(double xi, double yi, double xj, double yj, double theta);
  double calculateBeta(double xi, double yi, double xj, double yj, size_t thetIndex);
  double calculateVelocityDeficit(double dij);
  double calculateProjectedDistance(double xi, double yi, double xj, double yj, double theta);
  double calculateProjectedDistance(double xi, double yi, double xj, double yj, size_t thetIndex);
  double powOutput(double v);

  inline double wblcdf(double x, double sc=1.0, double sh=1.0)
  {
    return 1.0-std::exp(-fastPow(x/sc,sh));
  }

  // faster because b is usually equal to 2!
  inline static double fastPow(double a, double b) {
    if (std::abs(b-2)<0.0001) {
      return a*a;
    } if (std::abs(b-1)<0.0001) {
      return a;
    } if (std::abs(b)<0.0001) {
      return 1;
    } else {
      return std::pow(a,b);
    }
  }

  static size_t nEvals;
  static double CT;
  static double PRated;
  static double R;
  static double eta;
  static double k;
  static double lambda;
  static double vCin;
  static size_t vCout;
  static size_t vRated;
  static size_t vints_length;
  static size_t data_rows;
  enum data_col {C, K, OMEGA, THETA1, THETA2};
  static double wind_data[][5];
  static double* vints;
  static double* sin_mid_theta;
  static double* cos_mid_theta;
};

#endif /* defined(__EVALUATOR_H__) */
