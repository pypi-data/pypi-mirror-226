from acryl.executor.execution.executor import Executor
from acryl.executor.request.execution_request import ExecutionRequest
from acryl.executor.request.signal_request import SignalRequest
from acryl.executor.result.execution_result import ExecutionResult


class IgnoreExecutor(Executor):
    """Ignores CLI Execution Requests"""

    def __init__(self, id: str) -> None:
        self.id = id

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        pass

    def signal(self, request: SignalRequest) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def get_id(self) -> str:
        return self.id
