// #![feature(unboxed_closures)]
// #![feature(fn_traits)]

use std::collections::{HashMap, HashSet};
use std::iter::zip;
use std::ops::Range;

use ndarray::{prelude::*, IntoDimension, IxDynImpl, concatenate, stack};
use pyo3::types::PyDict;
use rand::{distributions::Uniform, Rng};
use std::ops::Div;

use numpy::{PyReadonlyArray2, PyArray1, PyReadonlyArray1, IntoPyArray, PyReadonlyArrayDyn, PyReadonlyArray3};
use pyo3::prelude::*;
use rayon::prelude::*;

mod optimisers;
mod cost_utils;
mod tests;
mod pricing_models;
mod pre_processing;


use crate::optimisers::{best_optimiser, inertial_optimiser, best_optimiser_with_details, Results, gradient_descent};
use crate::cost_utils::{cost, coverage, cost_final, final_coverage};
use crate::pricing_models::{PricingModel, Term};
use crate::pre_processing::{create_steps, create_space, CostFunction};



#[pyclass(unsendable, frozen)]
#[derive(Clone)]
pub struct FinalResults {
    pub commitments: HashMap<String, ArrayBase<ndarray::OwnedRepr<usize>, Dim<[usize; 1]>>>,
    #[pyo3(get)]
    pub n_iter: usize,
    #[pyo3(get)]
    pub minimum: f64,
    #[pyo3(get)]
    pub coverage: f64,
    #[pyo3(get)]
    pub convergence: Convergence
}

#[pymethods]
impl FinalResults {
    #[getter]
    fn commitments<'py>(&self,  py: Python<'py>) -> HashMap<String, &'py numpy::PyArray<usize, Dim<[usize; 1]>>> {
        let mut dict: HashMap<String, &numpy::PyArray<usize, Dim<[usize; 1]>>> = HashMap::new();
        for (k, v) in self.commitments.clone() {
            dict.insert(k, v.into_pyarray(py));
        }

        dict
    }
}

#[derive(Clone, Default)]
#[pyclass(unsendable, frozen)]
pub struct Convergence {
    costs: Option<Vec<f64>>,
    coverages: Option<Vec<f64>>,
    discounts: Option<Vec<f64>>,
    choices: Option<Vec<usize>>,
    underutilisation_cost: Option<Vec<f64>>,
    speeds: Option<Vec<f64>>,
}

#[pymethods]
impl Convergence {
    #[getter]
    fn underutilisation_cost<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.underutilisation_cost {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }
    #[getter]
    fn costs<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.costs {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }
    #[getter]
    fn coverages<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.coverages {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }
    #[getter]
    fn discounts<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.discounts {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }
    #[getter]
    fn speeds<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<f64>> {
        match &self.speeds {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }
    #[getter]
    fn choices<'py>(&self,  py: Python<'py>) -> Option<&'py PyArray1<usize>> {
        match &self.choices {
            Some(c) => Some(c.clone().into_pyarray(py)),
            None => None
        }
    }

}

impl Convergence {
    pub fn new() -> Self {
        Convergence { costs: Some(Vec::new()),
            coverages: Some(Vec::new()),
            discounts: Some(Vec::new()),
            choices: Some(Vec::new()),
            underutilisation_cost: Some(Vec::new()),
            speeds: Some(Vec::new()) }
    }
}





// impl FnMut<()> for CostFunction {
//     extern "rust-call" fn call_mut(&mut self, x: Array1<f64>) {

//             self.levels_copy = Array2::zeros(usage.dim()) + &x;
//             cost_final(self.usage.view(),
//                         self.prices.view(),
//                         &mut two_dim_levels, &models, b, &mut dump)
//         }
//     }


// impl FnOnce<()> for CostFunction {
//     type Output = ();

//     extern "rust-call" fn call_once(self, _args: Some(Vec::new())) {
//         println!("Call (FnOnce) for Foo");
//     }
// }


#[pymodule]
fn rust_as_backend(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    #[pyfn(m)]
    #[pyo3(name = "simple_optimisation")]
    fn py_simple_optimiser<'py>(usage: PyReadonlyArray2<f64>,
        prices: PyReadonlyArray2<f64>,
        period: String,
        convergence_details: Option<bool>,
        step: Option<f64>,
        starting_point: Option<PyReadonlyArray1<f64>>, 
    ) -> Py<Results> {

        let p = match period.as_str() {
            "D" => 24.,
            "H" => 1.,
            _ => {panic!("provide a valid period string : either D or H")}
        };

        let usage = usage.as_array();
        let prices = prices.as_array();

        let t = match step {
            Some(t) => t,
            None => 1.
        };

        let space = create_space(usage.view(), prices.view(), p);
        let steps = create_steps(prices.view(), t);

        let start = match starting_point {
            Some(t) => t.as_array().to_owned(),
            None  => Array1::from_iter(space.iter().map(|x| x.start))
        };

        let make_cost_function = || {
            let (i, j) = usage.dim();
            let mut two_dim_levels = Array2::zeros((i, j  + 1));
            let mut dump = Array2::zeros((i, j));
            let prices = prices.to_owned();
            println!("expensive copies here");
            move |levels: ArrayView1<f64>| {
                two_dim_levels = Array2::zeros((i, j+1)) + &levels;
                cost(usage.view(), prices.view(), two_dim_levels.view(), &mut dump)
            }
        };


        // let make_gradient = || {

        // }

        let res = match convergence_details {
            Some(b) if b =>  best_optimiser_with_details(usage.to_owned(), prices.to_owned(), t, Some(start)),
            _ => best_optimiser(&mut make_cost_function(), steps.view(), start)
        };

        Python::with_gil(|py| Py::new(py, res).unwrap())
    }


    #[pyfn(m)]
    #[pyo3(name = "cost_distribution")]
    fn py_cost_distribution<'py>(
        py: Python<'py>,
        usage: PyReadonlyArray3<f64>,
        prices: PyReadonlyArray2<f64>,
        levels: PyReadonlyArray2<f64>) -> &'py PyArray1<f64> {
        let usage = usage.as_array();
        let prices = prices.as_array();
        let levels = levels.as_array();
    
        let (n, i, j) = usage.dim();
        let mut cost_samples = Vec::with_capacity(n+1);

        usage.axis_iter(Axis(0))
        .into_par_iter()
        .with_min_len(n/8)
        .map_init(
        || Array2::zeros((i, j)),
        |init, row| cost(row.view(), prices.view(), levels.view(), init))
        .collect_into_vec(&mut cost_samples);

        Array1::from_vec(cost_samples).into_pyarray(py)
    }


    #[pyfn(m)]
    #[pyo3(name = "optimise_predictions")]
    fn py_optimise_predictions<'py>(
        predictions: PyReadonlyArray3<f64>,
        prices: PyReadonlyArray2<f64>,
        levels: PyReadonlyArray2<f64>) -> Py<Results> {
        
        let predictions = predictions.as_array();
        let prices = prices.as_array();
        let current_levels = levels
            .as_array()
            .to_owned();

        let (n, i, j) = predictions.dim();

        let make_cost_function = move || {
            let (_, i, j) = predictions.dim();
            let current_levels = current_levels.clone();
            let mut two_dim_levels = Array2::zeros((i, j  + 1));
            let mut dump = Array2::zeros((i, j));
            println!("expensive copies here");
            move |levels: ArrayView1<f64>| {
                two_dim_levels = &current_levels + &levels;
                predictions.axis_iter(Axis(0))
                .map(|pred| cost(pred.view(), prices.view(), two_dim_levels.view(), &mut dump))
                .sum() // here we just minimize the mean, but it could be a better idea to minimize the median or some quantile
                // but more compute intensive, as it implies one sort (but whatever)
            }
        };

        let space = predictions.fold_axis(
            Axis(2),
            Range { start: 0., end: 0. },
            |x, y| Range {
                start: y.min(x.start),
                end: y.max(x.end)
            }).into_raw_vec();
        
        let steps = create_steps(prices.view(), 1.);

        let res = best_optimiser(&mut make_cost_function(), steps.view(), Array1::from_iter(space.iter().map(|x| x.start)));

        Python::with_gil(|py| Py::new(py, res).unwrap())
    }

    #[pyfn(m)]
    #[pyo3(name = "cost")]
    fn py_cost(usage: PyReadonlyArray2<f64>, prices: PyReadonlyArray2<f64>, levels: PyReadonlyArrayDyn<'_, f64>) -> Option<f64> {
        let usage = usage.as_array();
        let prices = prices.as_array();

        let mut dump = usage.to_owned();
        let levels = levels
                            .as_array()
                            .to_owned();

        let z = match levels.dim().into_dimension().ndim() {
            1 => {
                let (i, j) = usage.dim();
                let one_dim_levels = levels.into_dimensionality::<Ix1>().unwrap();
                let two_dim_levels = Array2::zeros((i, j  + 1)) + &one_dim_levels;
                Some(cost(usage.view(),
                        prices.view(),
                        two_dim_levels.view(),
                        &mut dump))
                    },
            2 => Some(cost(usage.view(),
                        prices.view(),
                        levels.into_dimensionality::<Ix2>().unwrap().view(),
                        &mut dump)),
            _ => None
        };

        z
    }

    #[pyfn(m)]
    #[pyo3(name = "coverage")]
    fn py_coverage(usage: PyReadonlyArray2<f64>, prices: PyReadonlyArray2<f64>, levels: PyReadonlyArrayDyn<'_, f64>) -> Option<f64> {
        let usage = usage.as_array();
        let prices = prices.as_array();

        let levels = levels.as_array()
                            .to_owned();

        let z = match levels.dim().into_dimension().ndim() {
            1 => {
                let (i, j) = usage.dim();
                let one_dim_levels = levels.into_dimensionality::<Ix1>().unwrap();
                let two_dim_levels = Array2::zeros((i, j  + 1)) + &one_dim_levels;
                Some(coverage(usage.view(),
                        prices.view(),
                        two_dim_levels.view()))
            },
            2 => Some(coverage(usage.view(),
                        prices.view(),
                        levels.into_dimensionality::<Ix2>().unwrap().view())),
            _ => None
        };

        z
    }


    #[pyfn(m)]
    #[pyo3(name = "general_optimisation")]
    fn py_optim_final(usage: PyReadonlyArray2<f64>,
        prices: PyReadonlyArray2<f64>,
        current_levels: PyReadonlyArray2<f64>,
        pricing_models: Vec<&str>,
        period: &str,
        convergence_details: Option<bool>,
    ) -> Py<FinalResults> {

        let b = period == "D";
        let usage = usage.as_array().to_owned();
        let prices = prices.as_array().to_owned();
        let levels = current_levels.as_array();

        let mut models = Vec::with_capacity(pricing_models.len());
        let (timespan, n) = usage.dim();
        let mut j = 0;
        for (i, p) in pricing_models.into_iter().enumerate() {
            let model = match p {
                "OD" => PricingModel::OnDemand(prices.slice(s![i, ..])),
                "RI1Y" => PricingModel::Reservations(Term::OneYear, prices.slice(s![i, ..]), levels.slice(s![.., j..j+n])),
                "RI3Y" => PricingModel::Reservations(Term::ThreeYears, prices.slice(s![i, ..]), levels.slice(s![.., j..j+n])),
                "SP1Y" => PricingModel::SavingsPlans(Term::OneYear, prices.slice(s![i, ..]), levels.slice(s![.., j])),
                "SP3Y" => PricingModel::SavingsPlans(Term::ThreeYears, prices.slice(s![i, ..]), levels.slice(s![.., j])),
                _ => panic!("Not a known priving model")
            };
            match model {
                PricingModel::Reservations(_, _, _) => j += n,
                PricingModel::SavingsPlans(_, _, _) => j += 1,
                _ => ()
            }

            models.push(model);
        }
        let levels = Array1::zeros(j);
        models.sort();

        let mut c = CostFunction::new(usage, &models, b, false);

        let res = inertial_optimiser(&mut c, levels.view());
          
        let mut returned_df: HashMap<String, ArrayBase<ndarray::OwnedRepr<usize>, Dim<[usize; 1]>>> =  HashMap::new();

        let mut j = 0;
        for model in &models {
            match model {
                PricingModel::Reservations(t, _, _) => {
                    let mut r =  Array1::zeros(n + 1);
                    let mut s =  r.slice_mut(s![1..]);
                    s.assign(&res.argmin.slice(s![j..j+n]));
                    match t {
                        Term::OneYear => {
                            returned_df.insert(String::from("one_year_commitments"), r);
                        },
                        Term::ThreeYears => {
                            returned_df.insert(String::from("three_year_commitments"), r);
                        }
                    }
                    j += n;
                }
                PricingModel::SavingsPlans(t, _, _) => {
                    match t {
                        Term::OneYear => {
                            returned_df.get_mut("one_year_commitments").unwrap()[0] = res.argmin[j];
                        },
                        Term::ThreeYears => {
                            returned_df.get_mut("three_year_commitments").unwrap()[0] = res.argmin[j];
                        }
                    }
                    j += 1;
                },
                PricingModel::OnDemand(_) => ()
            } 
        }


        let fres = FinalResults {
            commitments : returned_df,
            n_iter : res.n_iter,
            coverage : 2.,
            minimum : res.minimum,
            convergence : res.convergence

        };
        Python::with_gil(|py| Py::new(py, fres).unwrap())        
    }


    #[pyfn(m)]
    #[pyo3(name = "final_cost_or_coverage")]
    fn py_cost_final(usage: PyReadonlyArray2<f64>,
        prices: PyReadonlyArray2<f64>,
        levels: PyReadonlyArray2<f64>,
        pricing_models: Vec<&str>,
        period: &str,
        cost_or_coverage: bool) -> f64 {

            let b = period == "D";
            let usage = usage.as_array();
            let prices = prices.as_array();
            let mut levels = levels.as_array().to_owned().mapv(|x| x as f64);
    
            let mut models = Vec::with_capacity(pricing_models.len());
            let (timespan, n) = usage.dim();
            let mut dump = Array2::zeros((timespan, n));
            let mut j = 0;
            for (i, p) in pricing_models.into_iter().enumerate() {
                let model = match p {
                    "OD" => PricingModel::OnDemand(prices.slice(s![i, ..])),
                    "RI1Y" => PricingModel::Reservations(Term::OneYear, prices.slice(s![i, ..]), levels.slice(s![.., j..j+n])),
                    "RI3Y" => PricingModel::Reservations(Term::ThreeYears, prices.slice(s![i, ..]), levels.slice(s![.., j..j+n])),
                    "SP1Y" => PricingModel::SavingsPlans(Term::OneYear, prices.slice(s![i, ..]), levels.slice(s![.., j])),
                    "SP3Y" => PricingModel::SavingsPlans(Term::ThreeYears, prices.slice(s![i, ..]), levels.slice(s![.., j])),
                    _ => panic!("Not a known priving model")
                };
                match model {
                    PricingModel::Reservations(_, _, _) => j += n,
                    PricingModel::SavingsPlans(_, _, _) => j += 1,
                    _ => ()
                }
    
                models.push(model);
            }

            let x = Array1::zeros(j);

            if cost_or_coverage {
                cost_final(usage.view(), &models, x.view(), b, &mut dump)
            } else {
                final_coverage(usage.view(), &models, x.view(), b, &mut dump)
            }
        }


    m.add_class::<Results>()?;


    Ok(())
}


