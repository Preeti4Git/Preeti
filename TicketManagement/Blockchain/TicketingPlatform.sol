// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Interfaces.sol";
import "./FactoryRegistry.sol";

contract TicketingPlatform is ITicketingPlatform {
    address registryAddress;
    mapping(string => address) private customers; // customerEmail => customerId
    mapping(string => address) private airlines; // _airlineCode => _airlineId
    mapping(address => address[]) private customerBookings; // customerId => bookingIds

    constructor() {
        IFactoryRegistry _factoryRegistry = new FactoryRegistry(msg.sender);
        registryAddress = address(_factoryRegistry);

        _factoryRegistry.registerFactory("FactoryRegistry", registryAddress);
    }

    function getCustomerFactory() private view returns (ICustomerFactory) {
        IFactoryRegistry _factories = IFactoryRegistry(registryAddress);
        address _customerFactoryAddress = _factories.getFactory("CustomerFactory");
        require(_customerFactoryAddress != address(0), "CustomerFactory is not registered!");

        return ICustomerFactory(_customerFactoryAddress);
    }

    function getAirlineFactory() private view returns (IAirlineFactory) {
        IFactoryRegistry _factories = IFactoryRegistry(registryAddress);
        address _airlineFactoryAddress = _factories.getFactory("AirlineFactory");
        require(_airlineFactoryAddress != address(0), "AirlineFactory is not registered!");

        return IAirlineFactory(_airlineFactoryAddress);
    }
    
    function getBookingFactory() private view returns (IBookingFactory) {
        IFactoryRegistry _factories = IFactoryRegistry(registryAddress);
        address _bookingFactoryAddress = _factories.getFactory("BookingFactory");
        require(_bookingFactoryAddress != address(0), "BookingFactory is not registered!");

        return IBookingFactory(_bookingFactoryAddress);
    }

    function registerCustomer(string memory _customerName, string memory _customerEmail) external override returns (address) {
        require(customers[_customerEmail] == address(0), "Customer already exists!");
        (, bytes memory result) = address(getCustomerFactory()).delegatecall(abi.encodeWithSignature("registerCustomer(string,string)", _customerName, _customerEmail));
        address _customerId = abi.decode(result, (address));

        customers[_customerEmail] = _customerId;

        return _customerId;
    }

    function registerAirline(string memory _airlineName, string memory _airlineCode, string memory _airlineEmail) external override returns (address) {
        require(airlines[_airlineCode] == address(0), "Airline already exists!");
        (, bytes memory result) = address(getAirlineFactory()).delegatecall(abi.encodeWithSignature("registerAirline(string,string,string)", _airlineName, _airlineCode, _airlineEmail));
        address _airlineId = abi.decode(result, (address));

        airlines[_airlineCode] = _airlineId;

        return _airlineId;
    }

    function registerFlight(string memory _airlineCode, uint16 _flightNumber, string memory _flightOrigin, 
    string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, 
    uint16 _flightSeats, uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs,
    uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs) external override returns (address) {
        IAirlineFactory _airlineFactory = getAirlineFactory();
        IAirline _airline = IAirline(airlines[_airlineCode]);
        require(address(_airline) != address(0), "Airline does not exist!");
        require(_airline.getAirlineId() == msg.sender, "Only airline owner can register flights!");
        require(_cancellationPenaltyPerc2to8hrs<100,  "Cancellation Penalty Percentage should be reviewed!");
        require(_cancellationPenaltyPerc8to16hrs<100, "Cancellation Penalty Percentage should be reviewed!");
        require(_cancellationPenaltyPerc16to24hrs<100, "Cancellation Penalty Percentage should be reviewed!");
        require(_cancellationPenaltyPercGT24hrs<100, "Cancellation Penalty Percentage should be reviewed!");
        require(_flightDepartureTime<_flightArrivalTime, "Inconsistent chronology of Departure & Arrival Time!");

        return _airlineFactory.registerFlight(address(_airline), _flightNumber, _flightOrigin,
         _flightDestination, _flightDepartureTime, _flightArrivalTime, _flightSeats, 
         _cancellationPenaltyPerc2to8hrs, _cancellationPenaltyPerc8to16hrs, _cancellationPenaltyPerc16to24hrs, _cancellationPenaltyPercGT24hrs);
    }

    function getAllFlights(string memory _airlineCode) external override view returns (address[] memory) {
        IAirline _airline = IAirline(airlines[_airlineCode]);
        require(address(_airline) != address(0), "Airline does not exist!");
        
        return _airline.getAllFlights();
    }

    function getFlights(string memory _airlineCode, string memory _flightOrigin, string memory _flightDestination) external override view returns (address[] memory) {
        IAirline _airline = IAirline(airlines[_airlineCode]);
        require(address(_airline) != address(0), "Airline does not exist!");

        return _airline.getFlights(_flightOrigin, _flightDestination);
    }
    
    function getAvailableSeats(address _flightId) external override view returns (string[] memory) {
        IFlight _flight = IFlight(_flightId);
        require(address(_flight) != address(0), "Flight is not registered!");

        return _flight.getAvailableSeats();
    }

    function getFlightStatus(address _flightId) external override view returns (uint8) {
        IFlight _flight = IFlight(_flightId);
        require(address(_flight) != address(0), "Flight is not registered!");

        return _flight.getFlightStatus();
    }

    function setFlightStatus(address _flightId, uint8 _flightStatus) external override returns (bool) {
        IFlight _flight = IFlight(_flightId);
        require(address(_flight) != address(0), "Flight is not registered!");

        return _flight.setFlightStatus(_flightStatus);
    }

    function makeBooking(string memory _customerEmail, address _flightId, string[] memory _seats) external override payable returns (address) {
        ICustomer _customer = ICustomer(customers[_customerEmail]);
        require(address(_customer) != address(0), "Customer is not registered!");
        address _customerId = _customer.getCustomerId();

        require(_customerId == msg.sender, "Not authorized to make a booking!");

        IFlight _flight = IFlight(_flightId);
        require(address(_flight) != address(0), "Flight is not registered!");
        require(_flight.getFlightStatus() == uint8(FLIGHT_STATUS.ON_TIME) || _flight.getFlightStatus() == uint8(FLIGHT_STATUS.DELAYED), "Flight not available for Booking!");

        address _bookingId = getBookingFactory().makeBooking{value: msg.value}(msg.sender, _flightId, _seats);
        customerBookings[_customerId].push(_bookingId);

        return _bookingId;
    }

    function getBookings(string memory _customerEmail) external view returns (address[] memory) {
        ICustomer _customer = ICustomer(customers[_customerEmail]);
        require(address(_customer) != address(0), "Customer is not registered!");
        address _customerId = _customer.getCustomerId();

        return customerBookings[_customerId];
    }

    function cancelBooking(address _bookingId) external override returns (bool) {
        IBooking _booking = IBooking(_bookingId);
        require(address(_booking) != address(0), "Booking does not exist!");

        return _booking.cancelBooking(msg.sender);
    }

    function refundBooking(address _bookingId) external override returns (bool) {
        IBooking _booking = IBooking(_bookingId);
        require(address(_booking) != address(0), "Booking does not exist!");
        return _booking.refundBooking(msg.sender);
    }

    function getRegistryAddress() external view returns (address) {
        return registryAddress;
    }
}