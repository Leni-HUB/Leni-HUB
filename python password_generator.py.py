import random
import string

# Function to generate a password
def generate_password(length=12, complexity="medium"):
    """
    Generate a random password.
    
    Args:
        length (int): Length of the password.
        complexity (str): Complexity level - "low", "medium", or "high".
    
    Returns:
        str: Generated password.
    """
    if complexity == "low":
        characters = string.ascii_lowercase
    elif complexity == "medium":
        characters = string.ascii_letters + string.digits
    elif complexity == "high":
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        raise ValueError("Invalid complexity level. Choose 'low', 'medium', or 'high'.")
    
    return ''.join(random.choice(characters) for _ in range(length))

# Function to save the password to a file
def save_password(password, filename="passwords.txt"):
    """
    Save the password to a file.
    
    Args:
        password (str): The password to save.
        filename (str): The file to save the password in.
    """
    with open(filename, "a") as file:
        file.write(password + "\n")
    print(f"Password saved to {filename}")

# Main program
if __name__ == "__main__":
    print("Welcome to the Password Generator!")
    length = int(input("Enter the desired password length: "))
    complexity = input("Enter the complexity level (low, medium, high): ").lower()
    
    try:
        password = generate_password(length, complexity)
        print(f"Generated Password: {password}")
        
        save_option = input("Do you want to save this password? (yes/no): ").lower()
        if save_option == "yes":
            save_password(password)
        else:
            print("Password not saved.")
    except ValueError as e:
        print(e)