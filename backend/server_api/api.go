package server_api

import (
	"backend/queries"
	"github.com/sirupsen/logrus"
	"net/http"
)

type ServerAPICtx struct {
	logger *logrus.Entry

	host string
	mux  *http.ServeMux

	queryMgr queries.QueryMgr
}

func CreateServerAPI(logger *logrus.Entry, queryMgr queries.QueryMgr, host string) *ServerAPICtx {
	ctx := new(ServerAPICtx)

	ctx.logger = logger.WithField("Service", "ServerAPI")
	ctx.host = host
	ctx.queryMgr = queryMgr
	ctx.mux = http.NewServeMux()

	return ctx
}

func (ctx *ServerAPICtx) RegisterEndpoints() {
	ctx.mux.HandleFunc("/result", ctx.handleResult)
}

func (ctx *ServerAPICtx) Start() {
	ctx.logger.
		WithError(http.ListenAndServe(ctx.host, ctx.mux)).
		Error("Server API Server stopped.")
}

func (ctx *ServerAPICtx) handleResult(w http.ResponseWriter, r *http.Request) {
	var requestID string
	var data string

	if r.Method == "POST" {
		err := r.ParseForm()
		if err != nil {
			w.WriteHeader(500)
			w.Write([]byte(err.Error()))
			ctx.logger.WithError(err).Error("Could not parse POST Form")
			return
		}

		requestID = r.FormValue("requestID")
		data = r.FormValue("data")

	} else if r.Method == "GET" {
		// For now, it is a GET only.
		qry := r.URL.Query()
		requestID = qry["requestID"][0]
		data = qry["data"][0]
	} else {
		w.WriteHeader(405)
		w.Write([]byte("GET or POST expected."))
		ctx.logger.WithField("Method", r.Method).Error("GET or POST expected.")
		return
	}

	err := ctx.queryMgr.Update(&queries.QueryUpdate{
		RequestID: requestID,
		Data:      data,
	})

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(err.Error()))
		ctx.logger.WithError(err).Error("Could not parse POST Form")
	} else {
		w.WriteHeader(200)
		w.Write([]byte("OK"))
	}
}
