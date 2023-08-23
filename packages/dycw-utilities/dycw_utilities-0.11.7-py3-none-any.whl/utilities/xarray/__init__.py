from collections.abc import Hashable, Mapping
from typing import Any, Optional, Union, cast

from beartype import beartype

from utilities._numbagg import move_exp_nanmean, move_exp_nansum
from utilities.xarray.typing import DataArrayF, DataArrayI


@beartype
def ewma(
    array: Union[DataArrayI, DataArrayF],
    halflife: Optional[Mapping[Hashable, int]] = None,
    /,
    *,
    keep_attrs: Optional[bool] = None,
    **halflife_kwargs: int,
) -> DataArrayF:
    """Compute the EWMA of an array."""
    rolling_exp = array.rolling_exp(halflife, window_type="halflife", **halflife_kwargs)
    return array.reduce(
        _move_exp_nanmean,
        dim=rolling_exp.dim,
        alpha=rolling_exp.alpha,
        keep_attrs=keep_attrs,
    )


@beartype
def _move_exp_nanmean(array: Any, /, *, axis: Any, alpha: Any) -> Any:
    if axis == ():  # pragma: no cover
        return array.astype(float)
    return cast(Any, move_exp_nanmean)(array, axis=axis, alpha=alpha)


@beartype
def exp_moving_sum(
    array: Union[DataArrayI, DataArrayF],
    halflife: Optional[Mapping[Hashable, int]] = None,
    /,
    *,
    keep_attrs: Optional[bool] = None,
    **halflife_kwargs: int,
) -> DataArrayF:
    """Compute the exponentially-weighted moving sum of an array."""
    rolling_exp = array.rolling_exp(halflife, window_type="halflife", **halflife_kwargs)
    return array.reduce(
        _move_exp_nansum,
        dim=rolling_exp.dim,
        alpha=rolling_exp.alpha,
        keep_attrs=keep_attrs,
    )


@beartype
def _move_exp_nansum(array: Any, /, *, axis: Any, alpha: Any) -> Any:
    if axis == ():  # pragma: no cover
        return array.astype(float)
    return cast(Any, move_exp_nansum)(array, axis=axis, alpha=alpha)
