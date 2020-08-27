# Python Standard Libraries
import sqlite3
# External Libraries
import pandas as pd



def get_article(name):
    conn = sqlite3.connect("./db/results.db")
    df = pd.read_sql_query(f"""
    SELECT * FROM articles
    WHERE article_title = "{name}";
    """, conn)
    
    # Changing order of columns for layout
    df = df[["article_id", "article_title", "article_abstract", "article_cites", "article_depth", "article_link"]]
    return df