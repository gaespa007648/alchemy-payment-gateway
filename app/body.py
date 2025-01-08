from pydantic import BaseModel, field_validator
from typing_extensions import Self
from app.tool import is_hex_address
import app.config as config

class Transfer(BaseModel):
    address: str
    amount: int
    
    @field_validator('address')
    @classmethod
    def address_rules(cls, v: str):
        if is_hex_address(v) == False:
            raise ValueError('Invalid address. Address should start with 0x and have 40 hex characters.')
        return v
    
    @field_validator('amount')
    @classmethod
    def amount_rules(cls, v: int):
        if v <= 0 or v>config.MAX_REWARD_AMOUNT:
            raise ValueError(f'Invalid amount. Amount should large than 0 or less than {config.MAX_REWARD_AMOUNT}.')
        return v