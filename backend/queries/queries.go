package queries

import (
	"bytes"
	"encoding/json"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/go-redis/redis"
	"github.com/google/uuid"
	"github.com/sirupsen/logrus"
	"sync"
	"time"
)

type QueryMgrCtx struct {
	logger *logrus.Entry

	awsSess           *session.Session
	s3Bucket          string
	s3bucketUploadDir string

	rConn          *redis.Client
	publishChannel string
	dataDuration   time.Duration

	waitMutex sync.Mutex
	waitMap   map[string]chan *QueryResult
}

type QueryMgr interface {
	Submit(uploadData []byte) (string, error)
	Update(upd *QueryUpdate) error
	Query(requestId string, timeout time.Duration) (*QueryResult, error)
}

type QueryUpdate struct {
	RequestID string `json:"request_id"`
	Data      string `json:"data"` // <- TODO
}

type QueryResult struct {
	Success bool
	Error   string
	Data    string `json:"data"` // <- TODO
}

const ErrTimeout = "TIMEOUT"

func CreateQueryMgr(logger *logrus.Entry,
	awsSess *session.Session, s3Bucket string, s3bucketUploadDir string,
	rConn *redis.Client, publishChannel string, dataDuration time.Duration) QueryMgr {

	ctx := new(QueryMgrCtx)
	ctx.logger = logger.WithField("Service", "QueryManager")
	ctx.awsSess = awsSess
	ctx.s3Bucket = s3Bucket
	ctx.s3bucketUploadDir = s3bucketUploadDir
	ctx.rConn = rConn
	ctx.publishChannel = publishChannel
	ctx.dataDuration = dataDuration
	ctx.waitMap = make(map[string]chan *QueryResult)

	go ctx.redisSubscriber()

	return ctx
}

func (ctx *QueryMgrCtx) Submit(uploadData []byte) (string, error) {
	requestId := uuid.New().String()

	_, err := s3.New(ctx.awsSess).PutObject(&s3.PutObjectInput{
		Bucket:               aws.String(ctx.s3Bucket),
		Key:                  aws.String(ctx.s3bucketUploadDir + requestId),
		ACL:                  aws.String("private"),
		Body:                 bytes.NewReader(uploadData),
		ContentLength:        aws.Int64(int64(len(uploadData))),
		ContentDisposition:   aws.String("attachment"),
		ServerSideEncryption: aws.String("AES256"),
	})

	return requestId, err
}

func (ctx *QueryMgrCtx) Update(upd *QueryUpdate) error {
	jsonData, err := json.Marshal(upd.Data)
	if err != nil {
		ctx.logger.WithError(err).Error("Could not marshal to JSON.")

		return err
	}

	setOut := ctx.rConn.Set(upd.RequestID, jsonData, ctx.dataDuration)
	if setOut.Err() != nil {
		ctx.logger.WithError(setOut.Err()).Error("Could not save to Redis.")

		return setOut.Err()
	}

	pubOut := ctx.rConn.Publish(ctx.publishChannel, upd.RequestID)
	if pubOut.Err() != nil {
		ctx.logger.WithError(pubOut.Err()).Error("Could not publish update.")

		return pubOut.Err()

	}

	return nil
}

func (ctx *QueryMgrCtx) Query(requestId string, timeout time.Duration) (*QueryResult, error) {
	data, err := ctx.readFromRedis(requestId)
	if err == redis.Nil {
		// Wait till timeout.
		waiter := ctx.registerWaiter(requestId)

		select {
		case <-time.After(timeout):
			ctx.deregisterWaiter(requestId)
			return &QueryResult{
				Success: false,
				Error:   ErrTimeout,
			}, nil

		case res := <-waiter:
			return res, nil
		}
	}

	return &QueryResult{
		Success: true,
		Data:    data,
	}, nil
}

func (ctx *QueryMgrCtx) registerWaiter(requestId string) chan *QueryResult {
	ctx.waitMutex.Lock()
	defer ctx.waitMutex.Unlock()

	waiter, exists := ctx.waitMap[requestId]
	if exists {
		waiter <- &QueryResult{
			Success: false,
			Error:   ErrTimeout,
		}
		close(waiter)
	}

	waiter = make(chan *QueryResult)
	ctx.waitMap[requestId] = waiter

	return waiter
}

func (ctx *QueryMgrCtx) deregisterWaiter(requestId string) {
	ctx.waitMutex.Lock()
	defer ctx.waitMutex.Unlock()

	waiter, exists := ctx.waitMap[requestId]
	if exists {
		waiter <- &QueryResult{
			Success: false,
			Error:   ErrTimeout,
		}
		close(waiter)
	}
}

func (ctx *QueryMgrCtx) redisSubscriber() {
	sub := ctx.rConn.PSubscribe(ctx.publishChannel)
	defer sub.Close()

	for msg := range sub.Channel() {
		requestId := msg.Payload
		ctx.logger.WithField("Payload", requestId).Info("Subscription: Message Received.")
		ctx.releaseListeners(requestId)
	}
}

func (ctx *QueryMgrCtx) releaseListeners(requestId string) {
	ctx.waitMutex.Lock()
	defer ctx.waitMutex.Unlock()

	waiter, exists := ctx.waitMap[requestId]
	if exists {
		data, _ := ctx.readFromRedis(requestId)
		waiter <- &QueryResult{
			Success: data != "",
			Data:    data,
		}
		close(waiter)

		delete(ctx.waitMap, requestId)
	}
}

func (ctx *QueryMgrCtx) readFromRedis(requestId string) (string, error) {
	getOut := ctx.rConn.Get(requestId)
	if getOut.Err() != nil && getOut.Err() != redis.Nil {
		ctx.logger.WithError(getOut.Err()).
			Error("Could not read from Redis.")

		return "", getOut.Err()
	}

	return getOut.Val(), getOut.Err()
}
