// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Interfaces.sol";

contract FactoryRegistry is IFactoryRegistry {
    mapping(string => address) private contracts;
    address private owner;

    constructor(address _senderId) {
        owner = _senderId;
    }

    function registerFactory(string memory _factoryName, address _factoryAddress) external override {
        require(_factoryAddress != address(0), "Contract address cannot be 0");
        // require(msg.sender == owner, "Only the owner can register a factory!");

        contracts[_factoryName] = _factoryAddress;
    }

    function getFactory(string memory _factoryName) external override view returns (address) {
        return contracts[_factoryName];
    }

    function getRegistryOwner() external override view returns (address) {
        return owner;
    }
}