/**
 * @file workflow.h
 * @brief The main workflow for abess.
 * @details It receives all inputs from API, runs the whole abess process
 * and then return the results as a list.
 */

#ifndef SRC_WORKFLOW_H
#define SRC_WORKFLOW_H

// #define R_BUILD
#ifdef R_BUILD

#include <Rcpp.h>
#include <RcppEigen.h>
// [[Rcpp::depends(RcppEigen)]]
using namespace Rcpp;

#else
#include <Eigen/Eigen>
#endif

#include <iostream>
#include <vector>

#include "Algorithm.h"
#include "Data.h"
#include "Metric.h"
#include "abessOpenMP.h"
#include "screening.h"
#include "utilities.h"

// typedef Eigen::Triplet<double> triplet;

using namespace Eigen;

// <Eigen::VectorXd, Eigen::VectorXd, double, Eigen::MatrixXd>                          for Univariate Dense
// <Eigen::VectorXd, Eigen::VectorXd, double, Eigen::SparseMatrix<double> >             for Univariate Sparse
// <Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::MatrixXd>                 for Multivariable Dense
// <Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::SparseMatrix<double> >    for Multivariable Sparse

/**
 * @brief The main workflow for abess.
 * @tparam T1 for y, XTy, XTone
 * @tparam T2 for beta
 * @tparam T3 for coef0
 * @tparam T4 for X
 * @param x sample matrix
 * @param y response matrix
 * @param n sample size
 * @param p number of variables
 * @param normalize_type type of normalize
 * @param weight weight of each sample
 * @param algorithm_type type of algorithm
 * @param path_type type of path: 1 for sequencial search and 2 for golden section search
 * @param is_warm_start whether enable warm-start
 * @param ic_type type of information criterion, used for not CV
 * @param Kfolds number of folds, used for CV
 * @param parameters parameters to be selected, including `support_size`, `lambda`
 * @param screening_size size of screening
 * @param g_index the first position of each group
 * @param early_stop whether enable early-stop
 * @param thread number of threads used for parallel computing
 * @param sparse_matrix whether sample matrix `x` is sparse matrix
 * @param cv_fold_id user-specified cross validation division
 * @param A_init initial active set
 * @param algorithm_list the algorithm pointer
 * @return the result of abess, including the best model parameters
 */
template <class T1, class T2, class T3, class T4>
List abessWorkflow(T4 &X, T1 &y, int n, int p, int normalize_type, Eigen::VectorXd weight, int algorithm_type,
                   int ic_type, double ic_coef, bool split_train_test, int screening_size, Eigen::VectorXi g_index,
                   bool early_stop, int thread, bool sparse_matrix, int init_max_sparsity,
                   Eigen::VectorXi &train_test_id, Eigen::VectorXi &A_init, Eigen::VectorXd &lambda_seq,
                   bool return_path, int init_type, int init_gs_start, int max_sparsity,
                   std::vector<Algorithm<T1, T2, T3, T4> *> algorithm_list) {
#ifndef R_BUILD
    std::srand(123);
#endif
    // cout << "[workflow]" << endl;
    int algorithm_list_size = algorithm_list.size();

    // Size of the candidate set:
    //     usually it is equal to `p`, the number of variable,
    //     but it could be different in e.g. RPCA.
    int beta_size = algorithm_list[0]->get_beta_size(n, p);

    // Data packing & normalize:
    //     pack & initial all information of data,
    //     including normalize.
    Data<T1, T2, T3, T4> data(X, y, weight, g_index, beta_size);
    if (algorithm_list[0]->model_type == 1 || algorithm_list[0]->model_type == 5) {
        add_weight(data.x, data.y, data.weight);
    }

    // Screening:
    //     if there are too many noise variables,
    //     screening can choose the `screening_size` most important variables
    //     and then focus on them later.
    Eigen::VectorXi screening_A;
    if (screening_size > 0) {
        screening_A = screening<T1, T2, T3, T4>(data, algorithm_list, screening_size, beta_size, lambda_seq(0), A_init);
    }

    // Split train_test
    Data<T1, T2, T3, T4> *train_data;
    Data<T1, T2, T3, T4> *test_data;
    if (split_train_test) {
        // cout << "[train_test]" << endl;
        std::vector<Eigen::VectorXi> mask = data.set_train_test_mask(train_test_id);
        train_data = new Data<T1, T2, T3, T4>(data, mask[0]);
        test_data = new Data<T1, T2, T3, T4>(data, mask[1]);
        // cout << "  ==> train size: " << train_data->n << endl;
        // cout << "  ==> test size: " << test_data->n << endl;
    } else {
        train_data = &data;
        test_data = &data;
    }

    // normalize
    // cout << "[normalize]" << endl;
    if (normalize_type > 0 && !sparse_matrix) {
        if (split_train_test) {
            train_data->normalize(normalize_type);
            test_data->normalize(normalize_type);
        } else {
            data.normalize(normalize_type);
        }
    }
    // cout << "x" << endl << train_data->x << endl << test_data->x << endl;
    // cout << "y" << endl << train_data->y << endl << test_data->y << endl;

    // Prepare metric
    Metric<T1, T2, T3, T4> metric(ic_type, ic_coef, split_train_test);

    // Fitting
    // cout << "[fit]" << endl;
    T2 beta;
    T3 coef0;
    Algorithm<T1, T2, T3, T4> *alg = algorithm_list[0];
    coef_set_zero(beta_size, data.M, beta, coef0);
    alg->update_return_path(return_path);
    alg->update_init_type(init_type);
    alg->update_init_gs_start(init_gs_start);
    alg->update_max_sparsity(max_sparsity);
    alg->update_init_max_sparsity(init_max_sparsity);
    alg->update_lambda_level(lambda_seq(0));  // todo: more lambda?
    alg->update_A_init(A_init);
    alg->update_beta_init(beta);
    alg->update_coef0_init(coef0);
    alg->update_bd_init(Eigen::VectorXd::Zero(data.g_num));
    alg->fit(*train_data, *test_data, metric);
    beta = alg->get_beta();
    coef0 = alg->get_coef0();

    Eigen::MatrixXd path = Eigen::MatrixXd::Zero(1, 1);
    if (return_path) {
        // Get path
        std::vector<Eigen::VectorXi> A_path = alg->get_A_path();
        std::vector<T2> beta_path = alg->get_beta_path();
        // std::vector<T3> coef0_path = alg->get_coef0_path();
        std::vector<double> loss_path = alg->get_loss_path();
        int path_len = 0;
        for (int i = 0; i < A_path.size(); i++) path_len += A_path[i].size();

        int k = 0;
        path.resize(4, path_len);
        for (int i = 0; i < A_path.size(); i++) {
            for (int j = 0; j < A_path[i].size(); j++) {
                path(0, k) = i + 1;
                path(1, k) = A_path[i](j);
                path(2, k) = beta_path[i](j);
                path(3, k) = loss_path[i];
                k++;
            }
        }
    }

    // Restore for normal:
    //    restore the changes if normalization is used.
    // cout << "[restore normal]" << endl;
    restore_for_normal<T2, T3>(beta, coef0, sparse_matrix, normalize_type, train_data->n, train_data->x_mean,
                               train_data->y_mean, train_data->x_norm);

    // Restore for screening
    //    restore the changes if screening is used.
    if (screening_size > 0) {
        int full_beta_size = algorithm_list[0]->get_beta_size(n, p);
        T2 full_beta = Eigen::MatrixXd::Zero(full_beta_size, data.M);

        slice_restore(beta, screening_A, full_beta);
        beta = full_beta;
    }

    if (split_train_test) {
        // cout << "[delete train test]" << endl;
        delete train_data;
        delete test_data;
    }

    // Return the result
    return pack_result(beta, coef0, path);
}

#endif  // SRC_WORKFLOW_H
