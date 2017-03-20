// Package models contains all of our models and utility functions for
// interacting with them
package models

import (
	"encoding/json"
	"fmt"
)

func jsonString(i interface{}) string {
	b, e := json.MarshalIndent(i, "", "\t")
	if e != nil {
		fmt.Println(e)
		return ""
	}

	return string(b)
}
