// package permission is used to store the various permission in
// praelatus, it acts as a pseudo-enumberation
package permission

// Permission is a string used for determining whether a user has
// access or not
type Permission string

// These are the permissions available in Praelatus
const (
	VIEWPROJECT      Permission = "VIEW_PROJECT"
	ADMINPROJECT                = "ADMIN_PROJECT"
	CREATETICKET                = "CREATE_TICKET"
	COMMENTTICKET               = "COMMENT_TICKET"
	REMOVECOMMENT               = "REMOVE_COMMENT"
	REMOVEOWNCOMMENT            = "REMOVE_OWN_COMMENT"
	EDITOWNCOMMENT              = "EDIT_OWN_COMMENT"
	EDITCOMMENT                 = "EDIT_COMMENT"
	TRANSITIONTICKET            = "TRANSITION_TICKET"
	EDITTICKET                  = "EDIT_TICKET"
	REMOVETICKET                = "REMOVE_TICKET"
)
