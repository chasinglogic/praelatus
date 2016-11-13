package models

import "errors"

var ErrInvalidDataType = errors.New("Invalid data type for field")

var DataTypes = []string{
	"FLOAT",
	"STRING",
	"INT",
	"DATE",
}

// Field is a ticket field
type Field struct {
	ID       int64  `json:"id"`
	Name     string `json:"name"`
	DataType string `json:"data_type"`
}

// FieldValue holds the value for a field on a given ticket.
type FieldValue struct {
	ID       int64       `json:"id"`
	Name     string      `json:"name"`
	DataType string      `json:"data_type"`
	Value    interface{} `json:"value"`
}

func isValidDataType(dt string) bool {
	for _, t := range DataTypes {
		if t == dt {
			return true
		}
	}

	return false
}

// NewField will verify a valid data type is given and return a field with that
// data type or an error if an invalid data type was supplied.
func NewField(name, dt string) (Field, error) {
	if !isValidDataType(dt) {
		return Field{}, ErrInvalidDataType
	}

	return Field{Name: name, DataType: dt}, nil
}
