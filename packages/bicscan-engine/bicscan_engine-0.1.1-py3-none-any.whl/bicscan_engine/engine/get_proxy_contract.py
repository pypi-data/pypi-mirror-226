# 프록시 컨트랙트의 로직 컨트랙트 주소 구하기
from engine.web3_provider import Web3Provider  # Web3Provider 클래스를 가져옴


class GetProxyContract:
    def __init__(self, web3_provider: Web3Provider):
        self.web3_provider = web3_provider

    async def is_proxy_transparent_func_call(self, contractAddress: str) -> str:
        try:
            web3 = self.web3_provider.get_web3()
            abi = [
                {
                    "constant": True,
                    "inputs": [],
                    "name": "implementation",
                    "outputs": [{"name": "", "type": "address"}],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function",
                }
            ]
            contract = web3.eth.contract(address=contractAddress, abi=abi)
            result = contract.functions.implementation().call()
            return result
        except Exception as e:
            print("Error occurred:", e)
            return False

    async def _get_formatted_logic_contract(
        self, contractAddress: str, slot: str
    ) -> str:
        web3 = self.web3_provider.get_web3()
        logicContract = web3.eth.get_storage_at(contractAddress, slot)
        hexLogicContract = web3.to_hex(logicContract)
        formattedLogicContract = hexLogicContract[0:2] + hexLogicContract[26:]
        return formattedLogicContract

    async def is_unstructured_storage_proxy_call(self, contractAddress: str):
        try:
            slot = "7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3"
            formattedLogicContract = await self._get_formatted_logic_contract(
                contractAddress, slot
            )
            return (
                formattedLogicContract
                if formattedLogicContract
                != "0x0000000000000000000000000000000000000000"
                else False
            )
        except Exception as e:
            print("Error occurred:", e)
            return False

    async def is_transparent_proxy_call(self, contractAddress: str):
        try:
            slot_first = (
                "b53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"
            )
            formattedLogicContract_first = await self._get_formatted_logic_contract(
                contractAddress, slot_first
            )
            if (
                formattedLogicContract_first
                != "0x0000000000000000000000000000000000000000"
            ):
                return formattedLogicContract_first

            slot_second = (
                "360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
            )
            formattedLogicContract_second = await self._get_formatted_logic_contract(
                contractAddress, slot_second
            )
            return (
                formattedLogicContract_second
                if formattedLogicContract_second
                != "0x0000000000000000000000000000000000000000"
                else False
            )
        except Exception as e:
            print("Error occurred:", e)
            return False

    async def is_universal_upgradeable_proxy_call(self, contractAddress: str):
        try:
            slot = "c5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7"
            formattedLogicContract = await self._get_formatted_logic_contract(
                contractAddress, slot
            )
            return (
                formattedLogicContract
                if formattedLogicContract
                != "0x0000000000000000000000000000000000000000"
                else False
            )
        except Exception as e:
            print("Error occurred:", e)
            return False
