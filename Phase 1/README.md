# Distributionally Robust Optimisation Simulation Experiments - Phase 1
This phase of the experiment investigates the **robustness** of Ordinary Least Square regression for the simple linear case under varying Heteroscedastic 
conditions

## Backgrounds to the Experiment
One of the key assumptions of Ordinary Least Squares (OLS) regression is homoscedasticity (constant error variance). This means that The error terms have 
a constant variance (Var(e)=sigma-squared) across all levels of independent variables. The violated of this assumption can invalidates standard errors, 
making hypothesis tests unreliable.
This experiment examines the simple effects of Heteroscedasticity on OLS regression 

## Experiment Design
- For simplicity, the sample size is fixed at 35 and the level of contaminations is fixed at 10%.
- For this phase, the experiment is divided into two cells:
	- Mixtures cell: contains standard normal, outliers, mixture_u, mixture_k and mixture_ku
	- Contaminations cell: contains contaminated_c, contaminated_e, contaminated_g, contaminated_t, contaminated_u
	
## Results Summary: KDE Analysis of Error Distributions and OLS Residuals
- Contamination Level: 10%
- Sample Size: (n = 35)

### 1. Error Distribution Characteristics (Data Generating Process)
![error models distribution]("C:\Users\User\Desktop\Mr Ope\GrandMEAN_Portfolio\Research\DRO Simulations\Phase 1\plots\LSE_kde_10.0% Contaminations Sample Size =35.png" "Distribution Plot of error model")
The KDE plots of the simulated errors reveal substantial departures from normality when mixture contamination is introduced
	
#### 1.1 Mixture Models
Key observations
-	Standard Normal Benchmark
	- Highly concentrated around zero.
	- Symmetric and sharply peaked density.
- 10% Outliers
	- Retains central concentration but shows moderate tail inflation.
	- Slight widening of the density relative to the benchmark.
- 10% Mixture_k
	- Displays heavy tails with noticeable probability mass far from the center.
	- Evidence of left-tail contamination (extreme negative values).
- 10% Mixture_u
	- Exhibits clear multimodality, including a secondary density peak around large positive values.
	- Indicates structured contamination rather than random noise.
- 10% Mixture_ku
	- Combines both heavy tails and dispersion.
	- Shows extreme right-tail expansion, reaching values near 20.
		
Mixture models produce highly non-Gaussian error structures, characterized by:
- Tail inflation
- Secondary modes
- Extreme outliers
These features violate the classical OLS assumptions of normality and homoscedasticity.

#### 1.2 Contamination Models
Compared to mixture models, contamination models display more controlled deviations from normality.

Key observations:
- 10% Contaminated_g
	- Noticeable variance inflation with wider spread.
	- Retains unimodal structure but with heavier tails.
- 10% Contaminated_t
	- Very close to the normal distribution in the central region.
	- Slightly heavier tails due to the t-distribution component.
- 10% Contaminated_u
	- Displays extreme negative outliers (long left tail).
	- Central density remains sharp.
- 10% Contaminated_e
	- Shows moderate skewness and broader dispersion.
- 10% Contaminated_c
	- Produces strong left-tail contamination, with isolated extreme values.
		
Contamination models tend to generate:
- Unimodal but heavy-tailed distributions
- More localized deviations from Gaussian assumptions
- Less structural distortion than mixture models.

### 2. Residual Distribution After OLS Estimation
![error models distribution]("C:\Users\User\Desktop\Mr Ope\GrandMEAN_Portfolio\Research\DRO Simulations\Phase 1\plots\LSE_Residuals_kdeplot10.0% Contaminations Sample Size =35.png" "Distribution Plot of error model")

The second set of KDE plots shows the OLS residual distributions. This provides insight into how well OLS absorbs or propagates contamination.
#### 2.1 Residuals Under Mixture Models
		
Key observations
- Central Peak Reduction: Compared to the benchmark, most contaminated cases display:
- Lower central density
- Increased spread
This indicates variance inflation in residuals.
		
- Persistence of Extreme Values
	- Mixture_u retains a visible secondary density peak near large positive residuals.
	- Mixture_k preserves extreme negative residuals.
		
- Partial Absorption
	- OLS estimation partially compresses extreme tails, but does not eliminate them.
OLS is not robust to mixture contamination. Structural features of the error distribution persist in the residuals.

#### 2.2 Residuals Under Contamination Models
Residual KDEs show a different pattern.
Key features:
- Contaminated_t and Contaminated_u
	- Residual distributions remain very close to normal near the center.
	- Only mild tail deviations remain.
- Contaminated_g
	- Residuals display moderate dispersion but retain symmetry.
- Contaminated_e
	- Slight skewness remains visible.
- Contaminated_c
	- Extreme negative residuals persist but are attenuated relative to the original errors.
OLS shows greater resilience to contamination models than to mixture models.
This suggests that:
	- Isolated contamination is partially absorbed during estimation.
	- Structured mixture contamination propagates more strongly into residuals.

### 3. Comparative Insights
#### 3.1 Results Table
	
	| models           | alpha       | beta        | bias       | variance    | MSE         | RMSE (%)      | contamination level | sample Size |
	| ---------------- | ----------- | ----------- | ---------- | ----------- | ----------- | ------------- | ------------------- | ----------- |
	| Contaminations_U | 5.013674525 | 1.997949948 | \-1.10E-14 | 0.81917845  | 0.81917845  | 2.866764999   | 10.00%              | 35          |
	| Standard         | 4.890461556 | 1.999535296 | \-1.22E-14 | 0.84335547  | 0.84335547  | 0             | 10.00%              | 35          |
	| Contaminations_T | 5.022989032 | 1.997999285 | \-2.21E-14 | 0.843520528 | 0.843520528 | \-0.019571576 | 10.00%              | 35          |
	| Outliers         | 5.01587377  | 1.998255795 | \-3.46E-14 | 1.152773702 | 1.152773702 | \-36.68894594 | 10.00%              | 35          |
	| Contaminations_E | 5.511275519 | 1.997903839 | \-3.60E-14 | 4.137740081 | 4.137740081 | \-390.6282379 | 10.00%              | 35          |
	| Contaminations_C | 5.349148672 | 1.979807593 | \-2.69E-14 | 8.830357985 | 8.830357985 | \-947.0505383 | 10.00%              | 35          |
	| Mixtures_U       | 6.003204374 | 1.99487722  | \-8.53E-15 | 9.178256101 | 9.178256101 | \-988.3021965 | 10.00%              | 35          |
	| Contaminations_G | 6.180682027 | 1.992691588 | \-2.16E-14 | 10.45973379 | 10.45973379 | \-1140.252084 | 10.00%              | 35          |
	| Mixtures_K       | 2.907183472 | 2.030205072 | \-2.09E-14 | 13.75784122 | 13.75784122 | \-1531.321751 | 10.00%              | 35          |
	| Mixtures_KU      | 6.260470682 | 1.990702609 | \-1.20E-14 | 14.53721271 | 14.53721271 | \-1623.734918 | 10.00%              | 35          |

#### 3.2 Behaviorual Summary

	| Property	| Mixture Models | Contamination Models |
	 ----------   --------------  --------------------
	| Tail behavior	| Very heavy	| Moderate |
	 --------------  -------------   ----------
	| Multimodality	| Present	| Absent |
	 --------------  ----------- --------
	| Residual distortion |	Strong | Mild |
	 --------------------- -------- ------
	| OLS robustness |	Low	| Moderate|
	
**Overall:**
- Mixture contamination introduces structural distortions that OLS cannot adequately absorb.
- Contamination models mainly produce variance inflation, which OLS handles more effectively.

### 4. Key Experimental Implications
- Sensitivity of OLS
	OLS estimators are highly sensitive to mixture-based contamination, especially when it introduces secondary modes or extreme outliers.
- Residual Diagnostics
	Residual KDE plots provide a clear diagnostic signal for detecting contamination structures.
- Robust Estimation Motivation
	The results strongly motivate the use of:
	- Robust regression methods
	- Distributionally robust optimization frameworks
	- Heavy-tailed likelihood models
	These methods explicitly account for contamination effects that OLS cannot mitigate.

### 5. Conclusion
Under 10% contamination and small sample size (n=35):
- Mixture contamination produces severe departures from Gaussian assumptions, leading to persistent distortions in OLS residuals.
- Contamination models produce milder deviations, with OLS residuals remaining approximately symmetric and unimodal.
- The experiment demonstrates that the structural form of contamination matters as much as the contamination level itself.
This highlights the need for robust statistical frameworks when modelling data subject to distributional shift or adversarial contamination.

