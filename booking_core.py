"""Small, testable movie-seat booking model.

Inspired by an original CLI project using dictionaries and 5x5 nested lists.
The model contains no UI code so the booking logic can be unit tested.
"""

from __future__ import annotations

from dataclasses import dataclass

MOVIE_PRICES = {"Movie A": 10, "Movie B": 12, "Movie C": 8}
ROWS = "ABCDE"
COLUMNS = 5


@dataclass(frozen=True)
class BookingReceipt:
    movie: str
    seats: tuple[str, ...]
    price_each: int
    total: int


class MovieTicketBooking:
    def __init__(self) -> None:
        # Match the original project: O = open, X = booked.
        self.movies = {
            title: {
                "price": price,
                "seats": [["O" for _ in range(COLUMNS)] for _ in ROWS],
            }
            for title, price in MOVIE_PRICES.items()
        }

    def _check_movie(self, movie: str) -> None:
        if movie not in self.movies:
            raise ValueError("Please choose a valid movie.")

    @staticmethod
    def seat_to_indices(seat: str) -> tuple[int, int]:
        """Convert labels like B3 to zero-based row and column indexes."""
        if not isinstance(seat, str):
            raise ValueError("Seat labels must be text such as A1.")
        label = seat.strip().upper()
        if len(label) != 2 or label[0] not in ROWS or label[1] not in "12345":
            raise ValueError(f"Invalid seat {seat!r}. Choose A1 to E5.")
        return ROWS.index(label[0]), int(label[1]) - 1

    def is_available(self, movie: str, seat: str) -> bool:
        self._check_movie(movie)
        row, col = self.seat_to_indices(seat)
        return self.movies[movie]["seats"][row][col] == "O"

    def available_count(self, movie: str) -> int:
        self._check_movie(movie)
        return sum(cell == "O" for row in self.movies[movie]["seats"] for cell in row)

    def quote(self, movie: str, seats: list[str] | tuple[str, ...]) -> int:
        self._check_movie(movie)
        return self.movies[movie]["price"] * len(seats)

    def book_tickets(self, movie: str, seats: list[str] | tuple[str, ...]) -> BookingReceipt:
        """Validate *every* seat before changing any reservations."""
        self._check_movie(movie)
        if not seats:
            raise ValueError("Select at least one seat to make a booking.")

        cleaned = [s.strip().upper() if isinstance(s, str) else s for s in seats]
        coordinates = [self.seat_to_indices(s) for s in cleaned]
        if len(set(coordinates)) != len(coordinates):
            raise ValueError("A seat can only be selected once per booking.")
        for seat, (row, col) in zip(cleaned, coordinates):
            if self.movies[movie]["seats"][row][col] != "O":
                raise ValueError(f"Seat {seat} is already booked. Choose another.")

        for row, col in coordinates:
            self.movies[movie]["seats"][row][col] = "X"
        ordered = tuple(sorted(cleaned, key=lambda s: self.seat_to_indices(s)))
        unit_price = self.movies[movie]["price"]
        return BookingReceipt(movie=movie, seats=ordered,
                              price_each=unit_price, total=unit_price * len(ordered))
