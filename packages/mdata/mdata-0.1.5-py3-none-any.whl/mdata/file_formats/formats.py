from typing import Literal
# noinspection PyUnresolvedReferences
from .csv.shared import HeaderFormatLiterals, HeaderFileFormats
from ..core.util import StringEnumeration


class ExportFormats(StringEnumeration):
    CSV = 'csv'
    HDF = 'h5'


ExportFormatLiterals = Literal['csv', 'h5']
