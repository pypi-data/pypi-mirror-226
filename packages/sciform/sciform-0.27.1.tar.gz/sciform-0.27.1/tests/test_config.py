import unittest

from sciform import (FormatOptions, SciNum, GlobalDefaultsContext, ExpMode,
                     Formatter, GroupingSeparator, RoundMode, SignMode,
                     set_global_defaults, reset_global_defaults,
                     global_add_c_prefix, global_add_small_si_prefixes,
                     global_add_ppth_form, global_reset_si_prefixes,
                     global_reset_parts_per_forms)


class TestConfig(unittest.TestCase):
    def test_set_reset_global_defaults(self):
        num = SciNum(0.0005632)
        self.assertEqual(f'{num}', '0.0005632')
        set_global_defaults(FormatOptions(
            exp_mode=ExpMode.ENGINEERING_SHIFTED,
            capitalize=True))
        self.assertEqual(f'{num}', '0.5632E-03')
        reset_global_defaults()
        self.assertEqual(f'{num}', '0.0005632')

    def test_global_defaults_context(self):
        num = SciNum(123.456)
        self.assertEqual(f'{num}', '123.456')
        with GlobalDefaultsContext(FormatOptions(
                sign_mode=SignMode.ALWAYS,
                exp_mode=ExpMode.SCIENTIFIC,
                round_mode=RoundMode.SIG_FIG,
                ndigits=2,
                decimal_separator=GroupingSeparator.COMMA)):
            self.assertEqual(f'{num}', '+1,2e+02')
        self.assertEqual(f'{num}', '123.456')

    def test_c_prefix(self):
        num = SciNum(123.456)
        fmt_spec = 'ex-2p'
        self.assertEqual(f'{num:{fmt_spec}}', '12345.6e-02')
        global_add_c_prefix()
        self.assertEqual(f'{num:{fmt_spec}}', '12345.6 c')
        global_reset_si_prefixes()
        self.assertEqual(f'{num:{fmt_spec}}', '12345.6e-02')

    def test_small_si_prefixes(self):
        num = SciNum(123.456)

        cases_dict = {-2: '12345.6 c',
                      -1: '1234.56 d',
                      +1: '12.3456 da',
                      +2: '1.23456 h'}

        global_add_small_si_prefixes()
        for exp, expected_num_str in cases_dict.items():
            num_str = f'{num:ex{exp:+}p}'
            self.assertEqual(num_str, expected_num_str)
        global_reset_si_prefixes()

    def test_ppth_form(self):
        num = 0.0024
        formatter = Formatter(FormatOptions(
            exp_mode=ExpMode.ENGINEERING,
            parts_per_exp=True
        ))
        self.assertEqual(formatter(num), '2.4e-03')
        global_add_ppth_form()
        self.assertEqual(formatter(num), '2.4 ppth')
        global_reset_parts_per_forms()
        self.assertEqual(formatter(num), '2.4e-03')
