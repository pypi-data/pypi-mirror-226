from engine.web3_provider import Web3Provider
from engine.contract_identifier import (
    ContractIdentifier,
    ContractTypeResult,
    ProxyContractTypeResult,
)
from engine.bytecode_checker import BytecodeChecker
from engine.trust_verifier_checker import TrustVerifierChecker
from engine.checklist import ERC20_CHECKLIST, ERC721_CHECKLIST, ERC1155_CHECKLIST
from engine.schemas import (
    TokenInfoResult,
    NFTInfoResult,
    ProxyTokenInfoResult,
    ProxyNFTInfoResult,
)


class ScanToken:
    def __init__(self, web3_provider: Web3Provider, moralis_api_key, alchemy_api_key):
        self.web3_provider = web3_provider
        self.ci = ContractIdentifier(
            web3_provider=self.web3_provider, moralis_api_key=moralis_api_key
        )
        self.bc = BytecodeChecker()
        self.tvc = TrustVerifierChecker(
            web3_provider=self.web3_provider, alchemy_api_key=alchemy_api_key
        )
        self.web3 = self.web3_provider.get_web3()

    async def scan_erc20(self, contractInfo: ContractTypeResult):
        contractAddress = contractInfo.contract_address

        moralisInfo = await self.ci.get_erc20_info_moralis(
            contractAddress=contractAddress, chain="eth"
        )
        bytecode = self.web3.eth.get_code(contractAddress).hex()
        eip20_standard = await self.bc.check_bytecode_elements(
            bytecode=bytecode, check_list=ERC20_CHECKLIST
        )
        eip20_ismint = await self.bc.check_bytecode_ismint(bytecode=bytecode)
        eip20_ispause = await self.bc.check_bytecode_ispause(bytecode=bytecode)

        is_above_threshold_transfer_10000 = (
            await self.tvc.get_erc20_total_transfer_transaction(
                contractAddress=contractAddress
            )
        )
        is_pair_uniswap_v2 = await self.tvc.get_pair_uniswap_v2_eth(
            contractAddress=contractAddress
        )
        is_pool_uniswap_v3 = await self.tvc.get_pool_uniswap_v3_eth(
            contractAddress=contractAddress
        )

        result_data = {
            "contract_type": "ERC-20",
            "eip20_standard": eip20_standard,
            "eip20_ismint": eip20_ismint,
            "eip20_ispause": eip20_ispause,
            "is_proxy": contractInfo.is_proxy,
            "token_name": moralisInfo.get("token_name", "null"),
            "token_symbol": moralisInfo.get("token_symbol", "null"),
            "spam_from_moralis": moralisInfo.get("is_spam", "null"),
            "is_above_threshold_transfer_10000": is_above_threshold_transfer_10000,
            "last_transfer": moralisInfo.get("last_transfer", "null"),
            "is_pair_uniswap_v2": is_pair_uniswap_v2,
            "is_pool_uniswap_v3": is_pool_uniswap_v3,
        }

        result = TokenInfoResult(**result_data)
        return result.json()

    async def scan_proxy_erc20(self, contractInfo: ProxyContractTypeResult):
        contractAddress = contractInfo.contract_address
        logicAddress = contractInfo.logic_contract_address

        moralisInfo = await self.ci.get_erc20_info_moralis(
            contractAddress=contractAddress, chain="eth"
        )
        bytecode = self.web3.eth.get_code(logicAddress).hex()
        eip20_standard = await self.bc.check_bytecode_elements(
            bytecode=bytecode, check_list=ERC20_CHECKLIST
        )
        eip20_ismint = await self.bc.check_bytecode_ismint(bytecode=bytecode)
        eip20_ispause = await self.bc.check_bytecode_ispause(bytecode=bytecode)

        is_above_threshold_transfer_10000 = (
            await self.tvc.get_erc20_total_transfer_transaction(
                contractAddress=contractAddress
            )
        )
        is_pair_uniswap_v2 = await self.tvc.get_pair_uniswap_v2_eth(
            contractAddress=contractAddress
        )
        is_pool_uniswap_v3 = await self.tvc.get_pool_uniswap_v3_eth(
            contractAddress=contractAddress
        )

        result_data = {
            "contract_type": "ERC-20",
            "eip20_standard": eip20_standard,
            "eip20_ismint": eip20_ismint,
            "eip20_ispause": eip20_ispause,
            "is_proxy": contractInfo.is_proxy,
            "logic_contract": logicAddress,
            "token_name": moralisInfo.get("token_name", "null"),
            "token_symbol": moralisInfo.get("token_symbol", "null"),
            "spam_from_moralis": moralisInfo.get("is_spam", "null"),
            "is_above_threshold_transfer_10000": is_above_threshold_transfer_10000,
            "last_transfer": moralisInfo.get("last_transfer", "null"),
            "is_pair_uniswap_v2": is_pair_uniswap_v2,
            "is_pool_uniswap_v3": is_pool_uniswap_v3,
        }

        result = ProxyTokenInfoResult(**result_data)
        return result.json()

    async def scan_nft(self, contractInfo: ContractTypeResult, checklist):
        contractAddress = contractInfo.contract_address
        contract_type = contractInfo.contract_type
        bytecode = self.web3.eth.get_code(contractAddress).hex()
        tokenUri = await self.ci.get_nfturi(
            contractAddress=contractAddress, contractType=contract_type
        )
        moralisInfo = await self.ci.get_nft_info_moralis(
            contractAddress=contractAddress, chain="eth"
        )
        eip_standard = await self.bc.check_bytecode_elements(
            bytecode=bytecode, check_list=checklist
        )
        is_above_threshold_transfer_10000 = (
            await self.tvc.get_nft_total_transfer_transaction(
                contractAddress=contractAddress, contractType=contract_type
            )
        )
        tokenUriInfo = await self.tvc.fetch_nft_info(nftUri=tokenUri)

        result_data = {
            "contract_type": contract_type,
            "eip_standard": eip_standard,
            "nft_name": await self.ci.get_nft_name(contractAddress=contractAddress),
            "is_proxy": contractInfo.is_proxy,
            "spam_from_moralis": moralisInfo.get("is_spam", "null"),
            "spam_from_alchemy": await self.tvc.is_nft_spam_alchemy(
                contractAddress=contractAddress, chain="eth"
            ),
            "is_above_threshold_transfer_10000": is_above_threshold_transfer_10000,
            "token_uri_metadata_extraction": tokenUriInfo[
                "token_uri_metadata_extraction"
            ],
            "token_uri_access_within_timeframe": tokenUriInfo[
                "token_uri_access_within_timeframe"
            ],
            "token_uri_storage_ipfs": tokenUriInfo["token_uri_storage_ipfs"],
            "token_uri_https": tokenUriInfo["token_uri_https"],
            "img_uri_storage_ipfs": tokenUriInfo["img_uri_storage_ipfs"],
            "img_uri_https": tokenUriInfo["img_uri_https"],
        }
        result = NFTInfoResult(**result_data)
        return result.json()

    async def proxy_scan_nft(self, contractInfo: ProxyContractTypeResult, checklist):
        contractAddress = contractInfo.contract_address
        contract_type = contractInfo.contract_type
        logicAddress = contractInfo.logic_contract_address
        bytecode = self.web3.eth.get_code(logicAddress).hex()
        tokenUri = await self.ci.get_nfturi(
            contractAddress=contractAddress, contractType=contract_type
        )
        moralisInfo = await self.ci.get_nft_info_moralis(
            contractAddress=contractAddress, chain="eth"
        )
        eip_standard = await self.bc.check_bytecode_elements(
            bytecode=bytecode, check_list=checklist
        )
        is_above_threshold_transfer_10000 = (
            await self.tvc.get_nft_total_transfer_transaction(
                contractAddress=contractAddress, contractType=contract_type
            )
        )
        tokenUriInfo = await self.tvc.fetch_nft_info(nftUri=tokenUri)

        result_data = {
            "contract_type": contract_type,
            "eip_standard": eip_standard,
            "is_proxy": contractInfo.is_proxy,
            "logic_contract": logicAddress,
            "nft_name": await self.ci.get_nft_name(contractAddress=contractAddress),
            "spam_from_moralis": moralisInfo.get("is_spam", "null"),
            "spam_from_alchemy": await self.tvc.is_nft_spam_alchemy(
                contractAddress=contractAddress, chain="eth"
            ),
            "is_above_threshold_transfer_10000": is_above_threshold_transfer_10000,
            "token_uri_metadata_extraction": tokenUriInfo[
                "token_uri_metadata_extraction"
            ],
            "token_uri_access_within_timeframe": tokenUriInfo[
                "token_uri_access_within_timeframe"
            ],
            "token_uri_storage_ipfs": tokenUriInfo["token_uri_storage_ipfs"],
            "token_uri_https": tokenUriInfo["token_uri_https"],
            "img_uri_storage_ipfs": tokenUriInfo["img_uri_storage_ipfs"],
            "img_uri_https": tokenUriInfo["img_uri_https"],
        }
        result = ProxyNFTInfoResult(**result_data)
        return result.json()

    async def scan_erc721(self, contractInfo):
        isProxy = contractInfo.is_proxy
        if isProxy:
            return await self.proxy_scan_nft(contractInfo, ERC721_CHECKLIST)
        else:
            return await self.scan_nft(contractInfo, ERC721_CHECKLIST)

    async def scan_erc1155(self, contractInfo):
        isProxy = contractInfo.is_proxy
        if isProxy:
            return await self.proxy_scan_nft(contractInfo, ERC1155_CHECKLIST)
        else:
            return await self.scan_nft(contractInfo, ERC1155_CHECKLIST)
