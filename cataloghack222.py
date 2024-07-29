import json
from sympy import mod_inverse

def convert_to_decimal(value, base):
    return int(value, base)

def lagrange_interpolation(x, y, p):
    """
    Lagrange interpolation to find the constant term of the polynomial.
    x: list of x-coordinates of the points
    y: list of y-coordinates of the points
    p: prime number for modulo operations
    """
    k = len(x)
    constant_term = 0
    
    for i in range(k):
        term = y[i]
        for j in range(k):
            if i != j:
                term *= x[j] * mod_inverse(x[j] - x[i], p)
                term %= p
        constant_term += term
        constant_term %= p
    
    return constant_term

def find_constant_term(json_data):
    # Parse the JSON data
    data = json.loads(json_data)
    
    keys = data['keys']
    n = keys['n']
    k = keys['k']
    
    # Collect points from JSON data
    x = []
    y = []
    for i in range(1, n + 1):
        if str(i) in data:
            try:
                point = data[str(i)]
                base = int(point['base'])
                value = point['value']
                decimal_value = convert_to_decimal(value, base)
                x.append(i)
                y.append(decimal_value)
                
                if len(x) == k:
                    break
            except ValueError:
                continue
    
    if len(x) < k:
        raise ValueError("Not enough valid shares to reconstruct the polynomial.")
    
    # Large prime number for modulo operations (suitable for 256-bit integers)
    p = 2**256 - 189  # Example of a large prime number
    
    # Find the constant term using Lagrange interpolation
    constant_term = lagrange_interpolation(x, y, p)
    
    return constant_term

# Load JSON data from file
with open('D:/Documents/sample-cata.json') as f:
    json_data = f.read()

constant_term = find_constant_term(json_data)
print(f"The constant term (private key) of the polynomial is: {constant_term}")
