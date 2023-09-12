## Getting Started


### request key from apple wit unix tools

```shell
    $ openssl genrsa -out key.pem 2048
    # $ openssl req -new -key key.pem -out request.pem
    $ openssl req -new -key key.pem -out request.csr -subj="/emailAddress=phil@bluedynamics.com,CN=Philipp Auersperg,C=AT"
```

if you self-sign the certificate, you can use the same key.pem for the certificate.pem

```shell
    $ openssl x509 -req -days 365 -in request.csr -signkey key.pem -out certificate.pem
```

if you need a real cert from apple you have to send the request.pem to apple and get the certificate.cer back and convert it to a certificate.pem file by calling

```shell
    $ openssl x509 -inform der -in pass.cer -out certificate.pem
```



### blabla
1) Get a Pass Type Id

* Visit the iOS Provisioning Portal -> Pass Type IDs -> New Pass Type ID
* Select pass type id -> Configure (Follow steps and download generated pass.cer file)
* Use Keychain tool to export a Certificates.p12 file (need Apple Root Certificate installed)

2) Generate the necessary certificate

```shell
    # $ openssl pkcs12 -in "Certificates.cer" -clcerts -nokeys -out certificate.pem   
    $ openssl x509 -inform der -in Certificate.cer -out certificate.pem
```
3) Generate the key.pem

```shell
    # $ openssl pkcs12 -in "Certificates.p12" -nocerts -out private.key

    openssl x509 -in "Certificate.cer" -nocerts -out Certificate-private.key
```

