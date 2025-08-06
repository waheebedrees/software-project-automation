
import unittest
from unittest.mock import patch
from io import StringIO
import sys
import datetime

from typing import List, Tuple, Union  # Import necessary type hints

# Assuming the code to be tested is in a file named calculator.py
# For testing, you might need to adjust the import based on your project structure
# For example: from calculator import Calculator, HistoryManager, CalculatorApp, DivisionByZero, InvalidInput, InvalidArgumentCount, CalculationEntry, CalculationHistory
# However, to make the test suite self-contained, I'm including the code directly.
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


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()
        self.history_manager = HistoryManager()
        self.calculator_app = CalculatorApp()

    def test_add(self):
        self.assertEqual(self.calculator.add(1, 2), 3)
        self.assertEqual(self.calculator.add(-1, 2), 1)
        self.assertEqual(self.calculator.add(0, 0), 0)
        self.assertEqual(self.calculator.add(1.5, 2.5), 4.0)

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(1, 2), -1)
        self.assertEqual(self.calculator.subtract(-1, 2), -3)
        self.assertEqual(self.calculator.subtract(0, 0), 0)
        self.assertEqual(self.calculator.subtract(2.5, 1.5), 1.0)

    def test_multiply(self):
        self.assertEqual(self.calculator.multiply(1, 2), 2)
        self.assertEqual(self.calculator.multiply(-1, 2), -2)
        self.assertEqual(self.calculator.multiply(0, 0), 0)
        self.assertEqual(self.calculator.multiply(2.5, 2), 5.0)

    def test_divide(self):
        self.assertEqual(self.calculator.divide(4, 2), 2)
        self.assertEqual(self.calculator.divide(-4, 2), -2)
        self.assertEqual(self.calculator.divide(0, 2), 0)
        self.assertEqual(self.calculator.divide(5, 2), 2.5)

    def test_divide_by_zero(self):
        with self.assertRaises(DivisionByZero):
            self.calculator.divide(4, 0)

    def test_add_calculation(self):
        self.history_manager.add_calculation("1 + 2", 3)
        self.assertEqual(len(self.history_manager.history), 1)
        self.assertEqual(self.history_manager.history[0].operation, "1 + 2")
        self.assertEqual(self.history_manager.history[0].result, 3)

    def test_get_history(self):
        self.history_manager.add_calculation("1 + 2", 3)
        self.history_manager.add_calculation("2 - 1", 1)
        history = self.history_manager.get_history(2)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].operation, "1 + 2")
        self.assertEqual(history[1].operation, "2 - 1")

        history_default = self.history_manager.get_history()
        self.assertEqual(len(history_default), 2)

        self.history_manager.history = [] # reset history
        history_empty = self.history_manager.get_history()
        self.assertEqual(len(history_empty), 0)

    def test_calculate_add(self):
        self.assertEqual(self.calculator_app.calculate("+", 1, 2), 3)

    def test_calculate_subtract(self):
        self.assertEqual(self.calculator_app.calculate("-", 1, 2), -1)

    def test_calculate_multiply(self):
        self.assertEqual(self.calculator_app.calculate("*", 1, 2), 2)

    def test_calculate_divide(self):
        self.assertEqual(self.calculator_app.calculate("/", 4, 2), 2)

    def test_calculate_invalid_operator(self):
        with self.assertRaises(InvalidInput):
            self.calculator_app.calculate("%", 1, 2)

    def test_calculate_division_by_zero(self):
        with self.assertRaises(DivisionByZero):
            self.calculator_app.calculate("/", 1, 0)

    def test_calculate_invalid_input(self):
        with self.assertRaises(InvalidInput):
            self.calculator_app.calculate("+", "a", 2)

    def test_display_history(self):
        # Capture stdout to check printed output
        captured_output = StringIO()
        sys.stdout = captured_output

        self.calculator_app.display_history()
        self.assertEqual(captured_output.getvalue().strip(), "No history to display.")

        sys.stdout = sys.__stdout__  # Reset stdout

        self.calculator_app.calculate("+", 1, 2)
        captured_output = StringIO()
        sys.stdout = captured_output
        self.calculator_app.display_history()
        self.assertTrue("1 + 2 = 3.0" in captured_output.getvalue())
        sys.stdout = sys.__stdout__
    
    @patch('sys.exit')
    @patch('builtins.print')
    def test_exit(self, mock_print, mock_exit):
        self.calculator_app.exit()
        mock_print.assert_called_with("Exiting calculator.")
        mock_exit.assert_called_with(0)

    def test_parse_arguments(self):
        args = ["+", "1", "2"]
        operator, operand1, operand2 = parse_arguments(args)
        self.assertEqual(operator, "+")
        self.assertEqual(operand1, 1.0)
        self.assertEqual(operand2, 2.0)

    def test_parse_arguments_invalid_input(self):
        args = ["+", "a", "2"]
        with self.assertRaises(InvalidInput):
            parse_arguments(args)

    def test_parse_arguments_invalid_argument_count(self):
        args = ["+", "1"]
        with self.assertRaises(InvalidArgumentCount):
            parse_arguments(args)
    
    @patch('sys.argv', ['calculator.py', '+', '2', '3'])
    @patch('builtins.print')
    def test_main_command_line_mode(self, mock_print):
        main()
        mock_print.assert_called_with(5.0)

    @patch('sys.argv', ['calculator.py'])
    @patch('builtins.input', side_effect=['+', '2', '3', 'exit'])
    @patch('builtins.print')
    def test_main_interactive_mode(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        # Assert that the calculator prints the result of the addition
        self.assertIn("5.0", [str(call[0][0]) for call in mock_print.call_args_list])
        # Assert that the calculator prints the exit message
        self.assertIn("Exiting calculator.", [str(call[0][0]) for call in mock_print.call_args_list])

    @patch('sys.argv', ['calculator.py'])
    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('builtins.print')
    def test_main_interactive_mode_history(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        # Assert that the calculator prints the exit message
        self.assertIn("No history to display.", [str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("Exiting calculator.", [str(call[0][0]) for call in mock_print.call_args_list])

    @patch('sys.argv', ['calculator.py'])
    @patch('builtins.input', side_effect=['+', '2', 'a', 'exit'])
    @patch('builtins.print')
    def test_main_interactive_mode_invalid_input(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        # Assert that the calculator prints the exit message
        self.assertIn("Invalid input. Please provide a valid number.", [str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("Exiting calculator.", [str(call[0][0]) for call in mock_print.call_args_list])

    @patch('sys.argv', ['calculator.py'])
    @patch('builtins.input', side_effect=['+', '2', '3', '/', '1', '0', 'exit'])
    @patch('builtins.print')
    def test_main_interactive_mode_division_by_zero(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        # Assert that the calculator prints the exit message
        self.assertIn("Division by zero is not allowed.", [str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("Exiting calculator.", [str(call[0][0]) for call in mock_print.call_args_list])

    @patch('sys.argv', ['calculator.py'])
    @patch('builtins.input', side_effect=['+', '2', '3', '+', '2', 'exit'])
    @patch('builtins.print')
    def test_main_interactive_mode_invalid_argument_count(self, mock_print, mock_input):
        with self.assertRaises(SystemExit):
            main()
        # Assert that the calculator prints the exit message
        self.assertIn("Incorrect number of arguments. Expected 2 operands and 1 operator.", [str(call[0][0]) for call in mock_print.call_args_list])
        self.assertIn("Exiting calculator.", [str(call[0][0]) for call in mock_print.call_args_list])


if __name__ == '__main__':
    unittest.main()
