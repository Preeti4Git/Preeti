// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Interfaces.sol";

contract Customer is ICustomer { 
    string private customerName;
    string private customerEmail;
    address private customerId;
    constructor(address _customerId, string memory _customerName, string memory _customerEmail) {
        customerName = _customerName;
        customerEmail = _customerEmail;
        customerId = _customerId;
    }

    function getCustomerId() external override view returns (address) {
        return customerId;
    }

    function getCustomerName() external override view returns (string memory) {
        return customerName;
    }

    function getCustomerEmail() external override view returns (string memory) {
        return customerEmail;
    }
}

contract CustomerFactory is ICustomerFactory {
    mapping(string => address) private customers; // customerEmail => customerId
    address private owner;

    // Function to update registry
    function updateRegistry(address _registryAddress) external override {
        require(_registryAddress != address(0), "Registry address cannot be 0");

        IFactoryRegistry _factoryRegistry = IFactoryRegistry(_registryAddress);
        require(address(_factoryRegistry) != address(0), "Registry address is not valid!");
        require(_factoryRegistry.getRegistryOwner() == msg.sender, "Only the owner can update the registry!");

        _factoryRegistry.registerFactory("CustomerFactory", address(this));
    }

    function registerCustomer(string memory _customerName, string memory _customerEmail) external override returns (address) {
        ICustomer customer = new Customer(msg.sender, _customerName, _customerEmail);
        address _customerAddress = address(customer);
        customers[_customerEmail] = _customerAddress;

        return _customerAddress;
    }
}