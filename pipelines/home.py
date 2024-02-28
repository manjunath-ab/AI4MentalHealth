import streamlit as st
#from  login import login, sign_up
import login
import agent_chat_prod
import therapy
import dashboard

def main():
    
    # Initialize login status
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    option = st.sidebar.selectbox("Menu", ["Chat", "Sign Up", "Login","Therapist View","Admin Dashboard"])

    if option == "Chat":
        if (st.session_state.is_logged_in and st.session_state.user_type == "Patient") or (st.session_state.is_logged_in and st.session_state.user_type == "Admin"):
            agent_chat_prod.main()
        else:
            st.write("Please log in as a patient to access the chat.")

    elif option == "Therapist View":
        if (st.session_state.is_logged_in and st.session_state.user_type == "Doctor") or (st.session_state.is_logged_in and st.session_state.user_type == "Admin"):
            

            therapy.main()
        else:
            st.write("Please log in as Therapist to access this page.")

    elif option == "Admin Dashboard":
        if st.session_state.is_logged_in and st.session_state.user_type == "Admin":
            st.write("Admin Dashboard")
            dashboard.main()
        else:
            st.write("Please log in as Admin to access the dashboard.")
    
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

