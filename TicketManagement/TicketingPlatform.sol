// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.6;

contract Ticket{

    enum TicketState{BOOKED, PAID, CANCELLED, REFUNDED, DELAYED}

    struct TicketData {
        address flight;
        address passenger;
        string passenger_name;
        uint8 seatsBooked;
        uint tkt_price;
        TicketState ticketState;
    }

    TicketData _ticketData;

    constructor(address _flight, address _passenger, string memory _passenger_name, uint8 _seatsBooked, uint _tkt_price) {
        _ticketData = TicketData({
                                    flight: _flight,
                                    passenger: _passenger,
                                    passenger_name: _passenger_name,
                                    seatsBooked: _seatsBooked,
                                    tkt_price: _tkt_price,
                                    ticketState: TicketState.BOOKED                                   
                            });
    }

    // Function to receive Ether. msg.data must be empty
    receive() external payable {}

    // Fallback function is called when msg.data is not empty
    fallback() external payable {}

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    /*function bookTicket() public view returns (uint) {
        ticket.TicketState = TicketState.BOOKED;
    }*/
}

contract Passenger{

    //add logic to initialise TicketingPlatform with address at which that contarct is deployed
    TicketingPlatform ticketingPlatform = TicketingPlatform(0x417Bf7C9dc415FEEb693B6FE313d1186C692600F);

    struct PassengerData {
        uint passenger_id; //unique ID of passenger like passport number
        string passenger_name;
    }

    PassengerData _passengerData;

    constructor(uint8 _passenger_id, string memory _passenger_name) {
        _passengerData = PassengerData({
                                    passenger_id: _passenger_id,
                                    passenger_name: _passenger_name
                            });
    }

    function searchFlights(string memory src, string memory dest) public view returns (uint8[] memory){
        uint8[] memory flights = ticketingPlatform.searchFlights(src, dest);
        return flights;
    }

    /*function searchFlightDetails(uint8 flight_id) public returns (uint8[] memory){
        uint8[] memory flights = ticketingPlatform.searchFlightDetails(flight_id);
        return flights;
    }*/

    function getPassengerName() public view returns (string memory){
        return _passengerData.passenger_name ;
    }

    function bookFlight(uint flight_id) public{
        Flight flight ;
    }

    function cancelFlight(uint flight_id) public{

    }

    function claimRefund(uint flight_id) public{

    }
    
}

contract Flight{

    enum FlightStatus {PLANNED, UNKNOWN, ON_TIME, DELAYED, CANCELLED}

    struct FlightData {
        //address airline_address; // Address of the initiator
        uint8 flight_id; // Raw number of initiator's choice - 1 for Rock, 2 for Paper, 3 for Scissors
        //uint8 airline_id;
        uint dep_time;
        uint arr_time;
        string dep_airport;
        string arr_airport;
        uint8 seats;
        uint8 tkt_price;
        FlightStatus status;
    }
    
    FlightData _flightData;
    
    constructor(uint8 _flight_id, uint _dep_time, uint _arr_time, string memory _dep_airport, 
    string memory _arr_airport, uint8 _seats, uint8 _tkt_price) {
        _flightData = FlightData({
                                    flight_id: _flight_id,
                                    dep_time: _dep_time,
                                    arr_time: _arr_time,
                                    dep_airport: _dep_airport,
                                    arr_airport: _arr_airport,
                                    seats: _seats,
                                    tkt_price: _tkt_price,
                                    status: FlightStatus.PLANNED
                            });
    }

    function bookSeat() public{
        require(_flightData.seats > 0, "Flight is already full");
        _flightData.seats -= 1;
    }

    function cancelFlight() public{
        _flightData.status = FlightStatus.CANCELLED;
    }

    function delayFlight() public{
        _flightData.status = FlightStatus.DELAYED;
    }

    function onTimeFlight() public{
        _flightData.status = FlightStatus.ON_TIME;
    }

    function getFlightId() public view returns (uint8 flight_id) {
        return (_flightData.flight_id);
    }

    function getFlightDetails() public view returns (uint8 flight_id, uint dep_time, 
    uint arr_time, string memory dep_airport, string memory arr_airport, uint8 seats, 
    uint8 tkt_price, FlightStatus status) {
        return (_flightData.flight_id, _flightData.dep_time, _flightData.arr_time, 
        _flightData.dep_airport, _flightData.arr_airport, _flightData.seats, 
        _flightData.tkt_price, _flightData.status);
    }

    function getTktPrice() public view returns (uint){
        return _flightData.tkt_price;
    }
}


contract Airline {
    // Mapping for each game instance with the first address being the initiator and internal key aaddress being the responder
    mapping(uint8 => Flight) _flightList;

    struct AirlineData {
        //address airline_address; // Address of the initiator
        uint8 airline_id; // Raw number of initiator's choice - 1 for Rock, 2 for Paper, 3 for Scissors
        string airline_name; // Random string chosen by the initiator
    }
    
    AirlineData _airlineData;
    
    constructor(uint8 _airline_id, string memory _airline_name) {
        _airlineData = AirlineData({
                                    airline_id: _airline_id,
                                    airline_name: _airline_name
                            });
    }
    
    function createFlight(uint8 flight_id, uint dep_time, uint arr_time, 
    string memory dep_airport, string memory arr_airport, uint8 seats, uint8 tkt_price) 
    public returns (Flight){
        //add logic to mandate only airline user can call this function
        Flight flight = new Flight(flight_id, dep_time, arr_time, dep_airport, arr_airport, 
        seats, tkt_price);
        _flightList[flight_id] = flight;
        return flight;
    }

    function searchFlightDetails(uint8 flight_id) public view returns (uint8, uint, uint,
        string memory, string memory, uint8, uint8, Flight.FlightStatus){
        //add logic to mandate who can call this function
        Flight flight = _flightList[flight_id];
        return flight.getFlightDetails();
    }

    function cancelFlight(uint8 flight_id) public{
        Flight flight = _flightList[flight_id];
        flight.cancelFlight();
    }

    function delayFlight(uint8 flight_id) public{
        Flight flight = _flightList[flight_id];
        flight.delayFlight();
    }

    function ontimeFlight(uint8 flight_id) public{
        Flight flight = _flightList[flight_id];
        flight.onTimeFlight();
    }
}

contract TicketingPlatform{
    mapping(uint8 => Airline) _airlinesList;
    mapping(uint8 => Flight) _flightsList;
    mapping(uint8 => Passenger) _passengersList;
    mapping(uint8 => Passenger[]) _flightPassengers;
    mapping(uint8 => mapping(uint8 => Flight)) _airlineFlightMapping;
    mapping(uint8 => mapping(uint8 => Ticket)) _passengerFlightTktMapping;
    //Flights would be internally mapped to airline via this mapping
    mapping(uint8 => uint8) _flightToAirline;
    mapping(string => mapping(string => Flight[])) _SrcDestFlightList;
    
    function registerAirline(uint8 airline_id, string memory airline_name) public{
        //add logic to mandate that only admin type account calls this function
        Airline airline = new Airline(airline_id, airline_name);
        _airlinesList[airline_id] = airline;
    }

    function getAirline(uint8 airline_id) public view returns (Airline) {
        return _airlinesList[airline_id];
    }

    function registerPassenger(uint8 passenger_id, string memory passenger_name) public returns (address){
        //add logic to mandate that only admin type account calls this function
        _passengersList[passenger_id] = new Passenger(passenger_id, passenger_name);
        return address(_passengersList[passenger_id]);
    }

    function createFlight(uint8 airline_id, uint8 flight_id, uint dep_time, uint arr_time, 
    string memory dep_airport, string memory arr_airport, uint8 seats, uint8 tkt_price) public returns (Flight){
        //add logic to mandate only airline user can call this function
        Airline airline = _airlinesList[airline_id];
        Flight flight  = airline.createFlight(flight_id, dep_time, arr_time, dep_airport, 
        arr_airport, seats, tkt_price);
        _SrcDestFlightList[dep_airport][arr_airport].push(flight);
        _flightToAirline[flight_id] = airline_id;
        _flightsList[flight_id] = flight;
        return flight;
    }

    function searchFlights(string memory dep_airport, string memory arr_airport) public view returns (uint8[] memory){
        Flight[] memory flights =  _SrcDestFlightList[dep_airport][arr_airport];
        uint8[] memory flight_ids = new uint8[](flights.length);
        for (uint8 i=0;i < flights.length;i++){
            Flight flight = Flight(flights[i]);
            flight_ids[i] = flight.getFlightId();
        }
        return flight_ids;
    }

    function searchFlightDetails(uint8 flight_id) public view returns  (uint8, uint, uint,
        string memory, string memory, uint8, uint8, Flight.FlightStatus){
        Airline airline = _airlinesList[_flightToAirline[flight_id]];
        return airline.searchFlightDetails(flight_id);

    }

    function bookFlight(uint8 flight_id, uint8 passenger_id, uint8 seats) public returns (Ticket) {
        Passenger passenger = _passengersList[passenger_id];
        Flight flight = _flightsList[flight_id];
        uint tkt_price = flight.getTktPrice();
        Ticket ticket = new Ticket(address(flight), 
        address(passenger), passenger.getPassengerName(), seats, tkt_price);
        _passengerFlightTktMapping[passenger_id][flight_id] = ticket;
        _flightPassengers[flight_id].push(passenger);
        return ticket;
    }

    function cancelFlight(uint8 flight_id) public returns (Passenger[] memory) {
        Flight flight = _flightsList[flight_id];
        flight.cancelFlight();
        Passenger[] memory passengers = _flightPassengers[flight_id];
        return passengers;
        /*for (uint8 i=0;i < passengers.length;i++){
            address _to = address(passengers[i]);
            (bool sent, bytes memory data) = _to.call{value: flight.getTktPrice()}("");
            require(sent, "Failed to send Ether");
        }*/
    }

    function cancelBooking(uint8 flight_id, uint8 passenger_id, uint8 seats) public returns (Ticket) {
        Passenger passenger = _passengersList[passenger_id];
        Flight flight = _flightsList[flight_id];
        uint tkt_price = flight.getTktPrice();
        Ticket ticket = new Ticket(address(flight), 
        address(passenger), passenger.getPassengerName(), seats, tkt_price);
        _passengerFlightTktMapping[passenger_id][flight_id] = ticket;        
        return ticket;        
        //TODO: maintain passenger and flight mapping
    }

    /*struct ConfirmationData {
        string confirmtaion_num;
        uint8 flight_id;
        uint dep_time;
        uint arr_time; 
        string dep_airport; 
        string arr_airport;
        uint8 seats;
        uint8 tkt_price;
        Flight.FlightStatus status;
    }*/

    function sendViaCall(uint8 passenger_id, uint8 flight_id) public payable returns (string memory, uint8){
        // Call returns a boolean value indicating success or failure.
        // This is the current recommended method to use.
        address _to = address(_passengerFlightTktMapping[passenger_id][flight_id]);
        (bool sent, bytes memory data) = _to.call{value: msg.value}("");
        require(sent, "Failed to send Ether");
        Flight flight = _flightsList[flight_id];
        return(string(abi.encodePacked(flight_id, "-", passenger_id)),flight_id);
        //,flight.getFlightDetails());
        //uint8, uint, uint, string memory, string memory, uint8, uint8, Flight.FlightStatus = flight.getFlightDetails());
        //ConfirmationData memory cd;
        //cd.confirmtaion_num = ConfirmationData(string(abi.encodePacked(flight_id, "-", passenger_id)));
        //return (cd);
        //TODO: change tkt status to PAID
        //TODO: can chk tkt balance amount in contract?
    }

    /*function test() public returns(Tuple){
        Flight flight = _flightsList[1];
        /*(uint8 flight_id, uint dep_time, uint arr_time, 
        string memory dep_airport, string memory arr_airport, uint8 seats, 
        uint8 tkt_price, FlightStatus.status) = flight.getFlightDetails();
        return (flight.getFlightDetails());
    }*/

    function checkTktBalance(uint8 passenger_id, uint8 flight_id) public view returns (uint){
        Ticket ticket = _passengerFlightTktMapping[passenger_id][flight_id];
        return ticket.getBalance();
    }
}