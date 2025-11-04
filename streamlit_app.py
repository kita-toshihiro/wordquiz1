from collections import defaultdict
# from pathlib import Path  <- 不要
# import sqlite3           <- 不要

import streamlit as st
import altair as alt
import pandas as pd
from st_supabase_connection import SupabaseConnection # 追加

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Inventory tracker",
    page_icon=":shopping_bags:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.

# connect_db() 関数は st.connection を使うため不要


def initialize_data(conn):
    """
    Initializes the inventory table with some data.
    Assumes the 'inventory' table *already exists* in Supabase.
    """
    
    #
    # 注：CREATE TABLEコマンドは Supabase SQL エディタで手動実行する必要があります:
    #
    # CREATE TABLE IF NOT EXISTS inventory (
    #     id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    #     item_name TEXT,
    #     price REAL,
    #     units_sold INTEGER,
    #     units_left INTEGER,
    #     cost_price REAL,
    #     reorder_point INTEGER,
    #     description TEXT
    # );
    #

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
        # st-supabase-connection の insert メソッドを使用
        conn.insert(table="inventory", data=data_to_insert)
    except Exception as e:
        st.error(f"Error initializing data: {e}")
        st.error("Please ensure the 'inventory' table exists and matches the required schema.")


def load_data(conn):
    """Loads the inventory data from the database."""
    
    df_columns = [
            "id",
            "item_name",
            "price",
            "units_sold",
            "units_left",
            "cost_price",
            "reorder_point",
            "description",
        ]
    
    try:
        # st-supabase-connection の 'query' ではなく 'select' メソッドを使用
        # idでソートして一貫した順序を保証
        result = conn.select("*", table="inventory", order="id") # <-- 修正点
        data = result.data
    except Exception as e:
        # 潜在的なエラー（テーブルが見つからないなど）をキャッチ
        st.error(f"Error loading data: {e}")
        st.warning("Ensure the 'inventory' table exists in your Supabase project.")
        return None

    if not data:
        # データがないがテーブルは存在する場合、空のDataFrameを返す
        return pd.DataFrame(columns=df_columns)

    df = pd.DataFrame(
        data,
        columns=df_columns,
    )

    return df


def update_data(conn, df, changes):
    """Updates the inventory data in the database."""
    try:
        if changes["edited_rows"]:
            deltas = st.session_state.inventory_table["edited_rows"]
            
            for i, delta in deltas.items():
                row_dict = df.iloc[i].to_dict()
                row_dict.update(delta)
                
                # id をペイロードから削除
                row_id = row_dict.pop("id") 
                
                # st-supabase-connection の update は matching_columns を使用 (デフォルト 'id')
                conn.update(
                    table="inventory", 
                    data=row_dict, 
                    matching_columns={"id": row_id}
                )

        if changes["added_rows"]:
            # 挿入用の行を準備
            rows_to_insert = [
                defaultdict(lambda: None, row) for row in changes["added_rows"]
            ]
            
            # 'id' が存在する場合は削除 (Supabaseが生成するため)
            for row in rows_to_insert:
                row.pop("id", None) 

            conn.insert(table="inventory", data=rows_to_insert)

        if changes["deleted_rows"]:
            for i in changes["deleted_rows"]:
                # 削除する行の実際の 'id' を取得
                row_id = int(df.loc[i, "id"])
                
                conn.delete(
                    table="inventory",
                    matching_columns={"id": row_id}
                )
        
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

# Connect to database
# secrets.toml (connections.supabase) を自動的に使用
conn = st.connection("supabase", type=SupabaseConnection)

# Load data from database
df = load_data(conn)

# テーブルが空の場合にデータを初期化
data_loaded_successfully = df is not None
if data_loaded_successfully and df.empty:
    initialize_data(conn)
    st.toast("Database initialized with some sample data.")
    # 初期化後にデータを再読み込み
    df = load_data(conn)

# 読み込みに失敗した場合 (テーブルが存在しないなど), df は None になる
if df is None:
    st.error("Failed to load data. Please ensure the 'inventory' table exists in Supabase.")
    st.info("You might need to run the CREATE TABLE script in the Supabase SQL Editor (see code comments in initialize_data).")
    st.stop() # テーブルが存在しない場合は実行を停止

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    column_config={
        # Show dollar sign before price columns.
        "price": st.column_config.NumberColumn(format="$%.2f"),
        "cost_price": st.column_config.NumberColumn(format="$%.2f"),
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

""
""
""

# -----------------------------------------------------------------------------

st.subheader("Best sellers", divider="orange")

""
""

st.altair_chart(
    alt.Chart(df)
    .mark_bar(orient="horizontal")
    .encode(
        x="units_sold",
        y=alt.Y("item_name").sort("-x"),
    ),
    use_container_width=True,
)
