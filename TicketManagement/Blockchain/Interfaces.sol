// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/* 
    Interface for Factory Registry - FactoryRegistry.sol
*/
interface IFactoryRegistry {
    function registerFactory(string memory _factoryName, address _factoryAddress) external;
    function getFactory(string memory _factoryName) external view returns (address);
    function getRegistryOwner() external view returns (address);
}

/* 
    Interface for all Factories - CustomerFactory (CustomerFactory.sol), AirlinesFactory (AirlineFactory.sol), etc.
*/
interface IFactory {
    function updateRegistry(address _registryAddress) external;
}

/* 
    Interface for Customer contract - CustomerFactory.sol
*/
interface ICustomer {
    function getCustomerId() external view returns (address);
    function getCustomerName() external view returns (string memory);
    function getCustomerEmail() external view returns (string memory);
}

/* 
    Interface for CustomerFactory - CustomerFactory.sol
*/
interface ICustomerFactory is IFactory {
    function registerCustomer(string memory _customerName, string memory _customerEmail) external returns (address);
}

/* 
    Interface for Airline contract - AirlineFactory.sol
*/
interface IAirline {
    function getAirlineId() external view returns (address);
    function registerFlight(uint16 _flightNumber, string memory _flightOrigin, string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, uint16 _flightSeats,  uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs, uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs) external returns (address);
    function getFlights(string memory _flightOrigin, string memory _flightDestination) external view returns (address[] memory);
    function getAllFlights() external view returns (address[] memory);
    function reserveSeats(address _flightId, string[] memory _seats) external returns (Seat[] memory);
    function setFlightStatus(address _flightId, uint8 _flightStatus) external returns (bool);
}

/*
    Interface for Flight contract - AirlineFactory.sol
*/
interface IFlight {
    function getFlightId() external view returns (address);
    function getFlightAirlineId() external view returns (address);
    function getFlightStatus() external view returns (uint8);
    function setFlightStatus(uint8 _flightStatus) external returns (bool);
    function getFlightDepartureTime() external view returns (uint);
    function getFlightArrivalTime() external view returns (uint);
    function getAvailableSeats() external view returns (string[] memory);
    function reserveSeats(string[] memory _seats) external returns (Seat[] memory);
    function unreserveSeats(Seat[] memory _seats) external returns (bool);
    function getReservationValue(string[] memory _seats) external view returns (uint);
    function getCancellationPenaltyPerc2to8hrs() external view returns (uint8);
    function getCancellationPenaltyPerc8to16hrs() external view returns (uint8);
    function getCancellationPenaltyPerc16to24hrs() external view returns (uint8);
    function getCancellationPenaltyPercGT24hrs() external view returns (uint8);
}

struct Seat {
    string seat;
    uint price;
    bool reserved;
}

enum FLIGHT_STATUS {
    ON_TIME,
    DELAYED,
    CANCELLED,
    ARRIVED
}

enum BOOKING_STATUS {
    PENDING,
    CONFIRMED,
    CANCELLED,
    REFUNDED 
}

/* 
    Interface for AirlineFactory - AirlineFactory.sol
*/
interface IAirlineFactory is IFactory {
    function registerAirline(string memory _airlineName, string memory _airlineCode, string memory _airlineEmail) external returns (address);
    function registerFlight(address _airlineId, uint16 _flightNumber, string memory _flightOrigin, string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, uint16 _flightSeats, uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs, uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs) external returns (address);
}

/*
    Interface for Booking contract - BookingFactory.sol
*/
interface IBooking {
    function getBookingId() external view returns (address);
    function cancelBooking(address _senderId) external returns (bool);
    function refundBooking(address _senderId) external returns (bool);
    function getCustomerId() external view returns (address);
    function getBookingTotalPrice() external view returns (uint256);
    function getBookingStatus() external view returns (uint8);
    function getCreationTime() external view returns (uint);
    function getBookingExpirationTime() external view returns (uint);
    function confirmBooking(address _senderId) external returns (bool);
}

/*
    Interface for BookingFactory - BookingFactory.sol
*/
interface IBookingFactory is IFactory {
    function makeBooking(address _customerId, address _flightId, string[] memory _seats) external payable returns (address);
    function getBookings(address _customerId) external view returns (address[] memory);
}

/*
    Interface for TicketingPlatform - TicketingPlatform.sol
*/
interface ITicketingPlatform {
    function registerCustomer(string memory _customerName, string memory _customerEmail) external returns (address);
    function registerAirline(string memory _airlineName, string memory _airlineCode, string memory _airlineEmail) external returns (address);
    function registerFlight(string memory _airlineCode, uint16 _flightNumber, string memory _flightOrigin, string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, uint16 _flightSeats, uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs, uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs) external returns (address);
    function getAllFlights(string memory _airlineCode) external view returns (address[] memory);
    function getFlights(string memory _airlineCode, string memory _flightOrigin, string memory _flightDestination) external view returns (address[] memory);
    function getAvailableSeats(address _flightId) external view returns (string[] memory);
    function getFlightStatus(address _flightId) external view returns (uint8);
    function setFlightStatus(address _flightId, uint8 _flightStatus) external returns (bool);
    function makeBooking(string memory _customerEmail, address _flightId, string[] memory _seats) external payable returns (address);
    function cancelBooking(address _bookingId) external returns (bool);
    function refundBooking(address _bookingId) external returns (bool);
}