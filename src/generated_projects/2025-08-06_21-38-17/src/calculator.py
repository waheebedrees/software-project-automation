```python
import datetime
import sys
from typing import List, Tuple, Union


class DivisionByZero(Exception):
    """Exception raised when division by zero is attempted."""

    def __init__(self, message: str = "Division by zero is not allowed.") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidInput(Exception):
    """Exception raised when the input is invalid."""

    def __init__(self, message: str = "Invalid input. Please provide a valid number.") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidArgumentCount(Exception):
    """Exception raised when the number of arguments is incorrect."""

    def __init__(self, message: str = "Incorrect number of arguments. Expected 2 operands and 1 operator.") -> None:
        self.message = message
        super().__init__(self.message)


class CalculationEntry:
    """Represents a calculation entry in the history."""

    def __init__(self, operation: str, result: float, timestamp: str) -> None:
        self.operation = operation
        self.result = result
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.operation} = {self.result}"


CalculationHistory = List[CalculationEntry]


class Calculator:
    """Interface for the Calculator."""

    def add(self, operand1: float, operand2: float) -> float:
        """Performs addition."""
        return operand1 + operand2

    def subtract(self, operand1: float, operand2: float) -> float:
        """Performs subtraction."""
        return operand1 - operand2

    def multiply(self, operand1: float, operand2: float) -> float:
        """Performs multiplication."""
        return operand1 * operand2

    def divide(self, operand1: float, operand2: float) -> float:
        """Performs division.

        Raises:
            DivisionByZero: If operand2 is zero.
        """
        if operand2 == 0:
            raise DivisionByZero()
        return operand1 / operand2


class HistoryManager:
    """Interface for History Management."""

    def __init__(self) -> None:
        self.history: CalculationHistory = []

    def add_calculation(self, operation: str, result: float) -> None:
        """Adds a calculation to the history."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = CalculationEntry(operation, result, timestamp)
        self.history.append(entry)

    def get_history(self, n: int = 5) -> CalculationHistory:
        """Retrieves the last N calculations from the history."""
        return self.history[-n:]


class CalculatorApp:
    """Interface for the Calculator Application."""

    def __init__(self) -> None:
        self.calculator = Calculator()
        self.history_manager = HistoryManager()

    def calculate(self, operator: str, operand1: float, operand2: float) -> float:
        """Performs a calculation based on the provided operator and operands.

        Raises:
            InvalidInput: If the input is not a valid number.
            DivisionByZero: If division by zero is attempted.
            InvalidArgumentCount: If the number of arguments is incorrect.
        """
        try:
            if operator == "+":
                result = self.calculator.add(operand1, operand2)
            elif operator == "-":
                result = self.calculator.subtract(operand1, operand2)
            elif operator == "*":
                result = self.calculator.multiply(operand1, operand2)
            elif operator == "/":
                result = self.calculator.divide(operand1, operand2)
            else:
                raise InvalidInput("Invalid operator.")

            self.history_manager.add_calculation(f"{operand1} {operator} {operand2}", result)
            return result
        except DivisionByZero as e:
            raise e
        except ValueError:
            raise InvalidInput()
        except Exception as e:
            raise e

    def display_history(self) -> None:
        """Displays the calculation history."""
        history = self.history_manager.get_history()
        if not history:
            print("No history to display.")
        else:
            for entry in history:
                print(entry)

    def exit(self) -> None:
        """Exits the application."""
        print("Exiting calculator.")
        sys.exit(0)


def parse_arguments(args: List[str]) -> Tuple[str, float, float]:
    """Parses command line arguments.

    Raises:
        InvalidInput: If the input is not a valid number.
        InvalidArgumentCount: If the number of arguments is incorrect.
    """
    if len(args) != 3:
        raise InvalidArgumentCount()

    try:
        operator = args[0]
        operand1 = float(args[1])
        operand2 = float(args[2])
        return operator, operand1, operand2
    except ValueError:
        raise InvalidInput()


def main() -> None:
    """Main function to run the calculator application."""
    app = CalculatorApp()

    if len(sys.argv) > 1:
        # Command-line mode
        try:
            operator, operand1, operand2 = parse_arguments(sys.argv[1:])
            result = app.calculate(operator, operand1, operand2)
            print(result)
        except InvalidInput as e:
            print(f"Error: {e.message}")
        except DivisionByZero as e:
            print(f"Error: {e.message}")
        except InvalidArgumentCount as e:
            print(f"Error: {e.message}")
    else:
        # Interactive mode
        while True:
            try:
                user_input = input("Enter calculation (e.g., + 1 2), 'history', or 'exit': ").strip().lower()

                if user_input == "exit":
                    app.exit()
                elif user_input == "history":
                    app.display_history()
                else:
                    parts = user_input.split()
                    if len(parts) != 3:
                        raise InvalidArgumentCount()

                    operator = parts[0]
                    operand1 = float(parts[1])
                    operand2 = float(parts[2])

                    result = app.calculate(operator, operand1, operand2)
                    print(result)

            except InvalidInput as e:
                print(f"Error: {e.message}")
            except DivisionByZero as e:
                print(f"Error: {e.message}")
            except InvalidArgumentCount as e:
                print(f"Error: {e.message}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
```