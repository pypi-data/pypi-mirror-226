#ifndef SRC_SCREENING_H
#define SRC_SCREENING_H

//  #define R_BUILD

#ifdef R_BUILD
#include <Rcpp.h>
#include <RcppEigen.h>
using namespace Rcpp;
// [[Rcpp::depends(RcppEigen)]]
#else
#include <Eigen/Eigen>
#endif

#include <algorithm>
#include <cfloat>
#include <iostream>

#include "Data.h"
#include "utilities.h"

using namespace std;
using namespace Eigen;

template <class T1, class T2, class T3, class T4>
Eigen::VectorXi screening(Data<T1, T2, T3, T4> &data, vector<Algorithm<T1, T2, T3, T4> *>algorithm_list, int screening_size,
                          int &beta_size, double lambda, Eigen::VectorXi &A_init) {
    Eigen::VectorXi screening_A(screening_size);
    Eigen::VectorXi always_select = algorithm_list[0]->always_select;
    Eigen::VectorXd coef_norm = Eigen::VectorXd::Zero(data.g_num);

    T2 beta;
    T3 coef0;

    for (int i = 0; i < data.g_num; i++) {
        int s_tmp = data.g_size(i);
        T4 x_tmp = data.x.middleCols(data.g_index(i), s_tmp);
        Eigen::VectorXi A_tmp = Eigen::VectorXi::LinSpaced(s_tmp, 0, s_tmp - 1);
        Eigen::VectorXi g_index_tmp = Eigen::VectorXi::LinSpaced(s_tmp, 0, s_tmp - 1);
        Eigen::VectorXi g_size_tmp = Eigen::VectorXi::Ones(s_tmp);
        coef_set_zero(s_tmp, data.M, beta, coef0);

        algorithm_list[0]->update_sparsity_level(s_tmp);
        algorithm_list[0]->update_lambda_level(lambda);
        algorithm_list[0]->primary_model_fit(x_tmp, data.y, data.weight, beta, coef0, DBL_MAX, A_tmp, g_index_tmp,
                                             g_size_tmp);

        coef_norm(i) = beta.squaredNorm() / s_tmp;
    }

    // keep always_select & A_init in active_set
    slice_assignment(coef_norm, always_select, DBL_MAX);
    slice_assignment(coef_norm, A_init, DBL_MAX - 1);
    screening_A = max_k(coef_norm, screening_size);

    // data after screening
    Eigen::VectorXi new_g_index(screening_size);
    Eigen::VectorXi new_g_size(screening_size);

    int new_p = 0;
    for (int i = 0; i < screening_size; i++) {
        new_p += data.g_size(screening_A(i));
        new_g_size(i) = data.g_size(screening_A(i));
    }

    new_g_index(0) = 0;
    for (int i = 0; i < screening_size - 1; i++) {
        new_g_index(i + 1) = new_g_index(i) + data.g_size(screening_A(i));
    }

    Eigen::VectorXi screening_A_ind = find_ind(screening_A, data.g_index, data.g_size, beta_size, data.g_num);
    T4 x_A;
    slice(data.x, screening_A_ind, x_A, 1);

    Eigen::VectorXd new_x_mean, new_x_norm;
    slice(data.x_mean, screening_A_ind, new_x_mean);
    slice(data.x_norm, screening_A_ind, new_x_norm);

    data.x = x_A;
    data.x_mean = new_x_mean;
    data.x_norm = new_x_norm;
    data.p = new_p;
    data.g_num = screening_size;
    data.g_index = new_g_index;
    data.g_size = new_g_size;
    beta_size = algorithm_list[0]->get_beta_size(data.n, new_p);

    if (always_select.size() != 0) {
        Eigen::VectorXi new_always_select(always_select.size());
        int j = 0;
        for (int i = 0; i < always_select.size(); i++) {
            while (always_select(i) != screening_A(j)) j++;
            new_always_select(i) = j;
        }
        int algorithm_list_size = algorithm_list.size();
        for (int i = 0; i < algorithm_list_size; i++) {
            algorithm_list[i]->always_select = new_always_select;
        }
    }

    if (A_init.size() != 0) {
        Eigen::VectorXi new_A_init(A_init.size());
        int j = 0;
        for (int i = 0; i < A_init.size(); i++) {
            while (A_init(i) != screening_A(j)) j++;
            new_A_init(i) = j;
        }
        A_init = new_A_init;
    }

    algorithm_list[0]->clear_setting();
    return screening_A_ind;
}

#endif  // SRC_SCREENING_H
