rm -rf .devcontainer/ssl
mkdir .devcontainer/ssl
openssl req -out .devcontainer/ssl/cert.pem -subj /CN=localhost -new -keyout .devcontainer/ssl/key.pem -nodes -x509 -days 90