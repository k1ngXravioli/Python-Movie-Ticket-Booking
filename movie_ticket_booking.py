"""Premium cinema-themed booking interface.

Uses the same booking_core.py logic as the original project.
Launch: python3 movie_ticket_booking_premium.py
Terminal mode: python3 movie_ticket_booking_premium.py --cli
"""

from __future__ import annotations

import argparse
import tkinter as tk

from booking_core import COLUMNS, MOVIE_PRICES, ROWS, MovieTicketBooking

# Deep forest-black, warm ivory and subdued champagne accents.
BG = "#0B0E0D"
PANEL = "#171B19"
PANEL_LIGHT = "#25251F"
PANEL_HOVER = "#2B2C25"
BORDER = "#444238"
GOLD = "#DFBF83"
GOLD_BRIGHT = "#F2D9A0"
TEXT = "#F2F0E9"
SECONDARY = "#B5B6AF"
FAINT = "#8C9085"
EMERALD = "#2B7558"
EMERALD_HOVER = "#348965"
SELECTED = GOLD
BOOKED = "#3B423C"
AVAILABLE = "#262E2A"
AVAILABLE_HOVER = "#323A34"
SUCCESS = "#A5ECC0"
ERROR = "#F3A09B"


def mix(c1: str, c2: str, ratio: float) -> str:
    """Blend two #RRGGBB colours without adding image dependencies."""
    a = [int(c1[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * (1-ratio) + y * ratio):02x}" for x, y in zip(a, b))


def roundrect(canvas: tk.Canvas, x1: float, y1: float, x2: float, y2: float,
              radius: float, fill: str, outline: str = "", width: float = 1,
              tags=()):
    """Draw a modern rounded rectangle with a smooth polygon."""
    r = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)
    coords = (
        x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
        x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
        x1, y2, x1, y2-r, x1, y1+r, x1, y1,
    )
    return canvas.create_polygon(*coords, smooth=True, splinesteps=16,
                                 fill=fill, outline=outline, width=width, tags=tags)


class ArtButton(tk.Canvas):
    """Theme-consistent clickable Canvas button (macOS dark-mode friendly)."""

    def __init__(self, parent, text: str, command, *, kind="primary", height=51):
        super().__init__(parent, height=height, bg=PANEL, highlightthickness=0,
                         bd=0, cursor="hand2")
        self.text = text
        self.command = command
        self.kind = kind
        self.disabled = False
        self.hover = False
        self.bind("<Configure>", lambda e: self.redraw())
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<Button-1>", self._click)

    def _enter(self, _):
        self.hover = True
        self.redraw()

    def _leave(self, _):
        self.hover = False
        self.redraw()

    def _click(self, _):
        if not self.disabled:
            self.command()

    def set_enabled(self, enabled: bool):
        self.disabled = not enabled
        self.configure(cursor="hand2" if enabled else "arrow")
        self.redraw()

    def redraw(self):
        self.delete("all")
        w = max(self.winfo_width(), 10)
        h = max(self.winfo_height(), 10)
        if self.kind == "primary":
            # Champagne-gold checkout is the single high-emphasis accent.
            bg = GOLD_BRIGHT if self.hover else GOLD
            fg = "#18201B"
            outline = GOLD_BRIGHT
        else:
            bg = PANEL_HOVER if self.hover else PANEL_LIGHT
            fg = TEXT
            outline = BORDER
        if self.disabled:
            bg, fg, outline = "#343833", "#929B90", "#41463D"
        roundrect(self, 1, 1, w-1, h-1, 12, bg, outline, 1.25)
        self.create_text(w / 2, h / 2, text=self.text, fill=fg,
                         font=("Helvetica Neue", 12, "bold"))


class MovieBookingGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("NOIR / Movie Ticket Booking")
        root.geometry("1060x850")
        root.minsize(920, 850)
        root.configure(bg=BG)
        self.booking = MovieTicketBooking()
        self.movie = "Movie A"
        self.selected: set[str] = set()
        self.cards = {}
        self._build()
        self.refresh()

    def label(self, parent, text: str, *, size=11, bold=False, colour=TEXT,
              bg=None, font=None, **kwargs):
        return tk.Label(parent, text=text, fg=colour, bg=bg or BG,
                        font=font or ("Helvetica Neue", size, "bold" if bold else "normal"),
                        anchor="w", justify="left", **kwargs)

    def _build(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Cinematic hero strip, rendered using a subtle neutral-charcoal gradient.
        self.hero = tk.Canvas(self.root, height=168, bg=BG, highlightthickness=0)
        self.hero.grid(row=0, column=0, sticky="ew")
        self.hero.bind("<Configure>", self._draw_hero)

        # Movie choice with thin champagne gold selection borders.
        picker = tk.Frame(self.root, bg=BG, padx=30)
        picker.grid(row=1, column=0, sticky="ew", pady=(19, 0))
        self.label(picker, "01  /  NOW SHOWING", size=10, bold=True, colour=GOLD).pack(anchor="w", pady=(0, 11))
        card_row = tk.Frame(picker, bg=BG)
        card_row.pack(fill="x")
        for idx, (movie, price) in enumerate(MOVIE_PRICES.items(), start=1):
            card = tk.Frame(card_row, bg=PANEL, highlightbackground=BORDER,
                            highlightthickness=1, height=78, cursor="hand2")
            card.pack(side="left", expand=True, fill="x", padx=(0, 12) if idx < len(MOVIE_PRICES) else 0)
            card.pack_propagate(False)
            inner = tk.Frame(card, bg=PANEL, padx=16, pady=12, cursor="hand2")
            inner.pack(fill="both", expand=True)
            small = self.label(inner, f"FEATURE 0{idx}", size=9, colour=FAINT, bg=PANEL)
            small.pack(anchor="w")
            line = tk.Frame(inner, bg=PANEL)
            line.pack(fill="x", pady=(4, 0))
            movie_label = self.label(line, movie, size=13, bold=True, bg=PANEL)
            movie_label.pack(side="left")
            price_label = self.label(line, f"${price} / seat", size=10, colour=GOLD, bg=PANEL)
            price_label.pack(side="right")
            self.cards[movie] = (card, inner, small, line, movie_label, price_label)
            for widget in (card, inner, small, line, movie_label, price_label):
                widget.bind("<Button-1>", lambda event, m=movie: self.set_movie(m))

        body = tk.Frame(self.root, bg=BG, padx=30)
        body.grid(row=2, column=0, sticky="nsew", pady=(19, 0))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(0, weight=1)
        left = tk.Frame(body, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 17))
        right = tk.Frame(body, bg=PANEL, highlightthickness=1, highlightbackground=BORDER, width=292)
        right.grid(row=0, column=1, sticky="ns")
        right.pack_propagate(False)

        tk.Frame(left, bg="#977C50", height=2).pack(side="top", fill="x")
        tk.Frame(right, bg="#977C50", height=2).pack(side="top", fill="x")
        left_head = tk.Frame(left, bg=PANEL, padx=24, pady=18)
        left_head.pack(fill="x")
        self.label(left_head, "02  /  CHOOSE YOUR SEATS", size=10, bold=True, colour=GOLD, bg=PANEL).pack(anchor="w")
        self.available_label = self.label(left_head, "", size=11, colour=SECONDARY, bg=PANEL)
        self.available_label.pack(anchor="w", pady=(8, 0))
        self.seat_canvas = tk.Canvas(left, bg=PANEL, highlightthickness=0, height=325)
        self.seat_canvas.pack(fill="both", expand=True, padx=12)
        self.seat_canvas.bind("<Configure>", lambda e: self._draw_seats())
        self.seat_canvas.bind("<Button-1>", self._seat_click)
        legend = tk.Frame(left, bg=PANEL, padx=23)
        legend.pack(fill="x", pady=(0, 17))
        for colour, desc, txtcol in ((AVAILABLE, "Available", SECONDARY),
                                     (SELECTED, "Selected", SECONDARY),
                                     (BOOKED, "Booked", SECONDARY)):
            item = tk.Frame(legend, bg=PANEL)
            item.pack(side="left", padx=(0, 22))
            swatch = tk.Canvas(item, width=18, height=17, bg=PANEL, highlightthickness=0)
            roundrect(swatch, 1, 1, 17, 16, 4, colour, BORDER if colour == AVAILABLE else colour)
            swatch.pack(side="left", padx=(0, 7))
            self.label(item, desc, size=10, colour=txtcol, bg=PANEL).pack(side="left")

        right_wrap = tk.Frame(right, bg=PANEL, padx=20, pady=11)
        right_wrap.pack(fill="both", expand=True)
        self.label(right_wrap, "YOUR RESERVATION", size=10, bold=True, colour=GOLD, bg=PANEL).pack(anchor="w")
        self.label(right_wrap, "Booking details", size=19, bold=True, bg=PANEL).pack(anchor="w", pady=(5, 5))
        tk.Frame(right_wrap, bg="#8A7350", height=1).pack(fill="x", pady=(0, 13))
        self.label(right_wrap, "SELECTED FILM", size=9, bold=True, colour=FAINT, bg=PANEL).pack(anchor="w")
        self.film_label = self.label(right_wrap, "Movie A", size=16, bold=True, bg=PANEL)
        self.film_label.pack(anchor="w", pady=(4, 7))
        self.label(right_wrap, "YOUR SEATS", size=9, bold=True, colour=FAINT, bg=PANEL).pack(anchor="w")
        self.seats_label = self.label(right_wrap, "None selected", size=12, bg=PANEL,
                                      wraplength=230)
        self.seats_label.pack(anchor="w", pady=(4, 7))
        self.label(right_wrap, "TOTAL", size=9, bold=True, colour=GOLD, bg=PANEL).pack(anchor="w")
        self.total_label = self.label(right_wrap, "$0", size=32, bold=True, colour=GOLD, bg=PANEL)
        self.total_label.pack(anchor="w", pady=(2, 10))
        self.confirm_button = ArtButton(right_wrap, "CONFIRM BOOKING   →", self.confirm_booking, height=47)
        self.confirm_button.pack(fill="x")
        self.clear_button = ArtButton(right_wrap, "Clear selection", self.clear_selection, kind="secondary", height=38)
        self.clear_button.pack(fill="x", pady=(6, 0))
        self.status_label = self.label(right_wrap, "Pick your favourite seats to begin.", size=10,
                                       colour=SECONDARY, bg=PANEL, wraplength=223)
        self.status_label.pack(anchor="w", fill="x", pady=(10, 0))

        foot = tk.Frame(self.root, bg=BG, padx=30)
        foot.grid(row=3, column=0, sticky="ew", pady=(11, 14))
        self.label(foot, "NOIR  /  THE CINEMA EXPERIENCE", size=9, bold=True, colour=FAINT).pack(side="left")
        self.label(foot, "DEMO MODE  ·  SEAT SELECTIONS RESET ON EXIT", size=9, colour=FAINT).pack(side="right")

    def _draw_hero(self, event=None):
        c = self.hero
        w = max(c.winfo_width(), 1)
        h = max(c.winfo_height(), 1)
        c.delete("all")
        for y in range(h):
            t = y / max(h - 1, 1)
            c.create_line(0, y, w, y, fill=mix("#0B100D", "#242722", t))
        # Gold overline and right-aligned decorative concentric rings.
        c.create_rectangle(30, 22, 66, 25, fill=GOLD, outline="")
        c.create_text(80, 23, text="N O I R   /   C I N E M A", fill=GOLD,
                      font=("Helvetica Neue", 10, "bold"), anchor="w")
        c.create_text(30, 83, text="Make it a movie night.", fill=TEXT,
                      font=("Helvetica Neue", 27, "bold"), anchor="w")
        c.create_text(31, 121, text="A refined way to choose the best seat in the house.",
                      fill=SECONDARY, font=("Helvetica Neue", 12), anchor="w")
        cx, cy = w - 90, 85
        for r, col in ((118, "#33362D"), (85, "#454637"), (54, "#655C44")):
            c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=col, width=2)
        c.create_text(cx, cy, text="✦", fill=GOLD, font=("Helvetica Neue", 32))
        c.create_line(0, h-2, w, h-2, fill="#756446", width=1)

    def _draw_seats(self):
        c = self.seat_canvas
        w, h = max(c.winfo_width(), 1), max(c.winfo_height(), 1)
        c.delete("all")
        center = w / 2
        # A gently glowing screen, like a real auditorium.
        screen_w = min(370, w * 0.72)
        left = center - screen_w / 2
        for i in range(16):
            val = i / 15
            colour = mix("#7D7056", PANEL, val)
            c.create_line(left+10, 33+i*2, left+screen_w-10, 33+i*2, fill=colour, width=2)
        c.create_arc(left, 11, left+screen_w, 64, start=20, extent=140,
                     style="arc", outline=GOLD, width=3)
        c.create_text(center, 79, text="S C R E E N", fill=GOLD,
                      font=("Helvetica Neue", 10, "bold"))

        # Seat footprint adapts to the available canvas width.
        dx = min(80, max(53, (w - 95) / 5))
        sx = center - dx * 2
        dy = min(48, max(38, (h - 132) / 5))
        for col in range(1, COLUMNS+1):
            x = sx + (col - 1) * dx
            c.create_text(x, 114, text=str(col), fill=FAINT, font=("Helvetica Neue", 10, "bold"))
        for i, row in enumerate(ROWS):
            y = 148 + i * dy
            c.create_text(sx-63, y, text=row, fill=FAINT, font=("Helvetica Neue", 10, "bold"))
            for j in range(COLUMNS):
                seat = f"{row}{j+1}"
                x = sx + j*dx
                booked = not self.booking.is_available(self.movie, seat)
                selected = seat in self.selected
                colour = BOOKED if booked else SELECTED if selected else AVAILABLE
                outline = "#646861" if booked else GOLD_BRIGHT if selected else "#4B5149"
                foreground = "#B1B6AB" if booked else "#1C201A" if selected else TEXT
                tag = f"seat:{seat}"
                halfwidth = min(29, dx * .38)
                roundrect(c, x-halfwidth, y-19, x+halfwidth, y+18,
                          9, colour, outline, 1.5, tags=(tag,))
                c.create_text(x, y, text="×" if booked else seat, fill=foreground,
                              font=("Helvetica Neue", 10, "bold"), tags=(tag,))

    def _seat_click(self, event):
        items = self.seat_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        labels = [tag for item in items for tag in self.seat_canvas.gettags(item)
                  if tag.startswith("seat:")]
        if not labels:
            return
        seat = labels[-1].split(":", 1)[1]
        if not self.booking.is_available(self.movie, seat):
            self._status(f"Seat {seat} has already been booked.", ERROR)
            return
        if seat in self.selected:
            self.selected.remove(seat)
        else:
            self.selected.add(seat)
        self._status(f"{len(self.selected)} seat(s) selected.")
        self.refresh()

    def _status(self, message, colour=SECONDARY):
        self.status_label.configure(text=message, fg=colour)

    def set_movie(self, movie):
        if movie == self.movie:
            return
        self.movie = movie
        self.selected.clear()
        self._status("Film changed. Select your preferred seats.")
        self.refresh()

    def refresh(self):
        for name, widgets in self.cards.items():
            card, inner, small, row, title, price = widgets
            is_active = name == self.movie
            background = PANEL_LIGHT if is_active else PANEL
            card.configure(bg=background, highlightbackground=GOLD if is_active else BORDER)
            for widget in (inner, small, row, title, price):
                widget.configure(bg=background)
            small.configure(fg=GOLD if is_active else FAINT)
            title.configure(fg=TEXT)
        self.film_label.configure(text=self.movie)
        self.available_label.configure(text=f"{self.booking.available_count(self.movie)} seats available   •   5 rows × 5 seats")
        seats = sorted(self.selected, key=self.booking.seat_to_indices)
        self.seats_label.configure(text=", ".join(seats) if seats else "None selected")
        self.total_label.configure(text=f"${self.booking.quote(self.movie, seats)}")
        self.confirm_button.set_enabled(bool(seats))
        self.clear_button.set_enabled(bool(seats))
        self._draw_seats()

    def clear_selection(self):
        self.selected.clear()
        self._status("Selection cleared.")
        self.refresh()

    def confirm_booking(self):
        try:
            receipt = self.booking.book_tickets(
                self.movie, sorted(self.selected, key=self.booking.seat_to_indices)
            )
        except ValueError as exc:
            self._status(str(exc), ERROR)
            return
        self.selected.clear()
        self.refresh()
        self._status(f"Booking confirmed: {', '.join(receipt.seats)} · ${receipt.total} total.", SUCCESS)


def run_cli():
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
        movie = movies[int(choice)-1]
        print(f"\nSeats for {movie} (O = available, X = booked):")
        for letter, row in zip(ROWS, booking.movies[movie]["seats"]):
            print(letter, " ".join(row))
        raw = input("Enter seats separated by commas (e.g., A1,A2), or blank to cancel: ").strip()
        if not raw:
            continue
        try:
            receipt = booking.book_tickets(movie, [s.strip() for s in raw.split(",")])
        except ValueError as exc:
            print(f"Cannot book: {exc}")
        else:
            print(f"Confirmed: {', '.join(receipt.seats)} for {movie}. Total ${receipt.total}.")


def main():
    parser = argparse.ArgumentParser(description="NOIR movie ticket booking demo")
    parser.add_argument("--cli", action="store_true", help="use terminal-based booking")
    args = parser.parse_args()
    if args.cli:
        run_cli()
    else:
        root = tk.Tk()
        MovieBookingGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()
