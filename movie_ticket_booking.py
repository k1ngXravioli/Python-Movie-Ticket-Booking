"""Movie ticket booking demo — graphical app + optional terminal mode.

Run: python3 movie_ticket_booking.py
CLI: python3 movie_ticket_booking.py --cli
"""

from __future__ import annotations

import argparse
import tkinter as tk
from tkinter import ttk

from booking_core import MOVIE_PRICES, ROWS, COLUMNS, MovieTicketBooking


class MovieBookingGUI:
    BG = "#F3F6FB"
    WHITE = "#FFFFFF"
    NAVY = "#18253E"
    MUTED = "#63718A"
    ACCENT = "#2862D9"
    SELECTED = "#2862D9"
    BOOKED = "#DDE3EB"
    BORDER = "#CDD7E5"
    SUCCESS = "#106748"
    ERROR = "#B13030"

    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Movie Ticket Booking")
        root.geometry("940x760")
        root.minsize(800, 700)
        root.configure(background=self.BG)
        self.booking = MovieTicketBooking()
        self.movie = "Movie A"
        self.selected: set[str] = set()
        self.movie_buttons: dict[str, ttk.Button] = {}
        self._style()
        self._build()
        self.refresh()

    def _style(self) -> None:
        s = ttk.Style(self.root)
        if "clam" in s.theme_names():
            s.theme_use("clam")
        s.configure("Primary.TButton", font=("Arial", 11, "bold"),
                    foreground=self.WHITE, background=self.ACCENT, padding=(15, 12), borderwidth=0)
        s.map("Primary.TButton", background=[("active", "#184BAF"), ("disabled", "#BAC5D4")],
              foreground=[("active", self.WHITE), ("disabled", "#62708A")])
        s.configure("Secondary.TButton", font=("Arial", 10, "bold"),
                    foreground=self.NAVY, background=self.WHITE, padding=(12, 9), borderwidth=1)
        s.map("Secondary.TButton", background=[("active", "#E3EAF6")])
        s.configure("Movie.TButton", font=("Arial", 10, "bold"),
                    foreground=self.NAVY, background=self.WHITE, padding=(13, 12), borderwidth=1)
        s.map("Movie.TButton", background=[("active", "#E3EAF6")])
        s.configure("MovieSelected.TButton", font=("Arial", 10, "bold"),
                    foreground=self.WHITE, background=self.ACCENT, padding=(13, 12), borderwidth=1)
        s.map("MovieSelected.TButton", background=[("active", "#184BAF")])

    def label(self, parent, text, *, size=11, bold=False, colour=None, bg=None):
        return tk.Label(parent, text=text, bg=bg or self.BG, fg=colour or self.NAVY,
                        font=("Arial", size, "bold" if bold else "normal"),
                        anchor="w", justify="left")

    def _build(self) -> None:
        wrap = tk.Frame(self.root, bg=self.BG, padx=30, pady=24)
        wrap.pack(fill="both", expand=True)
        self.label(wrap, "Movie Ticket Booking", size=24, bold=True).pack(anchor="w")
        self.label(wrap, "Choose a movie, select available seats and confirm your reservation.",
                   colour=self.MUTED).pack(anchor="w", pady=(3, 22))
        self.label(wrap, "1  Select a movie", size=13, bold=True).pack(anchor="w", pady=(0, 10))

        movies_row = tk.Frame(wrap, bg=self.BG)
        movies_row.pack(fill="x")
        for movie, price in MOVIE_PRICES.items():
            button = ttk.Button(movies_row, text=f"{movie}   •   ${price} / seat",
                                command=lambda m=movie: self.set_movie(m), style="Movie.TButton")
            button.pack(side="left", padx=(0, 12))
            self.movie_buttons[movie] = button

        content = tk.Frame(wrap, bg=self.BG)
        content.pack(fill="both", expand=True, pady=(26, 0))
        left = tk.Frame(content, bg=self.WHITE, highlightthickness=1,
                        highlightbackground=self.BORDER, padx=20, pady=17)
        left.pack(side="left", fill="both", expand=True, padx=(0, 16))
        right = tk.Frame(content, bg=self.WHITE, highlightthickness=1,
                         highlightbackground=self.BORDER, padx=18, pady=17, width=255)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.label(left, "2  Choose your seats", size=14, bold=True, bg=self.WHITE).pack(anchor="w")
        self.available_label = self.label(left, "", colour=self.MUTED, size=10, bg=self.WHITE)
        self.available_label.pack(anchor="w", pady=(5, 12))
        tk.Frame(left, bg=self.BORDER, height=1).pack(fill="x", pady=(0, 12))

        # A Canvas rather than system-native buttons keeps the seat colours
        # legible on both light and dark macOS themes.
        self.canvas = tk.Canvas(left, bg=self.WHITE, height=335, width=490,
                                highlightthickness=0)
        self.canvas.pack(fill="x")
        self.canvas.bind("<Button-1>", self._seat_click)

        legend = tk.Frame(left, bg=self.WHITE)
        legend.pack(anchor="w", pady=(6, 0))
        for colour, desc, border in (("#EEF3FA", "Available", self.BORDER),
                                     (self.SELECTED, "Selected", self.SELECTED),
                                     (self.BOOKED, "Booked", self.BOOKED)):
            item = tk.Frame(legend, bg=self.WHITE)
            item.pack(side="left", padx=(0, 14))
            tk.Label(item, text="■", bg=self.WHITE, fg=colour,
                     font=("Arial", 15)).pack(side="left")
            self.label(item, desc, size=9, colour=self.MUTED,
                       bg=self.WHITE).pack(side="left", padx=(4, 0))

        self.label(right, "Your booking", size=14, bold=True, bg=self.WHITE).pack(anchor="w")
        tk.Frame(right, bg=self.BORDER, height=1).pack(fill="x", pady=(13, 20))
        self.label(right, "FILM", colour=self.MUTED, size=9, bold=True,
                   bg=self.WHITE).pack(anchor="w")
        self.film_label = self.label(right, "", size=14, bold=True, bg=self.WHITE)
        self.film_label.pack(anchor="w", pady=(5, 20))
        self.label(right, "SELECTED SEATS", colour=self.MUTED, size=9, bold=True,
                   bg=self.WHITE).pack(anchor="w")
        self.seats_label = self.label(right, "None", size=12, bg=self.WHITE)
        self.seats_label.pack(anchor="w", pady=(6, 20))
        self.label(right, "TOTAL PRICE", colour=self.MUTED, size=9, bold=True,
                   bg=self.WHITE).pack(anchor="w")
        self.total_label = self.label(right, "$0", size=23, bold=True, bg=self.WHITE)
        self.total_label.pack(anchor="w", pady=(4, 26))

        self.book_button = ttk.Button(right, text="Confirm booking",
                                      style="Primary.TButton", command=self.confirm_booking)
        self.book_button.pack(fill="x")
        ttk.Button(right, text="Clear selection", style="Secondary.TButton",
                   command=self.clear_selection).pack(fill="x", pady=(10, 0))
        tk.Frame(right, bg=self.BORDER, height=1).pack(fill="x", pady=(22, 14))
        self.status_label = self.label(right, "Choose an available seat to begin.",
                                       size=10, colour=self.MUTED, bg=self.WHITE)
        self.status_label.configure(wraplength=212)
        self.status_label.pack(anchor="w", fill="x")
        self.label(wrap, "Demo only • All bookings reset when the program closes.",
                   colour=self.MUTED, size=9).pack(anchor="w", pady=(14, 0))

    def _set_status(self, msg: str, colour=None) -> None:
        self.status_label.configure(text=msg, fg=colour or self.MUTED)

    def set_movie(self, movie: str) -> None:
        if movie == self.movie:
            return
        self.movie = movie
        self.selected.clear()
        self._set_status("Movie changed. Select available seats.")
        self.refresh()

    def _seat_click(self, event: tk.Event) -> None:
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        seats = [t for item in items for t in self.canvas.gettags(item) if t.startswith("seat:")]
        if not seats:
            return
        seat = seats[-1].split(":", 1)[1]
        if not self.booking.is_available(self.movie, seat):
            self._set_status(f"{seat} is already booked.", self.ERROR)
            return
        if seat in self.selected:
            self.selected.remove(seat)
        else:
            self.selected.add(seat)
        self._set_status(f"{len(self.selected)} seat(s) selected.")
        self.refresh()

    def _draw_grid(self) -> None:
        c = self.canvas
        c.delete("all")
        # White cinema screen / viewing direction
        c.create_rectangle(90, 6, 414, 14, fill="#D8E4F5", outline="#D8E4F5")
        c.create_text(252, 31, text="SCREEN", fill=self.MUTED,
                      font=("Arial", 9, "bold"))
        for col in range(1, COLUMNS + 1):
            x = 112 + (col - 1) * 74
            c.create_text(x, 63, text=str(col), fill=self.MUTED,
                          font=("Arial", 11, "bold"))
        for r, row_letter in enumerate(ROWS):
            y = 101 + r * 48
            c.create_text(55, y, text=row_letter, fill=self.MUTED,
                          font=("Arial", 11, "bold"))
            for col in range(1, COLUMNS + 1):
                seat = f"{row_letter}{col}"
                x = 112 + (col - 1) * 74
                booked = not self.booking.is_available(self.movie, seat)
                selected = seat in self.selected
                fill = self.BOOKED if booked else self.SELECTED if selected else "#EFF4FB"
                foreground = "#8090A5" if booked else self.WHITE if selected else self.NAVY
                outline = self.BOOKED if booked else self.SELECTED if selected else self.BORDER
                tag = f"seat:{seat}"
                c.create_rectangle(x - 26, y - 17, x + 26, y + 17,
                                   fill=fill, outline=outline, width=1.5,
                                   tags=(tag,))
                c.create_text(x, y, text=seat if not booked else "×", fill=foreground,
                              font=("Arial", 10, "bold"), tags=(tag,))

    def refresh(self) -> None:
        for name, button in self.movie_buttons.items():
            button.configure(style="MovieSelected.TButton" if name == self.movie else "Movie.TButton")
        self.film_label.configure(text=self.movie)
        self.available_label.configure(text=f"{self.booking.available_count(self.movie)} seats available • 5 rows × 5 seats")
        seats = sorted(self.selected, key=self.booking.seat_to_indices)
        seat_text = ", ".join(seats) if seats else "None"
        if len(seat_text) > 23:
            seat_text = seat_text[:23] + "…"
        self.seats_label.configure(text=seat_text)
        self.total_label.configure(text=f"${self.booking.quote(self.movie, seats)}")
        self.book_button.configure(state="normal" if seats else "disabled")
        self._draw_grid()

    def clear_selection(self) -> None:
        self.selected.clear()
        self._set_status("Selection cleared.")
        self.refresh()

    def confirm_booking(self) -> None:
        try:
            receipt = self.booking.book_tickets(self.movie,
                                                sorted(self.selected, key=self.booking.seat_to_indices))
        except ValueError as exc:
            self._set_status(str(exc), self.ERROR)
            return
        self.selected.clear()
        self.refresh()
        self._set_status(f"Booking confirmed! {', '.join(receipt.seats)} • Total ${receipt.total}.",
                         self.SUCCESS)


def run_cli() -> None:
    """Simple terminal interface for users who prefer the original format."""
    booking = MovieTicketBooking()
    movies = list(MOVIE_PRICES)
    while True:
        print("\nMovies:")
        for i, name in enumerate(movies, 1):
            print(f"  {i}. {name}: ${MOVIE_PRICES[name]} per ticket")
        print("  0. Exit")
        choice = input("Choose a movie (0–3): ").strip()
        if choice == "0":
            return
        if choice not in ("1", "2", "3"):
            print("Please enter 1, 2, 3 or 0.")
            continue
        movie = movies[int(choice) - 1]
        print(f"\nSeats for {movie} (O = available, X = booked):")
        for letter, row in zip(ROWS, booking.movies[movie]["seats"]):
            print(letter, " ".join(row))
        raw = input("Enter seat labels separated by commas (e.g., A1,A2), or blank to cancel: ").strip()
        if not raw:
            continue
        try:
            receipt = booking.book_tickets(movie, [seat.strip() for seat in raw.split(",")])
        except ValueError as exc:
            print(f"Cannot book: {exc}")
        else:
            print(f"Confirmed: {', '.join(receipt.seats)} for {movie}. Total ${receipt.total}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Movie Ticket Booking demo")
    parser.add_argument("--cli", action="store_true", help="run the terminal version")
    args = parser.parse_args()
    if args.cli:
        run_cli()
    else:
        root = tk.Tk()
        MovieBookingGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()
