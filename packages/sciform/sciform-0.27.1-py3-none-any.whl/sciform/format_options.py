from typing import Union, get_args
from dataclasses import dataclass, asdict, InitVar
from pprint import pprint

from sciform.modes import (FillMode, SignMode, GroupingSeparator,
                           UpperGroupingSeparators, LowerGroupingSeparators,
                           DecimalGroupingSeparators, RoundMode, ExpMode,
                           AutoExpVal, AutoDigits)


@dataclass(frozen=True)
class RenderedFormatOptions:
    exp_mode: ExpMode
    exp_val: Union[int, type(AutoExpVal)]
    round_mode: RoundMode
    ndigits: Union[int, type(AutoDigits)]
    upper_separator: UpperGroupingSeparators
    decimal_separator: DecimalGroupingSeparators
    lower_separator: LowerGroupingSeparators
    sign_mode: SignMode
    fill_mode: FillMode
    top_dig_place: int
    prefix_exp: bool
    parts_per_exp: bool
    extra_si_prefixes: dict[int, str]
    extra_iec_prefixes: dict[int, str]
    extra_parts_per_forms: dict[int, str]
    capitalize: bool
    superscript_exp: bool
    latex: bool
    nan_inf_exp: bool
    bracket_unc: bool
    pdg_sig_figs: bool
    val_unc_match_widths: bool
    bracket_unc_remove_seps: bool
    unicode_pm: bool
    unc_pm_whitespace: bool

    def __post_init__(self):
        validate_options(self)


def _merge_dicts(left: dict, right: dict) -> dict:
    right_pruned = {key: val for key, val in right.items() if val is not None}
    return {**left, **right_pruned}


ExpReplaceDict = dict[int, Union[str, None]]


@dataclass(frozen=True)
class FormatOptions:
    # TODO: __repr__
    """
    :class:`FormatOptions` stores all the configuration options used to
    format numbers and number/uncertainty pairs. See
    :ref:`formatting_options` for more details on the available options.
    :class:`FormatOptions` instances are used to create
    :class:`Formatter` instances and to modify the global default
    configuration.

    It is not necessary to provide input for all options. At format
    time, any un-populated options (indicated by a ``None`` value) will
    be populated with the corresponding options from the global default
    options. See :ref:`global_config` for details about how to view and
    modify the global default options.

    The following checks are performed when creating a new
    :class:`FormatOptions` object:

    * ``ndigits`` >= 1 for significant figure rounding mode
    * ``exp_val`` must be consistent with the exponent mode. If
      ``exp_val`` is specified (i.e. not ``None``) and ``exp_val`` is
      not ``AutoExpVal`` then

      * ``exp_val`` must be 0 for fixed point and percent modes
      * ``exp_val`` must be a multiple of 3 for engineering and shifted
        engineering modes
      * ``exp_val`` must be a multiple of 10 for binary iec mode

    * ``upper_separator`` may be any :class:`GroupingSeparator` but must
      be different from ``decimal_separator``
    * ``decimal_separator`` may only be :class:`GroupingSeparator.POINT`
      or :class:`GroupingSeparator.COMMA`
    * ``lower_separator`` may only be :class:`GroupingSeparator.NONE`,
      :class:`GroupingSeparator.SPACE`, or
      :class:`GroupingSeparator.UNDERSCORE`
    * ``ndigits=None`` or ``ndigits=AutoDigits`` if
      ``pdg_sig_figs=True``
    * Only one of ``prefix_exp`` and ``parts_per_exp`` may be selected

    :param exp_mode: :class:`ExpMode` indicating the formatting
      mode to be used.
    :param exp_val: :class:`int` or :class:`AutoExpVal` sentinel
      indicating a value which must be used for the exponent. If
      specified, this value must be 0 for fixed point and percent modes,
      an integer multiple of 3 for engineering and engineering shifted
      modes, and an integer multiple of 10 for binary IEC mode.
    :param round_mode: :class:`RoundMode` indicating whether to round
      the number based on significant figures or decimal places.
    :param ndigits: :class:`int` or :class:`AutoDigits` sentinel
      indicating how many significant digits or which decimal place to
      use for rounding. Must be >= 1 for significant figure rounding.
      May be any integer for decimal place rounding.
    :param upper_separator: :class:`GroupingSeparator` indicating the
      character to be used to group digits above the decimal symbol.
    :param decimal_separator: :class:`GroupingSeparator` indicating
      the character to be used as the decimal symbol.
      :class:`GroupingSeparator.POINT` or
      :class:`GroupingSeparator.COMMA`. Note that ``decimal_separator``
      cannot be the same as ``upper_separator``
    :param lower_separator: :class:`GroupingSeparator` indicating the
      character to be used to group digits below the decimal symbol.
      :class:`GroupingSeparator.NONE`, :class:`GroupingSeparator.SPACE`,
      or :class:`GroupingSeparator.UNDERSCORE`.
    :param sign_mode: :class:`SignMode` indicating sign
      symbol behavior.
    :param fill_mode: :class:`FillMode` indicating whether
      to fill with zeros or spaces.
    :param top_dig_place: Positive ``int`` indicating the digits place
      to which the string will be left padded before the sign symbol. 0
      corresponds to the ones place, 1 corresponds to the tens place
      etc. E.g. ``top_dig_place=4`` will convert ``12`` into ``00012``.
    :param prefix_exp: :class:`bool` indicating if exponents should be
      replaced with either SI or IEC prefixes as appropriate.
    :param parts_per_exp: :class:`bool` indicating if "parts-per" exponent
      translations should be used.
    :param extra_si_prefixes: ``dict[int, Union[str, None]]`` mapping
      additional exponent values to si prefixes. Entries overwrite
      default values. A value of ``None`` means that exponent will not
      be converted.
    :param extra_iec_prefixes: ``dict[int, Union[str, None]]`` mapping
      additional exponent values to iec prefixes. Entries overwrite
      default values. A value of ``None`` means that exponent will not
      be converted.
    :param extra_parts_per_forms: ``dict[int, Union[str, None]]``
      mapping additional exponent values to "parts-per" forms. Entries
      overwrite default values. A value of ``None`` means that exponent
      will not be converted.
    :param capitalize: :class:`bool` indicating whether the exponentiation
      symbol should be upper- or lower-case.
    :param superscript_exp: :class:`bool` indicating if the exponent string
      should be converted into superscript notation. E.g. ``'1.23e+02'``
      is converted to ``'1.23×10²'``
    :param latex: :class:`bool` indicating if the resulting string should be
      converted into a latex parseable code, e.g.
      ``'\\left(1.23 \\pm 0.01\\right)\\times 10^{2}'``.
    :param nan_inf_exp: :class:`bool` indicating whether non-finite numbers
      such as ``float('nan')`` or ``float('inf')`` should be formatted
      with exponent symbols when exponent modes including exponent
      symbols are selected.
    :param bracket_unc: :class:`bool` indicating if bracket uncertainty mode
      (e.g. ``12.34(82)`` instead of ``12.34 +/- 0.82``) should be used.
    :param pdg_sig_figs: :class:`bool` indicating whether the
      particle-data-group conventions should be used to automatically
      determine the number of significant figures to use for
      uncertainty.
    :param val_unc_match_widths: :class:`bool` indicating if the value or
      uncertainty should be left padded to ensure they are both left
      padded to the same digits place.
    :param bracket_unc_remove_seps: :class:`bool` indicating if separator
      symbols should be removed from the uncertainty when using bracket
      uncertainty mode. E.g. expressing ``123.4 +/- 2.3`` as
      ``123.4(23)`` instead of ``123.4(2.3)``.
    :param unicode_pm: :class:`bool` indicating if the '+/-' separator should
      be replaced with the unicode plus minus symbol '±'.
    :param unc_pm_whitespace: :class:`bool` indicating if there should be
      whitespace surrounding the ``'+/-'`` symbols when formatting. E.g.
      ``123.4+/-2.3`` compared to ``123.4 +/- 2.3``.
    :param add_c_prefix: :class:`bool` (default ``False``) if ``True`` adds
      ``{-2: 'c'}`` to ``extra_si_prefixes``.
    :param add_small_si_prefixes: ``bool`` (default ``False``) if
      ``True`` adds ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` to
      ``extra_si_prefixes``.
    :param add_ppth_form: :class:`bool` (default ``False``) if ``True`` adds
      ``{-3: 'ppth'}`` to ``extra_parts_per_forms``.
    """
    exp_mode: ExpMode = None
    exp_val: Union[int, type(AutoExpVal)] = None
    round_mode: RoundMode = None
    ndigits: Union[int, type(AutoDigits)] = None
    upper_separator: UpperGroupingSeparators = None
    decimal_separator: DecimalGroupingSeparators = None
    lower_separator: LowerGroupingSeparators = None
    sign_mode: SignMode = None
    fill_mode: FillMode = None
    top_dig_place: int = None
    prefix_exp: bool = None
    parts_per_exp: bool = None
    extra_si_prefixes: dict[int, str] = None
    extra_iec_prefixes: dict[int, str] = None
    extra_parts_per_forms: dict[int, str] = None
    capitalize: bool = None
    superscript_exp: bool = None
    latex: bool = None
    nan_inf_exp: bool = None
    bracket_unc: bool = None
    pdg_sig_figs: bool = None
    val_unc_match_widths: bool = None
    bracket_unc_remove_seps: bool = None
    unicode_pm: bool = None
    unc_pm_whitespace: bool = None

    add_c_prefix: InitVar[bool] = False
    add_small_si_prefixes: InitVar[bool] = False
    add_ppth_form: InitVar[bool] = False

    def __post_init__(self, add_c_prefix, add_small_si_prefixes,
                      add_ppth_form):
        # TODO: Test that things do and don't get added appropriately
        if add_c_prefix:
            if self.extra_si_prefixes is None:
                super().__setattr__('extra_si_prefixes', dict())
            if -2 not in self.extra_si_prefixes:
                self.extra_si_prefixes[-2] = 'c'

        if add_small_si_prefixes:
            if self.extra_si_prefixes is None:
                super().__setattr__('extra_si_prefixes', dict())
            if -2 not in self.extra_si_prefixes:
                self.extra_si_prefixes[-2] = 'c'
            if -1 not in self.extra_si_prefixes:
                self.extra_si_prefixes[-1] = 'd'
            if +1 not in self.extra_si_prefixes:
                self.extra_si_prefixes[+1] = 'da'
            if +2 not in self.extra_si_prefixes:
                self.extra_si_prefixes[+2] = 'h'

        if add_ppth_form:
            if self.extra_parts_per_forms is None:
                super().__setattr__('extra_parts_per_forms', dict())
            if -3 not in self.extra_parts_per_forms:
                self.extra_parts_per_forms[-3] = 'ppth'

        validate_options(self)

    def merge(self, other: 'FormatOptions') -> 'FormatOptions':
        """
        Generate a new :class:`FormatOptions` instance from the current
        instance and another :class:`FormatOptions` instance,
        ``other``. The options for the new :class:`FormatOptions` are
        constructed by replacing the options from the current instance
        by any filled options from ``other``. Note that, even after
        merging, the resulting :class:`FormatOptions` may still have
        unfilled options.

        :param other: :class:`FormatOptions` instance containing options
          that will overwrite those of the current instance.
        :return: New :class:`FormatOptions` instance.
        """
        return FormatOptions(**_merge_dicts(asdict(self), asdict(other)))

    def render(
            self, defaults: RenderedFormatOptions = None
               ) -> RenderedFormatOptions:
        if defaults is None:
            defaults = get_global_defaults()
        try:
            rendered_format_options = RenderedFormatOptions(
                **_merge_dicts(asdict(defaults), asdict(self))
            )
        except ValueError as e:
            raise ValueError('Invalid format options resuling from merging '
                             'with default options.') from e

        return rendered_format_options


def validate_options(options: Union[FormatOptions, RenderedFormatOptions]):
    if options.round_mode is RoundMode.SIG_FIG:
        if isinstance(options.ndigits, int):
            if options.ndigits < 1:
                raise ValueError(f'Precision must be >= 1 for sig fig '
                                 f'rounding, not {options.ndigits}.')

    if (options.pdg_sig_figs and options.ndigits is not None
            and options.ndigits is not AutoDigits):
        raise ValueError(f'pdg_sig_figs=True can only be used with '
                         f'ndigits=AutoDigits, not ndigits={options.ndigits}.')

    if options.exp_val is not AutoExpVal and options.exp_val is not None:
        if (options.exp_mode is ExpMode.FIXEDPOINT
                or options.exp_mode is ExpMode.PERCENT):
            if options.exp_val != 0:
                raise ValueError(f'Exponent must must be 0, not '
                                 f'exp_val={options.exp_val}, for fixed '
                                 f'point and percent exponent modes.')
        elif (options.exp_mode is ExpMode.ENGINEERING
              or options.exp_mode is ExpMode.ENGINEERING_SHIFTED):
            if options.exp_val % 3 != 0:
                raise ValueError(f'Exponent must be a multiple of 3, not '
                                 f'exp_val={options.exp_val}, for '
                                 f'engineering exponent modes.')
        elif options.exp_mode is ExpMode.BINARY_IEC:
            if options.exp_val % 10 != 0:
                raise ValueError(f'Exponent must be a multiple of 10, not '
                                 f'exp_val={options.exp_val}, for binary IEC '
                                 f'exponent mode.')

    if options.upper_separator is not None:
        if options.upper_separator not in get_args(UpperGroupingSeparators):
            raise ValueError(f'upper_separator must be in '
                             f'{get_args(UpperGroupingSeparators)}, not '
                             f'{options.upper_separator}.')
        if options.upper_separator is options.decimal_separator:
            raise ValueError(f'upper_separator and decimal_separator '
                             f'({options.upper_separator}) cannot be equal.')

    if options.decimal_separator is not None:
        if (options.decimal_separator
                not in get_args(DecimalGroupingSeparators)):
            raise ValueError(f'upper_separator must be in '
                             f'{get_args(DecimalGroupingSeparators)}, not '
                             f'{options.upper_separator}.')

    if options.lower_separator is not None:
        if options.lower_separator not in get_args(LowerGroupingSeparators):
            raise ValueError(f'upper_separator must be in '
                             f'{get_args(LowerGroupingSeparators)}, not '
                             f'{options.upper_separator}.')

    if options.prefix_exp is not None and options.parts_per_exp is not None:
        if options.prefix_exp and options.parts_per_exp:
            raise ValueError('Only one of prefix exponent and parts-per '
                             'exponent modes may be selected.')


PKG_DEFAULT_OPTIONS = RenderedFormatOptions(
    exp_mode=ExpMode.FIXEDPOINT,
    exp_val=AutoExpVal,
    round_mode=RoundMode.SIG_FIG,
    ndigits=AutoDigits,
    upper_separator=GroupingSeparator.NONE,
    decimal_separator=GroupingSeparator.POINT,
    lower_separator=GroupingSeparator.NONE,
    sign_mode=SignMode.NEGATIVE,
    fill_mode=FillMode.SPACE,
    top_dig_place=0,
    prefix_exp=False,
    parts_per_exp=False,
    extra_si_prefixes=dict(),
    extra_iec_prefixes=dict(),
    extra_parts_per_forms=dict(),
    capitalize=False,
    superscript_exp=False,
    latex=False,
    nan_inf_exp=False,
    bracket_unc=False,
    pdg_sig_figs=False,
    val_unc_match_widths=False,
    bracket_unc_remove_seps=False,
    unicode_pm=False,
    unc_pm_whitespace=True
)


GLOBAL_DEFAULT_OPTIONS = PKG_DEFAULT_OPTIONS


def get_global_defaults() -> RenderedFormatOptions:
    return GLOBAL_DEFAULT_OPTIONS


def print_global_defaults():
    """
    Print current global default formatting options as a dictionary.
    """
    pprint(asdict(get_global_defaults()), sort_dicts=False)


def set_global_defaults(format_options: FormatOptions):
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = format_options.render()


def set_global_defaults_rendered(
        rendered_format_options: RenderedFormatOptions):
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = rendered_format_options


def reset_global_defaults():
    """
    Reset global default options to package defaults.
    """
    global GLOBAL_DEFAULT_OPTIONS
    GLOBAL_DEFAULT_OPTIONS = PKG_DEFAULT_OPTIONS


def global_add_c_prefix():
    """
    Include ``c`` as a prefix for the exponent value -2. Has no effect
    if exponent value -2 is already mapped to a prefix string. To modify
    this mapping, first use :func:`global_reset_si_prefixes` or
    use :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_c_prefix=True))


def global_add_small_si_prefixes():
    """
    Include ``{-2: 'c', -1: 'd', +1: 'da', +2: 'h'}`` as prefix
    substitutions. Note, if any of these exponent values are mapped,
    then that mapping will NOT be overwritten. To modify existing
    mappings either first use :func:`global_reset_si_prefixes` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_small_si_prefixes=True))


def global_add_ppth_form():
    """
    Include ``ppth`` as a "parts-per" form for the exponent value -3.
    Has no effect if exponent value -3 is already mapped to a
    "parts-per" format string. To modify this mapping, first use
    :func:`global_reset_parts_per_forms` or use
    :func:`set_global_defaults`.
    """
    set_global_defaults(FormatOptions(add_ppth_form=True))


def global_reset_si_prefixes():
    """
    Clear all extra SI prefix mappings.
    """
    set_global_defaults(FormatOptions(extra_si_prefixes=dict()))


def global_reset_iec_prefixes():
    """
    Clear all extra IEC prefix mappings.
    """
    set_global_defaults(FormatOptions(extra_iec_prefixes=dict()))


def global_reset_parts_per_forms():
    """
    Clear all extra "parts-per" forms.
    """
    set_global_defaults(FormatOptions(extra_parts_per_forms=dict()))


class GlobalDefaultsContext:
    """
    Temporarily update global default options. New settings are applied
    when the context is entered and original global settings are
    re-applied when the context is exited.
    """
    def __init__(self, format_options: FormatOptions):
        self.format_options = format_options
        self.initial_global_defaults = None

    def __enter__(self):
        self.initial_global_defaults = get_global_defaults()
        set_global_defaults(self.format_options)

    def __exit__(self, exc_type, exc_value, exc_tb):
        set_global_defaults_rendered(self.initial_global_defaults)
