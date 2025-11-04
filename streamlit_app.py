from collections import defaultdict
from pathlib import Path
# import sqlite3  <- 削除
from st_supabase_connection import SupabaseConnection # <- 追加

import streamlit as st
import altair as alt
import pandas as pd


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Inventory tracker",
    page_icon=":shopping_bags:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.

# connect_db() は st.connection に置き換えるため不要
# def connect_db(): ...

def initialize_data(conn: SupabaseConnection):
    """Initializes the inventory table with some data."""
    
    # CREATE TABLE は Supabase ダッシュボードで実行するため、ここでは実行しない
    
    # Supabase Python client (conn.client) を使ってデータを挿入
    data_to_insert = [
        # Beverages
        {'item_name': 'Bottled Water (500ml)', 'price': 1.50, 'units_sold': 115, 'units_left': 15, 'cost_price': 0.80, 'reorder_point': 16, 'description': 'Hydrating bottled water'},
        {'item_name': 'Soda (355ml)', 'price': 2.00, 'units_sold': 93, 'units_left': 8, 'cost_price': 1.20, 'reorder_point': 10, 'description': 'Carbonated soft drink'},
        {'item_name': 'Energy Drink (250ml)', 'price': 2.50, 'units_sold': 12, 'units_left': 18, 'cost_price': 1.50, 'reorder_point': 8, 'description': 'High-caffeine energy drink'},
        {'item_name': 'Coffee (hot, large)', 'price': 2.75, 'units_sold': 11, 'units_left': 14, 'cost_price': 1.80, 'reorder_point': 5, 'description': 'Freshly brewed hot coffee'},
        {'item_name': 'Juice (200ml)', 'price': 2.25, 'units_sold': 11, 'units_left': 9, 'cost_price': 1.30, 'reorder_point': 5, 'description': 'Fruit juice blend'},

        # Snacks
        {'item_name': 'Potato Chips (small)', 'price': 2.00, 'units_sold': 34, 'units_left': 16, 'cost_price': 1.00, 'reorder_point': 10, 'description': 'Salted and crispy potato chips'},
        {'item_name': 'Candy Bar', 'price': 1.50, 'units_sold': 6, 'units_left': 19, 'cost_price': 0.80, 'reorder_point': 15, 'description': 'Chocolate and candy bar'},
        {'item_name': 'Granola Bar', 'price': 2.25, 'units_sold': 3, 'units_left': 12, 'cost_price': 1.30, 'reorder_point': 8, 'description': 'Healthy and nutritious granola bar'},
        {'item_name': 'Cookies (pack of 6)', 'price': 2.50, 'units_sold': 8, 'units_left': 8, 'cost_price': 1.50, 'reorder_point': 5, 'description': 'Soft and chewy cookies'},
        {'item_name': 'Fruit Snack Pack', 'price': 1.75, 'units_sold': 5, 'units_left': 10, 'cost_price': 1.00, 'reorder_point': 8, 'description': 'Assortment of dried fruits and nuts'},

        # Personal Care
        {'item_name': 'Toothpaste', 'price': 3.50, 'units_sold': 1, 'units_left': 9, 'cost_price': 2.00, 'reorder_point': 5, 'description': 'Minty toothpaste for oral hygiene'},
        {'item_name': 'Hand Sanitizer (small)', 'price': 2.00, 'units_sold': 2, 'units_left': 13, 'cost_price': 1.20, 'reorder_point': 8, 'description': 'Small sanitizer bottle for on-the-go'},
        {'item_name': 'Pain Relievers (pack)', 'price': 5.00, 'units_sold': 1, 'units_left': 5, 'cost_price': 3.00, 'reorder_point': 3, 'description': 'Over-the-counter pain relief medication'},
        {'item_name': 'Bandages (box)', 'price': 3.00, 'units_sold': 0, 'units_left': 10, 'cost_price': 2.00, 'reorder_point': 5, 'description': 'Box of adhesive bandages for minor cuts'},
        {'item_name': 'Sunscreen (small)', 'price': 5.50, 'units_sold': 6, 'units_left': 5, 'cost_price': 3.50, 'reorder_point': 3, 'description': 'Small bottle of sunscreen for sun protection'},

        # Household
        {'item_name': 'Batteries (AA, pack of 4)', 'price': 4.00, 'units_sold': 1, 'units_left': 5, 'cost_price': 2.50, 'reorder_point': 3, 'description': 'Pack of 4 AA batteries'},
        {'item_name': 'Light Bulbs (LED, 2-pack)', 'price': 6.00, 'units_sold': 3, 'units_left': 3, 'cost_price': 4.00, 'reorder_point': 2, 'description': 'Energy-efficient LED light bulbs'},
        {'item_name': 'Trash Bags (small, 10-pack)', 'price': 3.00, 'units_sold': 5, 'units_left': 10, 'cost_price': 2.00, 'reorder_point': 5, 'description': 'Small trash bags for everyday use'},
        {'item_name': 'Paper Towels (single roll)', 'price': 2.50, 'units_sold': 3, 'units_left': 8, 'cost_price': 1.50, 'reorder_point': 5, 'description': 'Single roll of paper towels'},
        {'item_name': 'Multi-Surface Cleaner', 'price': 4.50, 'units_sold': 2, 'units_left': 5, 'cost_price': 3.00, 'reorder_point': 3, 'description': 'All-purpose cleaning spray'},

        # Others
        {'item_name': 'Lottery Tickets', 'price': 2.00, 'units_sold': 17, 'units_left': 20, 'cost_price': 1.50, 'reorder_point': 10, 'description': 'Assorted lottery tickets'},
        {'item_name': 'Newspaper', 'price': 1.50, 'units_sold': 22, 'units_left': 20, 'cost_price': 1.00, 'reorder_point': 5, 'description': 'Daily newspaper'}
    ]

    try:
        # conn.client (Supabase Python Client) を使って挿入
        conn.client.table("inventory").insert(data_to_insert).execute()
    except Exception as e:
        st.error(f"Error initializing data: {e}")
        st.stop()


def load_data(conn: SupabaseConnection):
    """Loads the inventory data from the database."""
    
    try:
        # conn.query() を使用 (SELECT * FROM inventory)
        # ttl=0 を設定し、キャッシュを無効にして常に最新データを取得
        response = conn.query("*", table="inventory", ttl=0).execute()
        
        if not response.data:
            return pd.DataFrame() # 空の DataFrame を返す

        df = pd.DataFrame(response.data)
        return df

    except Exception as e:
        # (例: "relation public.inventory does not exist" など)
        st.error(f"Error loading data: {e}")
        st.error("Have you created the 'inventory' table in your Supabase SQL Editor? (See instructions in the code)")
        return None


def update_data(conn: SupabaseConnection, df: pd.DataFrame, changes: dict):
    """Updates the inventory data in the database."""
    
    # conn.client (Supabase Python Client) を使用
    try:
        if changes["edited_rows"]:
            deltas = st.session_state.inventory_table["edited_rows"]
            for i, delta in deltas.items():
                row_dict = df.iloc[i].to_dict()
                row_id = int(row_dict["id"])
                
                # delta には変更されたカラムのみ含まれる
                conn.client.table("inventory").update(delta).eq("id", row_id).execute()

        if changes["added_rows"]:
            rows_to_add = []
            for row in changes["added_rows"]:
                # 'id' はDBで自動生成されるため、辞書から削除 (または None のままにする)
                row.pop('id', None) 
                # defaultdict は元のコードのままで動作するはず
                rows_to_add.append(defaultdict(lambda: None, row))
            
            if rows_to_add:
                conn.client.table("inventory").insert(rows_to_add).execute()

        if changes["deleted_rows"]:
            for i in changes["deleted_rows"]:
                row_id = int(df.loc[i, "id"])
                conn.client.table("inventory").delete().eq("id", row_id).execute()
        
        st.toast("Changes committed successfully!")

    except Exception as e:
        st.error(f"Error committing changes: {e}")


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
"""
# :shopping_bags: Inventory tracker

**Welcome to Alice's Corner Store's intentory tracker!**
This page reads and writes directly from/to our inventory database.
"""

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

# Connect to database (Supabase) using secrets
# conn, db_was_just_created = connect_db() <- 変更
try:
    conn = st.connection("supabase", type=SupabaseConnection)
except Exception as e:
    st.error(f"Error connecting to Supabase. Check your secrets: {e}")
    st.stop()


# Load data from database
df = load_data(conn)

# df が None (ロード失敗) の場合は停止
if df is None:
    st.stop()

# Initialize data (if table is empty)
# if db_was_just_created: <- 変更
if df.empty:
    st.warning("Inventory table is empty. Initializing with sample data.")
    initialize_data(conn)
    # データを再ロード
    df = load_data(conn)
    if df is None: # 再ロード失敗
        st.error("Failed to load data after initialization.")
        st.stop()
    st.rerun() # データを反映するために再実行


# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    column_config={
        # Show dollar sign before price columns.
        "price": st.column_config.NumberColumn(format="$%.2f"),
        "cost_price": st.column_config.NumberColumn(format="$%.2f"),
        # 'id' カラムを非表示にする (オプション)
        # "id": None, 
    },
    key="inventory_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.inventory_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.inventory_table),
)


# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Units left", divider="red")

# df が空の場合の処理を追加
if not df.empty:
    need_to_reorder = df[df["units_left"] < df["reorder_point"]].loc[:, "item_name"]

    if len(need_to_reorder) > 0:
        items = "\n".join(f"* {name}" for name in need_to_reorder)

        st.error(f"We're running dangerously low on the items below:\n {items}")

    ""
    ""

    st.altair_chart(
        # Layer 1: Bar chart.
        alt.Chart(df)
        .mark_bar(
            orient="horizontal",
        )
        .encode(
            x="units_left",
            y="item_name",
        )
        # Layer 2: Chart showing the reorder point.
        + alt.Chart(df)
        .mark_point(
            shape="diamond",
            filled=True,
            size=50,
            color="salmon",
            opacity=1,
        )
        .encode(
            x="reorder_point",
            y="item_name",
        ),
        use_container_width=True,
    )

    st.caption("NOTE: The :diamonds: location shows the reorder point.")
else:
    st.warning("No data to display charts.")

""
""
""

# -----------------------------------------------------------------------------

st.subheader("Best sellers", divider="orange")

""
""

if not df.empty:
    st.altair_chart(
        alt.Chart(df)
        .mark_bar(orient="horizontal")
        .encode(
            x="units_sold",
            y=alt.Y("item_name").sort("-x"),
        ),
        use_container_width=True,
    )
else:
    st.warning("No data to display charts.")
