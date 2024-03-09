JWTJuggler
--
JWTJuggler (JOT JUGGLER): JWT &amp; Authentication Testing Harness

Python-based testing harness designed for JWT authentication and authorization testing. Quick way to test and validate JWT implementations across various API endpoints.

Features
---

- **Dynamic User Authentication**: Automates the process of obtaining JWTs for user credentials provided in a configuration file.
- **Flexible Endpoint Testing**: Supports testing with both absolute URLs and relative paths, configurable via a simple JSON file.
- **Rich Output Formatting**: Utilizes the Rich library to display detailed test results in a visually appealing table format, complete with color-coded user types.
- **Output Options**: Offers the ability to output test results in JSON or CSV format for further analysis or reporting.
- **Proxy Support**: Includes functionality for routing all requests through a specified proxy server.


Configuration
---

Before using jwtjuggler, you need to configure it by specifying your test environment and credentials in a `config.json` file. Here's an example of the configuration structure:

```json
{
  "user1": {
    "username": "user1@example.com",
    "password": "password123"
  },
  "user2": {
    "username": "user2@example.com",
    "password": "password456"
  },
  "login_endpoint": "http://localhost:8080/login",
  "base_url": "http://localhost:8080",
  "proxy": "http://your-proxy-server:port",
  "endpoints_file": "endpoints.txt"
}
```
By default, the local `config.json`will be read, so in many cases you won't need to specify the location (if you're running this from the cloned repo).

-   `user1` and `user2` represent the credentials for the users you want to test.
-   `login_endpoint` specifies where the tool should send login requests to obtain JWTs.
-   `base_url` is used as the prefix for relative endpoint paths.
-   `proxy` (optional) allows specifying a proxy server for all requests.
-   `endpoints_file` is a text file listing all API endpoints to test, one per line. Endpoints can be specified as absolute URLs or relative paths.

Usage
-----

To use jwtjuggler, run the script from the command line, optionally specifying the output format:

```bash
python3 jwtjuggler.py
```
For JSON or CSV output formats:

```bash
python3 jwtjuggler.py --output json
python3 jwtjuggler.py --output csv
```

Example
-------

Given the configuration above, jwtjuggler will attempt to login using the provided credentials, obtain JWTs, and then test each API endpoint specified in `endpoints.txt` with and without authentication.

Assuming `endpoints.txt` contains:

```
/workshop/api/mechanic/mechanic_report
/identity/api/v2/vehicle/{vehicleId}/location
```

The tool will test these endpoints and display results in the terminal. Here's how to interpret the output:

-   Each row represents a request made to an endpoint.
-   Columns show the endpoint, the user (User 1, User 2, or Unauthenticated), status code, content length, and content type.
-   Color-coding: Authenticated user requests are displayed in their respective colors, and unauthenticated requests are red.

Output
---

The default output is color-coded table displayed in the terminal. Here's an example of what you might see:

![image](https://github.com/queencitycyber/jwtjuggler/assets/13237617/ad51d671-f35c-4630-b98e-b828728c7e6a)



For JSON or CSV outputs, files will be generated in the current directory with the results of the test in the specified format.

Acknowledgements & Shoutouts 
---
* [Autorize Project](https://github.com/PortSwigger/autorize) - Layout and original inspiration
* [crAPI](https://github.com/OWASP/crAPI) - Testing playground
* AI lol


Contributing
---

Contributions to JWTJuggler are welcome! Please submit pull requests or open issues to suggest improvements or report bugs.
