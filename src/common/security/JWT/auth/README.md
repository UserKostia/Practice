
```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -pubout -out jwt-public.pem
```