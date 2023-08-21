from engine.web3_provider import Web3Provider
import requests
import aiohttp
import time
from engine.config import Settings
from pydantic import BaseModel
from engine.util import Utils
import json
from typing import Optional
import re


class TokenUriResult(BaseModel):
    token_uri_metadata_extraction: Optional[bool]
    token_uri_access_within_timeframe: Optional[str]
    token_uri_storage_ipfs: Optional[bool]
    token_uri_https: Optional[bool]
    img_uri_storage_ipfs: Optional[bool]
    img_uri_https: Optional[bool]


class TrustVerifierChecker:
    def __init__(self, web3_provider: Web3Provider, alchemy_api_key):
        self.web3_provider = web3_provider
        self.headers = {"accept": "application/json"}
        self.alchemy_api_key = alchemy_api_key

    def is_eth_open_contract(self, contractAddress: str):
        res = requests.get(self.url, headers=self.headers)
        return res

    # eth,
    async def get_erc20_total_transfer_transaction(self, contractAddress: str):
        try:
            web3 = self.web3_provider.get_web3()
            abi = [
                {
                    "anonymous": False,
                    "inputs": [
                        {"indexed": True, "name": "from", "type": "address"},
                        {"indexed": True, "name": "to", "type": "address"},
                        {"indexed": False, "name": "value", "type": "uint256"},
                    ],
                    "name": "Transfer",
                    "type": "event",
                }
            ]
            contract = web3.eth.contract(address=contractAddress, abi=abi)
            event_filter = contract.events.Transfer.create_filter(
                fromBlock="earliest", toBlock="latest"
            )
            transfer_events = event_filter.get_all_entries()
            return len(transfer_events)
        except Exception as e:
            if "query returned more than 10000 results" in str(e):
                return True
            print("Error occurred:", e)
            return None

    # 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f v2 factory / 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 WETH ADDRESS
    # erc20, eth
    async def get_pair_uniswap_v2_eth(self, contractAddress: str):
        web3 = self.web3_provider.get_web3()
        abi = [
            {
                "constant": True,
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                ],
                "name": "getPair",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            }
        ]
        contract = web3.eth.contract(
            address="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f", abi=abi
        )
        pairAddress = contract.functions.getPair(
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", contractAddress
        ).call()
        if pairAddress == "0x0000000000000000000000000000000000000000":
            return False
        elif pairAddress != "0x0000000000000000000000000000000000000000":
            return True

    # erc20, eth
    async def get_pool_uniswap_v3_eth(self, contractAddress: str):
        web3 = self.web3_provider.get_web3()
        abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "address", "name": "", "type": "address"},
                    {"internalType": "uint24", "name": "", "type": "uint24"},
                ],
                "name": "getPool",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        contract = web3.eth.contract(
            address="0x1F98431c8aD98523631AE4a59f267346ea31F984", abi=abi
        )
        poolAddress = contract.functions.getPool(
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", contractAddress, 10000
        ).call()
        if poolAddress == "0x0000000000000000000000000000000000000000":
            return False
        elif poolAddress != "0x0000000000000000000000000000000000000000":
            return True

    async def fetch_nft_info(self, nftUri: str):
        try:
            if nftUri.startswith("ipfs://"):
                ipfs_hash = re.sub(r"^ipfs://", "", nftUri)
                nftUri = f"https://ipfs.io/ipfs/{ipfs_hash}"
            else:
                nftUri = nftUri
        except Exception as e:
            nftUri = nftUri
        print(nftUri)
        try:
            async with aiohttp.ClientSession() as session:
                startTime = time.time()
                async with session.get(nftUri) as response:
                    elapsedTime = time.time() - startTime
                    if response.status == 200:
                        data = await response.json()
                        imageUri = data.get("image", "")
                        result_data = {
                            "token_uri_metadata_extraction": True,
                            "token_uri_access_within_timeframe": elapsedTime,
                            "token_uri_storage_ipfs": Utils.is_ipfs_uri(nftUri),
                            "token_uri_https": Utils.is_https_uri(nftUri),
                            "img_uri_storage_ipfs": Utils.is_ipfs_uri(imageUri),
                            "img_uri_https": Utils.is_https_uri(imageUri),
                        }
                        result = TokenUriResult(**result_data)
                        result_json = json.loads(result.json())
                        return result_json
                    else:
                        result_data = {
                            "token_uri_metadata_extraction": False,
                            "token_uri_access_within_timeframe": None,
                            "token_uri_storage_ipfs": None,
                            "token_uri_https": None,
                            "img_uri_storage_ipfs": None,
                            "img_uri_https": None,
                        }
                        result = TokenUriResult(**result_data)
                        result_json = json.loads(result.json())
                        return result_json
        except Exception as e:
            result_data = {
                "token_uri_metadata_extraction": False,
                "token_uri_access_within_timeframe": None,
                "token_uri_storage_ipfs": None,
                "token_uri_https": None,
                "img_uri_storage_ipfs": None,
                "img_uri_https": None,
            }
            result = TokenUriResult(**result_data)
            result_json = json.loads(result.json())
            return result_json

    async def get_nft_total_transfer_transaction(
        self, contractAddress: str, contractType: str
    ):
        web3 = self.web3_provider.get_web3()
        nftAbi = [
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "from", "type": "address"},
                    {"indexed": True, "name": "to", "type": "address"},
                    {"indexed": True, "name": "tokenId", "type": "uint256"},
                ],
                "name": "Transfer",
                "type": "event",
            }
        ]
        mtAbi = [
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "_operator",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "_from",
                        "type": "address",
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "_to",
                        "type": "address",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_id",
                        "type": "uint256",
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "_value",
                        "type": "uint256",
                    },
                ],
                "name": "TransferSingle",
                "type": "event",
            }
        ]
        if contractType == "ERC-721":
            try:
                contract = web3.eth.contract(address=contractAddress, abi=nftAbi)
                event_filter = contract.events.Transfer.create_filter(
                    fromBlock="earliest", toBlock="latest"
                )
                transfer_events = event_filter.get_all_entries()
                return len(transfer_events)
            except Exception as e:
                if "query returned more than 10000 results" in str(e):
                    return True
                print("Error occurred:", e)
                return "None"
        elif contractType == "ERC-1155":
            try:
                contract = web3.eth.contract(address=contractAddress, abi=mtAbi)
                event_filter = contract.events.TransferSingle.create_filter(
                    fromBlock="earliest", toBlock="latest"
                )
                transfer_events = event_filter.get_all_entries()
                return len(transfer_events)
            except Exception as e:
                if "query returned more than 10000 results" in str(e):
                    return True
                print("Error occurred:", e)
                return "None"

    # eth, polygon
    async def is_nft_spam_alchemy(self, contractAddress: str, chain: str):
        baseurl = "https://{chain}-mainnet.g.alchemy.com/nft/v2/{api_key}/isSpamContract?contractAddress={address}"
        url = baseurl.format(
            chain=chain, address=contractAddress, api_key=self.alchemy_api_key
        )
        res = requests.get(url, self.headers)
        return res.text
