import typing
from collections.abc import Set

from ..base_machine_data import BaseMachineData
from mdata.core.shared_defs import Extension
from ..protocols import MachineData

support_levels = {BaseMachineData.supported_extensions: BaseMachineData}


def as_base(md: MachineData) -> BaseMachineData:
    """Explicitly cast Machine Data Instance to `BaseMachineData`. Useful for enabling autocompletion using static
    typechecking."""
    return typing.cast(BaseMachineData, md)


def as_supports(md: MachineData, required: Set[Extension]) -> BaseMachineData:
    min_supporting_type = min((supp for supp in support_levels if supp >= required))
    return typing.cast(min_supporting_type, md)
