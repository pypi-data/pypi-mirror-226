# bytecode_checker.py
from typing import List, Dict, Union

# 바이트 코드 검사
# 체크리스트 검사 후 바이트코드에 없는 체크 리스트 반환
class BytecodeChecker:
    # eth, polygon, klaytn 
    async def check_bytecode_elements(self, bytecode: str, check_list: Dict[str, str]) -> Union[bool, List[str]]:
        missing_elements = [function_name for bytecode_hex, function_name in check_list.items() if bytecode_hex not in bytecode]
        if not missing_elements:
            return True
        else:
             return missing_elements
    # erc20
    async def check_bytecode_ismint(self, bytecode: str) -> bool:
        return "40c10f19" in bytecode
    # erc20
    async def check_bytecode_ispause(self, bytecode: str) -> bool:
        return "8456cb59" in bytecode