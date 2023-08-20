from typing import List, Literal

from classiq.pyqmod.qmod_parameter import QParam
from classiq.pyqmod.qmod_variable import OutputQVar, QVar
from classiq.pyqmod.quantum_callable import QCallable
from classiq.pyqmod.quantum_function import ExternalQFunc


@ExternalQFunc
def H(target: QVar[Literal[1]]) -> None:  # noqa: N802
    pass


@ExternalQFunc
def CX(control: QVar[Literal[1]], target: QVar[Literal[1]]) -> None:  # noqa: N802
    pass


@ExternalQFunc
def PHASE(theta: QParam[float], target: QVar[Literal[1]]) -> None:  # noqa: N802
    pass


@ExternalQFunc
def CRZ(  # noqa: N802
    theta: QParam[float], control: QVar[Literal[1]], target: QVar[Literal[1]]
) -> None:
    pass


@ExternalQFunc
def SWAP(qbit0: QVar[Literal[1]], qbit1: QVar[Literal[1]]) -> None:  # noqa: N802
    pass


@ExternalQFunc
def repeat(
    count: QParam[int],
    port_size: QParam[int],
    iteration: QCallable[[QParam[int], QVar[Literal["port_size"]]]],
    qbv: QVar[Literal["port_size"]],
) -> None:
    pass


@ExternalQFunc
def allocate(
    num_qubits: QParam[int],
    target: OutputQVar[Literal["num_qubits"]],
) -> None:
    pass


@ExternalQFunc
def STATE_PREPARATION(  # noqa: N802
    probabilities: QParam[List[float]],
    bound: QParam[float],
    p: OutputQVar[Literal["*"]],
) -> None:
    pass


@ExternalQFunc
def ADDER(  # noqa: N802
    left_size: QParam[int],
    right_size: QParam[int],
    left: QVar[Literal["left_size"]],
    right: QVar[Literal["right_size"]],
    result: QVar[Literal["Max(left_size, right_size) + 1"]],
) -> None:
    pass


__all__ = [
    "H",
    "CX",
    "PHASE",
    "CRZ",
    "SWAP",
    "repeat",
    "allocate",
    "STATE_PREPARATION",
    "ADDER",
]
