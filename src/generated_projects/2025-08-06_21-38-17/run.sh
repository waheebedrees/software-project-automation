```
#!/bin/bash

# Install dependencies (if any).  Since this is pure Python with no external
# dependencies beyond the standard library, this step is not needed.
# But, we can add a check for Python to be installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found"
    echo "Please install python3"
    exit
fi

# Run unit tests
echo "Running unit tests..."
python3 -m unittest test_calculator.py

echo "Unit tests completed."
```