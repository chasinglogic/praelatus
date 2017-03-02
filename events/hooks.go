package events

import (
	"bytes"
	"errors"
	"fmt"
	"net/http"

	"github.com/alecthomas/template"
	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/models"
)

var (
	hookEventChan = make(chan models.Event)
	requestChan   = make(chan http.Request)

	webWorkers = config.WebWorkers()
)

func handleHookEvent(result chan Result) {
	for _ := range webWorkers {
		go sendRequest(result)
	}

	for {
		event := <-hookEventChan

		transition, ok := event.Data.(models.Transition)
		if !ok {
			continue
		}

		for _, hook := range transition.Hooks {
			res := Result{Reporter: "Hook Handler", Success: true}

			tmpl, err := template.New("hook-body").Parse(hook.Body)
			if err != nil {
				e := fmt.Sprintf("Error parsing body %s: %s %s\n",
					event.Ticket.Key, transition.Name, err.Error())
				res.Success = false
				res.Error = errors.New(e)
				result <- res
				continue
			}

			body := bytes.NewBuffer([]byte{})

			err = tmpl.Execute(body, event.Ticket)
			if err != nil {
				e := fmt.Sprintf("Error rendering body %s: %s %s\n",
					event.Ticket.Key, transition.Name, err.Error())
				res.Success = false
				res.Error = errors.New(e)
				result <- res
				continue
			}

			r, err := http.NewRequest(hook.Method, hook.Endpoint, body)
			if err != nil {
				e := fmt.Sprintf("Error creating request %s: %s %s\n",
					event.Ticket.Key, transition.Name, err.Error())
				res.Success = false
				res.Error = errors.New(e)
				result <- res
				continue
			}

			client := http.Client{}
			_, err = client.Do(r)
			if err != nil {
				e := fmt.Sprintf("Error sending request %s: %s %s\n",
					event.Ticket.Key, transition.Name, err.Error())
				res.Success = false
				res.Error = errors.New(e)
				result <- res
				continue
			}

			result <- res
		}

		result <- Result{
			Reporter: "Hook Handler",
			Success:  true,
			Error:    nil,
		}
	}
}

func sendRequest(result chan Result) {

}
