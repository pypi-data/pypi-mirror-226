# rspro82

Utility for programming channels into RadioShack PRO-branded scanners manufactured by GRE.

Several other radios use the same programming protocol. I have only tested it with the PRO-82,
but it may work with other radios including the PRO-64, PRO-76, PRO-79, PRO-89, PRO-2016, PRO-2017 and PRO-2041.

## Installation

`python3 -m pip install rspro82`

## Command-line interface

Prepare a CSV file that has at least these columns:

* _Channel_: The number of the channel you wish to program
* _Frequency_: Frequency in MHz, like `156.6`
* _Delay_: Boolean value for the channel delay flag (should the scanner pause on the channel for 2 seconds after a transmission ends?)
* _Priority_: Boolean value for the channel priority flag (should the scanner check this channel at least every 2 seconds?)

Additional columns are ignored.

Activate programming mode on the scanner by holding down the ENT and 9 keys on the scanner as you turn it on.

Run the CLI like:

`rspro82 <port path> <channel csv file path>`

On a Mac, the port argument will probably look like `/dev/cu.usbserial-<numbers>`.

On Windows, the port argument will look like `COM4`.

## Cable

The PRO-82 uses a very simple programming cable connecting a RS-232 serial port to the unit's TRS headphone jack.

The serial port's GND line (pin 5 on a DB-9 connector) is connected to the sheath.

The serial port's TXD line (pin 3 on a DB-9 connector) is connected to the ring.

These cables can be expensively purchased, or inexpensively made by sacrificing something with a 3.5mm jack,
like old headphones or a patch cable. [Solderless DB-9 connectors](https://www.amazon.ca/dp/B07DL13B32) are available and convenient.

Most Prolific-style USB/RS-232 adapters should work fine.
Devices targeting hobbyists that expose TTL-level outputs and skip the DB-9 interface may not work,
since TTL signal voltage levels are lower than the RS-232 spec requires.
If you try it, I'm curious how you make out!

## License

rspro82 is made available subject to the Apache License 2.0; see LICENSE for details.
