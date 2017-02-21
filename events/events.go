// Package events handles sending notifications to users and websockets
// when system events happen. Such as firing webhooks on workflow
// transitions.
package events

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
	"github.com/praelatus/praelatus/config"
	"github.com/praelatus/praelatus/models"
)

// evm is the global event manager which is interfaced with using the functions
// whose names match the methods of an EventManager
var evm = &EventManager{
	Result: make(chan Result, 10),
	Listeners: []chan models.Event{
		hookEventChan,
	},
	ActiveWS: make([]WSManager, 0),
}

var eventLog = log.New(config.LogWriter(), "EVENT", log.LstdFlags)

// Stop is a global channel used to stop all running event managers
var Stop = make(chan int)

// EventManager is the fan-in point for all available event listeners
type EventManager struct {
	Result    chan Result
	Listeners []chan models.Event
	ActiveWS  []WSManager
}

// FireEvent sends the given event to all registered listeners of the given
// event manager
func (e *EventManager) FireEvent(ev models.Event) {
	for _, listener := range e.Listeners {
		listener <- ev
	}

	return
}

// RegisterListener adds a listener to the EventManager
func (e *EventManager) RegisterListener(ev chan models.Event) {
	e.Listeners = append(e.Listeners, ev)
}

// ResultChan returns the result channel used on the global EventManager
func ResultChan() chan Result {
	return evm.Result
}

// Run starts the event manager, should be called in a go routine normally
func Run() {
	go handleHookEvent(evm.Result)

	for {
		select {
		case res := <-evm.Result:
			if !res.Success {
				eventLog.Printf("handler %s failed with error %s\n", res.Reporter, res.Error.Error())
				continue
			}

			eventLog.Printf("handler %s ran successfully", res.Reporter)
		case <-Stop:
			return
		}
	}
}

// AddWs will upgrade the given http connection to a websocket and register it
// with the EventManager
func (e *EventManager) AddWs(w http.ResponseWriter, r *http.Request, h http.Header) error {
	conn, err := websocket.Upgrade(w, r, h, 1024, 1024)
	if err != nil {
		return err
	}

	ws := WSManager{
		In:     make(chan []byte),
		Out:    make(chan []byte),
		Socket: conn,
	}

	e.ActiveWS = append(e.ActiveWS, ws)
	return nil
}

// New will return a blank event manager handling allocations for you as
// appropriate
func New() *EventManager {
	return &EventManager{
		Result:    make(chan Result),
		Listeners: []chan models.Event{},
		ActiveWS:  make([]WSManager, 0),
	}
}

// Result contains metadata sent back by an event handler
type Result struct {
	Reporter string
	Error    error
	Success  bool
}

// AddWs calls the method of the same name on the global EventManager
func AddWs(w http.ResponseWriter, r *http.Request, h http.Header) {
	evm.AddWs(w, r, h)
}

// FireEvent calls the method of the same name on the global EventManager
func FireEvent(e models.Event) {
	evm.FireEvent(e)
}
