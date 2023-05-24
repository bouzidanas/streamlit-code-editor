# EXAMPLE CODE

# Function to convert Fahrenheit to Celsius
def fahrenheit_to_celsius(fahrenheit):
    # Convert Fahrenheit to Celsius
    celsius = (fahrenheit - 32) / 1.8

    # Display the result
    print(f"{fahrenheit} degrees Fahrenheit is equivalent to {celsius} degrees Celsius")

# Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    # Convert Celsius to Fahrenheit
    fahrenheit = (celsius * 1.8) + 32

    # Display the result
    print(f"{celsius} degrees Celsius is equivalent to {fahrenheit} degrees Fahrenheit")

# User input temperature in Fahrenheit
fahrenheit = float(input("Enter temperature in Fahrenheit: "))

# Convert Fahrenheit to Celsius
fahrenheit_to_celsius(fahrenheit)

# User input temperature in Celsius
celsius = float(input("Enter temperature in Celsius: "))

# Convert Celsius to Fahrenheit
celsius_to_fahrenheit(celsius)
