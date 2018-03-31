pragma solidity ^0.4.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Example.sol";

contract TestExample {
    Example example = Example(DeployedAddresses.Example());

    function testSimple(){
        Assert.equal(1, example.get(), "error message");
    }
}
