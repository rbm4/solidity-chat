methods {
    // Assuming you have defined your Solidity contract with ERC4626 methods
    function deposit(uint256 assets, address receiver) external returns(uint256);
    function mint(uint256 shares, address receiver) external returns(uint256);
    function withdraw(uint256 assets, address receiver, address owner) external returns(uint256);
    function redeem(uint256 shares, address receiver, address owner) external returns(uint256);
}

//// ## Part 1: Basic Rules ////////////////////////////////////////////////////

/// Deposit must increase the total supply and the sender's balance after the deposit
rule depositSpec {
    address caller; address receiver; uint256 assets; uint256 expectedShares;
    
    env e;
    require e.msg.sender == caller;

    uint256 beforeSupply = totalSupply();
    uint256 beforeBalanceSender = balanceOf(caller);
    uint256 beforeBalanceReceiver = balanceOf(receiver);

    expectedShares = convertToShares(assets);
    deposit(assets, receiver);

    uint256 afterSupply = totalSupply();
    uint256 afterBalanceSender = balanceOf(caller);
    uint256 afterBalanceReceiver = balanceOf(receiver);

    assert afterSupply == beforeSupply + expectedShares,
        "deposit should increase the total supply";
    assert afterBalanceSender == beforeBalanceSender - assets,
        "deposit should decrease the sender's balance by the deposited assets";
    assert afterBalanceReceiver == beforeBalanceReceiver + expectedShares,
        "deposit should increase the recipient's balance by the corresponding shares";
}

/// Withdraw must decrease the total supply and the sender's balance after the withdrawal
rule withdrawalSpec {
    address owner; address recipient; uint256 assets; uint256 expectedShares;

    env e;
    require e.msg.sender == owner;

    uint256 beforeSupply = totalSupply();
    uint256 beforeBalanceOwner = balanceOf(owner);
    uint256 beforeBalanceRecipient = balanceOf(recipient);

    expectedShares = convertToShares(assets);
    withdraw(assets, recipient, owner);

    uint256 afterSupply = totalSupply();
    uint256 afterBalanceOwner = balanceOf(owner);
    uint256 afterBalanceRecipient = balanceOf(recipient);

    assert afterSupply == beforeSupply - expectedShares,
        "withdrawal should decrease the total supply";
    assert afterBalanceOwner == beforeBalanceOwner - assets,
        "withdrawal should decrease the sender's balance by the withdrawn assets";
    assert afterBalanceRecipient == beforeBalanceRecipient + assets,
        "withdrawal should increase the recipient's balance by the withdrawn assets";
}

/// Redemption must decrease the total supply and the sender's balance after the redemption
rule redemptionSpec {
    address owner; address recipient; uint256 shares; uint256 expectedAssets;

    env e;
    require e.msg.sender == owner;

    uint256 beforeSupply = totalSupply();
    uint256 beforeBalanceOwner = balanceOf(owner);
    uint256 beforeBalanceRecipient = balanceOf(recipient);

    expectedAssets = convertToAssets(shares);
    redeem(shares, recipient, owner);

    uint256 afterSupply = totalSupply();
    uint256 afterBalanceOwner = balanceOf(owner);
    uint256 afterBalanceRecipient = balanceOf(recipient);

    assert afterSupply == beforeSupply - shares,
        "redemption should decrease the total supply";
    assert afterBalanceOwner == beforeBalanceOwner - shares,
        "redemption should decrease the sender's balance by the redeemed shares";
    assert afterBalanceRecipient == beforeBalanceRecipient + expectedAssets,
        "redemption should increase the recipient's balance by the corresponding assets";
}

/// Withdrawal must revert if the user doesn't have enough assets
rule withdrawalRevertsOnInsufficientAssets {
    env e; address owner; uint256 assets;

    require balanceOf(owner) < assets;

    withdraw(assets, e.msg.sender, owner);
    assert lastReverted,
        "withdrawal must revert if the user doesn't have enough assets";
}

/// Redemption must revert if the user doesn't have enough shares
rule redemptionRevertsOnInsufficientShares {
    env e; address owner; uint256 shares;

    require balanceOf(owner) < shares;

    redeem(shares, e.msg.sender, owner);
    assert lastReverted,
        "redemption must revert if the user doesn't have enough shares";
}