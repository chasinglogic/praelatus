package pg_test

import (
	"testing"

	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"
	"github.com/praelatus/praelatus/store/pg"
)

var s *pg.Store
var seeded = false

func init() {
	if s == nil {
		p := pg.New(config.DBURL())

		e := p.Drop()
		if e != nil {
			panic(e)
		}

		e = p.Migrate()
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
