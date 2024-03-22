import streamlit as st

# Define function to perform multiplication
def multiply_numbers(num1, num2):
    return num1 * num2

# Create a Streamlit app
def main():
    # Set up the Streamlit app title and input fields
    st.title("Simple Streamlit Multiplication App")
    num1 = st.number_input("Enter the first number:")
    num2 = st.number_input("Enter the second number:")
    
    # Create a button to perform the multiplication
    if st.button("Multiply"):
        # Perform the multiplication
        result = multiply_numbers(num1, num2)
        # Store the result in session state
        st.session_state[f"{num1} * {num2}"] = result
       # st.session_state[f"{num1} * {num2}"] = result
       
       
    for key, value in st.session_state.items():
        st.write(f"{key} = {value}")
       
    
    # Display the result if it exists in session state
    if "result" in st.session_state:
        st.write(f"The result of multiplication is: {st.session_state.result}")

if __name__ == "__main__":
    main()
