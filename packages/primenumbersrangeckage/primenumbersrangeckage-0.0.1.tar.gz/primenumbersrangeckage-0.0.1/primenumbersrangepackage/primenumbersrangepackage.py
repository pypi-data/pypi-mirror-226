def minimum():
    # Asks for the minimum number
    while True:
        try:
            minimum_number = int(input("Minimum number: "))
            if minimum_number >= 1:
                return minimum_number
            else:
                print("The minimum number must be greater than or equal to 1.")
        except ValueError:
            print("Invalid input! Please enter a valid INTEGER.")


def maximum(minimum_number):
    # Asf for maximum number
    while True:
        try:
            maximum_number = int(input("Maximum number: "))
            if maximum_number > minimum_number:
                return maximum_number
            else:
                print("The maximum number must be greater than the minimum number.")
        except ValueError:
            print("Invalid input! Please enter a valid INTEGER.")


def find_prime_numbers(minimum_number, maximum_number):
    # Finds prime numbers in the range [minimum_number, maximum_number]
    for i in range(minimum_number, maximum_number + 1):
        rest = 0
        for j in range(2, i):
            if i % j == 0:
                rest += 1
        if rest == 0:
            print(i)
