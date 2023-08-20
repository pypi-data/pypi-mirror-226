__version__ = "0.1.0"

from engine.web3_provider import Web3Provider
from engine.scan_token import ScanToken
from engine.contract_identifier import ContractIdentifier


async def scan_eth_contract(
    ETHER_MAINNET_WEB3_RPC_URL: str,
    MORALIS_API_KEY: str,
    ALCHEMY_API_KEY: str,
    Contract_Address: str,
):
    web3_provider = Web3Provider(ETHER_MAINNET_WEB3_RPC_URL)

    ci = ContractIdentifier(web3_provider, MORALIS_API_KEY)
    st = ScanToken(web3_provider, MORALIS_API_KEY, ALCHEMY_API_KEY)

    contractInfo = await ci.contract_type(Contract_Address)
    contractType = contractInfo.contract_type
    isProxy = contractInfo.is_proxy
    if contractType == "ERC-20" and isProxy == False:
        return await st.scan_erc20(contractInfo)
    elif contractType == "ERC-20" and isProxy == True:
        return await st.scan_proxy_erc20(contractInfo)
    elif contractType == "ERC-721":
        return await st.scan_erc721(contractInfo)
    elif contractType == "ERC-1155":
        return await st.scan_erc1155(contractInfo)
    else:
        return "Not Token"
