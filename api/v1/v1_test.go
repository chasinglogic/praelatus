package v1

import "github.com/praelatus/praelatus/store"

func init() {
	Store, Cache = store.Mock()
}
