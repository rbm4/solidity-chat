

methods {
    function balanceOf(address)         external returns(uint) envfree;
    function allowance(address,address) external returns(uint) envfree;
    function totalSupply()              external returns(uint) envfree;
    function add(uint256 x, uint256 y)  external returns(uint256) envfree;          
}
//// ## Part 3: Ghosts and Hooks ///////////////////////////////////////////////

persistent ghost mathint sum_of_balances {
    init_state axiom sum_of_balances == 0;
}

hook Sstore _balances[KEY address a] uint new_value (uint old_value) {
    // when balance changes, update ghost
    sum_of_balances = sum_of_balances + new_value - old_value;
}

// This `sload` makes `sum_of_balances >= to_mathint(balance)` hold at the beginning of each rule.
hook Sload uint256 balance _balances[KEY address a]  {
  require sum_of_balances >= to_mathint(balance);
}

//// ## Part 4: Invariants

/** `totalSupply()` returns the sum of `balanceOf(u)` over all users `u`. */
invariant totalSupplyIsSumOfBalances()
    to_mathint(totalSupply()) == sum_of_balances;

// satisfy examples
// Generate an example trace for a first deposit operation that succeeds.
rule satisfyFirstDepositSucceeds(){
    env e;
    require totalSupply() == 0;
    deposit(e);
    satisfy totalSupply() == e.msg.value;
}

// Generate an example trace for a withdraw that results totalSupply == 0.
rule satisfyLastWithdrawSucceeds() {
    env e;
    uint256 amount;
    requireInvariant totalSupplyIsSumOfBalances();
    require totalSupply() > 0;
    withdraw(e, amount);
    satisfy totalSupply() == 0;
}

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



// A non-vacuous example where transfer() does not revert.
rule satisfyVacuityCorrection {
    env e; address recip; uint amount;

    require balanceOf(e.msg.sender) > 0;

    transfer(e, recip, amount);

    satisfy balanceOf(e.msg.sender) == 0;
}