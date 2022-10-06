// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Interfaces.sol";

import "@openzeppelin/contracts/utils/Strings.sol";

contract Airline is IAirline {
    string private airlineName;
    string private airlineCode;
    string private airlineEmail;
    address private airlineId;
    uint16 private flightsCount;
    mapping(string => mapping(string => address[])) private flights; // _flightOrigin => _flightDestination => _flightIds
    address[] private flightIds;

    constructor(address _ownerId, string memory _airlineName, string memory _airlineCode, string memory _airlineEmail) {
        airlineName = _airlineName;
        airlineCode = _airlineCode;
        airlineEmail = _airlineEmail;
        airlineId = _ownerId;
    }

    function getAirlineId() external override view returns (address) {
        return airlineId;
    }

    function registerFlight(uint16 _flightNumber, string memory _flightOrigin, string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, uint16 _flightSeats,uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs,
    uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs ) external override returns (address) {
        require(_flightNumber > 0, "Flight number must be greater than 0");
        require(bytes(_flightOrigin).length > 0, "Flight origin cannot be empty");
        require(bytes(_flightDestination).length > 0, "Flight destination cannot be empty");
        require(_flightDepartureTime > 0, "Flight departure time must be greater than 0");
        require(_flightArrivalTime > 0, "Flight arrival time must be greater than 0");
        require(_flightSeats > 0, "Flight seats must be greater than 0");

        IFlight _flight = new Flight(address(this), _flightNumber, _flightOrigin, _flightDestination, _flightDepartureTime, _flightArrivalTime, _flightSeats, _cancellationPenaltyPerc2to8hrs, _cancellationPenaltyPerc8to16hrs, _cancellationPenaltyPerc16to24hrs, _cancellationPenaltyPercGT24hrs);
        address _flightId = _flight.getFlightId();
        flights[_flightOrigin][_flightDestination].push(_flightId);
        flightIds.push(_flightId);
        flightsCount++;
        return _flightId;
    }

    function getFlights(string memory _flightOrigin, string memory _flightDestination) external override view returns (address[] memory) {
        return flights[_flightOrigin][_flightDestination];
    }

    function getAllFlights() external override view returns (address[] memory) {
       return flightIds;
    }

    function reserveSeats(address _flightId, string[] memory _seats) external override returns (Seat[] memory) {
        require(_flightId != address(0), "Flight id cannot be 0");

        IFlight _flight = IFlight(_flightId);
        require(address(_flight) != address(0), "Flight id is not valid!");
        require(_flight.getAvailableSeats().length >= _seats.length, "Flight does not have enough seats");

        return _flight.reserveSeats(_seats);
    }

    function setFlightStatus(address _flightId, uint8 _flightStatus) external override returns (bool) {
        require(_flightId != address(0), "Flight id cannot be 0");
        require(msg.sender == airlineId, "Only the owner can set flight status!");
        
        IFlight _flight = IFlight(_flightId);
        require(address(_flight) != address(0), "Flight id is not valid!");

        return _flight.setFlightStatus(_flightStatus);
    }
}


contract Flight is IFlight {
    uint16 private flightNumber;
    address private flightId;
    uint8 flightStatus;
    address private flightAirlineId;
    string private flightOrigin;
    string private flightDestination;
    uint private flightDepartureTime;
    uint private flightArrivalTime;
    string[] private flightSeats;
    uint8 private cancellationPenaltyPerc2to8hrs;
    uint8 private cancellationPenaltyPerc8to16hrs;
    uint8  private cancellationPenaltyPerc16to24hrs;
    uint8  private cancellationPenaltyPercGT24hrs;
    mapping(string => Seat) private seats; // _seatNumber => Seat

    constructor(address _flightAirlineId, uint16 _flightNumber, string memory _flightOrigin, 
    string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, 
    uint16 _seatsCount, uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs,
    uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs) {
        flightNumber =  _flightNumber;
        flightAirlineId = _flightAirlineId;
        flightOrigin = _flightOrigin;
        flightDestination = _flightDestination;
        flightDepartureTime = _flightDepartureTime;
        flightArrivalTime = _flightArrivalTime;
        flightStatus = uint8(FLIGHT_STATUS.ON_TIME);
        cancellationPenaltyPerc2to8hrs = _cancellationPenaltyPerc2to8hrs;
        cancellationPenaltyPerc8to16hrs = _cancellationPenaltyPerc8to16hrs;
        cancellationPenaltyPerc16to24hrs = _cancellationPenaltyPerc16to24hrs;
        cancellationPenaltyPercGT24hrs = _cancellationPenaltyPercGT24hrs;
        
        populateSeats(_seatsCount);
    }

    function populateSeats(uint16 _seatsCount) private {
        flightSeats = new string[](_seatsCount);

        string memory _seatNumber;
        for (uint i = 0; i < _seatsCount; i++) {
            if (i < _seatsCount / 10) {
                _seatNumber = string(bytes.concat(bytes(Strings.toString(i + 1)), "B")); // Business Class -> 1B, 2B, 3B, ...
                flightSeats[i] = _seatNumber;
                seats[_seatNumber] = Seat(_seatNumber, 2 ether, false);
            } else {
                _seatNumber = string(bytes.concat(bytes(Strings.toString(i + 1)), "E")); // Economy Class -> 11E, 12E, 13E, ...
                flightSeats[i] = _seatNumber;
                seats[_seatNumber] = Seat(_seatNumber, 1 ether, false);
            }
        }
    }

    function getFlightId() external override view returns (address) {
        return address(this);
    }

    function getFlightAirlineId() external override view returns (address) {
        return flightAirlineId;
    }

    function getFlightDepartureTime() external override view returns (uint) {
        return flightDepartureTime;
    }

    function getFlightArrivalTime() external override view returns (uint) {
        return flightArrivalTime;
    }

    function getFlightStatus() external override view returns (uint8) {
        return flightStatus;
    }

    function getCancellationPenaltyPerc2to8hrs() external override view returns (uint8) {
        return cancellationPenaltyPerc2to8hrs;
    }

    function getCancellationPenaltyPerc8to16hrs() external override view returns (uint8) {
        return cancellationPenaltyPerc8to16hrs;
    }

    function getCancellationPenaltyPerc16to24hrs() external override view returns (uint8) {
        return cancellationPenaltyPerc16to24hrs;
    }

    function getCancellationPenaltyPercGT24hrs() external override view returns (uint8) {
        return cancellationPenaltyPercGT24hrs;
    }

    function setFlightStatus(uint8 _flightStatus) external override returns (bool) {
        require(_flightStatus == uint8(FLIGHT_STATUS.ON_TIME) || _flightStatus == uint8(FLIGHT_STATUS.DELAYED) || _flightStatus == uint8(FLIGHT_STATUS.CANCELLED) || _flightStatus == uint8(FLIGHT_STATUS.ARRIVED), "Flight status must be ON_TIME, DELAYED, CANCELLED or ARRIVED");
        flightStatus = _flightStatus;

        return true;
    }

    function getAvailableSeats() external override view returns (string[] memory) {
        uint16 _seatsCount = uint16(flightSeats.length);
        string[] memory _availableSeats = new string[](_seatsCount);

        for (uint i = 0; i < _seatsCount; i++) {
            if (seats[flightSeats[i]].reserved) {
                continue;
            }
            _availableSeats[i] = flightSeats[i];
        }

        return _availableSeats;
    }

    function reserveSeats(string[] memory _seats) external override returns (Seat[] memory) {
        for (uint i = 0; i < _seats.length; i++) {
            require(seats[_seats[i]].reserved == false, "Seat is already reserved");
        }

        Seat[] memory _reservedSeats =  new Seat[](_seats.length);

        for (uint i = 0; i < _seats.length; i++) {
            seats[_seats[i]].reserved = true;
            _reservedSeats[i] = seats[_seats[i]];
        }

        return _reservedSeats;
    }

    function unreserveSeats(Seat[] memory _seats) external override returns (bool) {
        for (uint i = 0; i < _seats.length; i++) {
            require(seats[_seats[i].seat].reserved == true, "Seat is not reserved");
        }

        for (uint i = 0; i < _seats.length; i++) {
            seats[_seats[i].seat].reserved = false;
        }

        return true;
    }

    function getReservationValue(string[] memory _seats) external override view returns (uint) {
        require(_seats.length > 0, "Seats cannot be empty");
        uint _bookingPrice = 0;

        for (uint i = 0; i < _seats.length; i++) {
            _bookingPrice += seats[_seats[i]].price;
        }

        return _bookingPrice;
    }
}

contract AirlineFactory is IAirlineFactory {
    mapping(string => address) private airlines; // _airlineCode => _airlineId
    address private owner;

    // Function to update registry
    function updateRegistry(address _registryAddress) external override {
        IFactoryRegistry _factoryRegistry = IFactoryRegistry(_registryAddress);
        require(address(_factoryRegistry) != address(0), "Registry address is not valid!");
        require(_factoryRegistry.getRegistryOwner() == msg.sender, "Only the owner can update the registry!");

        _factoryRegistry.registerFactory("AirlineFactory", address(this));
    }

    function registerAirline(string memory _airlineName, string memory _airlineCode, string memory _airlineEmail) external override returns (address) {
        require(airlines[_airlineCode] == address(0), "Airline already exists!");
        require(bytes(_airlineName).length > 0 && bytes(_airlineCode).length > 0 && bytes(_airlineEmail).length > 0, "Airline name, code or email cannot be empty");

        IAirline _airline = new Airline(msg.sender, _airlineName, _airlineCode, _airlineEmail);
        address _airlineId = address(_airline);
        airlines[_airlineCode] = _airlineId;

        return _airlineId;
    }

    function registerFlight(address _airlineId, uint16 _flightNumber, string memory _flightOrigin, string memory _flightDestination, uint _flightDepartureTime, uint _flightArrivalTime, uint16 _flightSeats, 
    uint8 _cancellationPenaltyPerc2to8hrs, uint8 _cancellationPenaltyPerc8to16hrs, uint8 _cancellationPenaltyPerc16to24hrs, uint8 _cancellationPenaltyPercGT24hrs) external override returns (address) {
        IAirline _airline = IAirline(_airlineId);
        return _airline.registerFlight(_flightNumber, _flightOrigin, _flightDestination, _flightDepartureTime, _flightArrivalTime, _flightSeats, _cancellationPenaltyPerc2to8hrs, _cancellationPenaltyPerc8to16hrs, _cancellationPenaltyPerc16to24hrs, _cancellationPenaltyPercGT24hrs);
    }
}