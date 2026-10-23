"""Tests for booking logic, independent of the Tkinter GUI."""
import unittest
from booking_core import MovieTicketBooking


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.booking = MovieTicketBooking()

    def test_initial_seats_and_prices(self):
        self.assertEqual(self.booking.available_count("Movie A"), 25)
        self.assertEqual(self.booking.quote("Movie B", ["A1", "A2"]), 24)

    def test_confirm_booking_updates_only_selected_seats(self):
        receipt = self.booking.book_tickets("Movie A", ["B2", "A1"])
        self.assertEqual(receipt.seats, ("A1", "B2"))
        self.assertEqual(receipt.total, 20)
        self.assertFalse(self.booking.is_available("Movie A", "A1"))
        self.assertTrue(self.booking.is_available("Movie A", "A2"))
        self.assertTrue(self.booking.is_available("Movie B", "A1"))
        self.assertEqual(self.booking.available_count("Movie A"), 23)

    def test_cannot_double_book(self):
        self.booking.book_tickets("Movie C", ["E5"])
        with self.assertRaisesRegex(ValueError, "already booked"):
            self.booking.book_tickets("Movie C", ["E5"])

    def test_invalid_seat_rejected_without_partial_booking(self):
        for invalid in ("A0", "A6", "F1", "Z9", "A11", "", "11"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.booking.book_tickets("Movie B", ["A1", invalid])
            self.assertTrue(self.booking.is_available("Movie B", "A1"))

    def test_atomic_transaction_on_booked_seat(self):
        self.booking.book_tickets("Movie A", ["A3"])
        with self.assertRaises(ValueError):
            self.booking.book_tickets("Movie A", ["B1", "A3"])
        self.assertTrue(self.booking.is_available("Movie A", "B1"))

    def test_duplicate_selection_fails_without_booking(self):
        with self.assertRaisesRegex(ValueError, "only be selected once"):
            self.booking.book_tickets("Movie B", ["b1", "B1"])
        self.assertEqual(self.booking.available_count("Movie B"), 25)

    def test_missing_seats_or_unknown_movie(self):
        with self.assertRaises(ValueError):
            self.booking.book_tickets("Movie A", [])
        with self.assertRaises(ValueError):
            self.booking.book_tickets("Movie D", ["A1"])

    def test_last_seat_and_full_capacity(self):
        all_seats = [f"{row}{col}" for row in "ABCDE" for col in range(1, 6)]
        receipt = self.booking.book_tickets("Movie C", all_seats)
        self.assertEqual(receipt.total, 25 * 8)
        self.assertEqual(self.booking.available_count("Movie C"), 0)


if __name__ == "__main__":
    unittest.main()
