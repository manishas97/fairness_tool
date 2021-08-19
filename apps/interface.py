import streamlit as st
import numpy as np
from apps import firestore_calls as fc

def app():
    st.write(
        """
        ## 👾 Tic Tac Toe
        
        Let's play! This demo stores the entire game state (as a dict) in 
        `st.session_state` and uses the new callbacks to handle button clicks.
        """
    )
    st.write("")

    # Initialize state.
    if "board" not in st.session_state:
        board_values = np.array(fc.get_inequalities())

        st.session_state.board = board_values
        
        #st.session_state.board_2 = fc.get_philosophies(selected_model)

    # Define callbacks to handle button clicks.
    def handle_click(i,field):
      #if not recommend:
      st.session_state.board[i,field] = ( "." if st.session_state.board[i,field] == "X" else "X")
      #if recommend:
        #recommendation_board(board);

   # Show one button for each field.
    for i, field in enumerate(st.session_state.board):
        st.write(field)
        cols = st.beta_columns([0.1, 0.1, 0.1, 0.7])
        cols[i].button(".", key=f"{i-field}",
                on_click=handle_click(i,field),
                args=(i),
        )

    if st.session_state.winner:
        st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")

