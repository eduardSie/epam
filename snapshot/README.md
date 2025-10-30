# Snapshot System Monitor

A simple command-line tool to monitor system resources (CPU, Memory, Tasks) and save snapshots to a JSON file.

Installation

## Usage

The installation provides the snapshot command.

### Arguments

-i (Interval): Seconds between snapshots. (Default: 30)

-f (File): Output file name. (Default: "snapshot.json")

-n (Number): Total number of snapshots. (Default: 20)

### Examples

Run with defaults:

snapshot


Run 5 times, every 1 second:

snapshot -n 5 -i 1


Log to a different file:

snapshot -f "log.json"
