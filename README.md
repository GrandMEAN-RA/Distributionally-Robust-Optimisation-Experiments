# Distributionally Robust Optimisation Simulation Experiments
This project investigates the **robustness** of parameter estimation methods for the simple linear case under varying degrees and levels of contaminations.

## Backgrounds to the Experiment
Regression Analysis is one of the most widely explored method of exploring possible relationship between varibles with the aim of of predicting the value
of one (the feature variable) over the other (the response variable).

Ordinary Least Squares (OLS) estimation has been the go to method for fitting a linear regression model, and it is notable for producing 
Best Linear Unbiased Estimators (BLUE). However, OLS regression relies on several key assumptions to achieve this. The core assumptions include: 
- Linearity in parameters: The relationship between the independent variables X and the dependent variable Y is linear in the coefficients. 
- Strict exogeneity (Zero Conditional Mean): The error term has a population mean of zero, meaning errors are uncorrelated with independent 
variables i.e. Cov(X,e) = 0.
- No Perfect Multicollinearity: Independent variables should not be perfectly linearly related.
- Homoscedasticity (constant error variance): The error terms have a constant variance (Var(e)=sigma-squared) across all levels of independent variables
- No autocorrelation(No Serial Correlation): Errors are independent of each other (Cov(e_i,e_j)=0 for i != j).
- Normality of Errors: For small sample inference, the error terms are assumed to follow a normal distribution.
These assumptions when violated results in serious consequences. For example:
- Violation of exogeneity causes biased and inconsistent estimates.
- Heteroscedasticity (constant variance) invalidates standard errors, making hypothesis tests unreliable.
- Multicollinearity inflates variance, making estimates imprecise

## Aim of the experiment
This experiment examines the effect of Heteroscedasticity on OLS regression models and assesses the performances of alternative models using OLS as benchmark

## Significance of the Experiment.
Simulation experiments exploring regression models under distribution shifts is highly significant for evaluating the robustness and reliability 
of predictive models in real-world applications. Because real-world data often violates the classical Gauss-Markov assumptions, This particular experiment 
is significant in that:
- It tests the structural robustness of OLS by mixing normal variates with different scales and means (heteroscedasticity). While OLS is the Best 
Linear Unbiased Estimator (BLUE) under strict conditions, this experiment helps determine when standard OLS should be abandoned in favor of other regression 
methods. 
- Mixing normal with non-normal distributions (e.g., Cauchy) directly tests OLS in the presence of outliers and thus helps identify Breakdown Points under 
Non-Normality (Mixture of Non-Normals). Since OLS is notably sensitive to outliers because it minimizes the squared residuals, this aspect of the experiment 
helps quantify the threshold at which non-normality causes OLS to become less efficient or unreliable compared to other techniques. 
- Distributional shift occurs when the training data ("source") differs from the data being analyzed or predicted ("target"). The distinct experimental cells 
tests if OLS results learned under one condition hold when applied to a new condition. The results can guide researchers on whether to re-weight data or use 
a different model structure when data characteristics change. 
- This experiment creats a benchmark for when OLS works and when it fails. This provides a clear "before-and-after" comparison for identifying where OLS is 
insufficient and assists in validating whether sophisticated methods are necessary or if OLS is sufficient despite the violations. 

In summary, this experiment provides vital evidence for when OLS is reliable in heterogeneous, real-world data environments, and when (and which) alternative 
methods should be adopted in cases where OLS fails.

## Experiment Design
- The design variable X is generated as a uniform random variate between 0 and 100: X ~ U(0,100)
- The response variable Y is generated as Y = alpha + beta*X + e (for alpha = 5, beta = 2)
- For simplicity, the experiment is carried out in phases:
	- **Phase 1:** The sample size and the level of contaminations is fixed; this helps to measure simple effects of contaminations on OLS model
	- **Phase 2:** The sample size is fixed and the level of contaminations is varied; this helps measure the extent to which OLS can withstand contaminations
	- **Phase 3:** Phase 2 is extended as a comparative study of OLS and Least Trimmed Squares (%LTS) for different levels of trimming to study the effects of
	trimming on LTS.
	- **Phase 4:** The sample size and the level of contaminations are varied; This investigates the effects of sample size on OLS robustness under varying 
	contaminations conditions.
	- **Phase 5:** The sample size is varied and the errors are shifted from normal to:
		- student-t(v=10)
		- Uniform(0,100)
		- Geometric(p=0.2)
		- Exponention(p=5)
		- Cauchy(5,10)
	- **Phase 6:** Phase 5 is extended as a comparative study of OLS, LTS, Least Absolute Deviations (LAD), Theils, Weighted Theils (wTheils).
	- **Phase 7:** Phase 6 is extended as a comparative study of OLS, LTS, Theils and Bayesian regression.
	#### Note:
		- Phase 5 introduces the concept of distribution shifts to the experiment by studying the behaviour and sensitivity of OLS as the error distribution 
		shifts from normal to non-normal.
		- Phase 6 and 7 extends the experiment as a comparative study of non-parametric and parametric regression models under distribution shifts.

- For phase 1 to 4, the error terms are generated as:
	- standard normal: N(0,1)
	- outliers: N(0,1) mixed with outliers
	- mixture_u: N(0,1) mixed with Normal N(10,1) i.e. Normal variates with shifted mean and same variance
	- mixture_k: N(0,1) mixed with N(0,10) i.e. Normal variates with same mean and shifted variance
	- mixture_ku: N(0,1) mixed with N(10,10) i.e. Normal variates with both mean and variance shifted
	- contaminated_g: N(0,1) mixed with G(p=0.2) Geometric variate
	- contaminated_t: N(0,1) mixed with T(v=10)  Student-t variate
	- contaminated_u: N(0,1) mixed with U(0,1)   Uniform variate
	- contaminated_e: N(0,1) mixed with E(p=5)   Exponential variate
	- contaminated_c: N(0,1) mixed with C(a,b)   Standard Cauchy variate
	The experiment is divided into two cells:
		- Mixtures cell: contains standard normal, outliers, mixture_u, mixture_k and mixture_ku
		- Contaminations cell: contains contaminated_c, contaminated_e, contaminated_g, contaminated_t, contaminated_u
	#### Note:
		- X is a uniform r.v, thus contaminating the error term with U(0,1) is only used as a control for the contaminations cell of the experiment.
		- Outliers were generated as uniform random variates that are between -2 and 1.5-iqr below lower quartile or 1.5-iqr above upper quartile and 2.
		- The IQR is calculated for the standard normal errors.
		
## Evaluation
Model performance is assessed by:
- Bias
- Variance
- Mean Squared Error (MSE)
- Relative Root Mean Squared Error (RMSE - relative to benchmark)

## Summary of Findings
**Phase 1:**
Under 10% contamination and small sample size (n=35):
- Mixture contamination produces severe departures from Gaussian assumptions, leading to persistent distortions in OLS residuals.
- Contamination models produce milder deviations, with OLS residuals remaining approximately symmetric and unimodal.
- The experiment demonstrates that the structural form of contamination matters as much as the contamination level itself.
This highlights the need for robust statistical frameworks when modelling data subject to distributional shift or adversarial contamination.

**Phase 2:**
As contamination intensifies, the divergence from the Gaussian assumption becomes substantial, underscoring the need for robust statistical methodologies and 
distribution-aware decision frameworks. 
The combined results (pre- and post-estimation) establishes that:
1. OLS does not neutralize contamination, it redistributes it - an empirical fact: 
2. Residual distributions belong to expanded Wasserstein ambiguity sets - a theoretical implication
3. Residual KDEs can serve as data-driven estimators of distributional uncertainty for DRO calibration - a methodological insight

Overall, This phase of the experiment shows that under contamination, OLS residuals do not converge to the nominal distribution but instead exhibit 
heavy-tailed and skewed structures consistent with Wasserstein perturbations. This provides empirical justification for replacing classical estimation with 
distributionally robust formulations in small-sample, contamination-prone environments.