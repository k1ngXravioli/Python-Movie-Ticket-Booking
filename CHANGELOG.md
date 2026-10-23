# Changelog

## NOIR / CINEMA — Champagne Edition (23 October 2026)

- Adopted the Champagne Edition as the default `movie_ticket_booking.py` desktop interface.
- Restyled the cinema view using charcoal panels, champagne-gold highlights, muted emerald details and a subtle canvas gradient.
- Kept the existing seat-selection, confirmation and pricing behaviour backed by `booking_core.py`.
- Retained the 8 automated booking tests in `test_booking.py`.
- Updated the README with the current design, features and macOS launch instructions.

## Earlier development

- Expanded the original terminal-based booking program into a Tkinter graphical interface with a 5 × 5 seat map for each demonstration film.
- Added booking validation, duplicate-selection protection and checks that an invalid multi-seat request does not partially reserve seats.
- Preserved the initial terminal version in `legacy/original_movie_booking.py`.

All bookings are demonstrations only and do not persist after the app is closed.
