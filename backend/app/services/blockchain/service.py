from web3 import Web3
from app.core.config import settings
import json
import os

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
        self.account = None
        if settings.WALLET_PRIVATE_KEY:
            self.account = self.w3.eth.account.from_key(settings.WALLET_PRIVATE_KEY)
        
        self.contract_address = settings.CONTRACT_ADDRESS
        # In real app, load ABI from json file
        self.abi = [] 

    def is_connected(self) -> bool:
        return self.w3.is_connected()

    def create_record(self, campaign_id: str, influencer_address: str, amount_wei: int = 0) -> str:
        """
        Sends a transaction to the smart contract to record a new campaign.
        Returns the Transaction Hash.
        """
        if not self.account or not self.contract_address:
            raise Exception("Blockchain misconfigured")

        # Mock Contract Function Call
        # contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        # tx = contract.functions.createCampaign(campaign_id, influencer_address).build_transaction({
        #     'from': self.account.address,
        #     'nonce': self.w3.eth.get_transaction_count(self.account.address),
        #     'value': amount_wei,
        #     'gas': 200000,
        #     'gasPrice': self.w3.to_wei('50', 'gwei')
        # })
        
        # signed_tx = self.w3.eth.account.sign_transaction(tx, settings.WALLET_PRIVATE_KEY)
        # tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # return self.w3.to_hex(tx_hash)
        
        return "0x_mock_transaction_hash"

blockchain_service = BlockchainService()
