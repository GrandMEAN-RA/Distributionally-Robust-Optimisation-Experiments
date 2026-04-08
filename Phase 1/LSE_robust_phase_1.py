
#Import necessary libraries
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
from estimators import OLS

#Set file paths for saving results
BASE_PATH =  Path(__file__).resolve().parent
results_file_path = BASE_PATH / "simulation results"
results_file_path.mkdir(exist_ok=True)
plots_file_path = BASE_PATH / "plots"
plots_file_path.mkdir(exist_ok=True)

# Set random seed for reproducibility                       
np.random.seed(42)
random.seed(42)

# Define simulation parameters and initialize residuals dictionary
ssize = 35
pct_outliers = [0.1]
res_plots_met_mix = []
res_plots_met_cont = []
res_plots_par_mix = []
res_plots_par_cont = []

results = pd.DataFrame()

#Generate random normal errors
stn_errors = np.random.normal(0, 1, ssize) #standard normal N(0,1) distribution

#Generate design variable X
X = np.random.uniform(0, 100, ssize)

#Generate response variable Y
Y_st = 5 + 2 * X + stn_errors 
data = pd.DataFrame({'X': X, 'Y_st': Y_st})

#Loop over different levels of contamination and generate datasets, fit OLS, compute residuals and evaluation metrics, and visualize results
for pct in pct_outliers:
    n_outliers = int(ssize * pct)
    residual = {}

    mixn_errors_k = np.random.normal(0, 10, n_outliers) #N(0,10)
    mixn_errors_u = np.random.normal(10, 1, n_outliers) #N(5,1)
    mixn_errors_ku = np.random.normal(10, 10, n_outliers) #N(5,10)
    mixtures_k = stn_errors.copy()
    mixtures_k[-n_outliers:] = mixn_errors_k
    mixtures_u = stn_errors.copy()
    mixtures_u[-n_outliers:] = mixn_errors_u
    mixtures_ku = stn_errors.copy()
    mixtures_ku[-n_outliers:] = mixn_errors_ku

    rands = np.random.default_rng(seed=42)
    samples_g = rands.geometric(0.2, size=n_outliers)
    contaminations_g = stn_errors.copy()
    contaminations_g[-n_outliers:] = samples_g
    samples_t = rands.standard_t(10, size=n_outliers)
    contaminations_t = stn_errors.copy()
    contaminations_t[-n_outliers:] = samples_t
    samples_u = np.random.uniform(0, 1, size=n_outliers)
    contaminations_u = stn_errors.copy()
    contaminations_u[-n_outliers:] = samples_u
    samples_e = np.random.exponential(5, size=n_outliers)
    contaminations_e = stn_errors.copy()
    contaminations_e[-n_outliers:] = samples_e
    samples_c = rands.standard_cauchy(size=n_outliers) 
    contaminations_c = stn_errors.copy()
    contaminations_c[-n_outliers:] = samples_c

    #Generate outliers
    iqr = np.percentile(stn_errors, 75) - np.percentile(stn_errors, 25)
    lower_bound = np.percentile(stn_errors, 25) - 1.5 * iqr
    upper_bound = np.percentile(stn_errors, 75) + 1.5 * iqr

    lows = np.random.uniform(-2, lower_bound, int(n_outliers/2))
    highs = np.random.uniform(upper_bound, 2, int(n_outliers/2) if n_outliers % 2 == 0 else int(n_outliers/2)+1)
    extreme_val = np.concatenate((lows, highs))

    outliers = stn_errors.copy()
    outliers[-n_outliers:] = extreme_val

    #Visualize error models
    errors_mix = {'Standard Normal':stn_errors,'10% outliers':outliers,'10% Mixture_k':mixtures_k,'10% Mixture_u':mixtures_u,'10% Mixture_ku':mixtures_ku}
    errors_cont = {'Standard Normal':stn_errors,'10% Contaminated_g':contaminations_g,'10% Contaminated_t':contaminations_t,'10% Contaminated_u':contaminations_u,'10% Contaminated_e':contaminations_e,'10% Contaminated_c':contaminations_c}
    models_mix = pd.DataFrame(errors_mix)
    models_cont = pd.DataFrame(errors_cont)

    color_mix= ['red', 'blue', 'green', 'black', 'purple']
    color_map_mix = dict(zip(models_mix.columns, color_mix))
    color_cont = ['red', 'blue', 'green', 'black', 'purple', 'brown']
    color_map_cont = dict(zip(models_cont.columns, color_cont))

    fig, ax1 = plt.subplots(1,2, figsize=(12, 4))
    for k,c in color_map_mix.items():
        linestyle='--' if k == 'Standard Normal' else '-'
        linewidth=2 if k == 'Standard Normal' else 1
        sns.kdeplot(models_mix[k], ax=ax1[0], linestyle=linestyle, linewidth=linewidth, color=c)
    for k,c in color_map_cont.items():
        linestyle='--' if k == 'Standard Normal' else '-'
        linewidth=2 if k == 'Standard Normal' else 1
        sns.kdeplot(models_cont[k], ax=ax1[1], linestyle=linestyle, linewidth=linewidth,color=c)
    ax1[0].set_title(f'Mixture Models')
    ax1[1].set_title(f'Contamination Models')
    ax1[0].legend(models_mix.columns)
    ax1[1].legend(models_cont.columns)
    fig.suptitle(f'Error Distributions - {pct * 100:.1f}% Contaminations Sample Size ={ssize}') 
    fig.tight_layout()
    fig.savefig(f'{plots_file_path}/LSE_kde_{pct * 100:.1f}% Contaminations Sample Size ={ssize}.png')
    plt.show()

    data['Y_mix_k'] = 5 + 2 * X + mixtures_k
    data['Y_mix_u'] = 5 + 2 * X + mixtures_u
    data['Y_mix_ku'] = 5 + 2 * X + mixtures_ku

    data['Y_cont_g'] = 5 + 2 * X + contaminations_g
    data['Y_cont_t'] = 5 + 2 * X + contaminations_t
    data['Y_cont_u'] = 5 + 2 * X + contaminations_u
    data['Y_cont_e'] = 5 + 2 * X + contaminations_e
    data['Y_cont_c'] = 5 + 2 * X + contaminations_c

    data['Y_out'] = 5 + 2 * X + outliers

    #Visualize dataset
    res_vars_mix = ['Y_st','Y_mix_k','Y_mix_u','Y_mix_ku']
    res_vars_cont = ['Y_cont_g','Y_cont_t','Y_cont_u','Y_cont_e','Y_cont_c','Y_out']

    fig, ax2 = plt.subplots(1,2, figsize=(12, 4))
    for col in res_vars_mix:
        sns.scatterplot(x='X',y=col,data=data, ax=ax2[0])
    for col in res_vars_cont:
        sns.scatterplot(x='X',y=col,data=data, ax=ax2[1])
    ax2[0].set_title(f'Mixture Models')
    ax2[1].set_title(f'Contamination Models')
    ax2[0].legend(res_vars_mix)
    ax2[1].legend(res_vars_cont)
    fig.suptitle(f'Scatter Plots - {pct * 100:.1f}% Contaminations Sample Size ={ssize}')
    fig.tight_layout()
    fig.savefig(f'{plots_file_path}/LSE_robust_datasets_{pct * 100:.1f}% Contaminations Sample Size ={ssize}.png')
    plt.show()

    #Fit OLS SLM
    alpha_stm, beta_stm = OLS(data, model='standard')
    print(f"OLS estimates for the standard model: alpha = {alpha_stm}, beta = {beta_stm}")

    alpha_out, beta_out = OLS(data, model='outliers')
    print(f"OLS estimates for the outliers model: alpha = {alpha_out}, beta = {beta_out}")

    alpha_mix_k, beta_mix_k = OLS(data, model='mixtures_k')
    print(f"OLS estimates for the mixtures model: alpha = {alpha_mix_k}, beta = {beta_mix_k}")

    alpha_mix_u, beta_mix_u = OLS(data, model='mixtures_u')
    print(f"OLS estimates for the mixtures model: alpha = {alpha_mix_u}, beta = {beta_mix_u}")

    alpha_mix_ku, beta_mix_ku = OLS(data, model='mixtures_ku')
    print(f"OLS estimates for the mixtures model: alpha = {alpha_mix_ku}, beta = {beta_mix_ku}")

    alpha_cont_g, beta_cont_g = OLS(data, model='contaminations_g')
    print(f"OLS estimates for the contaminations model: alpha = {alpha_cont_g}, beta = {beta_cont_g}")

    alpha_cont_t, beta_cont_t = OLS(data, model='contaminations_t')
    print(f"OLS estimates for the contaminations model: alpha = {alpha_cont_t}, beta = {beta_cont_t}")

    alpha_cont_u, beta_cont_u = OLS(data, model='contaminations_u')
    print(f"OLS estimates for the contaminations model: alpha = {alpha_cont_u}, beta = {beta_cont_u}")

    alpha_cont_e, beta_cont_e = OLS(data, model='contaminations_e')
    print(f"OLS estimates for the contaminations model: alpha = {alpha_cont_e}, beta = {beta_cont_e}")

    alpha_cont_c, beta_cont_c = OLS(data, model='contaminations_c')
    print(f"OLS estimates for the contaminations model: alpha = {alpha_cont_c}, beta = {beta_cont_c}")

    #Compute residuals
    residual['Y'] = Y_st
    residual['Y_st_res'] = data['Y_st'] - (alpha_stm + beta_stm * data['X'])
    residual['Y_out_res'] = data['Y_out'] - (alpha_out + beta_out * data['X'])
    residual['Y_mix_k_res'] = data['Y_mix_k'] - (alpha_mix_k + beta_mix_k * data['X'])
    residual['Y_mix_u_res'] = data['Y_mix_u'] - (alpha_mix_u + beta_mix_u * data['X'])
    residual['Y_mix_ku_res'] = data['Y_mix_ku'] - (alpha_mix_ku + beta_mix_ku * data['X'])
    residual['Y_cont_g_res'] = data['Y_cont_g'] - (alpha_cont_g + beta_cont_g * data['X'])
    residual['Y_cont_t_res'] = data['Y_cont_t'] - (alpha_cont_t + beta_cont_t * data['X'])
    residual['Y_cont_u_res'] = data['Y_cont_u'] - (alpha_cont_u + beta_cont_u * data['X'])
    residual['Y_cont_e_res'] = data['Y_cont_e'] - (alpha_cont_e + beta_cont_e * data['X'])
    residual['Y_cont_c_res'] = data['Y_cont_c'] - (alpha_cont_c + beta_cont_c * data['X'])

    #Plot residuals
    res_vars_mix = ['Y_st_res','Y_out_res','Y_mix_k_res','Y_mix_u_res','Y_mix_ku_res']
    res_vars_cont = ['Y_st_res','Y_cont_g_res','Y_cont_t_res','Y_cont_u_res','Y_cont_e_res','Y_cont_c_res']

    color_mix= ['red', 'blue', 'green', 'black', 'purple']
    color_map_mix = dict(zip(res_vars_mix, color_mix))
    color_cont = ['red', 'blue', 'green', 'black', 'purple', 'brown']
    color_map_cont = dict(zip(res_vars_cont, color_cont))

    fig, ax5 = plt.subplots(1,2, figsize=(12, 4))
    for k,c in color_map_mix.items():
        linestyle='--' if k == 'Standard Normal' else '-'
        linewidth=2 if k == 'Standard Normal' else 1
        sns.kdeplot(residual[k], ax=ax5[0], linestyle=linestyle, linewidth=linewidth, color=c)
    for k,c in color_map_cont.items():
        linestyle='--' if k == 'Standard Normal' else '-'
        linewidth=2 if k == 'Standard Normal' else 1
        sns.kdeplot(residual[k], ax=ax5[1], linestyle=linestyle, linewidth=linewidth, color=c)
    ax5[0].set_title(f'Mixture Models')
    ax5[1].set_title(f'Contamination Models')
    ax5[0].legend(models_mix.columns)
    ax5[1].legend(models_cont.columns)
    fig.suptitle(f'Residuals KDE Plots - {pct * 100:.1f}% Contaminations Sample Size ={ssize}')
    fig.tight_layout()
    fig.savefig(f'{plots_file_path}/LSE_Residuals_kdeplot{pct * 100:.1f}% Contaminations Sample Size ={ssize}.png')
    plt.show()

    fig, ax3 = plt.subplots(1,2, figsize=(12, 4))
    for col in res_vars_mix:
        sns.scatterplot(x='Y_st_res',y=col,data=residual, ax=ax3[0])
    for col in res_vars_cont:
        sns.scatterplot(x='Y_st_res',y=col,data=residual, ax=ax3[1])
    ax3[0].set_title(f'Mixture Models - {pct * 100:.1f}% Contaminations Sample Size ={ssize}')
    ax3[1].set_title(f'Contamination Models - {pct * 100:.1f}% Contaminations Sample Size ={ssize}')
    ax3[0].set_xlabel('Standard Model Residuals')
    ax3[1].set_xlabel('Standard Model Residuals')
    ax3[0].set_ylabel('Model Residuals')
    ax3[1].set_ylabel('Model Residuals')    
    ax3[0].legend(res_vars_mix)
    ax3[1].legend(res_vars_cont)
    fig.suptitle(f'Residuals Scatter Plots - {pct * 100:.1f}% Contaminations Sample Size ={ssize}')
    fig.tight_layout()
    fig.savefig(f'{plots_file_path}/LSE_Residuals_scatterplot{pct * 100:.1f}% Contaminations Sample Size ={ssize}.png')
    plt.show()

    #Compute Evaluation metrics
    bias_stm = np.mean(residual['Y_st_res'])
    bias_out = np.mean(residual['Y_out_res'])
    bias_mix_k = np.mean(residual['Y_mix_k_res'])
    bias_mix_u = np.mean(residual['Y_mix_u_res'])
    bias_mix_ku = np.mean(residual['Y_mix_ku_res'])
    bias_cont_g = np.mean(residual['Y_cont_g_res'])
    bias_cont_t = np.mean(residual['Y_cont_t_res'])
    bias_cont_u = np.mean(residual['Y_cont_u_res'])
    bias_cont_e = np.mean(residual['Y_cont_e_res'])
    bias_cont_c = np.mean(residual['Y_cont_c_res'])

    var_stm = np.mean(residual['Y_st_res']**2)
    var_out = np.mean(residual['Y_out_res']**2)
    var_mix_k = np.mean(residual['Y_mix_k_res']**2)
    var_mix_u = np.mean(residual['Y_mix_u_res']**2)
    var_mix_ku = np.mean(residual['Y_mix_ku_res']**2)
    var_cont_g = np.mean(residual['Y_cont_g_res']**2)
    var_cont_t = np.mean(residual['Y_cont_t_res']**2)
    var_cont_u = np.mean(residual['Y_cont_u_res']**2)
    var_cont_e = np.mean(residual['Y_cont_e_res']**2)
    var_cont_c = np.mean(residual['Y_cont_c_res']**2)

    mse_stm = bias_stm**2 + var_stm
    mse_out = bias_out**2 + var_out
    mse_mix_k = bias_mix_k**2 + var_mix_k
    mse_mix_u = bias_mix_u**2 + var_mix_u
    mse_mix_ku = bias_mix_ku**2 + var_mix_ku
    mse_cont_g = bias_cont_g**2 + var_cont_g
    mse_cont_t = bias_cont_t**2 + var_cont_t
    mse_cont_u = bias_cont_u**2 + var_cont_u
    mse_cont_e = bias_cont_e**2 + var_cont_e
    mse_cont_c = bias_cont_c**2 + var_cont_c

    rmse_stm = 0
    rmse_out = (mse_stm - mse_out)/mse_stm * 100
    rmse_mix_k = (mse_stm - mse_mix_k)/mse_stm * 100
    rmse_mix_u = (mse_stm - mse_mix_u)/mse_stm * 100
    rmse_mix_ku = (mse_stm - mse_mix_ku)/mse_stm * 100
    rmse_cont_g = (mse_stm - mse_cont_g)/mse_stm * 100
    rmse_cont_t = (mse_stm - mse_cont_t)/mse_stm * 100
    rmse_cont_u = (mse_stm - mse_cont_u)/mse_stm * 100
    rmse_cont_e = (mse_stm - mse_cont_e)/mse_stm * 100
    rmse_cont_c = (mse_stm - mse_cont_c)/mse_stm * 100

    #Print results dataframe
    labels = ['models', 'alpha', 'beta', 'bias', 'variance', 'MSE','RMSE (%)','contamination level','sample Size']
    stm = ['Standard', alpha_stm, beta_stm, bias_stm, var_stm, mse_stm, rmse_stm,f'{pct * 100:.1f}%', ssize]
    out = ['Outliers', alpha_out, beta_out, bias_out, var_out, mse_out, rmse_out,f'{pct * 100:.1f}%', ssize]
    mix_k = ['Mixtures_K', alpha_mix_k, beta_mix_k, bias_mix_k, var_mix_k, mse_mix_k, rmse_mix_k,f'{pct * 100:.1f}%', ssize]
    mix_u = ['Mixtures_U', alpha_mix_u, beta_mix_u, bias_mix_u, var_mix_u, mse_mix_u, rmse_mix_u,f'{pct * 100:.1f}%', ssize]
    mix_ku = ['Mixtures_KU', alpha_mix_ku, beta_mix_ku, bias_mix_ku, var_mix_ku, mse_mix_ku, rmse_mix_ku,f'{pct * 100:.1f}%', ssize]
    cont_g = ['Contaminations_G', alpha_cont_g, beta_cont_g, bias_cont_g, var_cont_g, mse_cont_g, rmse_cont_g,f'{pct * 100:.1f}%', ssize]
    cont_t = ['Contaminations_T', alpha_cont_t, beta_cont_t, bias_cont_t, var_cont_t, mse_cont_t, rmse_cont_t,f'{pct * 100:.1f}%', ssize]
    cont_u = ['Contaminations_U', alpha_cont_u, beta_cont_u, bias_cont_u, var_cont_u, mse_cont_u, rmse_cont_u,f'{pct * 100:.1f}%', ssize]
    cont_e = ['Contaminations_E', alpha_cont_e, beta_cont_e, bias_cont_e, var_cont_e, mse_cont_e, rmse_cont_e,f'{pct * 100:.1f}%', ssize]
    cont_c = ['Contaminations_C', alpha_cont_c, beta_cont_c, bias_cont_c, var_cont_c, mse_cont_c, rmse_cont_c,f'{pct * 100:.1f}%', ssize]

    c_results = pd.DataFrame([stm, out, mix_k, mix_u, mix_ku, cont_g, cont_t, cont_u, cont_e, cont_c], columns=labels)
    print(f'{pct * 100:.1f}% Contaminations: \n\n',c_results)
    results = pd.concat([results, c_results], axis=0, ignore_index=True)
    results.sort_values(by=['RMSE (%)'], ascending=False, inplace=True)
    print(results.head())

    #Create a dataframe for plotting bias and RMSE
    res_plot_met = results[['models','bias','RMSE (%)','contamination level','sample Size']]
    res_plot_par = results[['models','alpha','beta','contamination level','sample Size']]

    res_plot_met_mix = res_plot_met[(res_plot_met['models'] == 'Mixtures_K') | (res_plot_met['models'] == 'Mixtures_U') | (res_plot_met['models'] == 'Mixtures_KU') | (res_plot_met['models'] == 'Outliers') | (res_plot_met['models'] == 'Standard')]
    res_plot_met_cont = res_plot_met[res_plot_met['models'].str.contains('Contaminations') | (res_plot_met['models'] == 'Standard')]

    res_plot_par_mix = res_plot_par[(res_plot_par['models'] == 'Mixtures_K') | (res_plot_par['models'] == 'Mixtures_U') | (res_plot_par['models'] == 'Mixtures_KU') | (res_plot_par['models'] == 'Outliers') | (res_plot_par['models'] == 'Standard')]
    res_plot_par_cont = res_plot_par[res_plot_par['models'].str.contains('Contaminations') | (res_plot_met['models'] == 'Standard')]

#Safe results to file as a csv
results.to_csv(f'{results_file_path}/simulation results.csv', index=False)

model_class_par = [res_plot_par_mix, res_plot_par_cont]
model_class_met = [res_plot_met_mix, res_plot_met_cont]

#Visualize Bias
fig, ax4 = plt.subplots(1,len(model_class_met), figsize=(12, 4)) 
for i, mod in enumerate(model_class_met):
    t_mod = 'Mixtures' if i == 0 else 'Contaminations'
    sns.pointplot(x="contamination level", y="bias", data=mod, hue='models', ax=ax4[i])
    ax4[i].set_title(f'Bias for {pct*100}% {t_mod}- Sample size: {ssize}')
plt.tight_layout()
fig.savefig(f'{plots_file_path}/LSE_Bias_{pct * 100:.1f}% Sample Size ={ssize}.png')
plt.show()

#Visualize RMSE
fig, ax4 = plt.subplots(1,len(model_class_met), figsize=(12, 4)) 
for i, mod in enumerate(model_class_met):
    t_mod = 'Mixtures' if i == 0 else 'Contaminations'
    sns.pointplot(x="contamination level", y="RMSE (%)", data=mod, hue='models', ax=ax4[i])
    ax4[i].set_title(f'RMSE for {pct*100}% {t_mod}- Sample size: {ssize}')
plt.tight_layout()
fig.savefig(f'{plots_file_path}/LSE_RMSE_{pct * 100:.1f}% Sample Size ={ssize}.png')
plt.show()
