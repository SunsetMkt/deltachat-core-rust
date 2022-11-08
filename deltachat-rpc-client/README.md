# Delta Chat RPC python client

RPC client connects to standalone Delta Chat RPC server `deltachat-rpc-server`
and provides asynchronous interface to it.

## Getting started

To use Delta Chat RPC client, first build a `deltachat-rpc-server` with `cargo build -p deltachat-rpc-server`.
Install it anywhere in your `PATH`.

## Testing

1. Build `deltachat-rpc-server` with `cargo build -p deltachat-rpc-server`.
2. Run `tox`.

Additional arguments to `tox` are passed to pytest, e.g. `tox -- -s` does not capture test output.
