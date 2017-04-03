package pg_test

import (
	"fmt"
	"testing"

	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"
	"github.com/praelatus/praelatus/store/pg"
)

var s store.Store
var seeded = true

func init() {
	if s == nil {
		fmt.Println("Prepping tests")
		p := pg.New(config.DBURL())

		e := p.Migrate()
		if e != nil {
			panic(e)
		}

		s = p
	}

	if !seeded {
		e := store.SeedAll(s)
		if e != nil {
			panic(e)
		}

		seeded = true
	}
}

func failIfErr(testName string, t *testing.T, e error) {
	if e != nil {
		t.Error(testName, " failed with error: ", e)
	}
}
