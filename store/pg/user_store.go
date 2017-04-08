package pg

import (
	"database/sql"

	"github.com/praelatus/praelatus/models"
)

// UserStore contains methods for storing and retrieving Users from a Postgres
// DB
type UserStore struct {
	db *sql.DB
}

func intoUser(row rowScanner, u *models.User) error {
	return row.Scan(&u.ID, &u.Username, &u.Password, &u.Email, &u.FullName,
		&u.ProfilePic, &u.IsAdmin)
}

// Get retrieves the user by row id
func (s *UserStore) Get(u *models.User) error {
	var row *sql.Row

	row = s.db.QueryRow(`
SELECT id, username, password, email, full_name, 
       profile_picture, is_admin 
FROM users
WHERE id = $1
OR username = $2
`,
		u.ID, u.Username)
	return handlePqErr(intoUser(row, u))
}

// GetAll retrieves all users from the database.
func (s *UserStore) GetAll() ([]models.User, error) {
	users := []models.User{}
	rows, err := s.db.Query(`
SELECT id, username, password, email, full_name, 
       profile_picture, is_admin 
FROM users`)
	if err != nil {
		return users, handlePqErr(err)
	}

	for rows.Next() {
		var u models.User

		err := intoUser(rows, &u)
		if err != nil {
			return users, handlePqErr(err)
		}

		users = append(users, u)
	}

	return users, nil
}

// Search retrieves a list of users whose name / username matches the given string
func (s *UserStore) Search(query string) ([]models.User, error) {
	users := []models.User{}
	rows, err := s.db.Query(`
SELECT id, username, password, email, full_name, 
       profile_picture, is_admin 
FROM users
WHERE full_name LIKE $1 OR username LIKE $2
`,
		"%"+query+"%", query+"%")
	if err != nil {
		return users, handlePqErr(err)
	}

	for rows.Next() {
		var u models.User

		err := intoUser(rows, &u)
		if err != nil {
			return users, handlePqErr(err)
		}

		users = append(users, u)
	}

	return users, nil
}

// Remove will update the given user into the database.
func (s *UserStore) Remove(u models.User) error {
	_, err := s.db.Exec(`
UPDATE users SET (is_active) = (false)
WHERE id = $1;
`,
		u.ID)
	return handlePqErr(err)
}

// Save will update the given user into the database.
func (s *UserStore) Save(u models.User) error {
	if u.Password == "" {
		_, err := s.db.Exec(`
UPDATE users 
SET (username, email, full_name, is_admin) = ($1, $2, $3, $4) 
WHERE id = $5;
`,
			u.Username, u.Email, u.FullName, u.IsAdmin, u.ID)

		return handlePqErr(err)
	}

	_, err := s.db.Exec(`
UPDATE users 
SET (username, password, email, full_name, is_admin) = ($1, $2, $3, $4, $5) 
WHERE id = $6;
`,
		u.Username, u.Password, u.Email, u.FullName, u.IsAdmin, u.ID)

	return handlePqErr(err)
}

// New will create the user in the database
func (s *UserStore) New(u *models.User) error {
	err := s.db.QueryRow(`
INSERT INTO users
(username, password, email, full_name, profile_picture, is_admin) 
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING id;
`,
		u.Username, u.Password, u.Email, u.FullName,
		u.ProfilePic, u.IsAdmin).
		Scan(&u.ID)

	return handlePqErr(err)
}
