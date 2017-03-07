package v1

import "github.com/gorilla/mux"

func V1Routes(router *mux.Router) {
	labelRouter(router)

}
