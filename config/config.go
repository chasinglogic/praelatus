// Package config defines the config struct and provides utility methods for
// querying it. Additionally it handles loading the config.json if present
package config

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"

	"github.com/praelatus/praelatus/store"
	"github.com/praelatus/praelatus/store/pg"
	"github.com/praelatus/praelatus/store/session/bolt"
)

// Config holds much of the configuration for praelatus, if reading from the
// configuration you should use the helper methods in this package as they do
// some prequisite processing and return appropriate types.
type Config struct {
	DBURL        string
	SessionURL   string
	Port         string
	ContextPath  string
	LogLocations []string
	SessionStore string
}

func (c Config) String() string {
	b, e := json.MarshalIndent(c, "", "\t")
	if e != nil {
		return ""
	}

	return string(b)
}

// Cfg is the global config variable used in the helper methods of this package
var Cfg Config

// TODO make this cross platform
func init() {
	Cfg.DBURL = os.Getenv("PRAELATUS_DB")
	if Cfg.DBURL == "" {
		Cfg.DBURL = "postgres://postgres:postgres@localhost:5432/prae_dev?sslmode=disable"
	}

	Cfg.SessionStore = os.Getenv("PRAELATUS_SESSION")
	if Cfg.SessionStore == "" {
		Cfg.SessionStore = "bolt"
	}

	Cfg.SessionURL = os.Getenv("PRAELATUS_SESSION_URL")
	if Cfg.SessionURL == "" {
		Cfg.SessionURL = "sessions.db"
	}

	Cfg.Port = os.Getenv("PRAELATUS_PORT")
	if Cfg.Port == "" {
		Cfg.Port = ":8080"
	}

	Cfg.ContextPath = os.Getenv("PRAELATUS_CONTEXT_PATH")

	Cfg.LogLocations = strings.Split(os.Getenv("PRAELATUS_LOGLOCATIONS"), ";")
	if os.Getenv("PRAELATUS_LOGLOCATIONS") == "" {
		Cfg.LogLocations = []string{"stdout"}
	}

	f, err := os.Open("config.json")
	if err != nil && !os.IsNotExist(err) {
		fmt.Println(err)
		os.Exit(1)
	}

	defer f.Close()

	if os.IsNotExist(err) {
		return
	}

	jsn, err := ioutil.ReadAll(f)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	var c Config

	err = json.Unmarshal(jsn, &c)
	if err != nil {
		fmt.Println("Error unmarshaling config file:", err)
		os.Exit(1)
	}

	Cfg = c
}

// DBURL will return the environment variable PRAELATUS_DB if set, otherwise
// return the default development database url.
func DBURL() string {
	return Cfg.DBURL
}

// Port will return the port / interfaces for the api to listen on based on the
// configuration
func Port() string {
	return Cfg.Port
}

// Store will return the correct data store based on the configuration of the
// instance
func Store() store.Store {
	return pg.New(DBURL())
}

// SessionStore will return a session store with a default location
// TODO support redis
func SessionStore() store.SessionStore {
	switch Cfg.SessionStore {
	case "bolt":
		return bolt.New(Cfg.SessionURL)
	default:
		return bolt.New(Cfg.SessionURL)
	}
}

// SessionURL will get the url to use for redis or file location for boltdb
func SessionURL() string {
	return Cfg.SessionURL
}

// ContextPath will return a context path if any is configured
func ContextPath() string {
	return Cfg.ContextPath
}
