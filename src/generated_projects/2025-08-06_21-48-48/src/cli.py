```
// IDL-like Specification for a Command-Line Calculator Application

// Data Structures

// Structure to represent a Calculation
struct Calculation {
    string operation; // e.g., "add", "subtract", "multiply", "divide"
    double operand1;
    double operand2;
    double result;
};

// Type Definitions
typedef sequence<Calculation> CalculationHistory; // A sequence (list) of Calculations

// Interface Definitions

// Interface for the Calculator
interface Calculator {
    // Performs addition
    double add(in double operand1, in double operand2);

    // Performs subtraction
    double subtract(in double operand1, in double operand2);

    // Performs multiplication
    double multiply(in double operand1, in double operand2);

    // Performs division
    double divide(in double operand1, in double operand2) raises (DivisionByZero);

    // Retrieves the calculation history
    CalculationHistory getHistory();

    // Clears the calculation history
    void clearHistory();
};

// Interface for User Input/Output
interface UserInterface {
    // Gets the operation from the user (e.g., "add", "subtract", etc.)
    string getOperation();

    // Gets an operand from the user
    double getOperand(in string prompt);

    // Displays the result to the user
    void displayResult(in double result);

    // Displays an error message to the user
    void displayError(in string message);

    // Displays the calculation history to the user
    void displayHistory(in CalculationHistory history);

    // Prompts the user to exit or continue
    boolean shouldExit();
};

// Error Specifications

// Exception for division by zero
exception DivisionByZero {
    string message; // Error message (e.g., "Division by zero is not allowed.")
};

// Exception for Invalid Input (e.g. non-numeric input)
exception InvalidInput {
    string message; //Error message (e.g. "Invalid input. Please enter a number.")
};

// Exception for Incorrect Arguments (e.g. wrong number of arguments)
exception IncorrectArguments {
    string message; // Error message (e.g. "Incorrect number of arguments provided.")
};
```