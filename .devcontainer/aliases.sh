alias test-build="docker build -t ticketing-hsg /workspaces/ticketing-hsg"
alias test-run="docker run -d -p 80:80 --name ticketing-hsg ticketing-hsg"
alias test-run-stop="docker stop ticketing-hsg"