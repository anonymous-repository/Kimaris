# Python Standard Libraries
import sqlite3
# External Libraries
import pandas as pd


def get_table_data():
    conn = sqlite3.connect("./db/results.db")

    #df = pd.read_sql_query("SELECT * from nodes", conn)
    df = pd.read_sql_query("SELECT * from articles", conn)
    # Changing order of columns for layout
    #df = df[["id", "name", "info", "cited_by", "depth", "link"]]
    df = df[["article_id", "article_title", "article_abstract", "article_publish_year", "article_cites", "article_depth", "article_link"]]
    df.columns = ["ID", "Title", "Abstract", "Year", "Cites", "Depth", "Link"]
    return df

