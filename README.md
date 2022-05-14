# Default Users
All users have default password `123456`.

* User ID 1 is the Owner.
* User ID 2-5 are the Managers.
* Other users are ordinary employees.

You can login as the Owner and choose `1` `1` for more details about default users.

There are also default products and sales. You can use the menu to see detailed information about them.

# Usage
Please follow the menu. The menu is coloured to enhance readability. Enter the numerical option of your choice as the input.

When inputing passwords, your input will not be shown. This is to prevent somebody looking over your shoulder.

# Access Levels
0 is the lowest, 2 is the highest

Main Menu

  1. Employees Information (Access level 1 and above)
  
  2. Products Information (Access level 0 and above)

  3. Sales Information (Access level 0 and above)

Employee table:

  1. Display (access level 1 and above)

  2. Individual Employee Actions (access level 2) / Additional Employee Info (Access Level 1) - same as Individual Employee Actions - but with less options

  3. Search (access level 1 and above)

  4. New (access level 2)

Inventory table:

  1. Display (Access level 0 and above)

  2. Individual Product Actions (Access Level 1 and above) / Additional Product Info (Access Level 0) - same as Individual Product Actions - but with less options

  3. Search (Access level 0 and above)

  4. New (access level 1 and above)

Sales table:

  1. Display (Access level 0 and above) 

  2. Individual Sale Actions (Access level 1 and above) / Additional Sale Info (Access Level 0) - same as Individual Sale Actions - but with less options

  3. Search (access level 0 and above)

  4. New (Access level 0 and above)

# Reset to Default
Go to "Shell" and run:
```sh
/bin/sh reset_db.sh
```

This will delete the current database and create a new one based on default data.

# Security
## Password Storage
Passwords are securely stored using a one-way hash function. Consequently, no one, including the server operator, can ever know the plain text password of any employee. This is a cryptographically strong "no one"; so in case the password is lost, it is only possible to *reset* the password, but not *recover* them.

Password hashes are properly salted and thus are resilient against rainbow tables or duplicate passwords. Thus, the plain text passwords will remain secret in event of a complete database breach.

## The Journal
For server operators, a file named `journal.log` contains the security log. Every time a login or a permission check failed, a new entry will be added to the security journal. You can then take appropriate actions to secure the system.

An event is firstly appended to the journal, before it is reported to the user, to ensure that user cannot `Ctrl-C` to prevent being logged; when they know their attempted access failed, it is already logged, so too late to `Ctrl-C`.

# Database
## Requirements
This system requires proper foreign key support to work. However, SQLite3 may not have such support depending on compile-time options given to `libsqlite3`. This system will refuse to operate and print the following error message if this is the case.

```
This version of SQLite3 is NOT compiled with foreign key support.
```

## Corruption & Backup
Because replit.com sucks, it cannot properly handle binary files. Obviously, binary files include database images, particularly `data.db`. This means that replit.com may decide to corrupt (!!) our database for fun and profit, which happens pretty often.

Thus, it is *imperative* to keep backups of the database. Go to "Shell", and run

```sh
sqlite3 data.db '.dump' > "dump-$(date +%s).sql"
```

To backup the current database content into `dump-XXX.sql` where `XXX` is the current Unix timestamp.

**Future projects should avoid replit.com at all costs.** replit.com is not in any way a replacement for proper version control & proper code editors. Nor is the "discussion threads" an adequate issue tracking mechanism.

## Maintenance
Over time, you need to vacuum the database for optimal performance. Use sqlite3 to open the database, then run `VACUUM;` to vacuum the database. It is recommended to vacuum weekly.

## A Warning to Server Operators
Sometimes, you may want to edit `data.db` directly using sqlite3 or some other programs, such as another python script. This is fine, but by default, sqlite3's foreign key enforcement is *off* (!!) and you must run (every time you connect, it is not persistent)

```sql
PRAGMA foreign_keys = ON;
```

to turn it on. *Also*, sqlite3 may not have foreign key support *at all* (!!) depending on a compile-time option to `libsqlite3`. In that case, the above command will *not* error out, but instead becomes a no-op (!!) and silently does nothing. So you *must* run the following command to verify:

```sql
PRAGMA foreign_keys;
```

If it returns `1`, you are good to go. Otherwise, foreign key enforcement is not available, so you need to be *extremely cautious* not to create invalid foreign references.

*Also*, sqlite3 does not have any kind of data-type enforcement (!!), so be careful not to insert a string into an integer column.

SQLite3 sucks.