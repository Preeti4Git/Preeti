# Ticketing Management System
## A blockchain based ticket management system for airlines

### Deployable Contracts

- AirlineFactory.sol
- BookingFactory.sol
- CustomerFactory.sol
- TicketingPlatform.sol

### Other Contracts

- Airline (AirlineFactory.sol)
- Flight (AirlineFactory.sol)
- Customer (CustomerFactory.sol)
- Booking (BookingFactory.sol)
- FactoryRegistry (FactoryRegistry.sol)

### Tech

The Ticketing Management System uses Blockchain for allowing both Airlines and Customers manage their bookings - while ensuring transparency.

The Booking contract is the intermediary between an Airline and the Customer - and acts as an escrow account.

### Installation Instructions

1. Deploy the TicketingPlatform contract
2. Deploy the factories - AirlineFactory, BookingFactory, CustomerFactory
3. Get the FactoryRegistry's address by calling getRegistryAddress of TicketingPlatform (copy the address)
4. Update the registry address from each of the factories by calling updateRegistry (use the copied address from step 3)
