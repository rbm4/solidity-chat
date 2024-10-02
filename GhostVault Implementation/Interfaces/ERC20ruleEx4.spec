// A witness with several function calls.
rule satisfyWithManyOps(){
    env e; env e1; env e2; env e3;
    address recipient; uint amount;

    requireInvariant totalSupplyIsSumOfBalances();
    // The following two requirement are to avoid overflow exmaples.
    require to_mathint(balanceOf(e.msg.sender)) > e.msg.value + 10 * amount;
    require balanceOf(recipient) + amount < max_uint;
    require e.msg.sender != 0;
    require recipient != 0;
    deposit(e1);
    depositTo(e2, recipient, amount);
    transfer(e3, recipient, amount);
    assert totalSupply() > 0;  
}