<!--
Copyright (C) 2020 National Institute of Informatics

Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

[日本語](mqtt-authentication-password.md)

# How to use an MQTT broker with password authentication

## Overview

This page describes how to connect from SINETStream to an MQTT broker that requires password authentication.

The description will be made in the following order.

1. Prerequisites
1. Configurations on the Mosquitto MQTT broker (server side)
1. Configurations on SINETStream (client side)
1. Behavior on authentication errors

## Prerequisites

Though the configuration and setting of an MQTT broker may vary, the following conditions are assumed for simplicity in this document.

* [Mosquitto](https://mosquitto.org/) is used as the MQTT broker
* SSL/TLS is used to connect to the MQTT broker
* A CA certificate has been created in PEM format in advance by a private certificate authority (*1)
* A server certificate and a client certificate have also been created in PEM format in advance (*1)

(*1) Refer to [How to create a certificate with a private certificate authority](certificate.en.md) for details.

The following values are used in the examples.
> In practice, use appropriate values for your environment.

* MQTT broker
    * Hostname
        * broker.example.org
    * Port
        * 8884
    * Username/password
        * `user01`/`user01-pass`
        * `user02`/`user02-pass`
        * `user03`/`user03-pass`
    * Configuration file path
        * /etc/mosquitto/mosquitto.conf
    * Password file path
        * /etc/mosquitto/pwfile
* Certificate (server side)
    * CA certificate
        * Certificate file path
            * /etc/pki/CA/cacert.pem
    * Server certificate of the MQTT broker
        * Certificate file path
            * /etc/pki/CA/certs/broker.crt
        * Private key file path
            * /etc/pki/CA/private/broker.key
* Certificate (client side)
    * CA certificate
        * /opt/certs/cacert.pem

## Configurations on the MQTT broker (server side)

The following procedure is needed for the MQTT broker to perform password authentication with SSL/TLS connection.

1. Edit the MQTT broker's configuration file
1. Set username and password in a password file
1. Reload the configuration file

### Edit the MQTT broker's configuration file

Add the following lines to the MQTT broker's configuration file `/etc/mosquitto/mosquitto.conf`.

```properties
per_listener_settings true
listener 8884
password_file /etc/mosquitto/pwfile
cafile /etc/pki/CA/cacert.pem
certfile /etc/pki/CA/certs/broker.crt
keyfile /etc/pki/CA/private/broker.key
require_certificate false
```

The meanings of the above settings are:

* `per_listener_settings`
    * Whether to configure authentication and access control on a per-lister basis or globally.
* `listener`
    * Specify the port number to listen on.
* `password_file`
    * Specify the password file path.
* `cafile`
    * Specify the CA certificate (PEM) file path.
* `certfile`
    * Specify the server certificate (PEM) file path.
* `keyfile`
    * Specify the private key file path for the server certificate.
* `require_certificate`
    * Whether to require client certificate for incoming connections.

### Set username and password in a password file

Use the `mosquitto_passwd` command to register username and password.

```bash
$ sudo touch /etc/mosquitto/pwfile
$ sudo mosquitto_passwd -b /etc/mosquitto/pwfile user01 user01-pass
$ sudo mosquitto_passwd -b /etc/mosquitto/pwfile user02 user02-pass
$ sudo mosquitto_passwd -b /etc/mosquitto/pwfile user03 user03-pass
```

### Reload the configuration file

Send a SIGHUP signal to reload the configuration file.

```bash
$ sudo killall -HUP mosquitto
```

## Configurations on SINETStream (client side)

The following procedure is needed for SINETStream to connect to the MQTT broker with authentication.

1. Prepare certificate
1. Edit the SINETStream's configuration file
1. Create a program that uses SINETStream

### Prepare certificate

The following certificate is required on the client side to use SSL/TLS connection.

* A CA certificate

Deploy the certificate created by a private CA etc. to your convenient location.
SINETStream reads the certificate from the path specified in the configuration file.

### Edit the SINETStream's configuration file

An example of SINETStream's configuration file is shown below.

```yaml
service-mqtt-password:
  brokers: broker.example.org:9093
  type: mqtt
  topic: topic-001
  tls:
    ca_certs: /opt/certs/cacert.pem
  username_pw_set:
    username: user01
    password: user01-pass
```

The settings for `brokers`, `type`, `topic`, `consistency`, `tls` are identical to those without authentication.
Settings related to password authentication are under `username_pw_set:`.

* `username`
    * User name
* `password`
    * Password

### Create a program that uses SINETStream

Your program will be identical with or without password authentication.
For example, a program that uses `MessageWriter` of the SINETStream's Python API is shown below.

```python
with sinetstream.MessageWriter(service='service-mqtt-password') as writer:
    writer.publish(b'message 001')
```

As you see, no code is written for authentication.

If you want to configure the authentication within your program, add parameters to the constructor arguments.

```python
user_password = {
    'username': 'user01',
    'password': 'user01-pass',
}
with sinetstream.MessageWriter(service='service-mqtt', username_pw_set=user_password) as writer:
    writer.publish(b'message 001')
```

## Behavior on authentication errors

### Python API

The methods listed below raises the `sinetstream.error.ConnectionError` exception when an authentication error occurs.

* `sinetstream.MessageWriter.__enter__()`
* `sinetstream.MessageWriter.open()`
* `sinetstream.MessageReader.__enter__()`
* `sinetstream.MessageReader.open()`

### Java API

The methods listed below throws the `jp.ad.sinet.stream.api.AuthenticationException` exception when an authentication error occurs.

* `jp.ad.sinet.stream.utils.MessageWriterFactory#getWriter()`
* `jp.ad.sinet.stream.utils.MessageReaderFactory#getReader()`
