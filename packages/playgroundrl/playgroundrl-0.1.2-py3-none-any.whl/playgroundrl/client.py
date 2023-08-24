from playgroundrl.actions import DictLikeAction
import socketio
from abc import ABC
import requests
import webbrowser
from urllib.parse import urljoin
from typing import Dict, Union
from enum import Enum
from .state import *
import cattrs
import json
import codecs
import pickle
import logging

logger = logging.getLogger("playgroundrl")


class GameType(Enum):
    """Enumeration of different supported games"""

    SNAKE = "snake"

    TICTACTOE = "tic_tac_toe"

    CHESS = "chess"

    CATAN = "catan"

    POKER = "poker"

    GO = "go"

    CODENAMES = "codenames"

    MININGDECARBONIZATION = "mining_decarbonization"

    PETTINGZOO = "petting_zoo"


TYPE_MAPPING = {
    GameType.SNAKE: SnakeState,
    GameType.TICTACTOE: TicTacToeState,
    GameType.CHESS: ChessState,
    GameType.CATAN: CatanState,
    GameType.POKER: PokerState,
    GameType.GO: GoState,
    GameType.CODENAMES: CodenamesState,
    GameType.MININGDECARBONIZATION: MiningDecarbonizationState,
}


# Hack to get cattrs to parse catan actions correctl
def hook(d, t):
    return d


cattrs.register_structure_hook(Union[str, List[str]], hook)


class Pool(Enum):
    """
    The pool determines the possible agents a user or model
    can match with during games.
    """

    HUMAN_ONLY = 0
    """ Humans playing humans (unjoinable by models) """

    MODEL_ONLY = 1
    """Models playing models"""

    OPEN = 2
    """Both humans and models playing each other"""


# TODO: Handle retrying and what happens if we never receive a message back ()
# TODO: Turn Dict messages into classes
# TODO: Kill the client better, sometimes it hangs
# TODO: Create enums for game_types (MODEL_ONLY=1, OPEN_POOL=2)
class PlaygroundClient(ABC):
    """
    The base client to interface with the server. Handles all non-game specific logic.

    See example usage at https://playgroundrl.com/guide.
    """

    def __init__(
        self,
        game: GameType,
        model_name: str,
        auth: Dict = None,
        auth_file: str = None,
        endpoint: str = "https://cdn.playgroundrl.com:8083",
        render_gameplay: bool = False,
        log_level: str = None,
    ):
        """
        Initializes a client Object and connects to the server.

        :param game: String representing game name. 'tictactoe', 'chess', or 'snake'.

        :param model_name: Name of your RL model. Should be distinct in your user.

        :param auth: Dictionary containing auth data. In simple case, should contain
                'email' and 'api_key' fields.

        :param auth_file: File containing endpoint and authdata (mutually exclusive with `auth and `endpoint`).
                Expects a JSON file, structured as {"endpoint": ..., "auth": {"api_key": ..., "email": ...}}
        :param endpoint: URL of backend endpoint to connect to. Mainly used for
                connecting to development server.

        :param render_gameplay: Whether to visualize game-play server-side

        :param log_level: If set, we automatically initialize the logger, and log messages of level
            `log_level` and above. Otherwise, logs are logged to 'playgroundrl`, and you can set the
            log level manually with logging.getLogger("playgroundrl").setLevel(...).
            See https://docs.python.org/3/library/logging.html.
        """

        if log_level is not None:
            logging.basicConfig(level=log_level)
            logging.getLogger("playgroundrl").setLevel(log_level)

        # Retrieve user id
        # urljoin has weird behavior when it's not terminated right
        if auth_file is not None:
            with open(auth_file, "r") as f:
                data = json.loads(f.read())
                if "endpoint" in data:
                    endpoint = data["endpoint"]
                # Otherwise, use default endpoint
                auth = data["auth"]

        if not endpoint.endswith("/"):
            endpoint += "/"

        url = urljoin(endpoint, "email_to_uid")
        response = requests.get(url, params={"email": auth["email"]})
        assert response.text != "email not found"
        assert response.status_code == 200
        self.user_id = response.text

        socket_auth = {
            "user_id": self.user_id,
            "api_key": auth["api_key"],
            "is_human": False,
        }
        self.endpoint = endpoint
        self.auth = socket_auth

        self.server_side_sid = None

        self.game_type = game
        self.model_name = model_name
        self.endpoint = endpoint
        # self.additional_parameters = additional_parameters

        self.pool = 1
        self.num_games = 1
        self.game_id = None
        self.self_training = False
        self.maximum_messages = 50000
        self.exchanged = 0
        self.render_gameplay = render_gameplay
        self.launched_renderer = False

    ### USER DEFINED FUNCTIONS ###

    def callback(self, state: GameState, reward: str) -> str:
        """
        User defined callback to implement RL strategies.

        Returns the action for the client to take,
        or none for no action.
        """
        # TODO: Make self, state, and reward proper objects
        pass

    def gym_callback(self, observation, reward, termination, truncation, info):
        """
        User defined callback to implement RL strategies for the gym/petting zoo environments.

        Returns the action for the client to take,
        or none for no action.
        """
        # TODO: Make self, state, and reward proper objects
        pass

    def gameover_callback(self, outcome) -> None:
        """Optional user-defined callback to run an action when the game ends"""
        pass

    ### PUBLIC FUNCTIONS ###

    def wait_for_game(self):
        """
        Wait for currently running game to complete
        """
        self.sio.wait()

    def game_in_progress(self):
        return self.running

    def is_current_user_move(self, state: GameState) -> bool:
        """
        Returns whether it is our move
        """
        _user = state.player_moving_id
        return _user in self.player_ids

    def run(
        self,
        pool: Pool = Pool(2),
        num_games: int = 1,
        maximum_messages: int = 50000,
        self_training: bool = False,
        game_parameters: Dict = {},
        create_lobby: bool = False,
        lobby_id: str = None,
        # TODO: This doesn't really work
        wait_for_game_end=True,
    ) -> None:
        """
        Starts game(s), and runs game(s) until completion.
        :param pool: Which game pool to play in, must be MODEL_ONLY or OPEN.
        :param num_games: Number of games to play before disconnecting
        :param maximum_messages: A timeout to prevent games from going on forever.
        :param self_training: Perform self-training. Instead of being matched with another
            player, this class will be responsible for all players in the game
        :param wait_for_game_end: Don't return from `run` until the game completes
        :param create_lobby: Optional parameter giving the option to create a lobby
        :param lobby_id: Optional parameter giving the option to join an existing lobby
        """
        assert pool.value in [1, 2]
        self.pool = pool
        self.game_id = None
        self.self_training = self_training
        self.maximum_messages = maximum_messages
        self.game_parameters = game_parameters
        self.exchanged = 0
        self.wait_for_game_end = wait_for_game_end
        self.create_lobby = create_lobby
        self.lobby_id = lobby_id

        logger.debug(" --Connecting to server...")
        self.sio = socketio.Client()
        self.sio.connect(self.endpoint, auth=self.auth, namespaces=["/"])
        self._register_handlers()

        if self.render_gameplay:
            self.sio.emit("request_server_side_sid", {})
        logger.info("Connected!")

        logger.debug("  --running")
        self.running = True
        self.num_games -= 1
        # TODO: modify this to include the petting zoo game parameters
        start_game_payload = (
            {
                "game": self.game_type.value,
                "game_type": self.pool.value,
                "model_name": self.model_name,
                "self_training": self.self_training,
                "game_parameters": self.game_parameters,
                "create_lobby": self.create_lobby,
                "lobby_id": self.lobby_id,
            },
        )
        logger.debug(f" --Sending request to start the game: {start_game_payload}")

        # start_game_payload.update(self.additional_parameters)
        self.sio.emit(
            "start_game",
            start_game_payload,
        )

        if wait_for_game_end:
            self.sio.wait()

    ### PRIVATE FUNCTIONS + HANDLERS ###

    def _register_handlers(self):
        self.sio.on(
            "return_server_side_sid", lambda msg: self._on_get_server_side_sid(msg)
        )
        self.sio.on("state_msg", lambda msg: self._on_state_msg(msg))
        # this now happens by default, when the state updated correctly
        self.sio.on("ack", lambda msg: self._on_action_ack_msg(msg))
        self.sio.on("game_over", lambda msg: self._on_game_over_msg(msg))
        self.sio.on("send_game_id", lambda msg: self._on_send_game_id_msg(msg))
        self.sio.on("exception", lambda msg: self._on_error_msg(msg))
        self.sio.on("lobby_update", lambda msg: self._on_lobby_update_msg(msg))
        self.sio.on("*", lambda type, msg: self._default_callback(type, msg))

    def _on_get_server_side_sid(self, msg):
        self.server_side_sid = msg["server_side_sid"]

    def _on_state_msg(self, msg):
        logger.info(" --state_msg received: ")  # , msg)
        state = msg["state"]
        reward = msg["reward"]
        is_game_over = msg["is_game_over"]
        if is_game_over or self.exchanged > self.maximum_messages:
            logger.info("Game is over or max number of messages has been reached...")
            return

        if self.game_type.value == "petting_zoo":
            # get python variables from serialized version
            unpickled = pickle.loads(codecs.decode(state.encode(), "base64"))
            raw_action = self.gym_callback(*unpickled)
            # pickle this so we preserve the typing
            action = codecs.encode(pickle.dumps(raw_action), "base64").decode()
        else:
            # Convert state from JSON to object
            state_type = TYPE_MAPPING[self.game_type]
            # converter = cattrs.Converter(detailed_validation=False)  # turn this off later for faster structure
            state = cattrs.structure(json.loads(state), state_type)

            action = self.callback(state, reward)

        if action is not None:
            if issubclass(type(action), DictLikeAction):
                # TODO: This is an unecessary JSON serialization
                action = json.dumps(cattrs.unstructure(action))
            payload = {"action": action, "game_id": self.game_id}
            logger.info(f" -- sending action: {action}")
            self.sio.emit("submit_agent_action", payload)

        self.exchanged += 1

    def _on_action_ack_msg(self, msg):
        logger.debug(f" --ack message received {msg}")

    # TODO: handle this gracefully
    def _on_game_over_msg(self, msg):
        logger.info(
            f"  --Game ended. Outcome for player {msg['player_id']}:  {msg['outcome']}"
        )
        self.gameover_callback(msg["outcome"])

        if self.num_games <= 0:
            logger.debug("  --No more games to run. Disconnecting...")
            self.sio.disconnect()
            self.running = False
            return

        # TODO: This is an ugly hack
        logger.info(" --Starting the next game...")
        self.run(
            Pool(self.pool),
            self.num_games,
            self.maximum_messages,
            self.self_training,
            self.wait_for_game_end,
            self.create_lobby,
            self.lobby_id,
        )

    def _on_send_game_id_msg(self, msg):
        logger.info("  --send_game_id message received {msg}")
        if (
            self.render_gameplay
            and self.game_id is None
            and self.server_side_sid is not None
            and not self.launched_renderer
        ):
            # TODO: figure out a cleaner way to do this
            url = (
                self.endpoint.replace(":8083/", "/")
                .replace(":8000/", "/")
                .replace("stagingcdn", "dev")
                .replace("cdn.", "")
            )
            if ".com" not in url:
                url = url[:-1]
                url += ":3000/"

            webbrowser.open(
                url
                + self.game_type.value.replace("_", "")
                + "/?listen_to_sid="
                + self.server_side_sid
                + "&game_id="
                + msg["game_id"]
            )
            self.launched_renderer = True

        self.game_id = msg["game_id"]
        assert self.game_id is not None

        # Server sends player_ids this client has ownership over
        self.player_ids = msg["player_ids"]

        self.sio.emit(
            "get_state", {"game_id": self.game_id, "player_id": self.player_ids[0]}
        )

    def _on_lobby_update_msg(self, msg):
        logger.info(f"Receiving lobby update with id {msg['lobby_id']}")
        self.lobby_id = msg["lobby_id"]

    def _default_callback(self, msg_type, msg):
        raise Exception("Received unexpected data from server ->", msg_type, msg)

    def _on_error_msg(self, msg):
        raise Exception(msg)
