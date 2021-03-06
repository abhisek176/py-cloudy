import numpy as np
import astropy.table as tab
from scipy.interpolate import interp2d


def get_true_model(model_path, Q= 18, true_nH = 1e-4,  logZ = -1, uvb = 'KS18'):
    """
    :param model: The data where Q18 model is stored
    :return: a row of ion column densities at n_H = 1e-4 cm^-2
    """
    model = model_path + '/try_{}_Q{}_Z{:.0f}.fits'.format(uvb, Q, (logZ+4)*100)
    data = tab.Table.read(model)
    true_ion_col = data [data['hden'] == true_nH]
   # print(true_ion_col)

    return true_ion_col

#----model interpolation
def get_interp_func(model_path, ions_to_use, Q_uvb, uvb = 'KS18'):
    logZ = np.around(np.arange(-3, 1, 0.05), decimals = 2) # hardcoded
    #get nH array
    logZ_try = -1
    model_try = model_path + '/try_{}_Q{}_Z{:.0f}.fits'.format(uvb, Q_uvb, (logZ_try+4)*100)
    model = tab.Table.read(model_try)
    lognH = np.log10(np.array(model['hden']))

    interpolation_function_list = []
    for ion in ions_to_use:
        z = np.zeros((len(lognH), len(logZ)))
        for i in range(len(logZ)):
            model = model_path + '/try_{}_Q{}_Z{:.0f}.fits'.format(uvb, Q_uvb, (logZ[i]+4)*100)
            d = tab.Table.read(model)
            d[ion][d[ion] == 0 ] = 1e-15 # for avoiding log10 (0) error
            z [:, i] = np.log10(d[ion]) #--- for log - log interpolation
        f = interp2d(lognH, logZ, z.T)
        interpolation_function_list.append(f)

    return interpolation_function_list




def get_LSF(model_path, Q_uvb, model_uvb, ions_to_use, true_Q, true_uvb):
    # run_mcmc(model_Q= model, ions_to_use= ions)
    # ------------------ here is a way to run code
    number_of_ions = len(ions_to_use)

    # get interpolation functions for model
    interp_logf = get_interp_func(model_path = model_path, ions_to_use = ions_to_use, Q_uvb = Q_uvb, uvb = model_uvb)

    print('interpolation done')


    # ---- the nine combinations
    true_nH_array = [1e-5, 1e-4, 1e-3]
    true_logZ_array  = [-2, -1, 0]
    for true_nH in true_nH_array:
        for true_logZ in true_logZ_array:
            # getting lsf array
            lognH_true = np.log10(true_nH)
            lognH_array = np.arange(lognH_true - 1, lognH_true + 1, 0.01)
            logZ_array = np.arange(true_logZ - 1, true_logZ + 1, 0.01)
            number_nH = len(lognH_array)
            number_Z = len(logZ_array)

            least_square_2D = np.zeros((number_nH, number_Z))
            # get true data
            data_col_all = get_true_model(model_path, Q=true_Q, true_nH=true_nH, logZ =true_logZ, uvb= true_uvb)
            # converting astropy table row to a list
            data_col = []
            for name in ions_to_use:
                data_col.append(data_col_all[name][0])

            obs_ion_col = np.log10(np.array(data_col))
            #print(obs_ion_col)

            for i in range(number_nH):
                val_lognH = lognH_array[i]
                for j in range(number_Z):
                    val_logZ = logZ_array[j]
                    col = []
                    for k in range(number_of_ions):
                        # print('==>', i, lognH, logT)
                        # print(interp_logf[i](lognH, logT), i, lognH, logT)
                        col_mod = interp_logf[k](val_lognH, val_logZ)[0]
                        col.append(col_mod)

                    model_col = np.array(col)
                    least_square_2D[i, j] = np.sum((model_col - obs_ion_col) ** 2)

            ind = np.unravel_index(np.argmin(least_square_2D, axis=None), least_square_2D.shape)

            print(lognH_array[ind[0]], logZ_array[ind[1]], np.min(least_square_2D), 'for (nH, Z)',
                np.log10(true_nH), true_logZ, 'true uvb: Q', true_Q, true_uvb, 'model uvb: Q', Q_uvb, model_uvb )

    return



ions_to_use= ['C+3', 'N+3', 'Si+3', 'O+5', 'C+2']
model_path  = '/home/abhisek/cloudy_run/metal_NH15_new'

get_LSF(model_path = model_path, Q_uvb = 18, model_uvb= 'FG20', ions_to_use = ions_to_use, true_Q =18, true_uvb = 'KS18')

"""
ions_to_use= ['C+3', 'N+3', 'Si+3', 'O+5', 'C+2']
true_Q =18
outpath = '/home/abhisek/cloudy_run/figures'

outfile = outpath + '/NH14_log_lsf_out.fits'

q=[14, 15, 16, 17, 18, 19, 20]
narray = []
zarray = []
value_ls=[]
for q_num in q:
    model = '/home/abhisek/cloudy_run/anshuman/try_Q{}.fits'.format(q_num)
    nH, Z, min_LS= find_nH_and_Z_LSF_log(model, ions_to_use)
    narray.append(np.log10(nH))
    zarray.append(np.log10(Z))
    value_ls.append(min_LS)

outdata = tab.Table([q, narray, zarray, value_ls], names =('Q', 'nH', 'Z', 'LS'))
outdata.write(outfile, overwrite =  True)

"""



