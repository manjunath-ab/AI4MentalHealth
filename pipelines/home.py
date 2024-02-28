import streamlit as st
#from  login import login, sign_up
import login
import agent_chat_prod
import dashboard
import pandas as pd

def main():
    
    # Initialize login status
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    option = st.sidebar.selectbox("Menu", ["Chat", "Sign Up", "Login", "Dashboard"])

    if option == "Chat":
        if st.session_state.is_logged_in:
            agent_chat_prod.main()
        else:
            st.write("Please log in to access the home page.")

    
    elif option == "Login":
        st.session_state.is_logged_in = login.main()
        st.session_state.is_logged_in=True

    elif option == "Dashboard":  # Add this new condition
        if st.session_state.is_logged_in:
            dashboard.main()  # Call the main function of the therapist dashboard
        else:
            st.write("Please log in to access the therapist dashboard.")

    else:
        st.session_state.is_logged_in = login.main()
        st.session_state.is_logged_in=True

if __name__ == "__main__":
    main()

