package cli

import (
	"fmt"

	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/store"
	"github.com/urfave/cli"
)

func seedDB(c *cli.Context) error {
	s := config.Store()

	if sql, ok := s.(store.Migrater); ok {
		err := sql.Migrate()
		if err != nil {
			return err
		}
	}

	return store.SeedAll(s)
}

func migrateDB(c *cli.Context) error {
	s := config.Store()

	if sql, ok := s.(store.Migrater); ok {
		sql.Migrate()
		return nil
	}

	fmt.Println("not a migrateable database ")
	return nil
}

func testDB(c *cli.Context) error {
	// these methods panic if connection fails
	config.Store()
	config.SessionStore()
	fmt.Println("connection successful!")
	return nil
}

func cleanDB(c *cli.Context) error {
	s := config.Store()
	sql, ok := s.(store.Droppable)
	if !ok {
		fmt.Println("Configured database is not droppable nothing to do.")
		return nil
	}

	err := sql.Drop()
	if err != nil {
		return err
	}

	fmt.Println("Database cleaned.")
	return nil
}
