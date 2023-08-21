__version__ = "0.1.2"

from .engine.web3_provider import Web3Provider
from .engine.scan_token import ScanToken
from .engine.contract_identifier import ContractIdentifier


class BicScanEngine:
    def __init__(
        self, eth_mainnet_web3_rpc_url: str, moralis_api_key: str, alchemy_api_key: str
    ):
        self.eth_mainnet_web3_rpc_url = eth_mainnet_web3_rpc_url
        self.moralis_api_key = moralis_api_key
        self.alchemy_api_key = alchemy_api_key

        self.web3_provider = Web3Provider(self.eth_mainnet_web3_rpc_url)
        self.contract_identifier = ContractIdentifier(
            self.web3_provider, self.moralis_api_key
        )
        self.scan_token = ScanToken(
            self.web3_provider, self.moralis_api_key, self.alchemy_api_key
        )

    async def scan_eth_contract(self, contract_address: str):
        contract_info = await self.contract_identifier.contract_type(contract_address)
        contract_type = contract_info.contract_type
        is_proxy = contract_info.is_proxy

        if contract_type == "ERC-20" and not is_proxy:
            return await self.scan_token.scan_erc20(contract_info)
        elif contract_type == "ERC-20" and is_proxy:
            return await self.scan_token.scan_proxy_erc20(contract_info)
        elif contract_type == "ERC-721":
            return await self.scan_token.scan_erc721(contract_info)
        elif contract_type == "ERC-1155":
            return await self.scan_token.scan_erc1155(contract_info)
        else:
            return "Not Token"
