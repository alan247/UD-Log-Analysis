#!/usr/bin/env python

import datetime

import os

import prettytable

import psycopg2

DB_NAME = "news"

TOP_ARTICLES_QUERY = """
select articles.title, count(log.path)
from articles, log
where log.path like '%'|| articles.slug ||'%'
and log.status like '%200%'
group by articles.title
order by count(log.path) desc limit 3;
"""

TOP_AUTHORS_QUERY = """
select authors.name, count(*) as hits
from authors, articles, log
where log.path like '%'|| articles.slug ||'%'
and articles.author = authors.id
and log.status = '200 OK'
group by authors.name, authors.id
order by hits desc
"""

HIGH_ERRORS_QUERY = """
select a.day, to_char(b.errors/a.hits*100, '99.99')
from daily_hits as a
join daily_errors as b on a.day=b.day
where b.errors/a.hits > 0.01;
"""

reports_list = [
    ["TOP ARTICLES BY VIEWS", TOP_ARTICLES_QUERY, "Articles", "Views", False],
    ["TOP AUTHORS BY VIEWS", TOP_AUTHORS_QUERY, "Authors", "Views", False],
    ["HIGH ERROR DAYS (+1%)", HIGH_ERRORS_QUERY, "Date", "Percentage", True]
]


def db_query(query):
    """ Creates a connection to the database, executes the query supplied,
    closes the connection and returns the results

    Args:
        query       (str):  The SQL query to be executed

    Returns:
        Array with rows resulting from the query
    """
    conn = psycopg2.connect(database=DB_NAME)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows


def create_table(query, column1, column2, percentage):
    """ Creates a plain text table populated with the rows resulting from
    the SQL query

    Args:
        query       (str):  The SQL query to be executed
        column1     (str):  First column's header
        column2     (str):  Second column's header
        percentage (bool):  True displays second column's values as a
                            percentage (23.34%). False formats second column's
                            value with commas for thousands separator

    Returns:
        A plain text table with headers and the rows resulting from the SQL
        query
    """
    result = db_query(query)
    table = prettytable.PrettyTable(
        [column1, column2],
        hrules=prettytable.ALL,
        padding_width=3
    )
    table.align[column1] = "l"

    for row in result:
        first_column = row[0]

        if percentage:
            second_column = row[1] + "%"
        else:
            second_column = str("{:,}".format(row[1]))

        table.add_row([first_column, second_column])

    return table


def create_reports():
    """ Clears the screen, prints the title and creates as many tables as
    items are in the reports_list.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    # Create title with border
    title = "NEWS WEBSITE REPORT TOOL"
    title_len = len(title) + 8  # 4 spaces on each side of the title
    title_border = "#" * title_len + "#\n"
    title_spacer = "#" + " " * (title_len - 1) + "#\n"
    title_text = "#    " + title + "   #\n"

    print title_border, title_spacer, title_text, title_spacer, title_border
    print "\n"

    # Create tables
    for item in reports_list:
        print item[0] + "\n"
        print create_table(item[1], item[2], item[3], item[4])
        print "\n\n"

    # Print creation date and time
    print "Report created on: " + datetime.datetime.now().strftime(
        '%d %b %Y, %H:%M') + "\n\n"


create_reports()
