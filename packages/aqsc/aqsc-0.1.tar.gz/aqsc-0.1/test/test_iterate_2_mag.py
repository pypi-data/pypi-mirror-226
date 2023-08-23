import unittest
import numpy as np
import aqsc

import jax.numpy as jnp

import aqsc
import jax.numpy as jnp
debug_path = '../test_data_eduardo/'

# No B theta
B_psi_coef_cp, B_theta_coef_cp, \
    Delta_coef_cp, p_perp_coef_cp,\
    X_coef_cp, Y_coef_cp, Z_coef_cp, \
    iota_coef, dl_p,\
    nfp, Xi_0, eta, \
    B_denom_coef_c, B_alpha_coef, \
    kap_p, tau_p = aqsc.read_first_three_orders(
        debug_path+'circ/', 
        R_array=[2,0,1,2,0.0001,0],
        Z_array=[1,2,0,0.001]
    )

equilibrium_mag = aqsc.leading_orders_magnetic(
    nfp=1, # Field period
    Rc=[1, 0, 0.0001], 
    Rs=[0, 0, 0],
    Zc=[0, 0, 0],
    Zs=[0, 0, 0.001], # Axis shape
    iota_0=0.52564852, # On-axis rotational transform
    B_theta_20=B_theta_coef_cp[2][0].content[0], # Average B_theta[2,0]
    B_psi_00=B_psi_coef_cp[0][0].content[0],
    Y20=Y_coef_cp[2][0].content[0],
    B_alpha_1=0.1,  # B_alpha
    B0=1,
    B11c=-1.8,
    B2=aqsc.ChiPhiFunc(
        jnp.array([[0.005+0.005j],
                 [0.01 +0.j   ],
                 [0.005-0.005j]]),
        nfp=1
    ),
    len_phi=1000,
    static_max_freq=(15, 20),
    traced_max_freq=(15, 20),
)



n_2_tolerance = 5e-8
n_4_tolerance = 8e-5

class TestCircularAxis(unittest.TestCase):

    def test_B_psi(self):
        
        equilibrium_init = aqsc.circular_axis()
        equilibrium_new = aqsc.iterate_2(
            equilibrium_init,
            n_eval=4,
            B_alpha_nb2=aqsc.ChiPhiFuncSpecial(0),
            B_denom_nm1=aqsc.ChiPhiFuncSpecial(0), 
            B_denom_n=aqsc.ChiPhiFuncSpecial(0), # B_denom_coef_c[3]
            iota_new=-6.6367278e-01,
            static_max_freq=(20,20),
            traced_max_freq=(-1,-1),
            # Traced.
            # -1 represents no filtering (default). This value is chosen so that
            # turning on or off off-diagonal filtering does not require recompiles.
            max_k_diff_pre_inv=(-1,-1),
        )
        print('Testing order 2, tolerance:', n_2_tolerance)
        (J, Cb, Ck, Ct, I, II, III) = equilibrium_new.check_governing_equations(2)
        print('J residue:')
        aqsc.print_fractional_error(J)
        self.assertTrue(J.filter(20).get_amplitude()<n_2_tolerance)
        print('Cb residue:')
        aqsc.print_fractional_error(Cb)
        self.assertTrue(Cb.filter(20).get_amplitude()<n_2_tolerance)
        print('Ck residue:')
        aqsc.print_fractional_error(Ck)
        self.assertTrue(Ck.filter(20).get_amplitude()<n_2_tolerance)
        print('Ct residue:')
        aqsc.print_fractional_error(Ct)
        self.assertTrue(Ct.filter(20).get_amplitude()<n_2_tolerance)
        print('I residue:')
        aqsc.print_fractional_error(I)
        self.assertTrue(I.filter(20).get_amplitude()<n_2_tolerance)
        print('II residue:')
        aqsc.print_fractional_error(II)
        self.assertTrue(II.filter(20).get_amplitude()<n_2_tolerance)
        print('III residue:')
        aqsc.print_fractional_error(III)
        self.assertTrue(III.filter(20).get_amplitude()<n_2_tolerance)
        print('Testing order 4, tolerance:', n_4_tolerance)
        (J, Cb, Ck, Ct, I, II, III) = equilibrium_new.check_governing_equations(4)
        print('J residue:')
        aqsc.print_fractional_error(J)
        self.assertTrue(J.filter(20).get_amplitude()<n_4_tolerance)
        print('Cb residue:')
        aqsc.print_fractional_error(Cb)
        self.assertTrue(Cb.filter(20).get_amplitude()<n_4_tolerance)
        print('Ck residue:')
        aqsc.print_fractional_error(Ck)
        self.assertTrue(Ck.filter(20).get_amplitude()<n_4_tolerance)
        print('Ct residue:')
        aqsc.print_fractional_error(Ct)
        self.assertTrue(Ct.filter(20).get_amplitude()<n_4_tolerance)
        print('I residue:')
        aqsc.print_fractional_error(I)
        self.assertTrue(I.filter(20).get_amplitude()<n_4_tolerance)
        print('II residue:')
        aqsc.print_fractional_error(II)
        self.assertTrue(II.filter(20).get_amplitude()<n_4_tolerance)
        print('III residue:')
        aqsc.print_fractional_error(III)
        self.assertTrue(III.filter(20).get_amplitude()<n_4_tolerance)
unittest.main()