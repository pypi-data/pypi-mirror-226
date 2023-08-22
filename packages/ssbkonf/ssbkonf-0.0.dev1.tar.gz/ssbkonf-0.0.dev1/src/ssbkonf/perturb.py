import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from pandas import DataFrame
from .util import convert2r, convert2py, prepare_input
from .pckg import importr_tryhard

_scr = importr_tryhard("SmallCountRounding")


def small_count_rounding(
    data: DataFrame,
    dim_var: list[str] = None,
    hierarchies: dict[str, DataFrame | list[DataFrame]] = None,
    formula: str = None,
    freq_var: str = "freq",
    round_base: int = 3,
):
    (rdata, freq_var, _, dim_var, hierarchies, formula) = prepare_input(
        data=data,
        freq_var=freq_var,
        dim_var=dim_var,
        formula=formula,
        hierarchies=hierarchies,
    )

    out = _scr.PLSrounding(
        data=rdata,
        dim_var=dim_var,
        hierarchies=hierarchies,
        formula=formula,
        freqVar=freq_var,
        roundBase=round_base,
    )
    return convert2py(out)
