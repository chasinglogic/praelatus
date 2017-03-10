package middleware

import (
	"log"
	"net/http"
	"time"
)

// LoggedResponseWriter wraps http.ResponseWriter so we can capture the status
// code for logging
type LoggedResponseWriter struct {
	status int
	http.ResponseWriter
}

// Status will return the status code used in this request.
func (w *LoggedResponseWriter) Status() int {
	return w.status
}

// WriteHeader implements http.ResponseWriter adding our custom functionality
// to it
func (w *LoggedResponseWriter) WriteHeader(code int) {
	w.status = code
	w.ResponseWriter.WriteHeader(code)
}

func (w *LoggedResponseWriter) Write(b []byte) (int, error) {
	if w.status == 0 {
		w.WriteHeader(200)
	}

	return w.ResponseWriter.Write(b)
}

// Logger will log a request and any information about the request, it should
// be the first middleware in any chain.
func Logger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		lrw := &LoggedResponseWriter{0, w}
		next.ServeHTTP(lrw, r)

		log.Printf("|%s| [%d] %s %s",
			r.Method, lrw.Status(), r.URL.Path, time.Since(start).String())
	})
}
