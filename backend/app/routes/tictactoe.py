from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from app.tictactoe import game_state

# Schemas for request/response
class MoveSchema(Schema):
    row = fields.Int(required=True, description="Row index (0-2)")
    col = fields.Int(required=True, description="Column index (0-2)")

class StateResponseSchema(Schema):
    board = fields.List(fields.List(fields.Str()), description="The 3x3 Tic Tac Toe board")
    current_player = fields.Str(description="Player whose turn is next ('X' or 'O')")
    winner = fields.Str(allow_none=True, description="Winning player symbol or None")
    is_draw = fields.Bool(description="Is the game a draw?")
    is_active = fields.Bool(description="Is the game still ongoing?")
    move_count = fields.Int(description="Number of moves made so far")

class ErrorResponseSchema(Schema):
    error = fields.Str(description="Error message")


# Blueprint for Tic Tac Toe APIs
blp = Blueprint(
    "TicTacToe", "tictactoe", url_prefix="/api/tictactoe",
    description="Tic Tac Toe game API"
)

# PUBLIC_INTERFACE
@blp.route("/state")
class GameStateAPI(MethodView):
    """
    Get the current game state.
    """
    @blp.response(200, StateResponseSchema)
    @blp.doc(summary="Get game state", description="Returns the current game board, turn, win/draw info, etc.", tags=["TicTacToe"])
    def get(self):
        """Get the game state."""
        return game_state.get_state()


# PUBLIC_INTERFACE
@blp.route("/move")
class MoveAPI(MethodView):
    """
    Submit a move to the game.
    """
    @blp.arguments(MoveSchema)
    @blp.response(200, StateResponseSchema)
    @blp.alt_response(400, ErrorResponseSchema)
    @blp.doc(summary="Submit move", description="Make a move for the current player. Returns an error if invalid.", tags=["TicTacToe"])
    def post(self, move_data):
        """Make a move on the board."""
        result = game_state.make_move(move_data['row'], move_data['col'])
        if "error" in result:
            abort(400, error=result["error"])
        return result

# PUBLIC_INTERFACE
@blp.route("/restart")
class RestartAPI(MethodView):
    """
    Restart or reset the game.
    """
    @blp.response(200, StateResponseSchema)
    @blp.doc(summary="Restart game", description="Resets all progress and starts a new empty game.", tags=["TicTacToe"])
    def post(self):
        """Restart the game."""
        game_state.reset()
        return game_state.get_state()
