# Notes

## Functionality

* Users have to be able to log in/log out
* Every user is identified by a unique number
* A password is required for authentication

### Allocator

* ?

### Seller Functionality

* Add items
  * Specify description
  * Specify category (must be picked from list, cannot define their own)
  * Specify set
  * Specify price
  * Specify charity (= if item is unsold, it goes to charity)
  * Specify donation (= if item is sold, all proceeds go to the BCT)
  * Register date/time when added
* Edit items (within limits)
* Generate labels
  * Pick which labels to generate
  * Define sheets specs in detail
* Maximum items per seller?
* Fluent user interface

### Cashier Functionality

* Take into account barcode scanner details
  * Does it send an enter or not?
* Allow same item to be sold multiple times (we don't want earlier mistakes preventing a sale)

### Admin Functionality

* View items/item counts by category
* View items/item counts by seller

## Command Line Interface

All functionality should be available through the command line interface.
The CLI should be usable while the server is running.

```bash
# Adding a user
$ bct add-user --role [admin|seller|cashier|...] --id ID --password PASSWORD

# Listing users
$ bct list-users

# Search for item
$ bct find-item [--id ID] [--description DESCRIPTION] [--price PRICE] [--category CATEGORY]

$ bct count-items --by-owner

$ bct count-items --by-category

$ bct list-sold-items
```
