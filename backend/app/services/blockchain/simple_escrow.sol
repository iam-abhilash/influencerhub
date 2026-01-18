// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title InfluencerEscrow
 * @dev A minimal escrow contract controlled by a Backend Authority.
 *      It DOES NOT require Brands/Influencers to sign transactions.
 *      Funds (MATIC) are deposited by the Backend Wallet (on behalf of users)
 *      and released to Influencers upon off-chain completion verification.
 */
contract InfluencerEscrow {
    
    address public backendAuthority; // The wallet controlled by FastAPI

    enum CampaignStatus { Created, Locked, Released, Refunded }

    struct Campaign {
        string offChainId;      // UUID from Postgres
        address influencer;     // The Influencer's received address
        uint256 amount;         // Amount in Wei (if crypto used) or 0 (if just record keeping)
        CampaignStatus status;
        uint256 createdAt;
    }

    // Mapping from Postgres UUID (hashed or string) to Campaign
    mapping(string => Campaign) public campaigns;

    event CampaignCreated(string indexed offChainId, address indexed influencer, uint256 amount);
    event CampaignReleased(string indexed offChainId, address indexed influencer, uint256 amount);
    event CampaignRefunded(string indexed offChainId, uint256 amount);

    modifier onlyAuthority() {
        require(msg.sender == backendAuthority, "Only Backend can call this");
        _;
    }

    constructor() {
        backendAuthority = msg.sender;
    }

    // 1. Create Escrow (Backend locks funds or records agreement)
    function createCampaign(string memory _offChainId, address _influencer) public payable onlyAuthority {
        require(campaigns[_offChainId].createdAt == 0, "Campaign already exists");

        campaigns[_offChainId] = Campaign({
            offChainId: _offChainId,
            influencer: _influencer,
            amount: msg.value,
            status: CampaignStatus.Locked,
            createdAt: block.timestamp
        });

        emit CampaignCreated(_offChainId, _influencer, msg.value);
    }

    // 2. Release Funds (Backend verifies work completed off-chain)
    function releaseFunds(string memory _offChainId) public onlyAuthority {
        Campaign storage c = campaigns[_offChainId];
        require(c.status == CampaignStatus.Locked, "Invalid status");

        c.status = CampaignStatus.Released;
        
        // Transfer MATIC to influencer
        if (c.amount > 0) {
            payable(c.influencer).transfer(c.amount);
        }

        emit CampaignReleased(_offChainId, c.influencer, c.amount);
    }
}
