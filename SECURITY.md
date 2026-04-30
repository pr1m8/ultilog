# Security

Logging can accidentally expose sensitive data. `ultilog` therefore defaults to:

- Rich markup disabled for log messages
- traceback locals disabled
- explicit context binding rather than automatic request-body capture
- optional integrations disabled unless configured

When enabling traceback locals, JSON output, or external exporters, review the
fields your application logs.
