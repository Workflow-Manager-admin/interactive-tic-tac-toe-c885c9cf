"""
TicTacToe game logic management (in-memory).
Provides game board management, player turn tracking,
move validation, win/draw detection, and reset logic.
"""

from typing import Dict, Any
import threading

class GameState:
    """
    In-memory representation of a Tic Tac Toe game.
    Handles the board, player turns, win/draw state, and resets.
    Thread-safe via self._lock.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()

    # PUBLIC_INTERFACE
    def reset(self):
        """Reset the game to its initial state."""
        with self._lock:
            self.board = [["" for _ in range(3)] for _ in range(3)]
            self.current_player = "X"
            self.winner = None
            self.is_draw = False
            self.move_count = 0
            self.is_active = True

    # PUBLIC_INTERFACE
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current game state for API response.
        """
        with self._lock:
            return {
                "board": self.board,
                "current_player": self.current_player,
                "winner": self.winner,
                "is_draw": self.is_draw,
                "is_active": self.is_active,
                "move_count": self.move_count
            }

    # PUBLIC_INTERFACE
    def make_move(self, row: int, col: int) -> Dict[str, Any]:
        """
        Apply a move for the current player at (row, col).
        Returns the updated state and any result messages.
        """
        with self._lock:
            if not self.is_active:
                return {"error": "Game is over. Please restart to play again."}
            
            if not (0 <= row < 3 and 0 <= col < 3):
                return {"error": "Move out of board range."}

            if self.board[row][col] != "":
                return {"error": "Cell already occupied."}
            
            self.board[row][col] = self.current_player
            self.move_count += 1

            if self._check_winner(self.current_player):
                self.winner = self.current_player
                self.is_active = False
            elif self.move_count == 9:
                self.is_draw = True
                self.is_active = False
            else:
                # Switch player
                self.current_player = "O" if self.current_player == "X" else "X"
            return self.get_state()

    def _check_winner(self, player: str) -> bool:
        """
        Internal: Check if current player has won.
        """
        board = self.board
        win_positions = (
            # Rows
            [(i, 0), (i, 1), (i, 2)] for i in range(3)
        )
        win_positions = list(win_positions)

        win_positions += [
            # Columns
            [(0, i), (1, i), (2, i)] for i in range(3)
        ]
        # Diagonals
        win_positions.append([(0, 0), (1, 1), (2, 2)])
        win_positions.append([(0, 2), (1, 1), (2, 0)])

        for positions in win_positions:
            if all(board[r][c] == player for r, c in positions):
                return True
        return False


# The global game object for this server session (not scalable for multi-room multiplayer).
game_state = GameState()
