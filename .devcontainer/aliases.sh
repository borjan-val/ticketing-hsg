alias test-build="docker build -t ticketing-hsg /workspaces/ticketing-hsg"
alias test-run="docker run -d --rm -p 80:80 --add-host host.docker.internal=host-gateway --env-file /workspaces/ticketing-hsg/.devcontainer/dev.env --name ticketing-hsg ticketing-hsg"
alias test-run-attached="docker run --rm -p 80:80 --add-host host.docker.internal=host-gateway --env-file /workspaces/ticketing-hsg/.devcontainer/dev.env --name ticketing-hsg ticketing-hsg"
alias test-run-stop="docker stop ticketing-hsg"