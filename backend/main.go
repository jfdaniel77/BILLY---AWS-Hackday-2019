package main

import (
	"backend/client_api"
	"backend/queries"
	"backend/server_api"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/go-redis/redis"
	"github.com/sirupsen/logrus"
	"time"
)

func main() {
	logger := logrus.WithField("App", "Hackday2019")

	awsCfg := &aws.Config{
		Region: aws.String("ap-southeast-1"),
	}

	awsSess, err := session.NewSession(awsCfg)
	if err != nil {
		logger.WithError(err).
			Fatal("Could not create AWS Session.")

	}

	rConn, err := connectToRedis(logger)
	if err != nil {
		logger.WithError(err).
			Fatal("Could not connect to Redis.")
	}

	queryMgr := queries.CreateQueryMgr(logger,
		awsSess, "TODO",
		rConn, "hackday.updates", 25 * time.Hour)

	clientApi := client_api.CreateClientAPI(logger, queryMgr, ":8080")
	clientApi.RegisterEndpoints()
	go clientApi.Start()

	serverApi := server_api.CreateServerAPI(logger, queryMgr, ":8081")
	serverApi.RegisterEndpoints()
	serverApi.Start()
}

func connectToRedis(logger *logrus.Entry) (*redis.Client, error) {
	// TODO: Change this
	hostname := "127.0.0.1:6379"

	redisConn := redis.NewClient(&redis.Options{
		Addr:     hostname,
		Password: "",
		DB:       0,
	})

	redisTest := redisConn.Ping()
	if redisTest.Err() != nil {
		logger.WithError(redisTest.Err()).
			Error("Could not connect to Redis.")

		return nil, redisTest.Err()
	}

	return redisConn, nil
}
