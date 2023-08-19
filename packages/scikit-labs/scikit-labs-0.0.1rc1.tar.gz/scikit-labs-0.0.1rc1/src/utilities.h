//
// Created by jiangkangkang on 2020/3/9.
//

/**
 * @file utilities.h
 * @brief some utilities for abess package.
 */

#ifndef SRC_UTILITIES_H
#define SRC_UTILITIES_H

#ifndef R_BUILD

#include <Eigen/Eigen>
#include <Eigen/Sparse>
#include <unsupported/Eigen/MatrixFunctions>
using List = std::tuple<Eigen::MatrixXd, Eigen::VectorXd, Eigen::MatrixXd>;

#else
#include <RcppEigen.h>
#endif

#include <cfloat>
#include <iostream>
using namespace Eigen;

/**
 * @brief return the indexes of all variables in groups in `L`.
 */
Eigen::VectorXi find_ind(Eigen::VectorXi &L, Eigen::VectorXi &index, Eigen::VectorXi &gsize, int beta_size, int N);

/**
 * @brief return part of X, which only contains columns in `ind`.
 */
template <class T4>
T4 X_seg(T4 &X, int n, Eigen::VectorXi &ind, int model_type) {
    if (ind.size() == X.cols() || model_type == 10 || model_type == 7) {
        return X;
    } else {
        T4 X_new(n, ind.size());
        for (int k = 0; k < ind.size(); k++) {
            X_new.col(k) = X.col(ind(k));
        }
        return X_new;
    }
};

// template <class T4>
// void X_seg(T4 &X, int n, Eigen::VectorXi &ind, T4 &X_seg)
// {
//     if (ind.size() == X.cols())
//     {
//         X_seg = X;
//     }
//     else
//     {
//         X_seg.resize(n, ind.size());
//         for (int k = 0; k < ind.size(); k++)
//         {
//             X_seg.col(k) = X.col(ind(k));
//         }
//     }
// };

template <class T4>
Eigen::Matrix<T4, -1, -1> compute_group_XTX(T4 &X, Eigen::VectorXi index, Eigen::VectorXi gsize, int n, int p, int N) {
    Eigen::Matrix<T4, -1, -1> XTX(N, 1);
    for (int i = 0; i < N; i++) {
        T4 X_ind = X.block(0, index(i), n, gsize(i));
        XTX(i, 0) = X_ind.transpose() * X_ind;
    }
    return XTX;
}

template <class T4>
Eigen::Matrix<Eigen::MatrixXd, -1, -1> Phi(T4 &X, Eigen::VectorXi index, Eigen::VectorXi gsize, int n, int p, int N,
                                           double lambda, Eigen::Matrix<T4, -1, -1> group_XTX) {
    Eigen::Matrix<Eigen::MatrixXd, -1, -1> phi(N, 1);
    for (int i = 0; i < N; i++) {
        Eigen::MatrixXd lambda_XtX =
            2 * lambda * Eigen::MatrixXd::Identity(gsize(i), gsize(i)) + group_XTX(i, 0) / double(n);
        lambda_XtX.sqrt().evalTo(phi(i, 0));
    }
    return phi;
}

Eigen::Matrix<Eigen::MatrixXd, -1, -1> invPhi(Eigen::Matrix<Eigen::MatrixXd, -1, -1> &Phi, int N);
// void max_k(Eigen::VectorXd &vec, int k, Eigen::VectorXi &result);
void slice_assignment(Eigen::VectorXd &nums, Eigen::VectorXi &ind, double value);
// Eigen::VectorXi get_value_index(Eigen::VectorXd &nums, double value);
// Eigen::VectorXd vector_slice(Eigen::VectorXd &nums, Eigen::VectorXi &ind);
Eigen::VectorXi vector_slice(Eigen::VectorXi &nums, Eigen::VectorXi &ind);
// Eigen::MatrixXd row_slice(Eigen::MatrixXd &nums, Eigen::VectorXi &ind);
// Eigen::MatrixXd matrix_slice(Eigen::MatrixXd &nums, Eigen::VectorXi &ind, int axis);

// Eigen::MatrixXd X_seg(Eigen::MatrixXd &X, int n, Eigen::VectorXi &ind);
/**
 * @brief complement of A, the whole set is {0..N-1}
 */
Eigen::VectorXi complement(Eigen::VectorXi &A, int N);
// Eigen::VectorXi Ac(Eigen::VectorXi &A, Eigen::VectorXi &U);
/**
 * @brief replace `B` by `C` in `A`
 */
Eigen::VectorXi diff_union(Eigen::VectorXi A, Eigen::VectorXi &B, Eigen::VectorXi &C);
/**
 * @brief return the indexes of min `k` values in `nums`.
 */
Eigen::VectorXi min_k(Eigen::VectorXd &nums, int k, bool sort_by_value = false);
/**
 * @brief return the indexes of max `k` values in `nums`.
 */
Eigen::VectorXi max_k(Eigen::VectorXd &nums, int k, bool sort_by_value = false);
// Eigen::VectorXi max_k_2(Eigen::VectorXd &vec, int k);

/**
 * @brief Extract `nums` at `ind` position, and store in `A`.
 */
void slice(Eigen::VectorXd &nums, Eigen::VectorXi &ind, Eigen::VectorXd &A, int axis = 0);
void slice(Eigen::MatrixXd &nums, Eigen::VectorXi &ind, Eigen::MatrixXd &A, int axis = 0);
void slice(Eigen::SparseMatrix<double> &nums, Eigen::VectorXi &ind, Eigen::SparseMatrix<double> &A, int axis = 0);
/**
 * @brief The inverse action of function slice.
 */
void slice_restore(Eigen::VectorXd &A, Eigen::VectorXi &ind, Eigen::VectorXd &nums, int axis = 0);
void slice_restore(Eigen::MatrixXd &A, Eigen::VectorXi &ind, Eigen::MatrixXd &nums, int axis = 0);

void coef_set_zero(int p, int M, Eigen::VectorXd &beta, double &coef0);
void coef_set_zero(int p, int M, Eigen::MatrixXd &beta, Eigen::VectorXd &coef0);

/**
 * @brief element-wise product: A.array() * B.array().
 */
Eigen::VectorXd array_product(Eigen::VectorXd &A, Eigen::VectorXd &B, int axis = 0);
/**
 * @brief product by specific axis.
 */
Eigen::MatrixXd array_product(Eigen::MatrixXd &A, Eigen::VectorXd &B, int axis = 0);
// Eigen::SparseMatrix<double> array_product(Eigen::SparseMatrix<double> &A, Eigen::VectorXd &B, int axis = 0);

/**
 * @brief element-wise division: A.array() / B.array().
 */
void array_quotient(Eigen::VectorXd &A, Eigen::VectorXd &B, int axis = 0);
/**
 * @brief division by specific axis.
 */
void array_quotient(Eigen::MatrixXd &A, Eigen::VectorXd &B, int axis = 0);

/**
 * @brief A.dot(B)
 */
double matrix_dot(Eigen::VectorXd &A, Eigen::VectorXd &B);
/**
 * @brief A.transpose() * B
 */
Eigen::VectorXd matrix_dot(Eigen::MatrixXd &A, Eigen::VectorXd &B);

// void matrix_sqrt(Eigen::MatrixXd &A, Eigen::MatrixXd &B);
// void matrix_sqrt(Eigen::SparseMatrix<double> &A, Eigen::MatrixXd &B);

/**
 * @brief Add an all-ones column as the first column in X.
 */
void add_constant_column(Eigen::MatrixXd &X);
/**
 * @brief Add an all-ones column as the first column in X.
 */
void add_constant_column(Eigen::SparseMatrix<double> &X);

// void set_nonzeros(Eigen::MatrixXd &X, Eigen::MatrixXd &x);
// void set_nonzeros(Eigen::SparseMatrix<double> &X, Eigen::SparseMatrix<double> &x);

// void overload_ldlt(Eigen::SparseMatrix<double> &X_new, Eigen::SparseMatrix<double> &X, Eigen::VectorXd &Z,
// Eigen::VectorXd &beta); void overload_ldlt(Eigen::MatrixXd &X_new, Eigen::MatrixXd &X, Eigen::VectorXd &Z,
// Eigen::VectorXd &beta);

// void overload_ldlt(Eigen::SparseMatrix<double> &X_new, Eigen::SparseMatrix<double> &X, Eigen::MatrixXd &Z,
// Eigen::MatrixXd &beta); void overload_ldlt(Eigen::MatrixXd &X_new, Eigen::MatrixXd &X, Eigen::MatrixXd &Z,
// Eigen::MatrixXd &beta);

// bool check_ill_condition(Eigen::MatrixXd &M);

/**
 * @brief If enable normalization, restore coefficients after fitting.
 */
template <class T2, class T3>
void restore_for_normal(T2 &beta, T3 &coef0, bool sparse_matrix, int normalize_type, int n, Eigen::VectorXd x_mean,
                        T3 y_mean, Eigen::VectorXd x_norm) {
    if (normalize_type == 0 || sparse_matrix) {
        // no need to restore
        return;
    }

    if (normalize_type == 1) {
        array_quotient(beta, x_norm, 1);
        beta = beta * sqrt(double(n));
        coef0 = y_mean - matrix_dot(beta, x_mean);
    } else if (normalize_type == 2) {
        array_quotient(beta, x_norm, 1);
        beta = beta * sqrt(double(n));
        coef0 = coef0 - matrix_dot(beta, x_mean);
    } else {
        array_quotient(beta, x_norm, 1);
        beta = beta * sqrt(double(n));
    }

    return;
}

template <class T4>
Eigen::VectorXd pi(T4 &X, Eigen::VectorXd &y, Eigen::VectorXd &coef) {
    int p = coef.size();
    int n = X.rows();
    Eigen::VectorXd Pi = Eigen::VectorXd::Zero(n);
    if (X.cols() == p - 1) {
        Eigen::VectorXd intercept = Eigen::VectorXd::Ones(n) * coef(0);
        Eigen::VectorXd one = Eigen::VectorXd::Ones(n);
        Eigen::VectorXd eta = X * (coef.tail(p - 1).eval()) + intercept;
        for (int i = 0; i < n; i++) {
            if (eta(i) > 30) {
                eta(i) = 30;
            } else if (eta(i) < -30) {
                eta(i) = -30;
            }
        }
        Eigen::VectorXd expeta = eta.array().exp();
        Pi = expeta.array() / (one + expeta).array();
        return Pi;
    } else {
        Eigen::VectorXd eta = X * coef;
        Eigen::VectorXd one = Eigen::VectorXd::Ones(n);

        for (int i = 0; i < n; i++) {
            if (eta(i) > 30) {
                eta(i) = 30;
            } else if (eta(i) < -30) {
                eta(i) = -30;
            }
        }
        Eigen::VectorXd expeta = eta.array().exp();
        Pi = expeta.array() / (one + expeta).array();
        return Pi;
    }
}

template <class T4>
void pi(T4 &X, Eigen::MatrixXd &y, Eigen::MatrixXd &beta, Eigen::VectorXd &coef0, Eigen::MatrixXd &pr) {
    int n = X.rows();
    Eigen::MatrixXd one = Eigen::MatrixXd::Ones(n, 1);
    Eigen::MatrixXd Xbeta = X * beta + one * coef0.transpose();
    pr = Xbeta.array().exp();
    Eigen::VectorXd sumpi = pr.rowwise().sum();
    for (int i = 0; i < n; i++) {
        pr.row(i) = pr.row(i) / sumpi(i);
    }

    // return pi;
};

template <class T4>
void pi(T4 &X, Eigen::MatrixXd &y, Eigen::MatrixXd &coef, Eigen::MatrixXd &pr) {
    int n = X.rows();
    // Eigen::MatrixXd one = Eigen::MatrixXd::Ones(n, 1);
    Eigen::MatrixXd Xbeta = X * coef;
    pr = Xbeta.array().exp();
    Eigen::VectorXd sumpi = pr.rowwise().sum();
    for (int i = 0; i < n; i++) {
        pr.row(i) = pr.row(i) / sumpi(i);
    }

    // return pi;
};

/**
 * @brief Add weights information into data.
 */
void add_weight(Eigen::MatrixXd &x, Eigen::VectorXd &y, Eigen::VectorXd weights);
/**
 * @brief Add weights information into data.
 */
void add_weight(Eigen::MatrixXd &x, Eigen::MatrixXd &y, Eigen::VectorXd weights);
/**
 * @brief Add weights information into data.
 */
void add_weight(Eigen::SparseMatrix<double> &x, Eigen::VectorXd &y, Eigen::VectorXd weights);
/**
 * @brief Add weights information into data.
 */
void add_weight(Eigen::SparseMatrix<double> &x, Eigen::MatrixXd &y, Eigen::VectorXd weights);

List pack_result(Eigen::VectorXd &beta, double &coef0, Eigen::MatrixXd &path);
List pack_result(Eigen::MatrixXd &beta, Eigen::VectorXd &coef0, Eigen::MatrixXd &path);

Eigen::MatrixXd Seg_by_row(Eigen::MatrixXd &x, Eigen::VectorXi &ind);
Eigen::SparseMatrix<double> Seg_by_row(Eigen::SparseMatrix<double> &x, Eigen::VectorXi &ind);

#endif  // SRC_UTILITIES_H
