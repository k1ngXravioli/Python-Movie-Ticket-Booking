# Python Movie Ticket Booking System

A small cinema reservation application built with **Python**, **object-oriented programming** and **nested lists**. It began as my terminal-based coding project and has since been expanded into a graphical app with stronger input validation and unit tests. The original terminal implementation is preserved in [`legacy/original_movie_booking.py`](legacy/original_movie_booking.py).

## Features

- Choose from three demonstration films: **Movie A ($10)**, **Movie B ($12)**, **Movie C ($8)**.
- View a separate **5 × 5 seating grid** for each film.
- Select one or more seats and see the total cost before confirming.
- Confirm bookings and mark those seats as unavailable.
- Prevent double bookings, duplicate selections and invalid seat numbers.
- Keep different movies' availability independent.
- Use the Tkinter graphical interface or run a terminal-based version.

These are sample movie titles and prices, retained from my original project. All bookings are **in memory** and reset when the program closes; no payments or real cinema reservations take place.

## Screenshot

![Movie booking application showing seat selections and a booking summary](screenshots/movie_booking_demo.png)

*Screenshot from a demonstration run of the Tkinter application.*

## Technologies and concepts

- **Python 3.10+** – logic, classes, dictionaries and loops
- **Tkinter / ttk** – desktop interface and selectable seat map
- **Nested lists** – each movie has five rows of five seats
- **Validation and state management** – check all seats before saving a booking
- **Unit testing** – built-in Python `unittest` framework

## Run it on macOS

Download and extract this repository. In Terminal, change into the extracted folder, then run:

```bash
python3 movie_ticket_booking.py
```

Python 3 and Tkinter are required. If your Python installation does not include Tkinter, install a version that provides it.

You can also run the terminal version:

```bash
python3 movie_ticket_booking.py --cli
```

**No external Python packages are required.**

## Running the tests

```bash
python3 -m unittest -v test_booking.py
```

These tests cover booking confirmation, prices, independence across films, rejecting invalid seat coordinates, double-booking prevention and ensuring a failed multi-seat booking doesn't reserve any seats.

## How the algorithm works

Every film has its own 5 × 5 nested list containing `O` (open) or `X` (booked). Seat `B3` maps to row index `1`, column index `2`. Before a booking is confirmed, the program checks **every** requested seat for validity, availability and duplicates. Only after all checks pass does it change the corresponding entries to `X`.

This prevents accidentally reserving some seats when another seat in the same request is invalid or already taken.

## My development journey

My **original** terminal version used a Python class, nested lists and `if` statements to check and update seat availability. It helped me practise breaking a larger booking process into smaller methods. In this expanded portfolio version, the interface, validation and automated tests were developed with AI assistance as a further learning and debugging exercise; the underlying project idea and initial implementation were my own.

## Current limitations and future improvements

- Booking data is not saved to a database or file, so reservations reset on restart.
- Movie names and prices are demonstration values.
- No user accounts, authentication, payment handling or customer-data storage.
- Next steps: persistent storage, booking reference numbers and more accessibility testing on macOS.