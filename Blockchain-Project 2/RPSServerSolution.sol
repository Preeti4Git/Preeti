// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.6;

contract RPSGame {
    // GameState - INITIATED after inital game setup, RESPONDED after responder adds hash choice, WIN or DRAW after final scoring
    enum RPSGameState {INITIATED, RESPONDED, WIN, DRAW}
    
    // PlayerState - PENDING until they add hashed choice, PLAYED after adding hash choice, CHOICE_STORED once raw choice and random string are stored
    enum PlayerState {PENDING, PLAYED, CHOICE_STORED}
    
    // 0 before choices are stored, 1 for Rock, 2 for Paper, 3 for Scissors. Strings are stored only to generate comment with choice names
    string[4] choiceMap = ['None', 'Rock', 'Paper', 'Scissors'];
    
    struct RPSGameData {
        address initiator; // Address of the initiator
        PlayerState initiator_state; // State of the initiator
        bytes32 initiator_hash; // Hashed choice of the initiator
        uint8 initiator_choice; // Raw number of initiator's choice - 1 for Rock, 2 for Paper, 3 for Scissors
        string initiator_random_str; // Random string chosen by the initiator
        
	address responder; // Address of the responder
        PlayerState responder_state; // State of the responder
        bytes32 responder_hash; // Hashed choice of the responder
        uint8 responder_choice; // Raw number of responder's choice - 1 for Rock, 2 for Paper, 3 for Scissors
        string responder_random_str; // Random string chosen by the responder
                
        RPSGameState state; // Game State
        address winner; // Address of winner after completion. addresss(0) in case of draw
        string comment; // Comment specifying what happened in the game after completion
    }
    
    RPSGameData _gameData;
    
    // Initiator sets up the game and stores its hashed choice in the creation itself. Game and player states are adjusted accordingly
    constructor(address _initiator, address _responder, bytes32 _initiator_hash) {
        _gameData = RPSGameData({
                                    initiator: _initiator,
                                    initiator_state: PlayerState.PLAYED,
                                    initiator_hash: _initiator_hash, 
                                    initiator_choice: 0,
                                    initiator_random_str: '',
                                    responder: _responder, 
                                    responder_state: PlayerState.PENDING,
                                    responder_hash: 0, 
                                    responder_choice: 0,
                                    responder_random_str: '',
                                    state: RPSGameState.INITIATED,
                                    winner: address(0),
                                    comment: ''
                            });
    }
    
    // Responder stores their hashed choice. Game and player states are adjusted accordingly.
    function addResponse(bytes32 _responder_hash) public {
        // Solution to problem 2(c)
        require(_gameData.state == RPSGame.RPSGameState.INITIATED, "Incorrect game state to call this function.");
        _gameData.responder_hash = _responder_hash;
        _gameData.state = RPSGameState.RESPONDED;
        _gameData.responder_state = PlayerState.PLAYED;
    }
    
    // Initiator adds raw choice number and random string. If responder has already done the same, the game should process the completion execution
    function addInitiatorChoice(uint8 _choice, string memory _randomStr) public returns (bool) {
        // Solution to problem 2(c)
        require(_gameData.state == RPSGame.RPSGameState.RESPONDED, "Incorrect game state to call this function.");
        _gameData.initiator_choice = _choice;
        _gameData.initiator_random_str = _randomStr;
        _gameData.initiator_state = PlayerState.CHOICE_STORED;
        if (_gameData.responder_state == PlayerState.CHOICE_STORED) {
            __validateAndExecute();
        }
        return true;
    }

    // Responder adds raw choice number and random string. If initiator has already done the same, the game should process the completion execution
    function addResponderChoice(uint8 _choice, string memory _randomStr) public returns (bool) {
        // Solution to problem 2(c)
        require(_gameData.state == RPSGame.RPSGameState.RESPONDED, "Incorrect game state to call this function.");
        _gameData.responder_choice = _choice;
        _gameData.responder_random_str = _randomStr;
        _gameData.responder_state = PlayerState.CHOICE_STORED;
        if (_gameData.initiator_state == PlayerState.CHOICE_STORED) {
            __validateAndExecute();
        }
        return true;
    }
    
    // Core game logic to check raw choices against stored hashes, and then the actual choice comparison
    // Can be split into multiple functions internally
    function __validateAndExecute() private {
        bytes32 initiatorCalcHash = sha256(abi.encodePacked(choiceMap[_gameData.initiator_choice], '-', _gameData.initiator_random_str));
        bytes32 responderCalcHash = sha256(abi.encodePacked(choiceMap[_gameData.responder_choice], '-', _gameData.responder_random_str));
        bool initiatorAttempt = false;
        bool responderAttempt = false;
        
        if (initiatorCalcHash == _gameData.initiator_hash) {
            initiatorAttempt = true;
        }
        
        if (responderCalcHash == _gameData.responder_hash) {
            responderAttempt = true;
        }

        // Add logic to complete the game first based on attempt validation states, and then based on actual game logic if both attempts are validation
        // Comments can be set appropriately like 'Initator attempt invalid', or 'Scissor beats Paper', etc.
        
        //Solution for problem 1(a)
        if (initiatorAttempt == false && responderAttempt == false) {
            _gameData.state = RPSGameState.DRAW;
            _gameData.winner = address(0);
            _gameData.comment = 'Both initiator and responder attempts are invalid';
        } else if (initiatorAttempt == true && responderAttempt == false) {
            _gameData.state = RPSGameState.WIN;
            _gameData.winner = _gameData.initiator;
            _gameData.comment = 'Responder attempt invalid';
        } else if (initiatorAttempt == false && responderAttempt == true) {
            _gameData.state = RPSGameState.WIN;
            _gameData.winner = _gameData.responder;
            _gameData.comment = 'Initiator attempt invalid';
        //Solution for problem 1(b)
        } else if (initiatorAttempt == true && responderAttempt == true) {
            //DRAW if both initiator and responder have same and valid choice
            if(_gameData.initiator_choice == _gameData.responder_choice) {
                _gameData.state = RPSGameState.DRAW;
                _gameData.winner = address(0);
                _gameData.comment = 'Both initiator and responder have same choice';
            } else if(_gameData.initiator_choice == 1) { //If initiator choses Rock
                if (_gameData.responder_choice == 2) {
                    _gameData.state = RPSGameState.WIN;
                    _gameData.winner = _gameData.responder;
                    _gameData.comment = string(abi.encodePacked(choiceMap[_gameData.responder_choice], ' beats ', choiceMap[_gameData.initiator_choice]));
                } else {
                    _gameData.state = RPSGameState.WIN;
                    _gameData.winner = _gameData.initiator;
                    _gameData.comment = string(abi.encodePacked(choiceMap[_gameData.initiator_choice], ' beats ', choiceMap[_gameData.responder_choice]));
                }
            } else if (_gameData.initiator_choice == 2) {  //If initiator choses Paper
                 if (_gameData.responder_choice == 3) {
                    _gameData.state = RPSGameState.WIN;
                    _gameData.winner = _gameData.responder;
                    _gameData.comment = string(abi.encodePacked(choiceMap[_gameData.responder_choice], ' beats ', choiceMap[_gameData.initiator_choice]));
                } else {
                    _gameData.state = RPSGameState.WIN;
                    _gameData.winner = _gameData.initiator;
                    _gameData.comment = string(abi.encodePacked(choiceMap[_gameData.initiator_choice], ' beats ', choiceMap[_gameData.responder_choice]));
                }
            } else if (_gameData.initiator_choice == 3) {  //If initiator choses Scissors
                 if (_gameData.responder_choice == 1) {
                    _gameData.state = RPSGameState.WIN;
                    _gameData.winner = _gameData.responder;
                    _gameData.comment = string(abi.encodePacked(choiceMap[_gameData.responder_choice], ' beats ', choiceMap[_gameData.initiator_choice]));
                } else {
                    _gameData.state = RPSGameState.WIN;
                    _gameData.winner = _gameData.initiator;
                    _gameData.comment = string(abi.encodePacked(choiceMap[_gameData.initiator_choice], ' beats ', choiceMap[_gameData.responder_choice]));
                }
            } 
        } else {
            _gameData.state = RPSGameState.DRAW;
            _gameData.winner = address(0);
            _gameData.comment = 'Game draw due to invalid choices';
        }
    }

    // Returns the address of the winner, GameState (2 for WIN, 3 for DRAW), and the comment
    function getResult() public view returns (address, RPSGameState, string memory) {
        // Solution to problem 2(c)
        require(_gameData.state == RPSGame.RPSGameState.WIN || _gameData.state == RPSGame.RPSGameState.DRAW, "Incorrect game state to call this function.");
        return (_gameData.winner, _gameData.state, _gameData.comment);
    } 
    
}


contract RPSServer {
    // Mapping for each game instance with the first address being the initiator and internal key aaddress being the responder
    mapping(address => mapping(address => RPSGame)) _gameList;
    
    // Initiator sets up the game and stores its hashed choice in the creation itself. New game created and appropriate function called    
    function initiateGame(address _responder, bytes32 _initiator_hash) public {
        // Solution to problem 2(a)
        require(msg.sender != _responder, "Cannot initiate the game with yourself.");
        require(_responder != address(0), "Cannot initiate the game with address(0).");
        RPSGame game = new RPSGame(msg.sender, _responder, _initiator_hash);
        _gameList[msg.sender][_responder] = game;
    }

    // Responder stores their hashed choice. Appropriate RPSGame function called   
    function respond(address _initiator, bytes32 _responder_hash) public  {
        // Solution to problem 2(a)
        require(msg.sender != _initiator, "Cannot play game with yourself.");
        require(_initiator != address(0), "Cannot respond to address(0).");
        RPSGame game = _gameList[_initiator][msg.sender];
        game.addResponse(_responder_hash);
    }

    // Initiator adds raw choice number and random string. Appropriate RPSGame function called  
    function addInitiatorChoice(address _responder, uint8 _choice, string memory _randomStr) public returns (bool) {
        // Solution to problem 2(a)
        require(msg.sender != _responder, "Cannot play game with yourself.");
        require(_responder != address(0), "Cannot add address(0).");
        // Solution to problem 2(b)
        require(_choice > 0 && _choice < 4, "Invalid choice.");
        RPSGame game = _gameList[msg.sender][_responder];
        return game.addInitiatorChoice(_choice, _randomStr);
    }

    // Responder adds raw choice number and random string. Appropriate RPSGame function called
    function addResponderChoice(address _initiator, uint8 _choice, string memory _randomStr) public returns (bool) {
        // Solution to problem 2(a)
        require(msg.sender != _initiator, "Cannot play game with yourself.");
        require(_initiator != address(0), "Cannot add address(0).");
        // Solution to problem 2(b)
        require(_choice > 0 && _choice < 4, "Invalid choice.");
        RPSGame game = _gameList[_initiator][msg.sender];
        return game.addResponderChoice(_choice, _randomStr);
    }
    
    // Result details request by the initiator
    function getInitiatorResult(address _responder) public view returns (address, RPSGame.RPSGameState, string memory) {
        // Solution to problem 2(a)
        require(msg.sender != _responder, "Cannot play game with yourself.");
        require(_responder != address(0), "Cannot add address(0).");
        RPSGame game = _gameList[msg.sender][_responder];
        return game.getResult();
    }

    // Result details request by the responder
    function getResponderResult(address _initiator) public view returns (address, RPSGame.RPSGameState, string memory) {
        // Solution to problem 2(a)
        require(msg.sender != _initiator, "Cannot play game with yourself.");
        require(_initiator != address(0), "Cannot add address(0).");
        RPSGame game = _gameList[_initiator][msg.sender];
        return game.getResult();
    }

}







