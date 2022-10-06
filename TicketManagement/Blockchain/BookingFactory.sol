// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Interfaces.sol";

contract Booking is IBooking {
    address private customerId;
    address private flightId;
    Seat[] private seats;
    uint256 private bookingTotalPrice;
    uint8 private bookingStatus;
    uint256 private creationTime;
    uint256 private bookingExpirationTime;

    constructor(address _customerId, address _flightId, Seat[] memory _seats) payable {
        customerId = _customerId;
        flightId = _flightId;
        bookingStatus = uint8(BOOKING_STATUS.PENDING);
        creationTime = block.timestamp;
        bookingExpirationTime = block.timestamp + 24*3600; // TODO: Set expiration time to flight arrival time + 24 HRS instead

        copySeats(_seats);
        calculateBookingTotalPrice(_seats);
    }

    receive() external payable {
    }

    function copySeats(Seat[] memory _seats) private {
        for (uint i = 0; i < _seats.length; i++) {
            seats.push(_seats[i]);
        }
    }

    function calculateBookingTotalPrice(Seat[] memory _seats) private {
        uint _totalPrice = 0;
        for(uint i = 0; i < _seats.length; i++) {
            _totalPrice += _seats[i].price;
        }

        bookingTotalPrice =  _totalPrice;
    }

    function getBookingId() external override view returns (address) {
        return address(this);
    }

    function cancelBooking(address _senderId) external override returns (bool) {
        require(block.timestamp < bookingExpirationTime, "Booking is not valid anymore!");
        require(bookingStatus == uint8(BOOKING_STATUS.CONFIRMED), "Booking has either been fulfilled or refunded!");

        if (bookingStatus == uint8(BOOKING_STATUS.CONFIRMED)) {         
            IFlight _flight = IFlight(flightId);
            IAirline _airline = IAirline(_flight.getFlightAirlineId());

            uint _flightDepartureTime = _flight.getFlightDepartureTime();
            
            bool isCustomer = customerId == _senderId;
            bool isAirline = _airline.getAirlineId() == _senderId;

            require(isCustomer || isAirline, "Only the customer or the airline can cancel the booking!");

            if (isCustomer) {
                /*
                    The customer should be able to trigger a cancellation anytime till 2 hours before the flight start time.
                    This should refund money to the customer minus the percentage penalty predefined in the contract by the airlines.
                    The penalty amount should be automatically sent to the airline account.
                */
                require(block.timestamp < _flightDepartureTime - 2*3600, "Cancellation cannot be made in 2 hours before the flight departure time!");
                
                // Add support for multiple cancellation penalties in favour of the airline,
                // and delay penalties in favour of the customer, based on various time ranges in the contract.
                uint timeInHours = (_flightDepartureTime - block.timestamp) / 3600;
                uint8 _cancellationPenaltyPerc = 0;
                if (timeInHours < 8) { // 2-8 hours left for departure
                    _cancellationPenaltyPerc = _flight.getCancellationPenaltyPerc2to8hrs();
                } else if (timeInHours < 16) { // 8-16 hours left for departure
                   _cancellationPenaltyPerc = _flight.getCancellationPenaltyPerc8to16hrs();
                } else if (timeInHours < 24) { // 16-24 hours left for departure
                   _cancellationPenaltyPerc = _flight.getCancellationPenaltyPerc16to24hrs();
                }else { // More than 24 hours left for departure
                    _cancellationPenaltyPerc = _flight.getCancellationPenaltyPercGT24hrs();
                }

                payable(customerId).transfer(bookingTotalPrice * (100 - _cancellationPenaltyPerc)/ 100);
                payable(_airline.getAirlineId()).transfer(bookingTotalPrice * _cancellationPenaltyPerc/ 100);
                bookingStatus = uint8(BOOKING_STATUS.CANCELLED);
                _flight.unreserveSeats(seats);
                return true;
            } else {
                /*
                    Any cancellation triggered by the airline before or after departure time 
                    should result in a complete amount refund to the customer.
                */
                payable(customerId).transfer(bookingTotalPrice);
                bookingStatus = uint8(BOOKING_STATUS.CANCELLED);
                _flight.unreserveSeats(seats);
                return true;
            }
        }
        return false;
    }

    function refundBooking(address _senderId) external override returns (bool) {
        /*
            The airline should update the status of the flight within 24 hours of the flight start time. 
            It can be on-time start, cancelled or delayed.
                
            24 hours after the flight departure time, the customer can trigger a claim function to demand a refund.
        */
        require(customerId == _senderId, "Only the customer can trigger a refund!");
        require(bookingStatus == uint8(BOOKING_STATUS.CONFIRMED), "Booking has either been fulfilled or cancelled!");
        require(block.timestamp < bookingExpirationTime, "Booking is not valid anymore!");

        if (bookingStatus == uint8(BOOKING_STATUS.CONFIRMED)) {
            IFlight _flight = IFlight(flightId);
            IAirline _airline = IAirline(_flight.getFlightAirlineId());

            uint _flightDepartureTime = _flight.getFlightDepartureTime();
            uint8 _flightStatus = _flight.getFlightStatus();
            bool isCustomer = customerId == _senderId;
            uint8 _delayCompensationPerc = 20;

            require(isCustomer, "Only the customer can claim a refund for the booking!");
            require(block.timestamp > _flightDepartureTime + 24*3600, "Only after 24 hours from flight departure!");
            require(_flightStatus != uint8(FLIGHT_STATUS.ARRIVED), "Flight status is not valid!");


            /*
                They should get a complete refund in case of cancellation by the airline. 
                In case of a delay, they should get a predefined percentage amount, and the rest should be sent to the airline.
                
                If the airline hasn’t updated the status within 24 hours of the flight departure time, and a customer claim is made, 
                it should be treated as an airline cancellation case by the contract.
            */
            if (_flightStatus == uint8(FLIGHT_STATUS.CANCELLED) || _flightStatus == uint8(FLIGHT_STATUS.ON_TIME)) {
                payable(customerId).transfer(bookingTotalPrice);

                bookingStatus = uint8(BOOKING_STATUS.REFUNDED);
                return true;
            } else if (_flightStatus == uint8(FLIGHT_STATUS.DELAYED)) {
                payable(customerId).transfer(bookingTotalPrice * _delayCompensationPerc/ 100);
                payable(_airline.getAirlineId()).transfer(bookingTotalPrice * (100-_delayCompensationPerc) / 100);

                bookingStatus = uint8(BOOKING_STATUS.REFUNDED);
                return true;
            }
        }
        
        return false;
    }

    function confirmBooking(address _senderId) external override returns (bool) {
        IFlight _flight = IFlight(flightId);
        IAirline _airline = IAirline(_flight.getFlightAirlineId());

        bool isAirline = _airline.getAirlineId() == _senderId;

        require(isAirline, "Only the airline can confirm the booking!");
        require(bookingStatus == uint8(BOOKING_STATUS.PENDING), "Booking has already been confirmed!");
        require(block.timestamp < bookingExpirationTime, "Booking is not valid anymore!");

        bookingStatus = uint8(BOOKING_STATUS.CONFIRMED);
        return true;
    }

    function getCustomerId() external override view returns (address) {
        return customerId;
    }

    function getReservedseats() external view returns (Seat[] memory) {
        return seats;
    }

    function getBookingStatus() external override view returns (uint8) {
        return bookingStatus;
    }

    function getBookingTotalPrice() external override view returns (uint256) {
        return bookingTotalPrice;
    }

    function getBookingExpirationTime() external override view returns (uint256) {
        return bookingExpirationTime;
    }

    function getCreationTime() external override view returns (uint256) {
        return creationTime;
    }
}


contract BookingFactory is IBookingFactory {
    mapping(address => address[]) private customerBookings; // customerId => bookingIds
    
    // Function to update registry
    function updateRegistry(address _registryAddress) external override {
        require(_registryAddress != address(0), "Registry address cannot be 0");

        IFactoryRegistry _factoryRegistry = IFactoryRegistry(_registryAddress);
        require(address(_factoryRegistry) != address(0), "Registry address is not valid!");
        require(_factoryRegistry.getRegistryOwner() == msg.sender, "Only the owner can update the registry!");

        _factoryRegistry.registerFactory("BookingFactory", address(this));
    }

    function makeBooking(address _customerId, address _flightId, string[] memory _seats) external override payable returns (address) {
        require(_flightId != address(0), "FlightId cannot be 0");
        require(_seats.length > 0, "Seats cannot be empty");

        IFlight _flight = IFlight(_flightId);
        IAirline _airline = IAirline(_flight.getFlightAirlineId());
        require(address(_flight) != address(0), "FlightId is not valid!");

        uint _reservationPrice = _flight.getReservationValue(_seats);
        require(_reservationPrice == msg.value, "Incorrect payment made!");

        Seat[] memory _seatsArray = _flight.reserveSeats(_seats);
        IBooking _booking = new Booking(_customerId, _flightId, _seatsArray);
        (payable(address(_booking))).transfer(msg.value);
        _booking.confirmBooking(_airline.getAirlineId());
        address _bookingId = _booking.getBookingId();
        customerBookings[_customerId].push(_bookingId);

        return _bookingId;
    }

    function getBookings(address _customerId) external override view returns (address[] memory) {
        return customerBookings[_customerId];
    }
}