// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract demo {
  string a;

  function scan(string memory b) public{
    a=b;
  }

  function print() public view returns(string memory){
    return(a);
  }
}
