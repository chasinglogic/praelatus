# github.com/praelatus/praelatus/

This is the REST API reference documentation for the Praelatus REST API, Praelatus is an Open Source Bug Tracking / Ticketing system.

## Routes

<details>
<summary>`/api/fields`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/fields**
		- **/**
			- _POST_
				- [CreateField](/api/fields.go#L49)
			- _GET_
				- [GetAllFields](/api/fields.go#L28)

</details>
<details>
<summary>`/api/fields/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/fields**
		- **/:id**
			- _GET_
				- [GetField](/api/fields.go#L80)
			- _PUT_
				- [UpdateField](/api/fields.go#L106)
			- _DELETE_
				- [DeleteField](/api/fields.go#L138)

</details>
<details>
<summary>`/api/labels`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/labels**
		- **/**
			- _GET_
				- [GetAllLabels](/api/labels.go#L28)
			- _POST_
				- [CreateLabel](/api/labels.go#L67)

</details>
<details>
<summary>`/api/labels/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/labels**
		- **/:id**
			- _GET_
				- [GetLabel](/api/labels.go#L41)
			- _DELETE_
				- [DeleteLabel](/api/labels.go#L143)
			- _PUT_
				- [UpdateLabel](/api/labels.go#L99)

</details>
<details>
<summary>`/api/projects`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/projects**
		- **/**
			- _GET_
				- [GetAllProjects](/api/projects.go#L48)
			- _POST_
				- [CreateProject](/api/projects.go#L69)

</details>
<details>
<summary>`/api/projects/:pkey`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/projects**
		- **/:pkey**
			- _GET_
				- [GetProject](/api/projects.go#L27)
			- _DELETE_
				- [RemoveProject](/api/projects.go#L101)
			- _PUT_
				- [UpdateProject](/api/projects.go#L125)

</details>
<details>
<summary>`/api/routes/*`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/routes/***
		- _*_
			- [(*Mux).Mount.func1](/vendor/github.com/pressly/chi/mux.go#L250)

</details>
<details>
<summary>`/api/teams`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/teams**
		- **/**
			- _GET_
				- [GetAllTeams](/api/teams.go#L28)
			- _POST_
				- [CreateTeam](/api/teams.go#L49)

</details>
<details>
<summary>`/api/teams/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/teams**
		- **/:id**
			- _DELETE_
				- [RemoveTeam](/api/teams.go#L138)
			- _GET_
				- [GetTeam](/api/teams.go#L80)
			- _PUT_
				- [UpdateTeam](/api/teams.go#L106)

</details>
<details>
<summary>`/api/tickets`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/tickets**
		- **/**
			- _GET_
				- [GetAllTickets](/api/tickets.go#L80)

</details>
<details>
<summary>`/api/tickets/:pkey`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/tickets**
		- **/:pkey**
			- _POST_
				- [CreateTicket](/api/tickets.go#L109)

</details>
<details>
<summary>`/api/tickets/:pkey/:key`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/tickets**
		- **/:pkey/:key**
			- _DELETE_
				- [RemoveTicket](/api/tickets.go#L142)
			- _PUT_
				- [UpdateTicket](/api/tickets.go#L165)
			- _GET_
				- [GetTicket](/api/tickets.go#L37)

</details>
<details>
<summary>`/api/tickets/:pkey/:key/comments`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/tickets**
		- **/:pkey/:key/comments**
			- _GET_
				- [GetComments](/api/tickets.go#L203)
			- _POST_
				- [CreateComment](/api/tickets.go#L276)

</details>
<details>
<summary>`/api/tickets/:pkey/tickets`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/tickets**
		- **/:pkey/tickets**
			- _GET_
				- [GetAllTicketsByProject](/api/tickets.go#L93)

</details>
<details>
<summary>`/api/tickets/comments/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/tickets**
		- **/comments/:id**
			- _PUT_
				- [UpdateComment](/api/tickets.go#L218)
			- _DELETE_
				- [RemoveComment](/api/tickets.go#L254)

</details>
<details>
<summary>`/api/types`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/types**
		- **/**
			- _GET_
				- [GetAllTicketTypes](/api/types.go#L28)
			- _POST_
				- [CreateTicketType](/api/types.go#L49)

</details>
<details>
<summary>`/api/types/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/types**
		- **/:id**
			- _GET_
				- [GetTicketType](/api/types.go#L80)
			- _PUT_
				- [UpdateTicketType](/api/types.go#L106)
			- _DELETE_
				- [RemoveTicketType](/api/types.go#L150)

</details>
<details>
<summary>`/api/users`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/users**
		- **/**
			- _GET_
				- [GetAllUsers](/api/users.go#L63)
			- _POST_
				- [CreateUser](/api/users.go#L88)

</details>
<details>
<summary>`/api/users/:username`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/users**
		- **/:username**
			- _GET_
				- [GetUser](/api/users.go#L37)
			- _PUT_
				- [UpdateUser](/api/users.go#L140)
			- _DELETE_
				- [DeleteUser](/api/users.go#L165)

</details>
<details>
<summary>`/api/users/sessions`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/users**
		- **/sessions**
			- _POST_
				- [CreateSession](/api/users.go#L190)
			- _GET_
				- [RefreshSession](/api/users.go#L247)

</details>
<details>
<summary>`/api/v1/fields`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/fields**
		- **/**
			- _GET_
				- [GetAllFields](/api/fields.go#L28)
			- _POST_
				- [CreateField](/api/fields.go#L49)

</details>
<details>
<summary>`/api/v1/fields/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/fields**
		- **/:id**
			- _PUT_
				- [UpdateField](/api/fields.go#L106)
			- _DELETE_
				- [DeleteField](/api/fields.go#L138)
			- _GET_
				- [GetField](/api/fields.go#L80)

</details>
<details>
<summary>`/api/v1/labels`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/labels**
		- **/**
			- _GET_
				- [GetAllLabels](/api/labels.go#L28)
			- _POST_
				- [CreateLabel](/api/labels.go#L67)

</details>
<details>
<summary>`/api/v1/labels/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/labels**
		- **/:id**
			- _GET_
				- [GetLabel](/api/labels.go#L41)
			- _DELETE_
				- [DeleteLabel](/api/labels.go#L143)
			- _PUT_
				- [UpdateLabel](/api/labels.go#L99)

</details>
<details>
<summary>`/api/v1/projects`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/projects**
		- **/**
			- _GET_
				- [GetAllProjects](/api/projects.go#L48)
			- _POST_
				- [CreateProject](/api/projects.go#L69)

</details>
<details>
<summary>`/api/v1/projects/:pkey`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/projects**
		- **/:pkey**
			- _PUT_
				- [UpdateProject](/api/projects.go#L125)
			- _GET_
				- [GetProject](/api/projects.go#L27)
			- _DELETE_
				- [RemoveProject](/api/projects.go#L101)

</details>
<details>
<summary>`/api/v1/routes/*`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/routes/***
		- _*_
			- [(*Mux).Mount.func1](/vendor/github.com/pressly/chi/mux.go#L250)

</details>
<details>
<summary>`/api/v1/teams`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/teams**
		- **/**
			- _GET_
				- [GetAllTeams](/api/teams.go#L28)
			- _POST_
				- [CreateTeam](/api/teams.go#L49)

</details>
<details>
<summary>`/api/v1/teams/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/teams**
		- **/:id**
			- _GET_
				- [GetTeam](/api/teams.go#L80)
			- _PUT_
				- [UpdateTeam](/api/teams.go#L106)
			- _DELETE_
				- [RemoveTeam](/api/teams.go#L138)

</details>
<details>
<summary>`/api/v1/tickets`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/tickets**
		- **/**
			- _GET_
				- [GetAllTickets](/api/tickets.go#L80)

</details>
<details>
<summary>`/api/v1/tickets/:pkey`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/tickets**
		- **/:pkey**
			- _POST_
				- [CreateTicket](/api/tickets.go#L109)

</details>
<details>
<summary>`/api/v1/tickets/:pkey/:key`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/tickets**
		- **/:pkey/:key**
			- _DELETE_
				- [RemoveTicket](/api/tickets.go#L142)
			- _PUT_
				- [UpdateTicket](/api/tickets.go#L165)
			- _GET_
				- [GetTicket](/api/tickets.go#L37)

</details>
<details>
<summary>`/api/v1/tickets/:pkey/:key/comments`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/tickets**
		- **/:pkey/:key/comments**
			- _GET_
				- [GetComments](/api/tickets.go#L203)
			- _POST_
				- [CreateComment](/api/tickets.go#L276)

</details>
<details>
<summary>`/api/v1/tickets/:pkey/tickets`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/tickets**
		- **/:pkey/tickets**
			- _GET_
				- [GetAllTicketsByProject](/api/tickets.go#L93)

</details>
<details>
<summary>`/api/v1/tickets/comments/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/tickets**
		- **/comments/:id**
			- _PUT_
				- [UpdateComment](/api/tickets.go#L218)
			- _DELETE_
				- [RemoveComment](/api/tickets.go#L254)

</details>
<details>
<summary>`/api/v1/types`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/types**
		- **/**
			- _GET_
				- [GetAllTicketTypes](/api/types.go#L28)
			- _POST_
				- [CreateTicketType](/api/types.go#L49)

</details>
<details>
<summary>`/api/v1/types/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/types**
		- **/:id**
			- _GET_
				- [GetTicketType](/api/types.go#L80)
			- _PUT_
				- [UpdateTicketType](/api/types.go#L106)
			- _DELETE_
				- [RemoveTicketType](/api/types.go#L150)

</details>
<details>
<summary>`/api/v1/users`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/users**
		- **/**
			- _GET_
				- [GetAllUsers](/api/users.go#L63)
			- _POST_
				- [CreateUser](/api/users.go#L88)

</details>
<details>
<summary>`/api/v1/users/:username`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/users**
		- **/:username**
			- _GET_
				- [GetUser](/api/users.go#L37)
			- _PUT_
				- [UpdateUser](/api/users.go#L140)
			- _DELETE_
				- [DeleteUser](/api/users.go#L165)

</details>
<details>
<summary>`/api/v1/users/sessions`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/users**
		- **/sessions**
			- _GET_
				- [RefreshSession](/api/users.go#L247)
			- _POST_
				- [CreateSession](/api/users.go#L190)

</details>
<details>
<summary>`/api/v1/workflows`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/workflows**
		- **/**
			- _GET_
				- [GetAllWorkflows](/api/workflows.go#L28)

</details>
<details>
<summary>`/api/v1/workflows/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api/v1**
	- **/workflows**
		- **/:id**
			- _PUT_
				- [UpdateWorkflow](/api/workflows.go#L114)
			- _DELETE_
				- [RemoveWorkflow](/api/workflows.go#L168)
			- _POST_
				- [CreateWorkflow](/api/workflows.go#L49)
			- _GET_
				- [GetWorkflow](/api/workflows.go#L90)

</details>
<details>
<summary>`/api/workflows`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/workflows**
		- **/**
			- _GET_
				- [GetAllWorkflows](/api/workflows.go#L28)

</details>
<details>
<summary>`/api/workflows/:id`</summary>

- [Logger](/mw/logger.go#L38)
- [Auth](/mw/auth.go#L143)
- **/api**
	- **/workflows**
		- **/:id**
			- _PUT_
				- [UpdateWorkflow](/api/workflows.go#L114)
			- _DELETE_
				- [RemoveWorkflow](/api/workflows.go#L168)
			- _POST_
				- [CreateWorkflow](/api/workflows.go#L49)
			- _GET_
				- [GetWorkflow](/api/workflows.go#L90)

</details>

Total # of routes: 44
