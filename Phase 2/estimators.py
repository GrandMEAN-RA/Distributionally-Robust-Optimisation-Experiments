
from pyexpat import model

import pandas as pd

def OLS(data, model=None):

    data_ = data.copy()
    if model == 'standard' or model == None:
        data_['Y'] = data_['Y_st']
    elif model == 'outliers':
        data_['Y'] = data_['Y_out']
    elif model == 'mixtures_k':
        data_['Y'] = data_['Y_mix_k']
    elif model == 'mixtures_u':
        data_['Y'] = data_['Y_mix_u']
    elif model == 'mixtures_ku':
        data_['Y'] = data_['Y_mix_ku']
    elif model == 'contaminations_g':
        data_['Y'] = data_['Y_cont_g']
    elif model == 'contaminations_t':
        data_['Y'] = data_['Y_cont_t']
    elif model == 'contaminations_u':
        data_['Y'] = data_['Y_cont_u']
    elif model == 'contaminations_e':
        data_['Y'] = data_['Y_cont_e']
    elif model == 'contaminations_c':
        data_['Y'] = data_['Y_cont_c']

    data_['dev_x'] = data_['X'] - data_['X'].mean()
    data_['dev_x-squared'] = data_['dev_x']**2
    data_['dev_y'] = data_['Y'] - data_['Y'].mean()
    data_['dev_xy'] = data_['dev_x'] * data_['dev_y']

    beta_OLS = data_['dev_xy'].sum() / data_['dev_x-squared'].sum()
    alpha_OLS = data_['Y'].mean() - beta_OLS * data_['X'].mean()

    #print("==== OLS Estimation Completed ====")

    return alpha_OLS, beta_OLS


def LTS(data, trim_pct = None):

    data_ = data.copy()
    alpha_OLS, beta_OLS = OLS(data_)

    data_['residuals'] = data_['Y'] - (alpha_OLS + beta_OLS * data_['X'])
    data_['squared_residuals'] = data_['residuals']**2
    data_['abs_residuals'] = data_['residuals'].abs()

    data_sorted = data_.sort_values(by='squared_residuals', ascending=True)

    trim_level = int(0.2 * len(data_)) if trim_pct == None else int(trim_pct * len(data_))
    data_trimmed = data_sorted.iloc[:len(data) - trim_level]

    data_trimmed['dev_x'] = data_trimmed['X'] - data_trimmed['X'].mean()
    data_trimmed['dev_x-squared'] = data_trimmed['dev_x']**2
    data_trimmed['dev_y'] = data_trimmed['Y'] - data_trimmed['Y'].mean()
    data_trimmed['dev_xy'] = data_trimmed['dev_x'] * data_trimmed['dev_y']

    beta_LTS = data_trimmed['dev_xy'].sum() / data_trimmed['dev_x-squared'].sum()
    alpha_LTS = data_trimmed['Y'].mean() - beta_LTS * data_trimmed['X'].mean()

    print("==== LTS Estimation Completed ====")
    print(f'\nEstimated beta_LTS:\n', beta_LTS)
    print(f'\nEstimated alpha_LTS:\n', alpha_LTS)

    return alpha_LTS, beta_LTS

def LAD(data):

    data_ = data.copy()
    
    x_0 = data_['X'].median()
    y_0 = data_['Y'].median()

    x_p_0 = x_0
    y_p_0 = y_0

    n_inter = 0
    while True:
        n_inter += 1
        data_['delta_y'] = data_['Y'] - y_0
        data_['delta_x'] = data_['X'] - x_0
        data_['slope'] = (data_['delta_y'] / data_['delta_x']).fillna(0)
        data_['abs_delta_x'] = data_['delta_x'].abs()
        data_['cabs_delta_x'] = data_['abs_delta_x'].cumsum()

        T_stat = data_['abs_delta_x'].sum()
        T_dec = T_stat / 2

        data_sorted = data_.sort_values(by='slope', ascending=True)

        for t in data_sorted['cabs_delta_x']:
            if t <= T_dec:
                cond = data_sorted['cabs_delta_x'] == t
                prev_row_mask = cond.shift(1, fill_value=False)
                ind_rows_before = data_sorted.index[prev_row_mask].tolist()
                break

        rows_before = data_sorted.loc[ind_rows_before]

        x_1 = rows_before['X'].values[0]
        y_1 = rows_before['Y'].values[0]

        if x_1 == x_p_0 and y_1 == y_p_0:
            print('Convergence achieved.')
            print(f'x_p_0:\n', x_p_0, '\ny_p_0:\n', y_p_0, '\n\n',f'x_0:\n', x_0, '\ny_0:\n', y_0, '\n\n',f'x_1:\n', x_1, '\ny_1:\n', y_1, '\n\n',f'Number of iterations:\n', n_inter)
            break
        else:
            print(f"Iteration {n_inter} completed. Updating parameters...")
            x_p_0 = x_0
            y_p_0 = y_0 
            x_0 = x_1
            y_0 = y_1

    print("==== LAD Estimation Completed ====")
    beta_LAD = (y_1 - y_0) / (x_1 - x_0)
    print(f'\nEstimated slope:\n', beta_LAD)
    alpha_LAD = y_0 - beta_LAD * x_0
    print(f'\nEstimated y-intercept:\n', alpha_LAD)
    xy_LAD = pd.DataFrame({'X':[x_0, x_1], 'Y':[y_0, y_1]})
    return alpha_LAD, beta_LAD , xy_LAD

def THEIL(data):
    data_ = data.copy()

    data_size = len(data_)

    paired_x_dev = []
    paired_y_dev = []
    ind = []

    i=0
    for j in range(data_size):
        for k in range(j+1, data_size):
            dev_y = data_['Y'].iloc[k] - data_['Y'].iloc[j]
            dev_x = data_['X'].iloc[k] - data_['X'].iloc[j]
            paired_y_dev.append(dev_y)
            paired_x_dev.append(dev_x)
            ind.append(i)
            i += 1
            
    data_paired = pd.DataFrame({'dev_x' : dev_x, 'dev_y' : dev_y}, index = ind)

    data_paired['slope'] = data_paired['dev_y']/data_paired['dev_x']
    beta_THEIL = data_paired['slope'].median()
    alpha_THEIL = data_['Y'].median() - beta_THEIL * data_['X'].median()

    print("==== THEIL Estimation Completed ====")
    print(f'\nEstimated beta_THEIL:\n', beta_THEIL, '\n\n')
    print(f'\nEstimated alpha_THEIL:\n', alpha_THEIL, '\n\n')

    return alpha_THEIL, beta_THEIL, data_paired

def wTHEIL(data):
    data_ = data.copy()

    _, _, data_paired = THEIL(data_)

    data_paired['dev_x_abs'] = data_paired['dev_x'].abs()
    data_paired['weight'] = data_paired['dev_x_abs'] / data_paired['dev_x_abs'].sum()

    data_paired_sorted = data_paired.sort_values(by='slope', ascending=True)
    data_paired_sorted['cum_weight'] = data_paired_sorted['weight'].cumsum()

    for cw in data_paired_sorted['cum_weight']:
        if cw > 0.5:
            beta_wTHEIL = data_paired_sorted[data_paired_sorted['cum_weight'] == cw]['slope']

    alpha_wTHEIL = data_['Y'].median() - beta_wTHEIL * data_['X'].median()

    print("==== wTHEIL Estimation Completed ====")
    print(f'\nEstimated beta_wTHEIL:\n', beta_wTHEIL, '\n\n')
    print(f'\nEstimated alpha_wTHEIL:\n', alpha_wTHEIL, '\n\n')

    return alpha_wTHEIL, beta_wTHEIL

    