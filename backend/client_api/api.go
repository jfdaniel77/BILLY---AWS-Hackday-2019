package client_api

import (
	"backend/queries"
	"encoding/json"
	"github.com/sirupsen/logrus"
	"net/http"
	"time"
)

type ClientAPICtx struct {
	logger *logrus.Entry

	host string
	mux *http.ServeMux

	queryMgr queries.QueryMgr
}

func CreateClientAPI(logger *logrus.Entry, queryMgr queries.QueryMgr, host string) *ClientAPICtx {
	ctx := new(ClientAPICtx)

	ctx.logger = logger.WithField("Service", "ClientAPI")
	ctx.host = host
	ctx.queryMgr = queryMgr
	ctx.mux = http.NewServeMux()

	return ctx
}

func (ctx *ClientAPICtx) RegisterEndpoints() {
	ctx.mux.HandleFunc("/submit", ctx.handleSubmit)
	ctx.mux.HandleFunc("/query", ctx.handleQuery)
}

func (ctx *ClientAPICtx) Start() {
	ctx.logger.
		WithError(http.ListenAndServe(ctx.host, ctx.mux)).
		Error("Client API Server stopped.")
}

func (ctx *ClientAPICtx) handleSubmit(w http.ResponseWriter, r *http.Request) {
	// TODO: Multipart image upload.
	requestID, err := ctx.queryMgr.Submit([]byte{}, "todo")

	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(requestID))
	} else {
		w.WriteHeader(200)
		w.Write([]byte(requestID))
	}
}

func (ctx *ClientAPICtx) handleQuery(w http.ResponseWriter, r *http.Request) {
	qry := r.URL.Query()
	requestID := qry["requestID"]

	out, err := ctx.queryMgr.Query(requestID[0], 30 * time.Second)
	jsonData, _ := json.Marshal(out)

	if err != nil {
		w.WriteHeader(500)
		w.Write(jsonData)
	} else {
		w.WriteHeader(200)
		w.Write(jsonData)
	}
}