/// If `approve` changes a holder's allowance, then it was called by the holder
rule onlyHolderCanChangeAllowance {
    address holder; address spender;

    mathint allowance_before = allowance(holder, spender);
    method f; env e; calldataarg args; // was: env e; uint256 amount;
    f(e, args);                        // was: approve(e, spender, amount);

    mathint allowance_after = allowance(holder, spender);

    assert allowance_after > allowance_before => e.msg.sender == holder,
        "approve must only change the sender's allowance";

    assert allowance_after > allowance_before =>
        (f.selector == sig:approve(address,uint).selector || f.selector == sig:increaseAllowance(address,uint).selector),
        "only approve and increaseAllowance can increase allowances";
}