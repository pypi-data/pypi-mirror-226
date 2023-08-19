// #define R_BUILD
#include <iostream>
#include <vector>

#ifdef R_BUILD

#include <Rcpp.h>
#include <RcppEigen.h>
// [[Rcpp::depends(RcppEigen)]]
using namespace Rcpp;

#else

#include <Eigen/Eigen>

#endif

#include "Algorithm.h"
#include "AlgorithmGLM.h"
#include "utilities.h"
#include "workflow.h"

// typedef Eigen::Triplet<double> triplet;

using namespace Eigen;

// [[Rcpp::export]]
List abessGLM_API(Eigen::MatrixXd X, Eigen::MatrixXd y, Eigen::VectorXd weight, int n, int p, int normalize_type,
                  int algorithm_type, int model_type, int max_iter, int exchange_num, int ic_type, double ic_coef,
                  Eigen::VectorXi g_index, Eigen::VectorXd lambda_seq, int screening_size,
                  Eigen::VectorXi always_select, int primary_model_fit_max_iter, double primary_model_fit_epsilon,
                  bool early_stop, bool approximate_Newton, int thread, bool covariance_update, bool sparse_matrix,
                  int splicing_type, int important_search, Eigen::VectorXi A_init, int init_max_sparsity,
                  bool split_train_test, Eigen::VectorXi train_test_id, bool return_path, int init_type,
                  int init_gs_start, int max_sparsity) {
#ifdef _OPENMP
    // Eigen::initParallel();
    int max_thread = omp_get_max_threads();
    if (thread == 0 || thread > max_thread) {
        thread = max_thread;
    }

    Eigen::setNbThreads(thread);
    omp_set_num_threads(thread);

#endif
    int algorithm_list_size = thread;

    vector<Algorithm<Eigen::VectorXd, Eigen::VectorXd, double, Eigen::MatrixXd> *> algorithm_list_uni_dense(
        algorithm_list_size);
    vector<Algorithm<Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::MatrixXd> *> algorithm_list_mul_dense(
        algorithm_list_size);
    vector<Algorithm<Eigen::VectorXd, Eigen::VectorXd, double, Eigen::SparseMatrix<double>> *>
        algorithm_list_uni_sparse(algorithm_list_size);
    vector<Algorithm<Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::SparseMatrix<double>> *>
        algorithm_list_mul_sparse(algorithm_list_size);

    for (int i = 0; i < algorithm_list_size; i++) {
        if (!sparse_matrix) {
            if (model_type == 1) {
                algorithm_list_uni_dense[i] = new abessLm<Eigen::MatrixXd>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search, covariance_update);
            } else if (model_type == 2) {
                auto temp = new abessLogistic<Eigen::MatrixXd>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_dense[i] = temp;
            } else if (model_type == 3) {
                auto temp = new abessPoisson<Eigen::MatrixXd>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_dense[i] = temp;
            } else if (model_type == 4) {
                auto temp = new abessCox<Eigen::MatrixXd>(algorithm_type, model_type, max_iter,
                                                          primary_model_fit_max_iter, primary_model_fit_epsilon,
                                                          exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_dense[i] = temp;
            } else if (model_type == 5) {
                auto temp = new abessMLm<Eigen::MatrixXd>(algorithm_type, model_type, max_iter,
                                                          primary_model_fit_max_iter, primary_model_fit_epsilon,
                                                          exchange_num, always_select, splicing_type, important_search);
                temp->covariance_update = covariance_update;
                algorithm_list_mul_dense[i] = temp;
            } else if (model_type == 6) {
                auto temp = new abessMultinomial<Eigen::MatrixXd>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_mul_dense[i] = temp;
            } else if (model_type == 8) {
                auto temp = new abessGamma<Eigen::MatrixXd>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_dense[i] = temp;
            } else if (model_type == 9) {
                auto temp = new abessOrdinal<Eigen::MatrixXd>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                algorithm_list_mul_dense[i] = temp;
            }
        } else {
            if (model_type == 1) {
                algorithm_list_uni_sparse[i] = new abessLm<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search, covariance_update);
            } else if (model_type == 2) {
                auto temp = new abessLogistic<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_sparse[i] = temp;
            } else if (model_type == 3) {
                auto temp = new abessPoisson<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_sparse[i] = temp;
            } else if (model_type == 4) {
                auto temp = new abessCox<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_sparse[i] = temp;
            } else if (model_type == 5) {
                auto temp = new abessMLm<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->covariance_update = covariance_update;
                algorithm_list_mul_sparse[i] = temp;
            } else if (model_type == 6) {
                auto temp = new abessMultinomial<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_mul_sparse[i] = temp;
            } else if (model_type == 8) {
                auto temp = new abessGamma<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                temp->approximate_Newton = approximate_Newton;
                algorithm_list_uni_sparse[i] = temp;
            } else if (model_type == 9) {
                auto temp = new abessOrdinal<Eigen::SparseMatrix<double>>(
                    algorithm_type, model_type, max_iter, primary_model_fit_max_iter, primary_model_fit_epsilon,
                    exchange_num, always_select, splicing_type, important_search);
                algorithm_list_mul_sparse[i] = temp;
            }
        }
    }

    List out_result;
    if (!sparse_matrix) {
        if (y.cols() == 1 && model_type != 5 && model_type != 6) {
            Eigen::VectorXd y_vec = y.col(0).eval();

            out_result = abessWorkflow<Eigen::VectorXd, Eigen::VectorXd, double, Eigen::MatrixXd>(
                X, y_vec, n, p, normalize_type, weight, algorithm_type, ic_type, ic_coef, split_train_test,
                screening_size, g_index, early_stop, thread, sparse_matrix, init_max_sparsity, train_test_id, A_init,
                lambda_seq, return_path, init_type, init_gs_start, max_sparsity, algorithm_list_uni_dense);
        } else {
            out_result = abessWorkflow<Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::MatrixXd>(
                X, y, n, p, normalize_type, weight, algorithm_type, ic_type, ic_coef, split_train_test, screening_size,
                g_index, early_stop, thread, sparse_matrix, init_max_sparsity, train_test_id, A_init, lambda_seq,
                return_path, init_type, init_gs_start, max_sparsity, algorithm_list_mul_dense);
        }
    } else {
        Eigen::SparseMatrix<double> sparse_x(n, p);

        // std::vector<triplet> tripletList;
        // tripletList.reserve(x.rows());
        // for (int i = 0; i < x.rows(); i++)
        // {
        //   tripletList.push_back(triplet(int(x(i, 1)), int(x(i, 2)), x(i, 0)));
        // }
        // sparse_x.setFromTriplets(tripletList.begin(), tripletList.end());

        sparse_x.reserve(X.rows());
        for (int i = 0; i < X.rows(); i++) {
            sparse_x.insert(int(X(i, 1)), int(X(i, 2))) = X(i, 0);
        }
        sparse_x.makeCompressed();

        if (y.cols() == 1 && model_type != 5 && model_type != 6) {
            Eigen::VectorXd y_vec = y.col(0).eval();

            out_result = abessWorkflow<Eigen::VectorXd, Eigen::VectorXd, double, Eigen::SparseMatrix<double>>(
                sparse_x, y_vec, n, p, normalize_type, weight, algorithm_type, ic_type, ic_coef, split_train_test,
                screening_size, g_index, early_stop, thread, sparse_matrix, init_max_sparsity, train_test_id, A_init,
                lambda_seq, return_path, init_type, init_gs_start, max_sparsity, algorithm_list_uni_sparse);
        } else {
            out_result = abessWorkflow<Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::SparseMatrix<double>>(
                sparse_x, y, n, p, normalize_type, weight, algorithm_type, ic_type, ic_coef, split_train_test,
                screening_size, g_index, early_stop, thread, sparse_matrix, init_max_sparsity, train_test_id, A_init,
                lambda_seq, return_path, init_type, init_gs_start, max_sparsity, algorithm_list_mul_sparse);
        }
    }

    for (int i = 0; i < algorithm_list_size; i++) {
        delete algorithm_list_uni_dense[i];
        delete algorithm_list_mul_dense[i];
        delete algorithm_list_uni_sparse[i];
        delete algorithm_list_mul_sparse[i];
    }

    return out_result;
};
