from engine.web3_provider import Web3Provider
from engine.bytecode_checker import BytecodeChecker
from moralis import evm_api
from engine.checklist import SIMPLE_ERC20_CHECKLIST
from engine.get_proxy_contract import GetProxyContract
import asyncio
from pydantic import BaseModel


class ContractTypeResult(BaseModel):
    contract_type: str
    is_proxy: bool
    contract_address: str


class ProxyContractTypeResult(BaseModel):
    contract_type: str
    is_proxy: bool
    contract_address: str
    logic_contract_address: str


class ContractIdentifier:
    def __init__(self, web3_provider: Web3Provider, moralis_api_key):
        self.headers = {"accept": "application/json"}
        self.web3_provider = web3_provider
        self.moralis_api_key = moralis_api_key

    async def is_erc20(self, contractAddress: str) -> bool:
        bc = BytecodeChecker()
        web3 = self.web3_provider.get_web3()
        bytecode = web3.eth.get_code(contractAddress).hex()
        iserc20 = await bc.check_bytecode_elements(
            bytecode=bytecode, check_list=SIMPLE_ERC20_CHECKLIST
        )
        if iserc20 == True:
            return True
        else:
            return False

    # eth, polygon, klaytn
    async def is_erc721(self, contractAddress: str) -> bool:
        web3 = self.web3_provider.get_web3()
        abi = [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        contract = web3.eth.contract(address=contractAddress, abi=abi)
        try:
            result = contract.functions.supportsInterface("0x80ac58cd").call()
        except Exception:
            result = False
        return result

    # eth, polygon, klaytn
    async def is_erc1155(self, contractAddress: str) -> bool:
        web3 = self.web3_provider.get_web3()
        abi = [
            {
                "inputs": [
                    {"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}
                ],
                "name": "supportsInterface",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        contract = web3.eth.contract(address=contractAddress, abi=abi)
        try:
            result = contract.functions.supportsInterface("0xd9b67a26").call()
        except Exception:
            result = False
        return result

    # eth, polygon
    async def get_erc20_info_moralis(self, contractAddress: str, chain: str):
        params = {"address": contractAddress, "chain": chain}  # eth,
        result = evm_api.token.get_token_transfers(
            api_key=self.moralis_api_key, params=params
        )
        if "result" in result and len(result["result"]) > 0:
            token_data = {
                "token_name": result["result"][0]["token_name"],
                "token_symbol": result["result"][0]["token_symbol"],
                "last_transfer": result["result"][0]["block_timestamp"],
                "is_spam": result["result"][0]["possible_spam"],
            }

            return token_data
        else:
            return False

    async def get_nft_name(self, contractAddress: str) -> str:
        web3 = self.web3_provider.get_web3()
        abi = [
            {
                "inputs": [],
                "name": "name",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        contract = web3.eth.contract(address=contractAddress, abi=abi)
        try:
            result = contract.functions.name().call()
        except Exception:
            result = "None"
        return result

    async def get_nfturi(self, contractAddress: str, contractType: str) -> str:
        web3 = self.web3_provider.get_web3()
        nftAbi = [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        mtAbi = [
            {
                "inputs": [
                    {"internalType": "uint256", "name": "id", "type": "uint256"}
                ],
                "name": "uri",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        if contractType == "ERC-721":
            contract = web3.eth.contract(address=contractAddress, abi=nftAbi)
            for token_id in range(100):
                try:
                    result = contract.functions.tokenURI(token_id).call()
                    if result is not None:
                        return result
                except Exception:
                    continue
            return None
        elif contractType == "ERC-1155":
            contract = web3.eth.contract(address=contractAddress, abi=mtAbi)
            for token_id in range(2):
                try:
                    result = contract.functions.uri(token_id).call()
                    if result is not None:
                        return result
                except Exception:
                    continue
            return None

    # eth, polygon
    async def get_nft_info_moralis(self, contractAddress: str, chain: str):
        params = {"address": contractAddress, "chain": chain}  # eth,
        result = evm_api.nft.get_nft_contract_transfers(
            api_key=self.moralis_api_key, params=params
        )
        if "result" in result and len(result["result"]) > 0:
            token_data = {
                "contract_type": result["result"][0]["contract_type"],
                "is_spam": result["result"][0]["possible_spam"],
            }

            return token_data
        else:
            return False

    # 프록시 컨트랙트의 로직 컨트랙트 주소 반환
    async def identify_proxy_contract(self, contractAddress: str):
        try:
            proxy_checkers = [
                ("is_proxy_transparent_func_call"),
                ("is_unstructured_storage_proxy_call"),
                ("is_transparent_proxy_call"),
                ("is_universal_upgradeable_proxy_call"),
            ]

            pc = GetProxyContract(self.web3_provider)

            async def check_proxy_type(checker_method):
                result = await getattr(pc, checker_method)(contractAddress)
                if result != "None":
                    return result
                return None

            tasks = [
                check_proxy_type(checker_method) for checker_method in proxy_checkers
            ]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result:
                    return result

            return False
        except Exception as e:
            return False

    # erc20, erc721, erc1155 외의 컨트랙트는 프록시 컨트랙트 체크 후 토큰 타입과 컨트랙트 주소를 반환하게 해야함
    async def identify_contract_type(self, contractAddress: str):
        if await self.is_erc721(contractAddress):
            return "ERC-721"
        elif await self.is_erc20(contractAddress):
            return "ERC-20"
        elif await self.is_erc1155(contractAddress):
            return "ERC-1155"
        else:
            return "Not-Token"

    async def contract_type(self, contractAddress: str):
        web3_provider = self.web3_provider
        web3 = web3_provider.get_web3()
        proxy_logic_address = await self.identify_proxy_contract(contractAddress)
        if proxy_logic_address:
            proxy_logic_address = web3.to_checksum_address(proxy_logic_address)
            contract_info = await self.identify_contract_type(proxy_logic_address)
            result_data = {
                "contract_type": contract_info,
                "is_proxy": True,
                "contract_address": contractAddress,
                "logic_contract_address": proxy_logic_address,
            }
            result = ProxyContractTypeResult(**result_data)
            return result
        contract_info = await self.identify_contract_type(contractAddress)
        if contract_info != "Not-Token":
            result_data = {
                "contract_type": contract_info,
                "is_proxy": False,
                "contract_address": contractAddress,
            }
            result = ContractTypeResult(**result_data)
            return result
        return None
