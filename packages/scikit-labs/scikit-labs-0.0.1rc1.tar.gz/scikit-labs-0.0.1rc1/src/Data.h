//
// Created by Jin Zhu on 2020/2/18.
//
//  #define R_BUILD
#ifndef SRC_DATA_H
#define SRC_DATA_H

#ifdef R_BUILD
#include <RcppEigen.h>
// [[Rcpp::depends(RcppEigen)]]
#else
#include <Eigen/Eigen>
#endif
#include <iostream>
#include <random>
#include <vector>

#include "normalize.h"
#include "utilities.h"
using namespace std;
using namespace Eigen;

template <class T1, class T2, class T3, class T4>
class Data {
   public:
    T4 x;
    T1 y;
    Eigen::VectorXd weight;
    Eigen::VectorXd x_mean;
    Eigen::VectorXd x_norm;
    T3 y_mean;
    int n;
    int p;
    int M;
    int N;
    int g_num;
    Eigen::VectorXi g_index;
    Eigen::VectorXi g_size;

    Data() = default;

    Data(Data<T1, T2, T3, T4> &full_data, Eigen::VectorXi &ind) {
        this->n = ind.size();
        this->p = full_data.p;
        this->M = full_data.M;

        // Slice x, y, weight:
        // (since "SparseMatrix" can NOT be sliced by row simply,
        // we use matrix multiplication to achieve it.)
        this->x = Seg_by_row(full_data.x, ind);
        this->y = (full_data.y).topRows(this->n);
        this->weight = Eigen::VectorXd::Zero(this->n);
        for (int i = 0; i < ind.size(); i++) {
            (this->y).row(i) = (full_data.y).row(ind(i)).eval();
            (this->weight).row(i) = (full_data.weight).row(ind(i)).eval();
        }

        this->g_index = full_data.g_index;
        this->g_size = full_data.g_size;
        this->g_num = full_data.g_num;
        this->x_mean = Eigen::VectorXd::Zero(this->p);
        this->x_norm = Eigen::VectorXd::Zero(this->p);
    }

    Data(T4 &x, T1 &y, Eigen::VectorXd &weight, Eigen::VectorXi &g_index, int beta_size) {
        this->x = x;
        this->y = y;
        this->n = x.rows();
        this->p = x.cols();
        this->M = y.cols();

        this->weight = weight;
        this->x_mean = Eigen::VectorXd::Zero(this->p);
        this->x_norm = Eigen::VectorXd::Zero(this->p);

        this->g_index = g_index;
        this->g_num = g_index.size();
        Eigen::VectorXi temp = Eigen::VectorXi::Zero(this->g_num);
        for (int i = 0; i < g_num - 1; i++) temp(i) = g_index(i + 1);
        temp(g_num - 1) = beta_size;
        this->g_size = temp - g_index;
    };

    void normalize(int normalize_type) {
        if (normalize_type == 1) {
            Normalize(this->x, this->y, this->weight, this->x_mean, this->y_mean, this->x_norm);
        } else if (normalize_type == 2) {
            Normalize3(this->x, this->weight, this->x_mean, this->x_norm);
        } else {
            Normalize4(this->x, this->weight, this->x_norm);
        }
    };

    std::vector<Eigen::VectorXi> set_train_test_mask(Eigen::VectorXi &train_test_id) {
        int train_size, test_size;
        Eigen::VectorXi train_list(this->n);
        Eigen::VectorXi test_list(this->n);

        if (train_test_id.size() == 0) {
            // std::random_device rd;
            std::mt19937 g(123);
            std::vector<int> ind(this->n);
            for (int i = 0; i < this->n; i++) ind[i] = i;
            std::shuffle(ind.begin(), ind.end(), g);

            train_size = int(this->n * 0.8);
            if (train_size == 0) train_size = 1;
            test_size = this->n - train_size;
            for (int i = 0; i < train_size; i++) train_list(i) = ind[i];
            for (int i = 0; i < test_size; i++) test_list(i) = ind[i + train_size];

            std::sort(train_list.data(), train_list.data() + train_size);
            std::sort(test_list.data(), test_list.data() + test_size);
        } else {
            // given train_test_id
            train_size = 0;
            test_size = 0;
            for (int i = 0; i < this->n; i++) {
                if (train_test_id(i) == 0) {
                    train_list(train_size++) = i;
                } else {
                    test_list(test_size++) = i;
                }
            }
        }

        std::vector<Eigen::VectorXi> mask;
        mask.push_back(train_list.head(train_size).eval());
        mask.push_back(test_list.head(test_size).eval());
        return mask;
    };
};

#endif  // SRC_DATA_H
