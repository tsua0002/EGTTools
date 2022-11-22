/** Copyright (c) 2019-2021  Elias Fernandez
  *
  * This file is part of EGTtools.
  *
  * EGTtools is free software: you can redistribute it and/or modify
  * it under the terms of the GNU General Public License as published by
  * the Free Software Foundation, either version 3 of the License, or
  * (at your option) any later version.
  *
  * EGTtools is distributed in the hope that it will be useful,
  * but WITHOUT ANY WARRANTY; without even the implied warranty of
  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  * GNU General Public License for more details.
  *
  * You should have received a copy of the GNU General Public License
  * along with EGTtools.  If not, see <http://www.gnu.org/licenses/>
*/
#include <egttools/Distributions.h>

//template<>
//size_t egttools::binomialCoeff<size_t, size_t>(size_t n, size_t k) {
//    if ((k > n) || (n == ULONG_MAX))
//        return 0;
//
//    // Since C(n, k) = C(n, n-k)
//    size_t n_terms = std::min(k, n - k);
//
//    size_t res = 1;
//    size_t m = n + 1;
//
//    // Calculate value of [n * (n-1) * ... * (n-k+1)] / [k * (k-1) * ... * 1]
//    for (size_t i = 1; i < n_terms + 1; ++i) {
//        res *= m - i;
//        res /= i;
//    }
//
//    return res;
//}

#if (HAS_BOOST)
mp::uint128_t egttools::binomial_precision(size_t n, size_t k) {
    if ((k > n) || (n == ULONG_MAX))
        return 0;

    // Since C(n, k) = C(n, n-k)
    size_t n_terms = std::min(k, n - k);

    mp::uint128_t res = 1;
    size_t m = n + 1;

    // Calculate value of [n * (n-1) * ... * (n-k+1)] / [k * (k-1) * ... * 1]
    for (mp::uint128_t i = 1; i < n_terms + 1; ++i) {
        res *= m - i;
        res /= i;
    }

    return res;
}
#endif

double
egttools::multivariateHypergeometricPDF(size_t m, size_t k, size_t n, const std::vector<size_t> &sample_counts,
                                        const std::vector<size_t> &population_counts) {

    uint_type_ res = 1;
    // First we calculate the number of unordered samples of size n chosen from the population
    auto denominator = binomial_coeff_(m, n);

    // Then we calculate the multiplication of the number of all unordered subsets of a subset of the population
    // with only 1 type of object
    for (size_t i = 0; i < k; ++i) {
        res *= binomial_coeff_(population_counts[i], sample_counts[i]);
    }

#if (HAS_BOOST)
    return static_cast<double>(res.convert_to<mp::cpp_dec_float_100>() / denominator.convert_to<mp::cpp_dec_float_100>());
#else
    return static_cast<double>(res) / static_cast<double>(denominator);
#endif
}

double
egttools::multivariateHypergeometricPDF(size_t m, size_t k, size_t n, const std::vector<size_t> &sample_counts,
                                        const Eigen::Ref<const VectorXui> &population_counts) {

    uint_type_ res = 1;
    // First we calculate the number of unordered samples of size n chosen from the population
    auto denominator = binomial_coeff_(m, n);

    // Then we calculate the multiplication of the number of all unordered subsets of a subset of the population
    // with only 1 type of object
    for (signed long i = 0; i < static_cast<signed long>(k); ++i) {
        res *= binomial_coeff_(population_counts(i), sample_counts[i]);
    }

#if (HAS_BOOST)
    return static_cast<double>(res.convert_to<mp::cpp_dec_float_100>() / denominator.convert_to<mp::cpp_dec_float_100>());
#else
    return static_cast<double>(res) / static_cast<double>(denominator);
#endif
}

double
egttools::multivariateHypergeometricPDF(size_t m, size_t k, size_t n, const Eigen::Ref<const VectorXui> &sample_counts,
                                        const Eigen::Ref<const VectorXui> &population_counts) {

    uint_type_ res = 1;
    // First we calculate the number of unordered samples of size n chosen from the population
    auto denominator = binomial_coeff_(m, n);

    // Then we calculate the multiplication of the number of all unordered subsets of a subset of the population
    // with only 1 type of object
    for (signed long i = 0; i < static_cast<signed long>(k); ++i) {
        res *= binomial_coeff_(population_counts(i), sample_counts(i));
    }

#if (HAS_BOOST)
    return static_cast<double>(res.convert_to<mp::cpp_dec_float_100>() / denominator.convert_to<mp::cpp_dec_float_100>());
#else
    return static_cast<double>(res) / static_cast<double>(denominator);
#endif
}

#if (HAS_BOOST)
double egttools::multinomialPMF(const Eigen::Ref<const VectorXui> &group_configuration, size_t n, const Eigen::Ref<const Vector> &p) {
    if (n == ULONG_MAX)
        return 0;
    // This would be an error, and probably better to throw an exception here!
    if (group_configuration.size() != p.size())
        throw std::invalid_argument("Arguments p and group configuration must have the same length!");

    mp::cpp_int n_factorial = egttools::math::factorial(n);
    mp::cpp_dec_float_100 prob = 1;

    // Iterate through the possible group configurations and
    // calculate the multiplications
    for(signed long i = 0; i < group_configuration.size(); ++i) {
        for (size_t j = 1; j < group_configuration(i) + 1; ++j) {
            prob *= p(i) / static_cast<int>(j);
        }
    }
    return (prob * n_factorial.convert_to<mp::cpp_dec_float_100>()).convert_to<double>();
}
#else
double egttools::multinomialPMF(const Eigen::Ref<const VectorXui> &group_configuration, size_t n, const Eigen::Ref<const Vector> &p) {
    if (n > 170)
        throw std::invalid_argument("n < 170 or there will be an overflow.");
    // This would be an error, and probably better to throw an exception here!
    if (group_configuration.size() != p.size())
        throw std::invalid_argument("Arguments p and group configuration must have the same length!");

    int64_t n_factorial = egttools::math::factorial(n);
    double prob = 1;

    // Iterate through the possible group configurations and
    // calculate the multiplications
    for(signed long i = 0; i < group_configuration.size(); ++i) {
        for (size_t j = 1; j < group_configuration(i) + 1; ++j) {
            prob *= p(i) / static_cast<int>(j);
        }
    }
    return prob * n_factorial;
}

#endif

//#if (HAS_BOOST)
//template<>
//mp::uint128_t egttools::starsBars<size_t, mp::uint128_t>(size_t stars, size_t bins) {
//    return egttools::binomial_precision(stars + bins - 1, stars);
//}
//#endif