import re
import typing as t
from textwrap import TextWrapper as _TextWrapper

from click import style

# https://stackoverflow.com/a/63839503
METRIC_LABELS: t.List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
BINARY_LABELS: t.List[str] = [
    "B",
    "KiB",
    "MiB",
    "GiB",
    "TiB",
    "PiB",
    "EiB",
    "ZiB",
    "YiB",
]
PRECISION_OFFSETS: t.List[float] = [0.5, 0.05, 0.005, 0.0005]  # PREDEFINED FOR SPEED.
PRECISION_FORMATS: t.List[str] = [
    "{}{:.0f} {}",
    "{}{:.1f} {}",
    "{}{:.2f} {}",
    "{}{:.3f} {}",
]  # PREDEFINED FOR SPEED.


def format_bytes(
    num: t.Union[int, float], metric: bool = False, precision: int = 1
) -> str:
    """
    Human-readable formatting of bytes, using binary (powers of 1024)
    or metric (powers of 1000) representation.
    """

    assert isinstance(num, (int, float)), "num must be an int or float"
    assert isinstance(metric, bool), "metric must be a bool"
    assert (
        isinstance(precision, int) and precision >= 0 and precision <= 3
    ), "precision must be an int (range 0-3)"

    unit_labels = METRIC_LABELS if metric else BINARY_LABELS
    last_label = unit_labels[-1]
    unit_step = 1000 if metric else 1024
    unit_step_thresh = unit_step - PRECISION_OFFSETS[precision]

    is_negative = num < 0
    if is_negative:  # Faster than ternary assignment or always running abs().
        num = abs(num)

    for unit in unit_labels:
        if num < unit_step_thresh:
            # VERY IMPORTANT:
            # Only accepts the CURRENT unit if we're BELOW the threshold where
            # float rounding behavior would place us into the NEXT unit: F.ex.
            # when rounding a float to 1 decimal, any number ">= 1023.95" will
            # be rounded to "1024.0". Obviously we don't want ugly output such
            # as "1024.0 KiB", since the proper term for that is "1.0 MiB".
            break
        if unit != last_label:
            # We only shrink the number if we HAVEN'T reached the last unit.
            # NOTE: These looped divisions accumulate floating point rounding
            # errors, but each new division pushes the rounding errors further
            # and further down in the decimals, so it doesn't matter at all.
            num /= unit_step

    return PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)  # type: ignore


def format_columns(data: t.Any, prefix=""):
    if isinstance(data, t.Dict):
        return _format_columns_dict(data, prefix)

    raise NotImplementedError(format_columns, data, type(data))


def _format_columns_dict(dict, prefix):
    if not dict:
        return ""
    c1_width = max(len(k) for k in dict.keys())
    return "\n".join(
        "{}{:<{c1_width}}\t{}".format(prefix, k, v, c1_width=c1_width)
        for k, v in dict.items()
    ).strip("\n")


_NAME_VER_FORMAT = style(
    "{{{name_field}}} " + style("{{{version_field}}}", fg="green", reset=False),
    bold=True,
)


def format_name_ver(obj, name_field="name", version_field="version"):
    return format(
        obj, _NAME_VER_FORMAT.format(name_field=name_field, version_field=version_field)
    )


_rst_inline = re.compile(r":.+:`(.+)`")


def format_rst_inline(text: str):
    """Strips inline roles and underlines their contents."""
    return re.sub(_rst_inline, style(r"\1", underline=True), text)


_ansi_re = re.compile(r"\033\[[;?0-9]*[a-zA-Z]")


class ANSIString(str):
    def __len__(self) -> int:
        return len(re.sub(_ansi_re, "", self))


class ANSITextWrapper(_TextWrapper):
    """Extension of TextWrapper that properly handles ANSI escape sequences.

    ANSI escape sequences are ignored when calculating string length."""

    def _split(self, text: str) -> t.List[str]:
        chunks = super()._split(text)
        return [ANSIString(s) for s in chunks]
