elif st.session_state.stage == "final_code_entry":
    st.subheader("🗝️ The Master Code")
    st.info("You have successfully collected all 3 secret codes from the sets. Combine them together to unlock the final submission.")
    
    master_input = st.text_input("Enter the combined Master Code:")
    
    if st.button("Submit Final Log"):
        # Combine all secret codes to check the answer (e.g., "TENYEARCYCLE")
        correct_master_code = "".join([s["secret_code"].lower() for s in SETS])
        
        # Clean user input (remove spaces, make lowercase)
        user_clean = master_input.strip().replace(" ", "").lower()
        
        if user_clean == correct_master_code:
            st.session_state.stage = "finished"
            st.rerun()
        else:
            st.error("❌ Incorrect Master Code. Please check the codes you received and try again.")
