#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

#include "api.h"
using List = std::tuple<Eigen::MatrixXd, Eigen::VectorXd, Eigen::MatrixXd>;

List pywrap_GLM(Eigen::MatrixXd X, Eigen::MatrixXd y, Eigen::VectorXd weight, int n, int p, int normalize_type,
                int algorithm_type, int model_type, int max_iter, int exchange_num, int ic_type, double ic_coef,
                Eigen::VectorXi g_index, Eigen::VectorXd lambda, int screening_size, Eigen::VectorXi always_select,
                int primary_model_fit_max_iter, double primary_model_fit_epsilon, bool early_stop,
                bool approximate_Newton, int thread, bool covariance_update, bool sparse_matrix, int splicing_type,
                int important_search, Eigen::VectorXi A_init, int init_max_sparsity, bool split_train_test,
                Eigen::VectorXi train_test_id, bool return_path, int init_type, int init_gs_start, int max_sparsity) {
    return abessGLM_API(X, y, weight, n, p, normalize_type, algorithm_type, model_type, max_iter, exchange_num, ic_type,
                        ic_coef, g_index, lambda, screening_size, always_select, primary_model_fit_max_iter,
                        primary_model_fit_epsilon, early_stop, approximate_Newton, thread, covariance_update,
                        sparse_matrix, splicing_type, important_search, A_init, init_max_sparsity, split_train_test,
                        train_test_id, return_path, init_type, init_gs_start, max_sparsity);
}

PYBIND11_MODULE(pybind_cabess, m) { m.def("pywrap_GLM", &pywrap_GLM); }
