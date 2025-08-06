```
## Command-Line Calculator Application Documentation

### 1. Introduction

This document provides comprehensive information on how to use the command-line calculator application. The application supports basic arithmetic operations, error handling, and a calculation history feature.

### 2. Installation and Setup

#### Prerequisites

-   Python 3.6 or higher must be installed on your system.

#### Installation Steps

1.  **Save the Code:** Save the provided Python code as a `.py` file (e.g., `calculator.py`). Ensure that all code is saved in the same file.
2.  **Run the Application:** Open a terminal or command prompt and navigate to the directory where you saved the file. Then, execute the application using the following command:

    ```bash
    python calculator.py
    ```

### 3. Available Operations

The calculator application supports the following operations:

-   **Addition:** Adds two numbers.
-   **Subtraction:** Subtracts one number from another.
-   **Multiplication:** Multiplies two numbers.
-   **Division:** Divides one number by another.
-   **History:** Displays the last 5 calculations.
-   **Clear:** Clears the calculation history.
-   **Exit:** Exits the application.

### 4. Usage Examples

#### Basic Calculations

1.  **Running the Calculator:**

    ```bash
    python calculator.py
    ```

2.  **Performing Addition:**

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): add
    Enter first operand: 5
    Enter second operand: 3
    Result: 8.0
    Exit? (yes/no): no
    ```

3.  **Performing Subtraction:**

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): subtract
    Enter first operand: 10
    Enter second operand: 4
    Result: 6.0
    Exit? (yes/no): no
    ```

4.  **Performing Multiplication:**

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): multiply
    Enter first operand: 2.5
    Enter second operand: 4
    Result: 10.0
    Exit? (yes/no): no
    ```

5.  **Performing Division:**

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): divide
    Enter first operand: 15
    Enter second operand: 3
    Result: 5.0
    Exit? (yes/no): no
    ```

#### History Feature

1.  **Viewing Calculation History:**

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): history
    Calculation History:
    divide(15.0, 3.0) = 5.0
    multiply(2.5, 4.0) = 10.0
    subtract(10.0, 4.0) = 6.0
    add(5.0, 3.0) = 8.0
    Exit? (yes/no): no
    ```

#### Clear Feature
1. **Clearing Calculation History:**
    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): clear
    History cleared.
    Exit? (yes/no): no
    ```

#### Exiting the Application

1.  **Exiting:**

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): exit
    ```

### 5. Error Handling Guide

The application includes error handling for common issues:

-   **Division by Zero:** If you attempt to divide a number by zero, the application will display an error message:

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): divide
    Enter first operand: 5
    Enter second operand: 0
    Error: Division by zero is not allowed.
    Exit? (yes/no): no
    ```

-   **Invalid Input:** If you enter non-numeric input when prompted for an operand, the application will display an error message:

    ```
    Enter operation (add, subtract, multiply, divide, history, clear, exit): add
    Enter first operand: abc
    Error: Invalid input. Please enter a number.
    Enter first operand: 5
    Enter second operand: 3
    Result: 8.0
    Exit? (yes/no): no
    ```

-   **Invalid Operation:** If you enter an invalid operation, the application will display an error:

    ```
     Enter operation (add, subtract, multiply, divide, history, clear, exit): invalid
     Error: Invalid operation.
     Exit? (yes/no): no
    ```

### 6. History Feature Usage

The application maintains a history of the last 5 calculations. To view the history, enter `history` at the operation prompt. The calculations are displayed in reverse chronological order (newest first).

If there is no history available, the application will display the message `No history available.`

The history is cleared when you enter `clear` at the operation prompt.

### 7. Troubleshooting

#### Application Not Starting

-   **Problem:** The application does not start when running `python calculator.py`.
-   **Solution:**
    -   Ensure that Python is installed correctly and is added to your system's PATH environment variable.
    -   Verify that you are running the command from the directory where the `calculator.py` file is located.
    -   Check for any syntax errors in the code.

#### Incorrect Calculation Results

-   **Problem:** The calculator returns incorrect results.
-   **Solution:**
    -   Double-check the operands and operation entered.
    -   If the issue persists, review the code for any logical errors in the arithmetic functions.

#### History Not Displaying

-   **Problem:** The history command does not display any calculations.
-   **Solution:**
    -   Ensure that you have performed some calculations first. The history is only populated after calculations are made.
    -   If you have cleared the history using the `clear` command, perform new calculations to populate the history again.

### 8. Unit Tests

The application includes unit tests to verify the correctness of the core arithmetic operations. To run the tests:

1.  Save the code with the tests as a `.py` file (e.g., `calculator.py`).
2.  Open a terminal or command prompt and navigate to the directory where you saved the file.
3.  Run the tests using the following command:

    ```bash
    python -m unittest calculator.py
    ```

All tests should pass. If any tests fail, review the code and tests to identify and fix the issues.
```