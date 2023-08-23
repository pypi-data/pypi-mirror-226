use ndarray::prelude::*;
use std::{ops::{Div, Range}, iter::zip};

use crate::pricing_models::PricingModel;
use crate::cost_utils::{*};
use crate::optimisers::Optimisable;
use crate::Convergence;


pub struct CostFunction<'a> {
    pub usage: Array2<f64>,
    pub models: &'a Vec<PricingModel<'a>>,
    pub day: bool,
    pub steps: Array1<f64>,
    usage_copy: Array2<f64>,
    pub record: bool,
    pub convergence: Convergence
}

impl<'a> CostFunction<'a> {
    pub fn new(usage: Array2<f64>, models: &'a Vec<PricingModel<'a>>, day: bool, record: bool) -> Self {
        let (timespan, n) = usage.dim();
        let mut steps = Vec::new();
        let mut average_cost = 1000.;
        for i in models.iter() {
            match i {
                PricingModel::Reservations(_, prices, current_levels) => {
                    steps.reserve_exact(n);
                    for p in prices {
                        steps.push(1. / p);
                    }
                },
                PricingModel::SavingsPlans(_, _, _) => {
                    steps.push(1.);
                }
                PricingModel::OnDemand(od_prices) => {
                    average_cost = (&usage * od_prices).sum() / timespan as f64;
                },
            }
        }
        let mut steps = Array1::from(steps);
        steps *= average_cost / 5_000.;
        CostFunction { usage: usage.to_owned(),
            models: models,
            day: day,
            steps: steps,
            usage_copy: usage.clone(),
            record: record,
            convergence: if record {Convergence::new()} else {Convergence::default()} }
    }
}

impl<'a>  Optimisable for CostFunction<'a>  {

    fn call(&mut self, x: ArrayView1<f64>) -> f64 {
        cost_final(self.usage.view(),
                    &self.models,
                    x,
                    self.day,
                    &mut self.usage_copy)
    }


    fn gradient(&mut self, x: ArrayView1<f64>) -> Array1<f64> {
        // cost_final_gradient(self.usage.view(),
        //             self.steps.view(),
        //             x,
        //             &self.models,
        //             self.day,
        //             &mut self.usage_copy)
        let mut h = Array2::from_diag(&self.steps);
        h += &x;

        h.map_axis_mut(Axis(1), |row| {
            self.call(row.view())
        })
    }

    fn record(&mut self, x: ArrayView1<f64>, c: f64, speed: Option<f64>) {
        let s = match speed {
            None => 0.,
            Some(s) => s            
        };

        if self.record {
            self.convergence.costs.as_mut().expect("correct initialisation").push(c);
            self.convergence.coverages.as_mut().expect("correct initialisation").push(
                final_coverage(self.usage.view(), &self.models, x, self.day, &mut self.usage_copy)
            );
            self.convergence.choices.as_mut().expect("correct initialisation").push(5);
            self.convergence.discounts.as_mut().expect("correct initialisation").push(5.);
            self.convergence.speeds.as_mut().expect("correct initialisation").push(s);
        //     self.convergence.underutilisation_cost.as_mut().expect("correct initialisation").push(
        //         underutilisation(self.usage.view(), self.prices.view(), &mut self.levels_copy, & self.models, self.day, &mut self.usage_copy)
        // );
        }
    }

}



pub fn create_steps(prices: ArrayView2<f64>, t: f64) -> Array1<f64>  {
    let (_, n) = prices.dim();
    let ri_price = prices.slice(s![2, ..]);
    let mut steps= Array::ones(n+1);
    let mut s =  steps.slice_mut(s![1..]);
    s.assign(&s.div(&ri_price));
    steps *= t;

    steps
}


pub fn create_space(usage: ArrayView2<f64>, prices: ArrayView2<f64>, p: f64) -> Vec<Range<f64>> {
    let min_usage = usage.fold_axis(Axis(0), f64::INFINITY, |a, &x| a.min(x));
    let max_usage = usage.fold_axis(Axis(0), -f64::INFINITY, |a, &x| a.max(x));
    let sp_prices = prices.slice(s![1, ..]);
    let max_sp = (&usage * &sp_prices).sum_axis(Axis(1)).fold(-f64::INFINITY, |a, &b| a.max(b));

    let mut space = Vec::with_capacity(usage.ncols() + 1);
    space.push(Range { start: 0., end: max_sp / p });

    for (borne_inf, borne_sup) in zip(min_usage, max_usage) {
        space.push(Range{ start: borne_inf / p, end: borne_sup / p});
    }
    
    space
}