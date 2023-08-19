//
// Created by Jin Zhu on 2020/2/18.
//
// #define R_BUILD
#ifndef SRC_METRICS_H
#define SRC_METRICS_H

#include <algorithm>
#include <random>
#include <vector>

#include "Algorithm.h"
#include "Data.h"
#include "utilities.h"

template <class T1, class T2, class T3, class T4>
// To do: calculate loss && all to one && lm poisson cox
class Metric {
   public:
    int ic_type;
    double ic_coef;
    bool split_train_test;

    Metric(int ic_type, double ic_coef = 1.0, bool split_train_test = false) {
        this->ic_type = ic_type;
        this->ic_coef = ic_coef;
        this->split_train_test = split_train_test;
    };

    double ic(double loss0, int n, int N, T2 &beta, T3 &coef0, int model_type, double lambda, double effective_number) {
        if (this->split_train_test) return loss0;

        double loss;
        if (model_type == 1 || model_type == 5) {
            loss = n * log(loss0 - lambda * beta.cwiseAbs2().sum());
        } else {
            loss = 2 * (loss0 - lambda * beta.cwiseAbs2().sum());
        }

        if (ic_type == 0) {
            return loss;
        } else if (ic_type == 1) {
            return loss + 2.0 * effective_number;
        } else if (ic_type == 2) {
            return loss + this->ic_coef * log(double(n)) * effective_number;
        } else if (ic_type == 3) {
            return loss + this->ic_coef * log(double(N)) * log(log(double(n))) * effective_number;
        } else if (ic_type == 4) {
            return loss + this->ic_coef * (log(double(n)) + 2 * log(double(N))) * effective_number;
        } else if (ic_type == 5) {
            return n * (loss0 - lambda * beta.cwiseAbs2().sum()) +
                   this->ic_coef * log(double(N)) * log(log(double(n))) * effective_number;
        } else
            return 0;
    };
};

#endif  // SRC_METRICS_H
