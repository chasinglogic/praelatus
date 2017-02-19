package cli

import "github.com/urfave/cli"

// Run runs the cli of Praelatus with the given argv
func Run(args []string) {
	app := cli.NewApp()
	app.Name = "praelatus"
	app.Usage = "Praelatus, an Open Source bug tracker / ticketing system"
	app.Version = "0.0.1"
	app.Action = runServer
	app.Authors = []cli.Author{
		{
			Name:  "Mathew Robinson",
			Email: "chasinglogic@gmail.com",
		},
		{
			Name:  "Mark Chandler",
			Email: "mark.allen.chandler@gmail.com",
		},
	}

	app.Commands = []cli.Command{
		{
			Name:   "seeddb",
			Usage:  "seed the database with test data",
			Action: seedDB,
		},
		{
			Name:   "serve",
			Usage:  "start running the REST api",
			Action: runServer,
			Flags: []cli.Flag{
				cli.BoolFlag{
					Name:  "devmode",
					Usage: "runs server in devmode which changes some security behavior to ease development",
				},
			},
		},
		{
			Name:   "config",
			Action: showConfig,
			Usage:  "view the configuration for this instance, useful for debugging",
		},
		{
			Name:   "testdb",
			Usage:  "will test the connections to the databases",
			Action: testDB,
		},
		{
			Name:   "cleandb",
			Usage:  "will clean the database (remove all tables), useful for testing",
			Action: cleanDB,
		},
		{
			Name:   "migratedb",
			Usage:  "will migrate the database if it is migrateable",
			Action: migrateDB,
		},
		{
			// TODO expand upon this as necessary
			Name:  "admin",
			Usage: "various admin functions for the instance",
			Subcommands: []cli.Command{
				{
					Name:   "createUser",
					Usage:  "create a user, useful for creating admin accounts",
					Action: adminCreateUser,
					Flags: []cli.Flag{
						cli.StringFlag{
							Name: "username",
						},
						cli.StringFlag{
							Name: "password",
						},
						cli.StringFlag{
							Name: "fullName",
						},
						cli.StringFlag{
							Name: "email",
						},
						cli.BoolFlag{
							Name:  "admin",
							Usage: "when this flag is given user will be created as an system admin",
						},
					},
				},
			},
		},
	}

	app.Run(args)
}
