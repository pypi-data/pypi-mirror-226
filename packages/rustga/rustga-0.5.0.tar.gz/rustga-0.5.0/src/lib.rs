mod crossover;
mod generation_iterator;
mod mutation;
mod search_range;
mod selection;

use chrono;
use crossover::*;
use generation_iterator::*;
use itertools::Itertools;
use mutation::*;
use ordered_float::OrderedFloat;
use pyo3::prelude::*;
use rand::Rng;
use search_range::SearchRange;
use search_range::*;
use selection::*;

/// Type alias for a pair of the individual and its score.
struct CandidateAndScore(IndividualType, OrderedFloat<f64>);

/// Python fitness function callback.
/// The callback should take a list of genomes and return a list of scores.
struct FitnessCalc<'a> {
    py: Python<'a>,
    callback: &'a PyObject,
}

impl FitnessCalc<'_> {
    fn fitness(&self, genomes: &Vec<IndividualType>) -> Vec<OrderedFloat<f64>> {
        let pygenomes = genomes.to_object(self.py);
        let res = self.callback.call(self.py, (pygenomes,), None).unwrap();
        let res: Vec<f64> = res.as_ref(self.py).extract().unwrap();
        res.iter().map(|r| OrderedFloat(*r)).collect::<Vec<_>>()
    }
}

/// Python transformer callback.
/// The callback should take a list of genomes and return a list of genomes.
/// This is used for the initial population and mutation.
struct Transformer<'a> {
    py: Python<'a>,
    callback: &'a PyObject,
}

impl Transformer<'_> {
    fn transform(&self, genomes: IndividualType) -> IndividualType {
        let pygenomes = genomes.to_object(self.py);
        let res = self.callback.call(self.py, (pygenomes,), None).unwrap();
        let res: IndividualType = res.as_ref(self.py).extract().unwrap();
        res
    }
}

#[pyclass(module = "gasolver")]
#[derive(Clone)]
struct GenomeBuilder {
    search_ranges: Vec<SearchRangeTypes>,
}

impl GenomeBuilder {
    fn build_genome<R>(&self, rng: &mut R) -> IndividualType
    where
        R: Rng + Sized,
    {
        self.search_ranges
            .iter()
            .map(|srtype| match srtype {
                SearchRangeTypes::ContinuousRange(cr) => cr.random_pick_from_rng(rng),
                SearchRangeTypes::SteppedRange(sr) => sr.random_pick_from_rng(rng),
                SearchRangeTypes::NumberFiniteSet(nf) => nf.random_pick_from_rng(rng),
                SearchRangeTypes::StringFiniteSet(sf) => sf.random_pick_from_rng(rng),
                SearchRangeTypes::MultiContinuousRange(mcr) => mcr.random_pick_from_rng(rng),
                SearchRangeTypes::MultiSteppedRange(msr) => msr.random_pick_from_rng(rng),
            })
            .collect::<Vec<_>>()
    }
}

#[pymethods]
impl GenomeBuilder {
    fn length(&self) -> usize {
        self.search_ranges.len()
    }
}

#[pyclass(module = "gasolver")]
#[derive(Clone, Copy)]
struct GAParams {
    population_size: usize,
    min_generation_num: usize,
    max_generation_num: usize,
    extended_generation_num: usize,
    point_mutation_pb: f64,
    mutation_pb: f64,
    crossover_pb: f64,
    selection_size_tournament: usize,
}

#[pymethods]
impl GAParams {
    #[new]
    fn new(
        population_size: usize,
        min_generation_num: usize,
        max_generation_num: usize,
        extended_generation_num: usize,
        point_mutation_pb: f64,
        mutation_pb: f64,
        crossover_pb: f64,
        selection_size_tournament: usize,
    ) -> Self {
        GAParams {
            population_size,
            min_generation_num,
            max_generation_num,
            extended_generation_num,
            point_mutation_pb,
            mutation_pb,
            crossover_pb,
            selection_size_tournament,
        }
    }
}
#[pyclass(module = "gasolver")]
#[derive(Clone)]
struct GASolver {
    calculate_score: PyObject,
    initial_transform: Option<PyObject>,
    mutation_transform: Option<PyObject>,
    #[pyo3(get)]
    genome_builder: GenomeBuilder,
    ga_params: GAParams,
    selection: Tournament,
    mutation: RandomMutation,
    crossover: TwoPointCrossOver,
    mutation_pb: f64,
    log_frequency: usize,
}

#[pymethods]
impl GASolver {
    #[new]
    fn new(
        calculate_score: PyObject,
        params: GAParams,
        initial_transform: Option<PyObject>,
        mutation_transform: Option<PyObject>,
    ) -> Self {
        GASolver {
            calculate_score: calculate_score,
            initial_transform: initial_transform,
            mutation_transform: mutation_transform,
            genome_builder: GenomeBuilder {
                search_ranges: vec![],
            },
            ga_params: params,
            selection: Tournament::new(params.population_size, params.selection_size_tournament),
            mutation: RandomMutation::new(params.point_mutation_pb),
            crossover: TwoPointCrossOver::new(params.crossover_pb),
            mutation_pb: params.mutation_pb,
            log_frequency: 200,
        }
    }
    fn add_continuous_range(mut self_: PyRefMut<'_, Self>, continuous_range: PyObject) {
        let cr: ContinuousRange = continuous_range.extract(self_.py()).unwrap();
        self_
            .genome_builder
            .search_ranges
            .push(SearchRangeTypes::ContinuousRange(cr));
    }
    fn add_stepped_range(mut self_: PyRefMut<'_, Self>, stepped_range: PyObject) {
        let sr: SteppedRange = stepped_range.extract(self_.py()).unwrap();
        self_
            .genome_builder
            .search_ranges
            .push(SearchRangeTypes::SteppedRange(sr));
    }
    fn add_number_finite_set(mut self_: PyRefMut<'_, Self>, number_finite_set: PyObject) {
        let nf: FiniteSet<f64> = number_finite_set.extract(self_.py()).unwrap();
        self_
            .genome_builder
            .search_ranges
            .push(SearchRangeTypes::NumberFiniteSet(nf));
    }
    fn add_string_finite_set(mut self_: PyRefMut<'_, Self>, string_finite_set: PyObject) {
        let sf: FiniteSet<String> = string_finite_set.extract(self_.py()).unwrap();
        self_
            .genome_builder
            .search_ranges
            .push(SearchRangeTypes::StringFiniteSet(sf));
    }
    fn add_multi_continuous_range(mut self_: PyRefMut<'_, Self>, multi_continuous_range: PyObject) {
        let mcr: MultiContinuousRange = multi_continuous_range.extract(self_.py()).unwrap();
        self_
            .genome_builder
            .search_ranges
            .push(SearchRangeTypes::MultiContinuousRange(mcr));
    }
    fn add_multi_stepped_range(mut self_: PyRefMut<'_, Self>, multi_stepped_range: PyObject) {
        let msr: MultiSteppedRange = multi_stepped_range.extract(self_.py()).unwrap();
        self_
            .genome_builder
            .search_ranges
            .push(SearchRangeTypes::MultiSteppedRange(msr));
    }
    fn run(self_: PyRef<'_, Self>) -> PyResult<PyObject> {
        let mut rng = rand::thread_rng();
        let mut iter = GenerationIterator::new(
            self_.ga_params.min_generation_num,
            self_.ga_params.max_generation_num,
            self_.ga_params.extended_generation_num,
        );
        let mut best = CandidateAndScore(
            self_.genome_builder.build_genome(&mut rand::thread_rng()),
            OrderedFloat(f64::MIN),
        );
        let fitnesscalc = FitnessCalc {
            py: self_.py(),
            callback: &self_.calculate_score,
        };
        let mutation_transformer = if self_.mutation_transform.is_some() {
            Some(Transformer {
                py: self_.py(),
                callback: self_.mutation_transform.as_ref().unwrap(),
            })
        } else {
            None
        };
        let mut candidates = self_.initial_pop(&mut rng);
        if self_.initial_transform.is_some() {
            let transformer = Transformer {
                py: self_.py(),
                callback: self_.initial_transform.as_ref().unwrap(),
            };
            candidates = candidates
                .into_iter()
                .map(|candidate| transformer.transform(candidate))
                .collect::<Vec<_>>();
        }
        let mut scores = fitnesscalc.fitness(&candidates);
        let mut counter = 0;
        while let Some(_) = iter.next() {
            let selected: Vec<Vec<IndividualElement>> =
                self_.select(&scores, &candidates, &mut rng);
            let crossed = self_.crossbreed(selected, &mut rng);
            let mut mutated: Vec<Vec<IndividualElement>> = self_.mutate(crossed, &mut rng);
            if let Some(transformer) = mutation_transformer.as_ref() {
                mutated = mutated
                    .into_iter()
                    .map(|candidate| transformer.transform(candidate))
                    .collect::<Vec<_>>();
            }
            let next = self_.finalize(&mutated, &fitnesscalc);
            iter.set_scores(&scores);
            if best.1 < next.0 .1 {
                best = next.0;
            }
            scores = next.1;
            candidates = mutated;
            if counter % self_.log_frequency == 0 {
                println!(
                    "[rustga] | {:?} | Generation {:?} finished with best score: {:?} and best individual: {:?}",
                    chrono::offset::Local::now(), counter, best.1, best.0
                );
            }
            counter += 1;
        }
        let best = (best.0, best.1.into_inner());
        Ok(best.to_object(self_.py()))
    }
}

impl GASolver {
    fn initial_pop<R>(&self, rng: &mut R) -> Vec<Vec<IndividualElement>>
    where
        R: Rng + Sized,
    {
        let mut candidates: Vec<Vec<IndividualElement>> =
            Vec::with_capacity(self.ga_params.population_size);
        for _ in 0..self.ga_params.population_size {
            let candidate: IndividualType = self.genome_builder.build_genome(rng);
            candidates.push(candidate);
        }
        candidates
    }

    fn select<R>(
        &self,
        scores: &Vec<OrderedFloat<f64>>,
        candidates: &Vec<Vec<IndividualElement>>,
        rng: &mut R,
    ) -> Vec<Vec<IndividualElement>>
    where
        R: Rng + Sized,
    {
        self.selection
            .select(scores, rng)
            .iter()
            .map(|idx| candidates[idx.unwrap()].clone())
            .collect()
    }

    fn crossbreed<R>(
        &self,
        selected: Vec<Vec<IndividualElement>>,
        rng: &mut R,
    ) -> Vec<Vec<IndividualElement>>
    where
        R: Rng + Sized,
    {
        let mut crossed = selected;
        for comb in (0..crossed.len()).combinations(2) {
            (crossed[comb[0]], crossed[comb[1]]) =
                self.crossover
                    .crossover(&crossed[comb[0]], &crossed[comb[1]], rng);
        }
        crossed
    }

    fn mutate<R>(
        &self,
        crossed: Vec<Vec<IndividualElement>>,
        rng: &mut R,
    ) -> Vec<Vec<IndividualElement>>
    where
        R: Rng + Sized,
    {
        crossed
            .into_iter()
            .map(|individual| {
                if rng.gen_range(0.0..1.0) <= self.mutation_pb {
                    self.mutation
                        .mutate(individual, &self.genome_builder.search_ranges, rng)
                } else {
                    individual
                }
            })
            .collect()
    }

    fn finalize(
        &self,
        mutated: &Vec<Vec<IndividualElement>>,
        fitnesscalc: &FitnessCalc,
    ) -> (CandidateAndScore, Vec<OrderedFloat<f64>>) {
        let scores = fitnesscalc.fitness(&mutated);
        let index_max: usize = scores
            .iter()
            .enumerate()
            .max_by(|(_, a), (_, b)| a.total_cmp(b))
            .map(|(index, _)| index)
            .unwrap();
        (
            CandidateAndScore(mutated[index_max].clone(), scores[index_max]),
            scores,
        )
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustga(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<GenomeBuilder>()?;
    m.add_class::<GAParams>()?;
    m.add_class::<GASolver>()?;
    Ok(())
}
