# USUMBUFU

Multi-authentication pipelines for HTTP with challenge-response


## OVERVIEW

The aim of this module is the let the client easily build authentication pipelines for HTTP.

For every authentication scheme, a pipeline can be built from any number of functions. If successfully executed, the output of the pipeline is:

- a resolved identity for the authorization.
- an authorization resource (ACL), or a locator to one. 

For every HTTP request, any number of such authentication schemes can be connected. These are executed in sequence, and the first successful schem provides the authentication will be used for the request.


### Schemes

- HTTP Basic, Bearer and HOBA
- SSL client certificates
- Query string (as in `username=&password=`)

### Features

- Fully detached file retrieval layer (anything that implements `get(key)`)
- Challenge/response handling (HOBA)
- Two-tierd session token handling
- Identity resolution and data validation from PGP signatures
- Identity resolution from Ethereum signatures (temporarily broken)
- UWSGI application bindings


## CODE LAYOUT

### Modules

- `retrieve` - session-scoped file retrieval and processing
- `ext` - request-scoped authentication execution
- `filter` - building blocks for creating authentication methods
- `client` - helper code for building python HTTP clients

### Session scope

Every authentication method should implement the `retrieve.Retriever` prototype. 

The decoder pipeline is built sequentially by using `add_decoder(...)`. 

During a HTTP request, an authentication scheme will call `load(...)` on the `Retriever`, and all decoders will be run in sequence, processing input from their predecessor.

Decoders pass four arguments between each other:

- The ip address of the client performing the HTTP request **(required)**
- The current transformation state of the original authentication input **(required)**
- The current state of the derived _signature_, if relevant
- The current state of the derived _identity_ of the authenticating party

Except for the `ip` argument, is fully up to the implementer to decide what type or format of data is used for the different arguments, as well as the expected state of the final output.

However, if any decoder step should fail, it **MUST** return `None` or raise an `AuthenticationError` exception. This will signal the `Retriever` to abort the authentication attempt for the current scheme.


### Request scope

Authentication schemes to be used for a single request are built using the `AuthVector` class. It executes a collection of objects implementing the `Auth` prototype in sequence. 

The responsibility of the `Auth` object is to parse raw authentication input into a format that the scheme decoder pipeline expects.

To add `Auth` objects to `AuthVector` the `register` then `activate` methods are used.

When `check()` is called on `AuthVector`, all schemes will be processed.

The builtin `Auth` implementations all take `Retriever` objects as a constructor argument. Calling `check()` will result in `Retriever.load()` being subsequently called.

Builtin `Auth` implemnetations also have `UWSGI` adapters, that format the authentication data directly from the UWSGI environment.


## EXAMPLES


Self-explanatory examples can be found in `examples/server*.py` and `example/client*.py`

And example client SSL certificate is also provided (the key has password `test`).

To run the example `server.py`, make sure the uwsgi python plugin is installed. Change directory to `/example`, then execute:

`PYTHONPATH=.. uwsgi --plugin python --wsgi-file server.py --ini uwsgi.ini`

The `server_hoba.py` should not be run with SSL. Instead run:

`PYTHONPATH=.. uwsgi --plugin python --wsgi-file server_hoba.py --http :5555`

### KNOWN ISSUES

the client cert provided in examples for ssl is expired. sorry.
