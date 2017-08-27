# Udacity SQL Log Analysis Project

A simple and scalable python module that retrieves information from a bogus newspaper website. It uses PostgreSQL to create a report that answers the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of requests lead to errors?

It's designed to allow easy addition of new reports. Adding a new table to the report is as easy as storing a new SQL query in a variable and adding a new item to a list. The code will take care of the rest.

## Instructions
### Install:
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com)
- [Pretty Table](https://github.com/dprince/python-prettytable)

### Create the virtual machine:
1. Get the [virtual machine configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip) from Udacity.
2. Unzip the file in any location you choose
3. In a terminal window, go to the directory you chose and run `vagrant up`
4. When the installation is done (will take a while!), get into the virtual machine with `vagrant ssh`

### Create the database:
1. Download and unzip the [database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) from Udacity.
2. Move `newsdata.sql` to the vagrant folder.
3. In your virtual machine, run: `psql -d news -f newsdata.sql`

Here's what this command does:

`psql` the PostgreSQL command line program

`-d news` connect to the database named news which has been set up for you

`-f newsdata.sql` run the SQL statements in the file newsdata.sql

### Create views:
This tool won't work unless you create these two views in the database. To create the views, in your virtual machine run: `psql -d news -f create_views.sql`

The `create_views.sql` file contains the following:

```sql
CREATE VIEW daily_errors AS
		SELECT COUNT(*)::decimal AS errors, time::date AS day
		FROM log
		WHERE status not LIKE '%200%'
		GROUP BY day
		ORDER BY day ASC;
```
```sql
CREATE VIEW daily_hits AS
		SELECT COUNT(*)::decimal AS hits, time::date AS day
		FROM log
		GROUP BY day
		ORDER BY day ASC;
```

###  Ready to create the reports!
1. Move `create_reports.py` into the vagrant directory.
2. In your virtual machine, make sure you are in the vagrant directory `cd /vagrant`
2. Run the following `python create_reports.py`