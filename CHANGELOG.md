# Changelog

## [v1.1.0] - 2020-03-19

### Added

- The capability to add `timestamp` to each send message
- Support for image type messages.
- English documents
- SINETStream Server Plugin Developer Guide (Japanese only)

### Changed

- Message is encoded by Apache Avro.
- `value_type` can be handled as a plugin.

### Fixed

- Fixed exception handling in case of authentication / authorization error.

## [v1.0.0] - 2019-12-24

### Added

- Tutorial
- open/close method for MessageReader/MessageWriter (python)

### Changed

- {python,java}/sample/text/*.py: remove -t option to specify the topic.
- Documents rearranged.
- To display the cheat sheet, `python3 -m sinetstream`. (python)
- The topic= argument is now optional in MessageReader/MessageWriter constructor. (python)

### Fixed

- Fix documents
- Fix deadlock in MqttWriter.publish().
- Bugfixes.

## [v0.9.7] - 2019-10-11

### Added

- Data encryption:
    - Supported: CBC, OFB, CTR, EAX, GCM
    - Not supported: CFB, OPENPGP
- Authentication:
    - Kafka:
        - security_protocol: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
        - sasl_mechanism: PLAIN, SCRAM-SHA-256, SCRAM-SHA_512.
        - Note: GSSAPI and OAUTHBEARER are not supported.
    - MQTT:
        - password
    - Read docs/auth.md for details.
- Authorization(document only)
    - Read docs/auth.md for details.

## [v0.9.5] - 2019-08-26

### Added

- Java implementation.
- python/MQTT plugin.
- parameter value_type=.
- display default paraterers during installation.
- TLS support.

### Changed

- default consistency is AT_MOST_ONCE (was EXACTLY_ONCE).
- default client_id is generated by SINETStream library (not Kafka,MQTT).

### Fixed

- many bugfixes.

## [v0.9.1] - 2019-07-11

first alpha release.
