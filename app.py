import streamlit as st
import pandas as pd
import os

# CSV file to store data
DATA_FILE = r"https://docs.google.com/spreadsheets/d/1Gg2bd5mj-Nqo7Ffag4dnvY5FdgAs-uzW8rrJ0OuD_0c/edit?gid=0#gid=0"

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["goods", "total_paid", "quantity", "unit_price"])

# Save data to CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Main app
st.title("Goods Cost Tracker")

# Load historical data
df = load_data()

# Input form
with st.form("purchase_form", clear_on_submit=True):
    goods = st.text_input("Goods name")
    total_paid = st.number_input("Total paid", min_value=0.0, step=0.01, format="%.2f")
    quantity = st.number_input("Quantity", min_value=1.0, step=1.0, format="%.0f")
    submitted = st.form_submit_button("Add purchase")

    if submitted and goods and total_paid > 0 and quantity > 0:
        unit_price = total_paid / quantity

        # Check for historical average
        matching = df[df["goods"] == goods]
        if not matching.empty:
            avg_past_price = matching["unit_price"].mean()
            if unit_price > avg_past_price * 1.10:
                st.warning(
                    f"⚠️ The price per unit ({unit_price:.2f}) is more than 10% higher than your historical average ({avg_past_price:.2f}) for '{goods}'."
                )

        # Add new row
        new_row = {"goods": goods, "total_paid": total_paid, "quantity": quantity, "unit_price": unit_price}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success(f"Added purchase for {goods}.")

# Show dropdown for existing goods
if not df.empty:
    st.subheader("Purchase History")
    goods_list = df["goods"].unique().tolist()
    selected_goods = st.selectbox("Select goods to view history", [""] + goods_list)
    if selected_goods:
        st.dataframe(df[df["goods"] == selected_goods].reset_index(drop=True))
    else:
        st.dataframe(df)

st.caption("All data is stored locally in 'purchase_history.csv'.")
