import re

def is_hex_address(address):
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))

def is_valid_tid(tid):
    pattern = r'^0x[a-fA-F0-9]{64}$'
    return bool(re.match(pattern, tid))