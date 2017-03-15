// Package utils contains utility functions used throughout the api
// package
package utils

// Message is a general purpose json struct used primarily for error responses.
import (
	"encoding/json"
	"log"
	"net/http"
	"strings"
)

// APIMessage is a general purpose struct for sending messages to the client,
// generally used for errors
type APIMessage struct {
	Field   string `json:"field,omitempty"`
	Message string `json:"message"`
}

// APIError is a convenience function for generating an API Message
func APIError(msg string, fields ...string) []byte {
	e := APIMessage{
		Message: msg,
	}

	if fields != nil {
		e.Field = strings.Join(fields, ",")
	}

	byt, _ := json.Marshal(e)
	return byt
}

// SendJSON is a convenience function for sending JSON to the given ResponseWriter
func SendJSON(w http.ResponseWriter, v interface{}) {
	resp, err := json.Marshal(v)
	if err != nil {
		w.WriteHeader(500)
		w.Write(APIError("Failed to marshal database response to JSON."))
		log.Println(err)
		return
	}

	w.Write(resp)
}
