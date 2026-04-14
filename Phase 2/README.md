# Distributionally Robust Optimisation Simulation Experiments - Phase 2
This phase of the experiment investigates the **robustness** of Ordinary Least Square regression for the simple linear case under varying heteroscedastic 
conditions and levels of contaminations.

## Backgrounds to the Experiment
This phase is built on phase 1 to examine the combined effects of heteroscedasticity and levels of contaminatins in a dataset on OLS regression 

## Experiment Design
- The same experimental seup in phase 1.
- The sample size is fixed at 35 and the level of contaminations is varied at 5%, 10%, 20%, 30% and 50%.
	
## Results Summary: KDE Analysis of Error Distributions and OLS Residuals
- Contamination Level: 5%, 10%, 20%, 30%, 50%. Only 5%, 20% and 50% are reported.
- Sample Size: (n = 35)

### 1. Error Distribution Characteristics (Data Generating Process)
![error models distribution]("C:\Users\User\Desktop\Mr Ope\GrandMEAN_Portfolio\Research\DRO Simulations\Phase 1\plots\LSE_kde_10.0% Contaminations Sample Size =35.png" "Distribution Plot of error model")
The KDE plots of the simulated errors reveal substantial departures from normality when mixture contamination is introduced
	
#### 1.1 Low Contamination Regime (5%)
At 5% contamination, the KDE curves for most models remain close to the standard normal benchmark.

##### Mixture models
Key observations include:
•	Mixture_k and mixture_u introduce mild tail thickening, but the central mass remains approximately normal.
•	Mixture_ku exhibits slightly wider dispersion, suggesting that combined kurtosis–uniform mixtures introduce early-stage heavy-tailedness.
•	The outlier model displays isolated tail deviations but maintains a central peak comparable to the normal reference.

##### Contamination models
The contamination-based models display closer adherence to the normal reference, particularly:
•	Contaminated_t and contaminated_c, which maintain strong central concentration.
•	Contaminated_g, which introduces mild right-skewness due to asymmetric contamination.

Overall, under low contamination, mixture models preserve the location and general shape of the base distribution while modestly inflating tail probabilities.
At this level, contamination produces localized perturbations rather than structural changes in the distribution.

#### 1.2. Moderate Contamination Regime (20%)
When contamination rises to 20%, the distortion becomes structurally visible.

##### Mixture models
Several phenomena emerge:
- Central peak attenuation — density near zero declines relative to the normal reference.
- Variance inflation — the distributions widen significantly.
- Emergence of heavy tails.
	Particularly:
	- Mixture_u shows a secondary density region, indicating the presence of distinct outlier clusters.
	- Mixture_ku generates a strongly right-skewed heavy-tailed distribution, suggesting sensitivity to extreme values.

##### Contamination models
Compared to mixture models, contamination models remain more centralized. However:
- Contaminated_g exhibits strong right-tail extension.
- Contaminated_e begins to display variance expansion with a flatter peak.
- Contaminated_u retains sharp central concentration but shows occasional extreme realizations.

These results indicate that mixture models translate moderate contamination into substantial dispersion effects, which can severely bias classical estimators 
such as OLS. Contamination mechanisms, on the other hand, affect tail behavior more than central density, producing asymmetric uncertainty.
		
#### 1.3. High Contamination Regime (50%)
At 50% contamination, the distributions diverge dramatically from the standard normal baseline.

##### Mixture models
The mixture models display the most severe distortions:
- Extremely heavy tails
- Strong skewness
- Multimodal behavior in some cases
	Specifically:	
	- Mixture_u produces large right-side mass far from the center, indicating extreme outlier propagation.
	- Mixture_ku exhibits the widest dispersion, implying substantial kurtosis inflation.
	- The central peak becomes significantly flattened, indicating that variance is dominated by contaminating observations.

##### Contamination models
Interestingly, the contamination models show greater structural stability than mixture models.
Key patterns include:
- A sharp central spike (especially in contaminated_u).
- Moderate tail expansion rather than explosive dispersion.
- Some extreme outliers appearing far from the center, particularly in contaminated_e.

This regime effectively represents distributional breakdown, where the original normal structure is no longer identifiable. This suggests that non-normal 
contaminations preserve the core generating distribution, even when a large fraction of observations are perturbed.

### 2. Residual Distribution After OLS Estimation
![error models distribution]("C:\Users\User\Desktop\Mr Ope\GrandMEAN_Portfolio\Research\DRO Simulations\Phase 1\plots\LSE_Residuals_kdeplot10.0% 
Contaminations Sample Size =35.png" "Distribution Plot of error model")
Under correct model specification and classical assumptions, OLS residuals should approximate: ê_i ~ N(0,var). Thus, deviations in the KDE of residuals from 
normality directly indicate:
- model misspecification
- presence of contamination
- failure of OLS robustness

#### 2.1 Low Contamination (5%) 
Near-Recovery with Early Instability

##### Mixture Models
- Residuals remain centered around zero, indicating unbiased estimation.
- However, compared to the original error distributions, we observe:
	- slight tail persistence
	- minor asymmetry (especially in mixture_u and mixture_ku)

##### Contamination Models
- Residual KDEs align closely with the Gaussian benchmark.
- The main deviation appears in:
	- Contaminated_g, which shows mild right-skew
	- slight variance inflation

At 5% contamination, OLS partially absorbs contamination into parameter estimates but cannot fully eliminate tail effects:
- OLS behaves approximately efficiently
- Residuals are nearly Gaussian
- Contamination impact is subcritical

#### 2.2. Moderate Contamination (20%)
Breakdown of Gaussian Residual Structure

##### Mixture Models
Clear deviations emerge:
- Flattened central peak
- significant spread
- emergence of skewness
	Notably:
	- Mixture_u produces visible secondary density regions
	- Mixture_ku shows extended right tails

##### Contamination Models
- Central peak remains sharper than mixture models
- However:
	- variance increases substantially
	- heavy tails emerge
	- skewness becomes visible

**Critical Insight:** 
- OLS fails to correctly separate signal from contamination, embedding outliers into residual structure, even under mild mixtures.
- Even though contamination models preserve a nominal core, OLS residuals reflect:
	- leakage of contamination into estimation error
	- loss of Gaussianity

#### 2.3. Severe Contamination (50%)
Complete Residual Distortion

##### Mixture Models
Residuals exhibit:
- extreme dispersion
- pronounced skewness
- loss of unimodality in some cases

##### Contamination Models
A striking phenomenon appears:
- Sharp central spike (especially contaminated_u)
- long extreme tails
- occasional mass far from zero

With severe contaminations:
- the Gaussian benchmark is no longer a meaningful reference - a textbook case of OLS breakdown under high contamination.
- The contamination case now reflects a dual structure:
	- a retained nominal component
	- a dominant contamination influence

### 3. Comparative Structural Insights
Across all contamination levels, several consistent patterns emerge:
1. Mixture models amplify tail risk
	Mixture structures tend to spread probability mass across extreme values, producing:
	- heavier tails
	- skewness
	- potential multimodality
	This makes them a useful framework for studying catastrophic distribution shifts.
2. Contamination models preserve the core distribution
	Contamination frameworks retain a dominant central mode, even when contamination increases. This implies:
	- robustness of the core distribution
	- outliers appearing as additive disturbances rather than structural shifts.
3. Small-sample amplification
	With n = 35, contamination effects are magnified due to sampling variability. Even moderate contamination levels significantly distort the empirical 
	density.
4. Residuals as a Distorted Pushforward
	Let the true error distribution be (P_ê). The OLS estimator induces a transformation: ê = Y - (alpha + beta*X).
	
	Under contamination:
	- beta is biased toward contaminated observations
	- residuals become a pushforward distribution of P_ê under a biased projection.
	Thus, residuals are not “cleaned errors” — they are re-weighted contaminated distributions.
5. OLS is not a contraction mapping in Wasserstein space under contamination. Instead:
	- contamination → biased parameters → distorted residuals → larger ambiguity sets
	- The residual distributions can now be interpreted as: P_ê in { Q : W_p(Q, P_0) <= delta } where δ increases, not decreases, after estimation.
	- OLS does not project onto the nominal distribution. Instead, it often amplifies Wasserstein distance.

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

#### 3.2 Link to Influence Function and Breakdown Point
OLS has:
- unbounded influence function
- breakdown point = 0%
Implication:
- Even a small fraction of extreme contamination can distort estimates
- As contamination increases, distortion grows nonlinearly

The kde plots empirically validate this:
----------------------------------------------------------
| Contamination |	Residual Behavior|	Interpretation   |
----------------------------------------------------------
|            5%	|         Near normal|	 Stable regime   |
----------------------------------------------------------
|           20%	|        Heavy-tailed| Efficiency loss   |
----------------------------------------------------------
|           50%	|    Highly distorted|	     Breakdown   |
----------------------------------------------------------

	
**Overall:**
- Mixture contamination introduces structural distortions that OLS cannot adequately absorb.
- Contamination models mainly produce variance inflation, which OLS handles more effectively.

### 4. Implications for Statistical Modeling
These results highlight important consequences for estimation and decision systems.

#### Sensitivity of classical estimators
Estimators assuming Gaussian errors (e.g., OLS) will experience:
- variance inflation
- bias under skew contamination
- instability under mixture-generated outliers.

#### Motivation for robust frameworks
The observed distortions justify the use of:
- robust regression methods
- heavy-tailed likelihood models
- distributionally robust optimization (DRO) approaches.

### 5. Recommendations
1. Residual diagnostics are essential
KDE plots show that:
- checking residual normality is a direct test of robustness
- OLS residuals fail this test under moderate/severe contamination

### 6. Link to Distributionally Robust Optimisation
In particular, the heavy tails and skew patterns observed resemble ambiguity sets commonly modeled using Wasserstein or contamination-based DRO formulations.
Residual distributions provide an empirical way to:
- estimate Wasserstein radius ( \delta )
- characterize uncertainty sets
- design robust decision rules

### 7. Conclusion
The simulation demonstrates that even modest contamination levels can significantly distort empirical error distributions in small samples. 
While contamination models primarily affect tail behavior, mixture models produce more profound structural distortions, including heavy tails 
and skewness. 

As contamination intensifies, the divergence from the Gaussian assumption becomes substantial, underscoring the need for robust statistical 
methodologies and distribution-aware decision frameworks.

The results illustrate two distinct mechanisms of distribution shift:
1.	Mixture-induced shifts ( model misspecification): structural distribution changes, where the generating process itself becomes heterogeneous.
2.	Contamination-induced shifts (Huber ε-contamination neighborhoods): adversarial or stochastic perturbations of an otherwise stable distribution.

The combined results (pre- and post-estimation) establishes that:
1. OLS does not neutralize contamination, it redistributes it - an empirical fact: 
2. Residual distributions belong to expanded Wasserstein ambiguity sets - a theoretical implication
3. Residual KDEs can serve as data-driven estimators of distributional uncertainty for DRO calibration - a methodological insight

This experiment shows that under contamination, OLS residuals do not converge to the nominal distribution but instead exhibit heavy-tailed and skewed 
structures consistent with Wasserstein perturbations. This provides empirical justification for replacing classical estimation with distributionally robust 
formulations in small-sample, contamination-prone environments.

