""" 
Nov 09 2024

File successfully demonstrates how marvin/openai assistant can be used in a streamlit app, using predefined functions as tools that maniuplate the data.

Simply do "if prompt := st.chat_input("Enter your prompt"):" to get a chatbox in the app.
and make sure that your data is changed downstream (in the .py file) of that chatbox.

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from marvin.beta import Assistant, Application, Thread
from streamlit_chat import message


# Create an editable data frame with two columns, X and Y
data = {"X": [1, 2, 3, 4, 5], "Y": [2, 3, 5, 7, 11]}
df = pd.DataFrame(data)
edited_df = st.data_editor(df, num_rows="dynamic")

# Dropdown menu for styles and functions
style_options = ["Line", "Bar", "Scatter"]
function_options = ["None", "Square", "Square Root"]

selected_style = st.selectbox("Select plot style", style_options)
selected_function = st.selectbox("Select function to apply", function_options)

# Apply function to the Y column
if selected_function == "Square":
    edited_df["Y"] = edited_df["Y"] ** 2
elif selected_function == "Square Root":
    edited_df["Y"] = edited_df["Y"] ** 0.5


# Define the tool_function
def change_data_tool():
    # Multiply the Y column by -1, reflects data about the x-axis
    edited_df["Y"] = edited_df["Y"] * -1
    st.write("Tool function executed! Data has been multiplied by -1.")


# Initialize the Marvin AI assistant
instructions = """\
    You are an assistant data analyst who helps users analyze data and make plots. You facilitate data manipulations, style changes, data queries, and statistic evaluations by using the tools provided.\
    """

assistant = Assistant(
    name="Data Analyst",
    instructions=instructions,
    tools=[change_data_tool],
)

# Add a button to run tool_function
if st.button("Run Tool Function"):
    change_data_tool()

# Chatbox for interacting with the Marvin AI assistant
st.header("### Chat with Marvin AI Assistant")
if prompt := st.chat_input("Enter your prompt"):
    run = assistant.say(prompt)
    st.write(run.messages[-1].content[-1].text.value)


# Plot the results
fig, ax = plt.subplots()
if selected_style == "Line":
    ax.plot(edited_df["X"], edited_df["Y"])
elif selected_style == "Bar":
    ax.bar(edited_df["X"], edited_df["Y"])
elif selected_style == "Scatter":
    ax.scatter(edited_df["X"], edited_df["Y"])

ax.set_title("Function called!")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")

st.pyplot(fig)


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# for i, msg in enumerate(st.session_state["messages"]):
#     message(msg["content"], is_user=msg["is_user"], key=str(i))

# # User input
# user_input = st.text_input("You: ", "")

# if user_input:
#     # Display user message in chat message container
#     st.session_state["messages"].append({"content": user_input, "is_user": True})
#     message(user_input, is_user=True)

#     # Get assistant response
#     run = assistant.say(user_input)
#     text = run.messages[-1].content[-1].text.value

#     st.session_state["messages"].append({"content": text, "is_user": False})
#     message(text, is_user=False)

#     st.write(run)
