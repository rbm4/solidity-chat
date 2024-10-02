// Generate an example trace for a first deposit operation that succeeds.
rule satisfyFirstDepositSucceeds(){
    env e;
    require totalSupply() == 0;
    deposit(e);
    satisfy totalSupply() == e.msg.value;
}