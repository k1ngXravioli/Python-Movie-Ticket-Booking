class MovieTicketBooking:
    def __init__(self):
        self.movies = {
            "Movie A": {"price": 10, "seats": [["O" for _ in range(5)] for _ in range(5)]},
            "Movie B": {"price": 12, "seats": [["O" for _ in range(5)] for _ in range(5)]},
            "Movie C": {"price": 8, "seats": [["O" for _ in range(5)] for _ in range(5)]},
        }

    def display_movies(self):
        print("\nAvailable Movies:")
        for idx, movie in enumerate(self.movies):
            print(f"{idx + 1}. {movie} - Price: ${self.movies[movie]['price']}")

    def display_seats(self, movie):
        seats = self.movies[movie]['seats']
        print("\nSeat Layout:")
        for row in seats:
            print(" ".join(row))
        print()

    def book_tickets(self, movie, num_tickets):
        seats = self.movies[movie]['seats']
        booked_seats = []

        for _ in range(num_tickets):
            while True:
                row = int(input("Enter row number (1-5): ")) - 1
                col = int(input("Enter seat number (1-5): ")) - 1

                if seats[row][col] == "O":
                    seats[row][col] = "X"
                    booked_seats.append((row, col))
                    break
                else:
                    print(f"Seat at ({row + 1}, {col + 1}) is already booked. Choose another seat.")

        self.movies[movie]['seats'] = seats
        total_price = self.movies[movie]['price'] * num_tickets
        print(f"\nSuccessfully booked {num_tickets} tickets for {movie}. Total price: ${total_price}")
        print("Booked seats:", booked_seats)

    def run(self):
        while True:
            self.display_movies()

            choice = input("Choose a movie by number (or type 'exit' to quit): ")
            if choice.lower() == 'exit':
                break

            if choice.isdigit() and 1 <= int(choice) <= len(self.movies):
                movie = list(self.movies.keys())[int(choice) - 1]
                self.display_seats(movie)

                num_tickets = int(input("Enter the number of tickets you want to book: "))
                self.book_tickets(movie, num_tickets)
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    booking_system = MovieTicketBooking()
    booking_system.run()
