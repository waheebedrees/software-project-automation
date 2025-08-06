```
# Calculator Application Documentation

## Overview

This document provides comprehensive information on how to use the command-line calculator application. The application supports basic arithmetic operations: addition, subtraction, multiplication, and division. It can handle both integer and floating-point numbers and offers a history feature to display the last 5 calculations.

## 1. Installation and Setup

### Prerequisites

-   Python 3.6 or higher must be installed on your system.

### Installation Steps

1.  **Download the application:** Obtain the `calculator.py` file.
2.  **No further installation is required:** The application is a single Python script and does not require any additional installation steps.

## 2. Available Operations

The calculator supports the following operations:

-   **Addition:** `+`
-   **Subtraction:** `-`
-   **Multiplication:** `*`
-   **Division:** `/`

## 3. Usage Examples

The calculator can be used in two modes: command-line mode and interactive mode.

### Command-Line Mode

To use the calculator in command-line mode, open your terminal and run the script with the operator and operands as arguments.

#### Syntax

```bash
python calculator.py <operator> <operand1> <operand2>
```

#### Examples

1.  **Addition:**

    ```bash
    python calculator.py + 5 3
    ```

    Output:

    ```
    8.0
    ```

2.  **Subtraction:**

    ```bash
    python calculator.py - 10 4
    ```

    Output:

    ```
    6.0
    ```

3.  **Multiplication:**

    ```bash
    python calculator.py * 2.5 4
    ```

    Output:

    ```
    10.0
    ```

4.  **Division:**

    ```bash
    python calculator.py / 15 3
    ```

    Output:

    ```
    5.0
    ```

### Interactive Mode

To use the calculator in interactive mode, run the script without any arguments. The application will prompt you to enter calculations.

#### Running in Interactive Mode

```bash
python calculator.py
```

#### Interactive Mode Commands

-   Enter a calculation in the format: `<operator> <operand1> <operand2>`
-   Type `history` to view the calculation history.
-   Type `exit` to exit the application.

#### Interactive Mode Example

```
Enter calculation (e.g., + 1 2), 'history', or 'exit': + 5 5
10.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': - 10 2
8.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': history
2024-10-27 10:00:00 - 5.0 + 5.0 = 10.0
2024-10-27 10:01:00 - 10.0 - 2.0 = 8.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': exit
Exiting calculator.
```

## 4. Error Handling Guide

The calculator includes error handling to manage common issues.

### Division by Zero

Attempting to divide by zero will result in an error message.

#### Example

```bash
python calculator.py / 10 0
```

Output:

```
Error: Division by zero is not allowed.
```

In interactive mode:

```
Enter calculation (e.g., + 1 2), 'history', or 'exit': / 10 0
Error: Division by zero is not allowed.
```

### Invalid Input

Invalid input, such as non-numeric operands or invalid operators, will result in an error message.

#### Example

```bash
python calculator.py + 5 a
```

Output:

```
Error: Invalid input. Please provide a valid number.
```

In interactive mode:

```
Enter calculation (e.g., + 1 2), 'history', or 'exit': + 5 a
Error: Invalid input. Please provide a valid number.
```

### Incorrect Number of Arguments

Providing an incorrect number of arguments in command-line mode will result in an error message.

#### Example

```bash
python calculator.py + 5
```

Output:

```
Error: Incorrect number of arguments. Expected 2 operands and 1 operator.
```

In interactive mode, ensure that each calculation entry has exactly one operator and two operands.

## 5. History Feature Usage

The calculator keeps track of the last 5 calculations. To view the history, type `history` in interactive mode.

### Viewing History

In interactive mode:

```
Enter calculation (e.g., + 1 2), 'history', or 'exit': + 1 1
2.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': - 5 2
3.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': * 4 2
8.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': / 10 2
5.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': + 6 3
9.0
Enter calculation (e.g., + 1 2), 'history', or 'exit': history
2024-10-27 10:02:00 - 1.0 + 1.0 = 2.0
2024-10-27 10:03:00 - 5.0 - 2.0 = 3.0
2024-10-27 10:04:00 - 4.0 * 2.0 = 8.0
2024-10-27 10:05:00 - 10.0 / 2.0 = 5.0
2024-10-27 10:06:00 - 6.0 + 3.0 = 9.0
```

The history displays the timestamp, operation, and result of each calculation.  Only the last 5 calculations are stored.

## 6. Troubleshooting

### Application Not Running

-   **Problem:** The application does not start when running `python calculator.py`.
-   **Solution:** Ensure that Python is correctly installed and that the `calculator.py` file exists in the directory where you are running the command.

### Incorrect Calculation Results

-   **Problem:** The calculator returns incorrect results.
-   **Solution:** Verify that you are using the correct operator and operands. Double-check the input values for any typos.

### Error Messages

-   **Problem:** Encountering error messages during calculations.
-   **Solution:** Refer to the Error Handling Guide (Section 4) for explanations and solutions to common error messages.
```