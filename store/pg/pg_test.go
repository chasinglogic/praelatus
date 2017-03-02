package pg_test

import (
	"fmt"
	"testing"

	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"
	"github.com/praelatus/praelatus/store/pg"
)

var s store.Store
var seeded bool

func init() {
	if !seeded {
		fmt.Println("Prepping tests")
		p := pg.New(config.DBURL())

		e := p.Migrate()
		if e != nil {
			panic(e)
		}

		s = p
		e = store.SeedAll(s)
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
