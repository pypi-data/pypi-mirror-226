# schemas.py
from typing import List, Union, Optional
from pydantic import BaseModel


class TokenInfoResult(BaseModel):
    contract_type: str
    eip20_standard: Union[bool, List[str]]
    eip20_ismint: bool
    eip20_ispause: bool
    is_proxy: bool
    token_name: str
    token_symbol: str
    spam_from_moralis: bool
    is_above_threshold_transfer_10000: Union[bool, str]
    last_transfer: str
    is_pair_uniswap_v2: bool
    is_pool_uniswap_v3: bool


class NFTInfoResult(BaseModel):
    contract_type: str
    eip_standard: Union[bool, List[str]]
    is_proxy: bool
    nft_name: str
    spam_from_moralis: bool
    spam_from_alchemy: bool
    is_above_threshold_transfer_10000: Union[bool, str]
    token_uri_metadata_extraction: Optional[bool]
    token_uri_access_within_timeframe: Optional[str]
    token_uri_storage_ipfs: Optional[bool]
    token_uri_https: Optional[bool]
    img_uri_storage_ipfs: Optional[bool]
    img_uri_https: Optional[bool]


class ProxyTokenInfoResult(BaseModel):
    contract_type: str
    eip20_standard: Union[bool, List[str]]
    eip20_ismint: bool
    eip20_ispause: bool
    is_proxy: bool
    logic_contract: str
    token_name: str
    token_symbol: str
    spam_from_moralis: bool
    is_above_threshold_transfer_10000: Union[bool, str]
    last_transfer: str
    is_pair_uniswap_v2: bool
    is_pool_uniswap_v3: bool


class ProxyNFTInfoResult(BaseModel):
    contract_type: str
    eip_standard: Union[bool, List[str]]
    is_proxy: bool
    logic_contract: str
    nft_name: str
    spam_from_moralis: bool
    spam_from_alchemy: bool
    is_above_threshold_transfer_10000: Union[bool, str]
    token_uri_metadata_extraction: Optional[bool]
    token_uri_access_within_timeframe: Optional[str]
    token_uri_storage_ipfs: Optional[bool]
    token_uri_https: Optional[bool]
    img_uri_storage_ipfs: Optional[bool]
    img_uri_https: Optional[bool]
