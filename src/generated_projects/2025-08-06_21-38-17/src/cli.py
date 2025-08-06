```
// Calculator Application IDL-like Specification

// Data Structures

// Structure to represent a calculation entry in history
struct CalculationEntry {
    string operation; // e.g., "1 + 2"
    double result;
    string timestamp; // e.g., "2024-10-27 10:00:00"
};

// Type Definitions
typedef sequence<CalculationEntry> CalculationHistory; // A sequence (list) of CalculationEntry

// Error Specifications

// Exception for division by zero
exception DivisionByZero {
    string message; // Error message: "Division by zero is not allowed."
};

// Exception for invalid input
exception InvalidInput {
    string message; // Error message: "Invalid input. Please provide a valid number."
};

// Exception for incorrect number of arguments
exception InvalidArgumentCount {
    string message; // Error message: "Incorrect number of arguments. Expected 2 operands and 1 operator."
};

// Interface Definitions

// Interface for the Calculator
interface Calculator {
    // Performs addition
    double add(in double operand1, in double operand2);

    // Performs subtraction
    double subtract(in double operand1, in double operand2);

    // Performs multiplication
    double multiply(in double operand1, in double operand2);

    // Performs division; may raise DivisionByZero exception
    double divide(in double operand1, in double operand2) raises DivisionByZero;
};

// Interface for History Management
interface HistoryManager {
    // Adds a calculation to the history
    void addCalculation(in string operation, in double result);

    // Retrieves the last N calculations from the history
    CalculationHistory getHistory(in long n); // long n = max history items to retrieve
};

// Interface for the Calculator Application
interface CalculatorApp {
    // Performs a calculation based on the provided operator and operands.
    // Returns the result of the calculation.
    // May raise InvalidInput, DivisionByZero, or InvalidArgumentCount exceptions.
    double calculate(in string operator, in double operand1, in double operand2) raises InvalidInput, DivisionByZero, InvalidArgumentCount;

    // Displays the calculation history
    void displayHistory();

    // Exits the application
    void exit();
};
```