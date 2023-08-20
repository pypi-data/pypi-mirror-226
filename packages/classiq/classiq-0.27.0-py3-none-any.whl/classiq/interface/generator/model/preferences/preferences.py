import itertools
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, List, MutableSet, Optional, Union

import pydantic
from typing_extensions import TypeAlias

from classiq.interface.backend.backend_preferences import BackendPreferences
from classiq.interface.backend.quantum_backend_providers import (
    AllBackendsNameByVendor,
    ProviderVendor,
)
from classiq.interface.generator.model.preferences.randomness import create_random_seed
from classiq.interface.generator.transpiler_basis_gates import (
    DEFAULT_BASIS_GATES,
    DEFAULT_ROUTING_BASIS_GATES,
    ROUTING_TWO_QUBIT_BASIS_GATES,
    TWO_QUBIT_GATES,
    TranspilerBasisGates,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticNonNegIntTuple

from classiq._internals.enum_utils import StrEnum

if TYPE_CHECKING:
    VisualizationLevel: TypeAlias = Optional[int]
else:
    VisualizationLevel: TypeAlias = Optional[pydantic.conint(ge=-1)]
ConnectivityMap = List[PydanticNonNegIntTuple]

BACKEND_VALIDATION_ERROR_MESSAGE = (
    "Backend service provider and backend name should be specified together."
)


class CustomHardwareSettings(pydantic.BaseModel):
    basis_gates: List[TranspilerBasisGates] = pydantic.Field(
        default=list(),
        description="The basis gates of the hardware. "
        "This set will be used during the model optimization. "
        "If none given, use default values: "
        f"If no connectivity map is given or the connectivity map is symmetric - {DEFAULT_BASIS_GATES}. "
        f"If a non-symmetric connectivity map is given - {DEFAULT_ROUTING_BASIS_GATES}. ",
    )
    connectivity_map: Optional[ConnectivityMap] = pydantic.Field(
        default=None,
        description="Qubit connectivity map, in the form [ [q0, q1], [q1, q2],...]. "
        "If none given, assume the hardware is fully connected",
    )
    is_symmetric_connectivity: bool = pydantic.Field(
        default=True,
        description="Assumes that the coupling map forms an undirected graph, "
        "so for every qubit pair [q0, q1], both qubits can act as control and target. "
        "If false, the first / second qubit denotes the control / target, respectively",
    )
    _width: Optional[int] = pydantic.PrivateAttr(default=None)
    _is_default: bool = pydantic.PrivateAttr(default=False)

    @pydantic.validator("connectivity_map")
    def _validate_connectivity_map(
        cls, connectivity_map: Optional[ConnectivityMap]
    ) -> Optional[ConnectivityMap]:
        if connectivity_map is None:
            return connectivity_map
        if not connectivity_map:
            raise ValueError("Connectivity map cannot be empty")
        connectivity_map = _reindex_qubits(connectivity_map)
        return connectivity_map

    @pydantic.root_validator()
    def _symmetrize_connectivity_map(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        connectivity_map = values.get("connectivity_map")
        if connectivity_map is None:
            return values

        is_symmetric = values.get("is_symmetric_connectivity")
        if is_symmetric:
            connectivity_map = _symmetrize_connectivity_map(connectivity_map)
            values["connectivity_map"] = connectivity_map

        if not _is_connected_map(connectivity_map):
            raise ValueError(
                f"Connectivity map must be connected: {connectivity_map} is not connected."
            )
        return values

    @pydantic.root_validator()
    def _validate_basis_gates(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        connectivity_map = values.get("connectivity_map")
        specified_basis_gates = values.get("basis_gates", [])
        if connectivity_map is None:
            values["basis_gates"] = specified_basis_gates or list(DEFAULT_BASIS_GATES)
            return values

        is_symmetric_connectivity = values.get("is_symmetric")
        if is_symmetric_connectivity or _check_symmetry(connectivity_map):
            values["basis_gates"] = specified_basis_gates or list(DEFAULT_BASIS_GATES)
            return values

        values["basis_gates"] = specified_basis_gates or list(
            DEFAULT_ROUTING_BASIS_GATES
        )
        invalid_gates = [
            gate
            for gate in specified_basis_gates
            if gate in TWO_QUBIT_GATES and gate not in ROUTING_TWO_QUBIT_BASIS_GATES
        ]
        if invalid_gates:
            raise ValueError(
                "Connectivity-aware synthesis with non-symmetric coupling map "
                "is currently supported for the following two-qubit gates only: cx, ecr, rzx."
            )

        return values

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._width: Optional[int] = (
            len(set(itertools.chain.from_iterable(self.connectivity_map)))
            if self.connectivity_map
            else None
        )
        self._is_default: bool = self._is_default_custom_hardware_settings()

    @property
    def width(self) -> Optional[int]:
        return self._width

    @property
    def is_default(self) -> bool:
        return self._is_default

    def _is_default_custom_hardware_settings(self) -> bool:
        if self.connectivity_map is not None:
            return False
        default_basis_gates = {gate.lower() for gate in DEFAULT_BASIS_GATES}
        return default_basis_gates == {gate.lower() for gate in self.basis_gates}


def _is_connected_map(connectivity_map: ConnectivityMap) -> bool:
    nodes: MutableSet[int] = set()
    node_to_neighbors: Dict[int, MutableSet[int]] = defaultdict(set)
    for edge in connectivity_map:
        nodes.add(edge[0])
        nodes.add(edge[1])
        node_to_neighbors[edge[0]].add(edge[1])
        node_to_neighbors[edge[1]].add(edge[0])
    visited: MutableSet[int] = set()
    starting_node = list(nodes)[0]
    _node_dfs(starting_node, node_to_neighbors, visited)
    return len(visited) == len(nodes)


def _node_dfs(
    node: int, node_to_neighbors: Dict[int, MutableSet[int]], visited: MutableSet[int]
) -> None:
    visited.add(node)
    neighbors = node_to_neighbors[node]
    for neighbor in neighbors:
        if neighbor in visited:
            continue
        _node_dfs(neighbor, node_to_neighbors, visited)
    return


def _reindex_qubits(connectivity_map: ConnectivityMap) -> ConnectivityMap:
    qubits = sorted({q for pair in connectivity_map for q in pair})
    return [(qubits.index(pair[0]), qubits.index(pair[1])) for pair in connectivity_map]


def _check_symmetry(connectivity_map: ConnectivityMap) -> bool:
    undirected_edges = {tuple(sorted(edge)) for edge in connectivity_map}
    return len(undirected_edges) == len(connectivity_map) / 2


def _symmetrize_connectivity_map(connectivity_map: ConnectivityMap) -> ConnectivityMap:
    # A more complicated implementation than using set to maintain the order
    connectivity_map_no_duplicates = []
    for edge in connectivity_map:
        reversed_edge = (edge[1], edge[0])
        if (
            edge not in connectivity_map_no_duplicates
            and reversed_edge not in connectivity_map_no_duplicates
        ):
            connectivity_map_no_duplicates.append(edge)
    reversed_connectivity_map = [
        (edge[1], edge[0]) for edge in connectivity_map_no_duplicates
    ]
    return connectivity_map_no_duplicates + reversed_connectivity_map


class QuantumFormat(StrEnum):
    QASM = "qasm"
    QSHARP = "qsharp"
    QIR = "qir"
    IONQ = "ionq"
    CIRQ_JSON = "cirq_json"
    QASM_CIRQ_COMPATIBLE = "qasm_cirq_compatible"
    CUDAQ_JSON = "cudaq_json"


_SERVICE_PROVIDER_TO_FORMAT: Dict[str, QuantumFormat] = {
    ProviderVendor.IONQ: QuantumFormat.IONQ,
    ProviderVendor.AZURE_QUANTUM: QuantumFormat.QSHARP,
    ProviderVendor.IBM_QUANTUM: QuantumFormat.QASM,
    ProviderVendor.NVIDIA: QuantumFormat.QASM,
    ProviderVendor.AMAZON_BRAKET: QuantumFormat.QASM,
}


if TYPE_CHECKING:
    PydanticConstrainedQuantumFormatList = List[QuantumFormat]
else:
    PydanticConstrainedQuantumFormatList = pydantic.conlist(
        QuantumFormat, min_items=1, max_items=len(QuantumFormat)
    )


class TranspilationOption(StrEnum):
    NONE = "none"
    DECOMPOSE = "decompose"
    OPTIMIZE = "optimize"


class Preferences(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    _backend_preferences: Optional[BackendPreferences] = pydantic.PrivateAttr(
        default=None
    )
    backend_service_provider: Optional[Union[str, ProviderVendor]] = pydantic.Field(
        default=None, description="Provider company or cloud for the requested backend."
    )
    backend_name: Optional[Union[str, AllBackendsNameByVendor]] = pydantic.Field(
        default=None, description="Name of the requested backend or target."
    )
    custom_hardware_settings: CustomHardwareSettings = pydantic.Field(
        default_factory=CustomHardwareSettings,
        description="Custom hardware settings which will be used during optimization. "
        "This field is ignored if backend preferences are given.",
    )
    support_circuit_visualization: bool = pydantic.Field(
        default=True,
        description="Support visualizing the circuit via the IDE. "
        "Setting this option to False can potentially speed up the synthesis, and is"
        "recommended for executing iterative algorithms.",
    )
    output_format: PydanticConstrainedQuantumFormatList = pydantic.Field(
        default=[QuantumFormat.QASM],
        description="The quantum circuit output format(s). ",
    )

    pretty_qasm: bool = pydantic.Field(
        True,
        description="Prettify the OpenQASM2 outputs (use line breaks inside the gate "
        "declarations).",
    )

    qasm3: Optional[bool] = pydantic.Field(
        None,
        description="Output OpenQASM 3.0 instead of OpenQASM 2.0. Relevant only for "
        "the `qasm` and `transpiled_circuit.qasm` attributes of `GeneratedCircuit`.",
    )

    transpilation_option: TranspilationOption = pydantic.Field(
        default=TranspilationOption.OPTIMIZE,
        description="If true, the returned result will contain a "
        "transpiled circuit and its depth",
    )

    timeout_seconds: pydantic.PositiveInt = pydantic.Field(
        default=300, description="Generation timeout in seconds"
    )

    optimization_timeout_seconds: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="Optimization timeout in seconds, or None for no "
        "optimization timeout (will still timeout when the generation timeout is over)",
    )

    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )

    @pydantic.validator("optimization_timeout_seconds")
    def optimization_timeout_less_than_generation_timeout(
        cls,
        optimization_timeout_seconds: Optional[pydantic.PositiveInt],
        values: Dict[str, Any],
    ) -> Optional[pydantic.PositiveInt]:
        generation_timeout_seconds = values.get("timeout_seconds")
        if generation_timeout_seconds is None or optimization_timeout_seconds is None:
            return optimization_timeout_seconds
        if optimization_timeout_seconds >= generation_timeout_seconds:
            raise ValueError(
                f"Generation timeout ({generation_timeout_seconds})"
                f"is greater than or equal to "
                f"optimization timeout ({optimization_timeout_seconds}) "
            )
        return optimization_timeout_seconds

    @pydantic.validator("output_format", pre=True)
    def make_output_format_list(cls, output_format: Any) -> List:
        if not pydantic.utils.sequence_like(output_format):
            output_format = [output_format]

        return output_format

    @pydantic.validator("output_format", always=True)
    def validate_output_format(
        cls, output_format: PydanticConstrainedQuantumFormatList, values: Dict[str, Any]
    ) -> PydanticConstrainedQuantumFormatList:
        if len(output_format) != len(set(output_format)):
            raise ValueError(
                f"output_format={output_format}\n"
                "has at least one format that appears twice or more"
            )

        service_provider = values.get("backend_service_provider")
        if service_provider is None:
            return output_format

        provider_format = _SERVICE_PROVIDER_TO_FORMAT.get(service_provider)
        if provider_format is not None and provider_format not in output_format:
            output_format.append(provider_format)

        return output_format

    @pydantic.root_validator()
    def validate_backend(cls, values):
        backend_name = values.get("backend_name")
        backend_service_provider = values.get("backend_service_provider")
        if (backend_name is None) != (backend_service_provider is None):
            raise ValueError(BACKEND_VALIDATION_ERROR_MESSAGE)
        return values

    @property
    def backend_preferences(self) -> Optional[BackendPreferences]:
        if self.backend_name is None or self.backend_service_provider is None:
            return None
        if self._backend_preferences is None:
            self._backend_preferences = BackendPreferences(
                backend_name=self.backend_name,
                backend_service_provider=self.backend_service_provider,
            )
        return self._backend_preferences
