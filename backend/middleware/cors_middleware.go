package middleware

import (
	"net/http"
	"time"
)

var epoch = time.Unix(0, 0).Format(time.RFC1123)
var noCacheHeaders = map[string]string{
	"Access-Control-Allow-Origin":  "*",
	"Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
	"Access-Control-Allow-Headers": "Authorization",
	"Expires":                      epoch,
	"Cache-Control":                "no-cache, private, max-age=0",
	"Pragma":                       "no-cache",
	"X-Accel-Expires":              "0",
}

func CORSWrapper(handler http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		for k, v := range noCacheHeaders {
			w.Header().Set(k, v)
		}

		// Short circuit for OPTIONS method.
		if r.Method == http.MethodOptions {
			w.WriteHeader(200)
			return
		}

		handler(w, r)
	}
}
