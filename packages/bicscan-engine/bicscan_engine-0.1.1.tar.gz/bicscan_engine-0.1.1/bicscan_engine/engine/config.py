import pydantic
import dotenv

dotenv.load_dotenv()


class Settings(pydantic.BaseSettings):
    ETHER_MAINNET_WEB3_RPC_URL: str = pydantic.Field(
        default="local", env="ETHER_MAINNET_WEB3_RPC_URL"
    )
    POLYGON_MAINNET_WEB3_RPC_URL: str = pydantic.Field(
        default="local", env="POLYGON_MAINNET_WEB3_RPC_URL"
    )
    KLAYTN_CYPRESS_WEB3_RPC_URL: str = pydantic.Field(
        default="local", env="KLAYTN_CYPRESS_WEB3_RPC_URL"
    )
    MORALIS_API_KEY: str = pydantic.Field(default="local", env="MORALIS_API_KEY")
    ALCHEMY_API_KEY: str = pydantic.Field(default="local", env="ALCHEMY_API_KEY")
