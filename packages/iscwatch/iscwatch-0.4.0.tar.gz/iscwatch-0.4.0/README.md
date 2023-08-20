# iscwatch - A Command Line Application For Monitoring Intel Security Center Product Advisories

![Version](https://img.shields.io/badge/version-0.3.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Description

`iscwatch` is a command line application that searches for summaries of [Intel's Security Center Product Advisories](https://www.intel.com/content/www/us/en/security-center/default.html) and outputs those summaries to stdout in CSV format. Included in the output per advisory summary is its title, full text url, advisory ID, updated date, and released date.  The actual advisories referenced by the summaries can be found by following the full text url provided by `iscwatch`.

## Features

- Fetches some or all summaries of Intel's Security Center Product advisories.
- Outputs advisory summary data in CSV format with our without headers.
- Date filtering enables iscwatch to be used to only output latest advisory summaries.

## Installation

You can install `iscwatch` using pip:

```
pip install iscwatch
```

## Usage

```
Usage: iscwatch
[OPTIONS]

Output security advisory summaries from the Intel Security Center website.

With no options, iscwatch outputs all Intel security advisory summaries in CSV format with column headers.  Typically, a starting date is specified using the --since option to  constrain the output to a manageable subset.

Options
--since         -s      [%Y-%m-%d]  Only output those advisories updated or
                                    released since specified date.
                                    [default: 0001-01-01 00:00:00]
--version       -v                  Show iscwatch application version and exit.
--no-header    -n                   Omit column header from CSV advisory summary
                                    output.
--last-updated  -l                  Show date when Intel last updated its security
                                    advisories and exit.
--help                              Show this message and exit.
```


## CSV Format

The CSV output includes the following columns:

- Advisories
- Advisory Number
- Updated
- Release Date
- Link

```bash
> iscwatch --since 2023-08-01 --no-headers
Intel® RealSenseTM SDK Advisory,INTEL-SA-00946,2023-08-08,2023-08-08,https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00946.html
Intel® ITS Software Advisory,INTEL-SA-00938,2023-08-08,2023-08-08,https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00938.html
MAVinci Desktop Software for Intel® Falcon 8+ Advisory,INTEL-SA-00934,2023-08-08,2023-08-08,https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00934.html
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request.

## Acknowledgments

- This application relies on Intel's Security Center for fetching advisories data.
