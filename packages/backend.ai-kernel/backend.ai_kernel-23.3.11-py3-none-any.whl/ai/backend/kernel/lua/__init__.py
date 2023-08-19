import logging
import tempfile
from pathlib import Path

from .. import BaseRunner

log = logging.getLogger()


class Runner(BaseRunner):
    log_prefix = "lua-kernel"
    default_runtime_path = "/usr/local/bin/lua"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def init_with_loop(self):
        pass

    async def build_heuristic(self) -> int:
        log.info("no build process for lua language")
        return 0

    async def execute_heuristic(self) -> int:
        if Path("main.lua").is_file():
            cmd = [str(self.runtime_path), "main.lua"]
            return await self.run_subproc(cmd)
        else:
            log.error('cannot find executable ("main.lua").')
            return 127

    async def query(self, code_text) -> int:
        with tempfile.NamedTemporaryFile(suffix=".lua", dir=".") as tmpf:
            tmpf.write(code_text.encode("utf8"))
            tmpf.flush()
            cmd = [str(self.runtime_path), tmpf.name]
            return await self.run_subproc(cmd)

    async def complete(self, data):
        return []

    async def interrupt(self):
        # subproc interrupt is already handled by BaseRunner
        pass

    async def start_service(self, service_info):
        return None, {}
