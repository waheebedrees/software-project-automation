```python
import sys
from typing import List, TypedDict, Protocol, runtime_checkable, Optional
import unittest
from unittest.mock import patch
from io import StringIO

# Data Structures

class Calculation(TypedDict):
    operation: str
    operand1: float
    operand2: float
    result: float

CalculationHistory = List[Calculation]

# Error Specifications

class DivisionByZero(Exception):
    def __init__(self, message: str = "Division by zero is not allowed.") -> None:
        self.message = message
        super().__init__(self.message)

class InvalidInput(Exception):
    def __init__(self, message: str = "Invalid input. Please enter a number.") -> None:
        self.message = message
        super().__init__(self.message)

class IncorrectArguments(Exception):
    def __init__(self, message: str = "Incorrect number of arguments provided.") -> None:
        self.message = message
        super().__init__(self.message)


# Interface Definitions

@runtime_checkable
class Calculator(Protocol):
    def add(self, operand1: float, operand2: float) -> float:
        """Performs addition."""
        ...

    def subtract(self, operand1: float, operand2: float) -> float:
        """Performs subtraction."""
        ...

    def multiply(self, operand1: float, operand2: float) -> float:
        """Performs multiplication."""
        ...

    def divide(self, operand1: float, operand2: float) -> float:
        """Performs division."""
        ...

    def get_history(self) -> CalculationHistory:
        """Retrieves the calculation history."""
        ...

    def clear_history(self) -> None:
        """Clears the calculation history."""
        ...

@runtime_checkable
class UserInterface(Protocol):
    def get_operation(self) -> str:
        """Gets the operation from the user."""
        ...

    def get_operand(self, prompt: str) -> float:
        """Gets an operand from the user."""
        ...

    def display_result(self, result: float) -> None:
        """Displays the result to the user."""
        ...

    def display_error(self, message: str) -> None:
        """Displays an error message to the user."""
        ...

    def display_history(self, history: CalculationHistory) -> None:
        """Displays the calculation history to the user."""
        ...

    def should_exit(self) -> bool:
        """Prompts the user to exit or continue."""
        ...

# Implementations

class SimpleCalculator:
    def __init__(self) -> None:
        self._history: CalculationHistory = []
        self.history_limit: int = 5

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
        """Performs division."""
        if operand2 == 0:
            raise DivisionByZero()
        return operand1 / operand2

    def get_history(self) -> CalculationHistory:
        """Retrieves the calculation history."""
        return self._history

    def clear_history(self) -> None:
        """Clears the calculation history."""
        self._history = []

    def _add_to_history(self, calculation: Calculation) -> None:
         """Adds calculation to history, maintaining the limit"""
         self._history.append(calculation)
         if len(self._history) > self.history_limit:
             self._history = self._history[-self.history_limit:] #Keep the latest

class CommandLineUI:
    def get_operation(self) -> str:
        """Gets the operation from the user."""
        return input("Enter operation (add, subtract, multiply, divide, history, clear, exit): ").lower()

    def get_operand(self, prompt: str) -> float:
        """Gets an operand from the user."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                self.display_error("Invalid input. Please enter a number.")

    def display_result(self, result: float) -> None:
        """Displays the result to the user."""
        print(f"Result: {result}")

    def display_error(self, message: str) -> None:
        """Displays an error message to the user."""
        print(f"Error: {message}")

    def display_history(self, history: CalculationHistory) -> None:
        """Displays the calculation history to the user."""
        if not history:
            print("No history available.")
            return

        print("Calculation History:")
        for calc in reversed(history): #display in reverse chronological order
            print(f"{calc['operation']}({calc['operand1']}, {calc['operand2']}) = {calc['result']}")

    def should_exit(self) -> bool:
        """Prompts the user to exit or continue."""
        answer = input("Exit? (yes/no): ").lower()
        return answer == "yes"

# Main Application

class CalculatorApp:
    def __init__(self, calculator: Calculator, ui: UserInterface) -> None:
        self.calculator = calculator
        self.ui = ui

    def run(self) -> None:
        """Runs the calculator application."""
        while True:
            operation = self.ui.get_operation()

            if operation == "exit":
                break
            elif operation == "history":
                self.ui.display_history(self.calculator.get_history())
            elif operation == "clear":
                self.calculator.clear_history()
                print("History cleared.")
            elif operation in ("add", "subtract", "multiply", "divide"):
                try:
                    operand1 = self.ui.get_operand("Enter first operand: ")
                    operand2 = self.ui.get_operand("Enter second operand: ")

                    if operation == "add":
                        result = self.calculator.add(operand1, operand2)
                    elif operation == "subtract":
                        result = self.calculator.subtract(operand1, operand2)
                    elif operation == "multiply":
                        result = self.calculator.multiply(operand1, operand2)
                    elif operation == "divide":
                        result = self.calculator.divide(operand1, operand2)
                    else:
                        raise ValueError("Unexpected operation. This should not happen.")

                    self.ui.display_result(result)
                    calculation: Calculation = {
                        "operation": operation,
                        "operand1": operand1,
                        "operand2": operand2,
                        "result": result,
                    }
                    if isinstance(self.calculator, SimpleCalculator):
                        self.calculator._add_to_history(calculation) #access protected member

                except DivisionByZero as e:
                    self.ui.display_error(e.message)
                except InvalidInput as e:
                    self.ui.display_error(e.message)
                except IncorrectArguments as e:
                    self.ui.display_error(e.message)
                except Exception as e:
                    self.ui.display_error(f"An unexpected error occurred: {e}")
            else:
                self.ui.display_error("Invalid operation.")

            if self.ui.should_exit():
                break

# Unit Tests

class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator: Calculator = SimpleCalculator()

    def test_add(self) -> None:
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(-1, 1), 0)
        self.assertEqual(self.calculator.add(2.5, 3.5), 6.0)

    def test_subtract(self) -> None:
        self.assertEqual(self.calculator.subtract(5, 2), 3)
        self.assertEqual(self.calculator.subtract(1, -1), 2)
        self.assertEqual(self.calculator.subtract(5.5, 2.5), 3.0)

    def test_multiply(self) -> None:
        self.assertEqual(self.calculator.multiply(2, 3), 6)
        self.assertEqual(self.calculator.multiply(-1, 1), -1)
        self.assertEqual(self.calculator.multiply(2.5, 2), 5.0)

    def test_divide(self) -> None:
        self.assertEqual(self.calculator.divide(6, 2), 3)
        self.assertEqual(self.calculator.divide(1, -1), -1)
        self.assertEqual(self.calculator.divide(5.0, 2.0), 2.5)

        with self.assertRaises(DivisionByZero):
            self.calculator.divide(5, 0)

    def test_history(self) -> None:
        self.calculator.add(1,2)
        self.calculator.subtract(5,3)
        history = self.calculator.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['operation'], "add")
        self.assertEqual(history[1]['operation'], "subtract")
        self.assertEqual(history[0]['operand1'], 1)
        self.assertEqual(history[0]['operand2'], 2)
        self.assertEqual(history[1]['operand1'], 5)
        self.assertEqual(history[1]['operand2'], 3)

    def test_clear_history(self) -> None:
        self.calculator.add(1,2)
        self.calculator.clear_history()
        self.assertEqual(len(self.calculator.get_history()), 0)

    def test_history_limit(self) -> None:
        self.calculator.history_limit = 3 #Reduce history limit for testing
        self.calculator.add(1,1)
        self.calculator.subtract(2,1)
        self.calculator.multiply(3,1)
        self.calculator.divide(4,1)
        history = self.calculator.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['operation'], "subtract")
        self.assertEqual(history[1]['operation'], "multiply")
        self.assertEqual(history[2]['operation'], "divide")

class TestCommandLineUI(unittest.TestCase):
    @patch('builtins.input', return_value='add')
    def test_get_operation(self, mock_input) -> None:
        ui = CommandLineUI()
        self.assertEqual(ui.get_operation(), 'add')

    @patch('builtins.input', return_value='5')
    def test_get_operand(self, mock_input) -> None:
        ui = CommandLineUI()
        self.assertEqual(ui.get_operand("Enter operand: "), 5.0)

    @patch('builtins.input', side_effect=['abc', '5'])
    def test_get_operand_invalid_input(self, mock_input) -> None:
        ui = CommandLineUI()
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            self.assertEqual(ui.get_operand("Enter operand: "), 5.0)
            self.assertIn("Invalid input", stdout.getvalue())

    def test_display_result(self) -> None:
        ui = CommandLineUI()
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            ui.display_result(10.0)
            self.assertEqual(stdout.getvalue().strip(), "Result: 10.0")

    def test_display_error(self) -> None:
        ui = CommandLineUI()
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            ui.display_error("Test Error")
            self.assertEqual(stdout.getvalue().strip(), "Error: Test Error")

    def test_display_history(self) -> None:
        ui = CommandLineUI()
        history: CalculationHistory = [{"operation": "add", "operand1": 1.0, "operand2": 2.0, "result": 3.0}]
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            ui.display_history(history)
            self.assertIn("Calculation History:", stdout.getvalue())
            self.assertIn("add(1.0, 2.0) = 3.0", stdout.getvalue())

    def test_display_history_empty(self) -> None:
        ui = CommandLineUI()
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            ui.display_history([])
            self.assertIn("No history available.", stdout.getvalue())

    @patch('builtins.input', return_value='yes')
    def test_should_exit(self, mock_input) -> None:
        ui = CommandLineUI()
        self.assertTrue(ui.should_exit())

    @patch('builtins.input', return_value='no')
    def test_should_not_exit(self, mock_input) -> None:
        ui = CommandLineUI()
        self.assertFalse(ui.should_exit())

class TestCalculatorApp(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = SimpleCalculator()
        self.ui = CommandLineUI()
        self.app = CalculatorApp(self.calculator, self.ui)

    @patch('builtins.input', side_effect=['add', '2', '3', 'yes'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_add(self, mock_stdout, mock_input) -> None:
        self.app.run()
        self.assertIn("Result: 5.0", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['divide', '5', '0', 'yes'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_divide_by_zero(self, mock_stdout, mock_input) -> None:
        self.app.run()
        self.assertIn("Division by zero", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['invalid', 'yes'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_invalid_operation(self, mock_stdout, mock_input) -> None:
        self.app.run()
        self.assertIn("Invalid operation.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['history', 'yes'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_history(self, mock_stdout, mock_input) -> None:
       #First perform a calculation to have something in history
        self.calculator.add(5,5)
        self.app.run()
        self.assertIn("Calculation History:", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['clear', 'yes'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_clear(self, mock_stdout, mock_input) -> None:
        #First perform a calculation to have something in history
        self.calculator.add(5,5)
        self.app.run()
        self.assertIn("History cleared.", mock_stdout.getvalue())
        self.assertEqual(len(self.calculator.get_history()), 0)

    @patch('builtins.input', side_effect=['exit'])
    def test_run_exit(self, mock_input) -> None:
        self.app.run()
# Documentation

"""
How to run the application:

1.  Save the code as a Python file (e.g., calculator.py).
2.  Run the file from the command line: python calculator.py

Features:

-   The application supports addition, subtraction, multiplication, and division.
-   It handles both integer and floating-point numbers.
-   It includes error handling for division by zero and invalid input.
-   It keeps a history of the last 5 calculations.
-   You can type 'history' to view the calculation history.
-   You can type 'clear' to clear the calculation history.
-   Type 'exit' to quit the application.
"""

# Main Execution
if __name__ == "__main__":
    calculator = SimpleCalculator()
    ui = CommandLineUI()
    app = CalculatorApp(calculator, ui)
    app.run()
```