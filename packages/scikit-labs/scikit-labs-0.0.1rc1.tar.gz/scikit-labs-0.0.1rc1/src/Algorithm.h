/**
 * @file Algorithm.h
 * @brief the algorithm for fitting on given parameter.
 * @author   Jin Zhu (zhuj37@mail2.sysu.edu.cn),
 * Kangkang Jiang (jiangkk3@mail2.sysu.edu.cn),
 * Junhao Huang (huangjh256@mail2.sysu.edu.cn)
 * @version  0.0.1
 * @date     2021-07-31
 * @copyright  GNU General Public License (GPL)
 */

/*****************************************************************************
 *  OpenST Basic tool library                                                 *
 *  Copyright (C) 2021 Kangkang Jiang  jiangkk3@mail2.sysu.edu.cn                         *
 *                                                                            *
 *  This file is part of OST.                                                 *
 *                                                                            *
 *  This program is free software; you can redistribute it and/or modify      *
 *  it under the terms of the GNU General Public License version 3 as         *
 *  published by the Free Software Foundation.                                *
 *                                                                            *
 *  You should have received a copy of the GNU General Public License         *
 *  along with OST. If not, see <http://www.gnu.org/licenses/>.               *
 *                                                                            *
 *  Unless required by applicable law or agreed to in writing, software       *
 *  distributed under the License is distributed on an "AS IS" BASIS,         *
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  *
 *  See the License for the specific language governing permissions and       *
 *  limitations under the License.                                            *
 *                                                                            *
 *----------------------------------------------------------------------------*
 *  Remark         : Description                                              *
 *----------------------------------------------------------------------------*
 *  Change History :                                                          *
 *  <Date>     | <Version> | <Author>       | <Description>                   *
 *----------------------------------------------------------------------------*
 *  2021/07/31 | 0.0.1     | Kangkang Jiang | First version                   *
 *----------------------------------------------------------------------------*
 *                                                                            *
 *****************************************************************************/

#ifndef SRC_ALGORITHM_H
#define SRC_ALGORITHM_H

#ifndef R_BUILD
#include <Eigen/Eigen>
#include <unsupported/Eigen/MatrixFunctions>
#endif

#include <cfloat>
#include <iostream>
#include <vector>

#include "Data.h"
#include "Metric.h"
#include "utilities.h"

using namespace std;

#define FINAL_FIT_ITER_ADD 20

bool quick_sort_pair_max(std::pair<int, double> x, std::pair<int, double> y);

// <Eigen::VectorXd, Eigen::VectorXd, double, Eigen::MatrixXd> for Univariate Dense
// <Eigen::VectorXd, Eigen::VectorXd, double, Eigen::SparseMatrix<double> > for Univariate Sparse
// <Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::MatrixXd> for Multivariable Dense
// <Eigen::MatrixXd, Eigen::MatrixXd, Eigen::VectorXd, Eigen::SparseMatrix<double> > for Multivariable Sparse

/**
 * @brief Variable select based on splicing algorithm.
 * @tparam T1 for y, XTy, XTone
 * @tparam T2 for beta
 * @tparam T3 for coef0
 * @tparam T4 for X
 */
template <class T1, class T2, class T3, class T4>
class Algorithm {
   public:
    int model_fit_max;        // Maximum number of iterations taken for the primary model fitting.
    int model_type;           // primary model type.
    int algorithm_type;       // algorithm type.
    int group_df = 0;         // freedom
    int sparsity_level = 0;   // Number of non-zero coefficients.
    double lambda_level = 0;  // l2 normalization coefficients.
    // Eigen::VectorXi train_mask;
    int max_iter;      // Maximum number of iterations taken for the splicing algorithm to converge.
    int exchange_num;  // Max exchange variable num.
    bool warm_start;  // When tuning the optimal parameter combination, whether to use the last solution as a warm start
                      // to accelerate the iterative convergence of the splicing algorithm.
    T4 *x = NULL;
    T1 *y = NULL;
    T2 beta;                  // coefficients.
    Eigen::VectorXd bd;       // sacrifices.
    T3 coef0;                 // intercept.
    double loss = 0.;         // loss.
    T2 beta_init;             // initialization coefficients.
    T3 coef0_init;            // initialization intercept.
    Eigen::VectorXi A_init;   // initialization active set.
    Eigen::VectorXi I_init;   // initialization inactive set.
    Eigen::VectorXd bd_init;  // initialization bd vector.

    Eigen::VectorXi A_out;  // final active set.
    Eigen::VectorXi I_out;  // final active set.

    bool lambda_change;  // lambda_change or not.

    Eigen::VectorXi always_select;     // always select variable.
    double tau;                        // algorithm stop threshold
    int primary_model_fit_max_iter;    // The maximal number of iteration for primaty model fit
    double primary_model_fit_epsilon;  // The epsilon (threshold) of iteration for primaty model fit

    double effective_number;  // effective number of parameter.
    int splicing_type;        // exchange number update mathod.
    int important_search;     // size of sub_searching in splicing
    int U_size;

    int max_sparsity;
    int init_max_sparsity;
    int init_type;
    int init_gs_start;

    bool return_path = false;
    std::vector<Eigen::VectorXi> A_path;
    std::vector<T2> beta_path;
    std::vector<T3> coef0_path;
    std::vector<double> loss_path;

    Algorithm() = default;

    virtual ~Algorithm(){};

    Algorithm(int algorithm_type, int model_type, int max_iter = 100, int primary_model_fit_max_iter = 10,
              double primary_model_fit_epsilon = 1e-8, int exchange_num = 5,
              Eigen::VectorXi always_select = Eigen::VectorXi::Zero(0), int splicing_type = 0,
              int important_search = 0) {
        this->max_iter = max_iter;
        this->model_type = model_type;
        this->exchange_num = exchange_num;
        this->always_select = always_select;
        this->algorithm_type = algorithm_type;
        this->primary_model_fit_max_iter = primary_model_fit_max_iter;
        this->primary_model_fit_epsilon = primary_model_fit_epsilon;

        this->splicing_type = splicing_type;
        this->important_search = important_search;
    };

    void update_return_path(bool return_path) { this->return_path = return_path; }

    void update_beta_init(T2 beta_init) { this->beta_init = beta_init; }

    void update_A_init(Eigen::VectorXi A_init) { this->A_init = A_init; }

    void update_bd_init(Eigen::VectorXd bd_init) { this->bd_init = bd_init; }

    void update_coef0_init(T3 coef0) { this->coef0_init = coef0; }

    void update_group_df(int group_df) { this->group_df = group_df; }

    void update_lambda_level(double lambda_level) {
        this->lambda_change = this->lambda_level != lambda_level;
        this->lambda_level = lambda_level;
    }

    void update_sparsity_level(double sparsity_level) { this->sparsity_level = sparsity_level; }

    void update_exchange_num(int exchange_num) { this->exchange_num = exchange_num; }

    // virtual void update_tau(int train_n, int N) {
    //     if (train_n == 1) {
    //         this->tau = 0.0;
    //     } else {
    //         this->tau =
    //             0.01 * (double)this->sparsity_level * log((double)N) * log(log((double)train_n)) / (double)train_n;
    //     }
    // }

    void update_init_type(int init_type) { this->init_type = init_type; }
    void update_init_gs_start(int init_gs_start) { this->init_gs_start = init_gs_start; }
    void update_init_max_sparsity(int init_max_sparsity) { this->init_max_sparsity = init_max_sparsity; }
    void update_max_sparsity(int max_sparsity) { this->max_sparsity = max_sparsity; }

    double get_loss() { return this->loss; }

    int get_group_df() { return this->group_df; }

    double get_effective_number() { return this->effective_number; }

    int get_sparsity_level() { return this->sparsity_level; }

    T2 get_beta() { return this->beta; }

    T3 get_coef0() { return this->coef0; }

    int get_model_type() { return this->model_type; }

    Eigen::VectorXi get_A_out() { return this->A_out; };

    Eigen::VectorXi get_I_out() { return this->I_out; };

    Eigen::VectorXd get_bd() { return this->bd; }

    std::vector<Eigen::VectorXi> get_A_path() { return this->A_path; }
    std::vector<T2> get_beta_path() { return this->beta_path; }
    std::vector<T3> get_coef0_path() { return this->coef0_path; }
    std::vector<double> get_loss_path() { return this->loss_path; }

    virtual int get_beta_size(int n, int p) { return p; }

    void record_path(Eigen::VectorXi &A_ind, T2 &beta, T3 &coef0, Eigen::VectorXi &U_ind, double &loss) {
        Eigen::VectorXi A_temp(A_ind.size());
        T2 beta_temp = beta.topRows(A_ind.size());
        for (int i = 0; i < A_ind.size(); i++) {
            A_temp(i) = U_ind(A_ind(i));
            beta_temp.row(i) = beta.row(A_ind(i)).eval();
        }
        this->A_path.push_back(A_temp);
        this->beta_path.push_back(beta_temp);
        this->coef0_path.push_back(coef0);
        this->loss_path.push_back(loss);
        return;
    }

    /**
     * @param train_x sample matrix for training
     * @param train_y response matrix for training
     * @param train_weight weight of each sample
     * @param g_index the first position of each group
     * @param g_size size of each group
     * @param train_n sample size for training, i.e. the number of rows in `train_x`
     * @param p number of variables, i.e. the number of columns in `train_x`
     * @param N number of different groups
     */
    void fit(Data<T1, T2, T3, T4> &train_data, Data<T1, T2, T3, T4> &test_data, Metric<T1, T2, T3, T4> &metric) {
        // cout << "[fit in]" << endl;
        this->x = &train_data.x;
        this->y = &train_data.y;

        // Specific init:
        //     Some specific initial setting for each algorithm,
        //     e.g. pre-computed items.
        // cout << "[init setting]" << endl;
        this->inital_setting(train_data.x, train_data.y, train_data.weight, train_data.g_index, train_data.g_size,
                             train_data.g_num);

        // Initial active/inactive set:
        //     Defaultly, choose `T0` groups with largest `bd_init` as initial active set.
        //     If there is no `bd_init` (may be no warm-start), compute it on `beta_init`, `coef0_init`, `A_init`.
        //     However, you can also define your own criterion by rewrite the function.
        // cout << "[init screen]" << endl;
        Eigen::VectorXi A = this->inital_screening(train_data, test_data, metric);
        this->sparsity_level = A.size();
        this->effective_number = A.size();

        // cout << "  ==> A = " << A.transpose() << endl;
        // cout << "  ==> sparsity = " << this->sparsity_level << endl;
        // cout << "  ==> loss = " << this->loss << endl;

        // Initialize sub-search:
        //     To speed up, we focus on a subset of all groups, named `U`,
        //     whose size is equal or smaller than N.
        //     (More details can be found in function `get_A` below)
        if (this->important_search == 0 || this->important_search + this->sparsity_level > train_data.g_num)
            this->U_size = train_data.g_num;
        else
            this->U_size = this->important_search + this->sparsity_level;
        // cout << "  ==> U_size = " << this->U_size << endl;

        // Start splicing:
        //     `get_A()` is to update active set A.
        this->get_A(train_data, test_data, metric, A);

        // // Final fitting on `A`:
        // //     For higher accuracy, fit again on chosen active set
        // //     with stricter settings.
        // this->final_fitting(train_data, A);

        // cout << "[final]" << endl;
        // cout << "  ==> A_out = " << A.transpose() << endl;
        // cout << "  ==> sparsity = " << this->sparsity_level << endl;
        // cout << "  ==> loss = " << this->loss << endl;

        // Result & Output
        this->A_out = A;
        Eigen::VectorXi A_ind =
            find_ind(A, train_data.g_index, train_data.g_size, (this->beta).rows(), train_data.g_num);
        this->group_df = A_ind.size();

        return;
    };

    void get_A(Data<T1, T2, T3, T4> &train_data, Data<T1, T2, T3, T4> &test_data, Metric<T1, T2, T3, T4> &metric,
               Eigen::VectorXi &A) {
        // cout << "[get A]" << endl;
        // Universal set:
        //     We only consider splicing on a set `U`,
        //     which may not contain all groups, but we hope all "useful" groups are included.
        //     We need to extract these groups out, e.g. `X`->`X_U`, `A`->`A_U`,
        //     and they have a new index from 0 to `U_size`-1.
        Eigen::VectorXi U;
        Eigen::VectorXi U_ind;
        Eigen::VectorXi g_index_U;
        Eigen::VectorXi g_size_U;
        T4 *X_U;
        T4 *test_X_U;
        T2 beta_U;
        Eigen::VectorXi A_U;
        Eigen::VectorXi always_select_U(this->always_select.size());

        // The outer iteration:
        //     1. extract data from U
        //     2. splicing & fitting on U (inner iteration), update active set
        //     3. update U
        //     4. if U unchanged, exit
        int iter = 0;
        while (iter++ < this->max_iter) {
            // cout << "[iter]" << endl;
            // mapping
            if (this->U_size == train_data.g_num) {
                // If consider all groups, it is no need to map or give a new index.
                U = Eigen::VectorXi::LinSpaced(train_data.g_num, 0, train_data.g_num - 1);
                X_U = &train_data.x;
                test_X_U = &test_data.x;
                U_ind = Eigen::VectorXi::LinSpaced((this->beta).rows(), 0, (this->beta).rows() - 1);
                beta_U = this->beta;
                g_size_U = train_data.g_size;
                g_index_U = train_data.g_index;
                A_U = A;
                always_select_U = this->always_select;
            } else {
                // Extract `X`, `beta`, `g_index`, `g_size`, `always_select` on U,
                // give them new index (from 0 to U_size-1),
                // and name as `X_U`, `beta_U`, `g_index_U`, `g_size_U`, `always_select_U` respectively.
                U = max_k(this->bd, this->U_size, true);
                X_U = new T4;
                test_X_U = new T4;
                U_ind = find_ind(U, train_data.g_index, train_data.g_size, (this->beta).rows(), train_data.g_num);
                *X_U = X_seg(train_data.x, train_data.n, U_ind, this->model_type);
                *test_X_U = X_seg(test_data.x, test_data.n, U_ind, this->model_type);
                slice(this->beta, U_ind, beta_U);

                g_index_U.resize(this->U_size);
                g_size_U.resize(this->U_size);
                int pos = 0;
                for (int i = 0; i < U.size(); i++) {
                    g_size_U(i) = train_data.g_size(U(i));
                    g_index_U(i) = pos;
                    pos += g_size_U(i);
                }

                // Since we have ranked U from large to small with sacrifice,
                // the first `this->sparsity_level` group should be initial active sets.
                A_U = Eigen::VectorXi::LinSpaced(this->sparsity_level, 0, this->sparsity_level - 1);

                // always_select
                Eigen::VectorXi temp = Eigen::VectorXi::Zero(train_data.g_num);
                int s = this->always_select.size();
                for (int i = 0; i < s; i++) {
                    temp(this->always_select(i)) = 1;
                }
                for (int i = 0; i < this->U_size; i++) {
                    if (s == 0) break;
                    if (temp(U(i)) == 1) {
                        always_select_U(this->always_select.size() - s) = i;
                        s--;
                    }
                }
            }

            // The inner iteration:
            //     1. splicing on U
            //     2. update A_U
            int num = -1;
            bool converge = true;
            while (true) {
                // cout << "[inner iter]" << endl;
                num++;
                Eigen::VectorXi A_ind = find_ind(A_U, g_index_U, g_size_U, U_ind.size(), this->U_size);
                T4 X_A = X_seg(*X_U, train_data.n, A_ind, this->model_type);
                T2 beta_A;
                slice(beta_U, A_ind, beta_A);
                if (this->return_path) {
                    this->record_path(A_ind, beta_U, this->coef0, U_ind, this->loss);
                }

                Eigen::VectorXd bd_U = Eigen::VectorXd::Zero(this->U_size);
                Eigen::VectorXi I_U = complement(A_U, this->U_size);
                this->sacrifice(*X_U, X_A, train_data.y, beta_U, beta_A, this->coef0, A_U, I_U, train_data.weight,
                                g_index_U, g_size_U, this->U_size, A_ind, bd_U, U, U_ind, num);

                for (int i = 0; i < always_select_U.size(); i++) {
                    bd_U(always_select_U(i)) = DBL_MAX;
                }

                // Splicing:
                //     Try to exchange items in active and inactive set,
                //     If new loss is smaller, accept it and return TRUE.
                bool exchange =
                    this->splicing(*X_U, train_data.y, *test_X_U, test_data.y, A_U, I_U, beta_U, this->coef0, bd_U,
                                   train_data.weight, test_data.weight, g_index_U, g_size_U, this->U_size, metric);
                // cout << "  ==> A_U = " << A_U.transpose() << endl;
                // cout << "  ==> sparsity = " << this->sparsity_level << endl;

                if (exchange) {
                    converge = false;
                } else {
                    // A_U is unchanged, so break.
                    break;
                }
            }

            // If A_U not change, U will not change and we can stop.
            if (converge) break;

            // Update & Restore beta, A from U
            slice_restore(beta_U, U_ind, beta);

            if (this->U_size == train_data.g_num) {
                // If U is the full set, there is no need to update, so stop.
                A = A_U;
                break;
            } else {
                Eigen::VectorXi ind = Eigen::VectorXi::Zero(train_data.g_num);
                for (int i = 0; i < A_U.size(); i++) ind(U(A_U(i))) = 1;
                A.resize(A_U.size());
                int tempA = 0;
                for (int i = 0; i < train_data.g_num; i++)
                    if (ind(i) != 0) {
                        A(tempA++) = i;
                    }
                // cout << "  ==> A = " << A.transpose() << endl;
                // cout << "  ==> sparsity = " << this->sparsity_level << endl;

                // Compute sacrifices in full set
                Eigen::VectorXi A_ind0 =
                    find_ind(A, train_data.g_index, train_data.g_size, (this->beta).rows(), train_data.g_num);
                T4 X_A0 = X_seg(train_data.x, train_data.n, A_ind0, this->model_type);
                T2 beta_A0;
                slice(beta, A_ind0, beta_A0);
                Eigen::VectorXi U0 =
                    Eigen::VectorXi::LinSpaced(train_data.g_num, 0, train_data.g_num - 1);  // U0 contains all groups
                Eigen::VectorXi I = complement(A, train_data.g_num);
                Eigen::VectorXi U_ind0 = Eigen::VectorXi::LinSpaced((this->beta).rows(), 0, (this->beta).rows() - 1);
                this->sacrifice(train_data.x, X_A0, train_data.y, beta, beta_A0, coef0, A, I, train_data.weight,
                                train_data.g_index, train_data.g_size, train_data.g_num, A_ind0, this->bd, U0, U_ind0,
                                0);

                // If U is changed in the new situation, update it and iter again.
                for (int i = 0; i < this->sparsity_level; i++) this->bd(A(i)) = DBL_MAX;

                if (this->important_search + this->sparsity_level > train_data.g_num) {
                    this->U_size = train_data.g_num;
                } else {
                    this->U_size = this->important_search + this->sparsity_level;
                }
                delete X_U;
                delete test_X_U;
            }
        }
        return;
    };

    bool splicing(T4 &X, T1 &y, T4 &test_X, T1 &test_y, Eigen::VectorXi &A, Eigen::VectorXi &I, T2 &beta, T3 &coef0,
                  Eigen::VectorXd &bd, Eigen::VectorXd &weights, Eigen::VectorXd &test_weights,
                  Eigen::VectorXi &g_index, Eigen::VectorXi &g_size, int N, Metric<T1, T2, T3, T4> &metric) {
        int n = X.rows();
        int test_n = test_X.rows();

        int A_size = A.size();
        int I_size = I.size();

        Eigen::VectorXd beta_A_group(A_size);
        Eigen::VectorXd d_I_group(I_size);
        for (int i = 0; i < A_size; i++) {
            beta_A_group(i) = bd(A(i));
        }

        for (int i = 0; i < I_size; i++) {
            d_I_group(i) = bd(I(i));
        }

        // cout << "  ==> bd: " << bd.transpose() << endl;

        int k_max = max(1, min(this->exchange_num, min(A_size, I_size)));
        Eigen::VectorXi A_min = min_k(beta_A_group, min(k_max, A_size), true);
        Eigen::VectorXi I_max = max_k(d_I_group, min(k_max, I_size), true);
        Eigen::VectorXi s1 = vector_slice(A, A_min);
        Eigen::VectorXi s2 = vector_slice(I, I_max);

        // cout << "  ==> s1: " << s1.transpose() << endl;
        // cout << "  ==> s2: " << s2.transpose() << endl;

        Eigen::VectorXi A_exchange;
        Eigen::VectorXi A_ind_exchange;
        T4 X_A_exchange;
        T4 test_X_A_exchange;
        T2 beta_A_exchange;
        T3 coef0_A_exchange;

        double L_best = this->loss;
        Eigen::VectorXi A_exchange_best;
        Eigen::VectorXi A_ind_exchange_best;
        T2 beta_A_exchange_best;
        T3 coef0_A_exchange_best;

        int k = 1;
        if (this->splicing_type == 1 || this->splicing_type == 2) {
            k = k_max;
        } else {
            k = 1;
        }
        // for (int k = 1; k <= k_max; k++) {
        for (; k >= 1 && k <= k_max;) {
            // cout << "  ==> k=" << k << endl;
            int s1_size = min(k, A_size);
            int s2_size = min(min(k, I_size), this->max_sparsity - A_size);
            A_exchange.resize(A_size + s2_size);
            A_exchange << A, s2.head(s2_size).eval();
            sort(A_exchange.data(), A_exchange.data() + A_exchange.size());

            // active variables <=> inactive variables
            for (int C = 0; C <= k; C++) {
                // cout << "  ==> A_exchange=" << A_exchange.transpose() << endl;
                A_ind_exchange = find_ind(A_exchange, g_index, g_size, (this->beta).rows(), N);
                X_A_exchange = X_seg(X, n, A_ind_exchange, this->model_type);
                test_X_A_exchange = X_seg(test_X, test_n, A_ind_exchange, this->model_type);
                slice(beta, A_ind_exchange, beta_A_exchange);
                coef0_A_exchange = coef0;

                this->primary_model_fit(X_A_exchange, y, weights, beta_A_exchange, coef0_A_exchange, DBL_MAX,
                                        A_exchange, g_index, g_size);
                double loss0 = this->loss_function(test_X_A_exchange, test_y, test_weights, beta_A_exchange,
                                                   coef0_A_exchange, A_exchange, g_index, g_size, this->lambda_level);
                double L = metric.ic(loss0, n, N, beta_A_exchange, coef0_A_exchange, this->model_type,
                                     this->lambda_level, A_exchange.size());

                // if (this->loss > L) {
                //     A = A_exchange;
                //     I = complement(A_exchange, N);
                //     slice_restore(beta_A_exchange, A_ind_exchange, beta);
                //     coef0 = coef0_A_exchange;
                //     this->loss = L;
                //     this->sparsity_level = A.size();
                //     return true;
                // }
                if (L_best > L) {
                    A_exchange_best = A_exchange;
                    A_ind_exchange_best = A_ind_exchange;
                    beta_A_exchange_best = beta_A_exchange;
                    coef0_A_exchange_best = coef0_A_exchange;
                    L_best = L;
                }

                // all active variables are thrown, stop
                if (C == k) break;

                // update A_exchange
                // throw the most unimportant active & inactive variable
                int i, i_new = 0, A_throw = C, I_throw = s2_size - C - 1;
                bool bo1 = A_throw < s1_size;
                bool bo2 = I_throw >= 0;
                Eigen::VectorXi A_exchange_new(A_exchange.size() - bo1 - bo2);
                for (i = 0; i < A_exchange.size(); i++) {
                    if (!bo1 && !bo2) break;
                    if (bo1 && A_exchange(i) == s1(A_throw)) {
                        bo1 = false;
                        continue;
                    }
                    if (bo2 && A_exchange(i) == s2(I_throw)) {
                        bo2 = false;
                        continue;
                    }
                    A_exchange_new(i_new++) = A_exchange(i);
                }
                int rest = A_exchange.size() - i;
                A_exchange_new.bottomRows(rest) = A_exchange.bottomRows(rest);
                A_exchange = A_exchange_new;
            }

            if (this->splicing_type == 1) {
                k--;
            } else if (this->splicing_type == 2) {
                k = int(k / 2);
            } else {
                k++;
            }
        }

        // no need to exchange
        if (L_best == this->loss) return false;

        // best exchange
        A = A_exchange_best;
        I = complement(A_exchange_best, N);
        slice_restore(beta_A_exchange_best, A_ind_exchange_best, beta);
        coef0 = coef0_A_exchange_best;
        this->loss = L_best;
        this->sparsity_level = A.size();
        return true;
    };

    virtual void inital_setting(T4 &X, T1 &y, Eigen::VectorXd &weights, Eigen::VectorXi &g_index,
                                Eigen::VectorXi &g_size, int &N){};
    virtual void clear_setting(){};

    virtual Eigen::VectorXi inital_screening(Data<T1, T2, T3, T4> &train_data, Data<T1, T2, T3, T4> &test_data,
                                             Metric<T1, T2, T3, T4> &metric) {
        T2 beta_temp;
        T3 coef0_temp;
        this->bd = this->bd_init;

        // coefficient-wise beta
        for (int i = 0; i < train_data.g_num; i++) {
            int p_temp = train_data.g_size(i);
            T4 x_temp = train_data.x.middleCols(train_data.g_index(i), p_temp);
            Eigen::VectorXi A_temp = Eigen::VectorXi::LinSpaced(p_temp, 0, p_temp - 1);
            Eigen::VectorXi g_index_temp = Eigen::VectorXi::LinSpaced(p_temp, 0, p_temp - 1);
            Eigen::VectorXi g_size_temp = Eigen::VectorXi::Ones(p_temp);
            coef_set_zero(p_temp, train_data.M, beta_temp, coef0_temp);

            this->update_sparsity_level(p_temp);
            this->primary_model_fit(x_temp, train_data.y, train_data.weight, beta_temp, coef0_temp, DBL_MAX, A_temp,
                                    g_index_temp, g_size_temp);

            this->bd(i) = beta_temp.squaredNorm() / p_temp;
        }

        slice_assignment(this->bd, this->always_select, DBL_MAX);
        slice_assignment(this->bd, this->A_init, DBL_MAX - 1);

        Eigen::VectorXi ind = max_k(this->bd, train_data.g_num, true);
        // cout << "  ==> ind: " << ind.transpose() << endl;

        // choose initial sparsity
        Eigen::VectorXi A_best;
        if (this->init_max_sparsity <= 0) {
            this->init_max_sparsity = min(train_data.n, train_data.g_num);
        }
        // std::cout << "  init_max_sparsity=" << init_max_sparsity << std::endl;

        if (this->init_type == 0) {
            // sequence search from s_min to s_max
            int s_min = 1, s_max = this->init_max_sparsity;
            bool s_max_changed = false;
            for (int s = s_min; s <= s_max; s++) {
                beta_temp = this->beta_init;
                coef0_temp = this->coef0_init;
                double loss_temp = 0;
                Eigen::VectorXi A = ind.topRows(s).eval();
                sort(A.data(), A.data() + s);
                fit_on_specificed_set(train_data, test_data, metric, A, beta_temp, coef0_temp, loss_temp);
                // cout << "  ==> s: " << s << " | loss: " << loss_temp << endl;

                if (loss_temp < this->loss || s == s_min) {
                    // cout << "  ==> update initial set" << endl;
                    this->loss = loss_temp;
                    this->beta = beta_temp;
                    this->coef0 = coef0_temp;
                    A_best = A;
                } else if (!s_max_changed) {
                    s_max = min(this->init_max_sparsity, s + this->init_max_sparsity / 10);
                    s_max_changed = true;
                }
            }
        } else if (this->init_type == 1) {
            // golden search with adaptive interval
            int s_min = 1, s_max = min(this->init_gs_start, this->init_max_sparsity);

            // default
            Eigen::VectorXi A = ind.topRows(s_max).eval();
            this->beta = this->beta_init;
            this->coef0 = this->coef0_init;
            sort(A.data(), A.data() + s_max);
            fit_on_specificed_set(train_data, test_data, metric, A, this->beta, this->coef0, this->loss);
            A_best = A;
            // std::cout << "  ==> Default range: "<<s_min<<" - "<<s_max<<" | loss="<<this->loss<<std::endl;

            int s, s_best = s_max;
            while (s_min <= s_max) {
                // gs
                while (s_min <= s_max) {
                    // left
                    double loss_temp_l = 0;
                    s = round(0.618 * s_min + 0.382 * s_max);
                    beta_temp = this->beta_init;
                    coef0_temp = this->coef0_init;
                    Eigen::VectorXi A = ind.topRows(s).eval();
                    sort(A.data(), A.data() + s);
                    fit_on_specificed_set(train_data, test_data, metric, A, beta_temp, coef0_temp, loss_temp_l);
                    // std::cout << "    GS left: " << s << " | loss=" << loss_temp_l << std::endl;
                    if (loss_temp_l < this->loss || s == 1) {
                        // cout << "  ==> update initial set" << endl;
                        this->loss = loss_temp_l;
                        this->beta = beta_temp;
                        this->coef0 = coef0_temp;
                        A_best = A;
                        s_best = s;
                    }
                    // right
                    double loss_temp_r = 0;
                    if (s == round(0.382 * s_min + 0.618 * s_max)) {
                        loss_temp_r = loss_temp_l;
                    } else {
                        s = round(0.382 * s_min + 0.618 * s_max);
                        beta_temp = this->beta_init;
                        coef0_temp = this->coef0_init;
                        A = ind.topRows(s).eval();
                        sort(A.data(), A.data() + s);
                        fit_on_specificed_set(train_data, test_data, metric, A, beta_temp, coef0_temp, loss_temp_r);
                        // std::cout << "    GS right: " << s << " | loss=" << loss_temp_l << std::endl;
                        if (loss_temp_r < this->loss || s == 1) {
                            // cout << "  ==> update initial set" << endl;
                            this->loss = loss_temp_r;
                            this->beta = beta_temp;
                            this->coef0 = coef0_temp;
                            A_best = A;
                            s_best = s;
                        }
                    }
                    // update sparsity range
                    if (loss_temp_l <= loss_temp_r) {
                        s_max = round(0.382 * s_min + 0.618 * s_max);
                    } else {
                        s_min = round(0.618 * s_min + 0.382 * s_max);
                    }
                    // std::cout << "    Shrink: ("<<s_min<<", "<<s_max<<")"<<std::endl;
                    // exit iter
                    if (s_min >= s_max - 1) break;
                }
                // update s_min, s_max
                if (s_best != s_max) break;
                s_min = s_max + 1;
                s_max = min(s_max * 2, this->init_max_sparsity);
                // std::cout << "  --> Update range: "<<s_min<<" - "<<s_max<<" | loss="<<this->loss<<std::endl;
            }
        }
        // cout << "  ==> A_init: " << A_best.transpose() << endl;
        return A_best;
    }

    void fit_on_specificed_set(Data<T1, T2, T3, T4> &train_data, Data<T1, T2, T3, T4> &test_data,
                               Metric<T1, T2, T3, T4> &metric, Eigen::VectorXi &A, T2 &beta, T3 &coef0, double &loss) {
        // get A_ind from A
        Eigen::VectorXi A_ind = find_ind(A, train_data.g_index, train_data.g_size, beta.rows(), train_data.g_num);
        T4 X_A = X_seg(train_data.x, train_data.n, A_ind, this->model_type);
        T4 test_X_A = X_seg(test_data.x, test_data.n, A_ind, this->model_type);
        T2 beta_A;
        slice(beta, A_ind, beta_A);

        // fit
        this->update_sparsity_level(A.size());
        this->primary_model_fit(X_A, train_data.y, train_data.weight, beta_A, coef0, DBL_MAX, A, train_data.g_index,
                                train_data.g_size);
        slice_restore(beta_A, A_ind, beta);

        // compute loss
        double loss0_temp = this->loss_function(test_X_A, test_data.y, test_data.weight, beta_A, coef0, A,
                                                test_data.g_index, test_data.g_size, this->lambda_level);
        loss = metric.ic(loss0_temp, train_data.n, train_data.g_num, beta, coef0, this->model_type, this->lambda_level,
                         A.size());
    };

    // void final_fitting(T4 &train_x, T1 &train_y, Eigen::VectorXd &train_weight, Eigen::VectorXi &A,
    //                    Eigen::VectorXi &g_index, Eigen::VectorXi &g_size, int train_n, int N) {
    //     Eigen::VectorXi A_ind = find_ind(A, g_index, g_size, (this->beta).rows(), N);
    //     T4 X_A = X_seg(train_x, train_n, A_ind, this->model_type);
    //     T2 beta_A;
    //     slice(this->beta, A_ind, beta_A);

    //     this->primary_model_fit_max_iter += FINAL_FIT_ITER_ADD;
    //     // coef0_old = this->coef0;
    //     bool success =
    //         this->primary_model_fit(X_A, train_y, train_weight, beta_A, this->coef0, DBL_MAX, A, g_index, g_size);
    //     // if (!success){
    //     //   this->coef0 = coef0_old;
    //     // }else{
    //     slice_restore(beta_A, A_ind, this->beta);
    //     this->loss = this->loss_function(X_A, train_y, train_weight, beta_A, this->coef0, A, g_index, g_size,
    //                                      this->lambda_level);
    //     // }
    //     this->primary_model_fit_max_iter -= FINAL_FIT_ITER_ADD;
    // }

    virtual double loss_function(T4 &X, T1 &y, Eigen::VectorXd &weights, T2 &beta, T3 &coef0, Eigen::VectorXi &A,
                                 Eigen::VectorXi &g_index, Eigen::VectorXi &g_size, double lambda) {
        return 0;
    };

    virtual void sacrifice(T4 &X, T4 &XA, T1 &y, T2 &beta, T2 &beta_A, T3 &coef0, Eigen::VectorXi &A,
                           Eigen::VectorXi &I, Eigen::VectorXd &weights, Eigen::VectorXi &g_index,
                           Eigen::VectorXi &g_size, int N, Eigen::VectorXi &A_ind, Eigen::VectorXd &bd,
                           Eigen::VectorXi &U, Eigen::VectorXi &U_ind, int num) {
        return;
    };

    virtual bool primary_model_fit(T4 &X, T1 &y, Eigen::VectorXd &weights, T2 &beta, T3 &coef0, double loss0,
                                   Eigen::VectorXi &A, Eigen::VectorXi &g_index, Eigen::VectorXi &g_size) {
        return true;
    };

    virtual double effective_number_of_parameter(T4 &X, T4 &XA, T1 &y, Eigen::VectorXd &weights, T2 &beta, T2 &beta_A,
                                                 T3 &coef0) {
        return this->sparsity_level;
    };
};

#endif  // SRC_ALGORITHM_H
