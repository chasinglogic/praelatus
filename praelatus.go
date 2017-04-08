// Praelatus is an Open Source bug tracking and ticketing system. The
// backend API is written in Go and the frontend is a React.js
// app. You are viewing the Godoc for the API if you would like
// information about how to use the API as a client or how to start
// working on the backend visit https://docs.praelatus.io
package main

import (
	"os"

	"github.com/praelatus/praelatus/cli"
)

func main() {
	cli.Run(os.Args)
}
