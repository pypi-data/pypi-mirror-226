from typing import Any, Callable, Dict, Optional, get_origin

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

from classiq.exceptions import ClassiqError
from classiq.pyqmod.declaration_inferrer import infer_func_decl
from classiq.pyqmod.qmod_parameter import QParam
from classiq.pyqmod.qmod_variable import QVar
from classiq.pyqmod.quantum_callable import QCallable, all_decl_arg_names
from classiq.pyqmod.quantum_expandable import QExpandable, QTerminalCallable


def _validate_no_gen_params(annotations: Dict[str, Any]) -> None:
    if not all(
        name == "return"
        or get_origin(annotation) in {QParam, QCallable}
        or QVar.is_qvar_type(annotation)
        for name, annotation in annotations.items()
    ):
        raise ClassiqError(f"{QFunc.__name__} with generative parameters not supported")


def _lookup_qfunc(name: str) -> Optional[QuantumFunctionDeclaration]:
    # FIXME: to be generalized to existing user-defined functions
    return QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.get(name)


def create_model(
    entry_point: "QFunc",
    constraints: Optional[Constraints] = None,
    execution_preferences: Optional[ExecutionPreferences] = None,
    preferences: Optional[Preferences] = None,
) -> SerializedModel:
    return entry_point.create_model(
        constraints, execution_preferences, preferences
    ).get_model()


class QFunc(QExpandable):
    _NATIVE_DEFS: Dict[str, NativeFunctionDefinition] = dict()

    def __init__(self, py_callable: Callable) -> None:
        _validate_no_gen_params(py_callable.__annotations__)
        if _lookup_qfunc(py_callable.__name__) is not None:
            raise ValueError(
                f"Cannot redefine existing quantum function {py_callable.__name__!r}"
            )
        super().__init__(infer_func_decl(py_callable), py_callable)

    def __call__(self, *args, **kwargs) -> None:
        super().__call__(*args, **kwargs)
        self._add_native_func_def()

    def create_model(
        self,
        constraints: Optional[Constraints] = None,
        execution_preferences: Optional[ExecutionPreferences] = None,
        preferences: Optional[Preferences] = None,
    ) -> Model:
        self._add_native_func_def()
        return Model(
            functions=list(QFunc._NATIVE_DEFS.values()),
            constraints=constraints or Constraints(),
            execution_preferences=execution_preferences or ExecutionPreferences(),
            preferences=preferences or Preferences(),
        )

    def _add_native_func_def(self) -> None:
        if self._decl.name in self._NATIVE_DEFS:
            return
        self._NATIVE_DEFS[self._decl.name] = NativeFunctionDefinition(
            **self._decl.__dict__, local_handles=self.local_handles, body=self.body
        )


class ExternalQFunc(QTerminalCallable):
    def __init__(self, py_callable: Callable) -> None:
        decl = _lookup_qfunc(py_callable.__name__)
        if decl is None:
            raise ValueError(f"Definition of {py_callable.__name__!r} not found")

        py_callable.__annotations__.pop("return", None)
        if (
            py_callable.__annotations__
            and set(all_decl_arg_names(decl)) != py_callable.__annotations__.keys()
        ):
            raise ValueError(
                f"Parameter type hints for {py_callable.__name__!r} do not match imported declaration"
            )
        super().__init__(decl)
