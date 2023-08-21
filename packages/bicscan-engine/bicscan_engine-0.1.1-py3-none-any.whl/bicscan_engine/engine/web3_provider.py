from web3 import Web3

# settings= Settings() / web3_provider = Web3Provider(settings.ETHER_MAINNET_WEB3_RPC_URL)
class Web3Provider:
    def __init__(self, mainnet: str):
        self.web3 = Web3(Web3.HTTPProvider(mainnet))

    def get_web3(self) -> Web3:
        return self.web3