package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

// Message is the standard payload format for internal communication.
type Message struct {
	Source    string      `json:"source"`
	EventType string      `json:"event_type"`
	Payload   interface{} `json:"payload"`
}

// System represents a component in your ecosystem.
type System interface {
	Listen() <-chan Message
}

// JuliusServiceBus manages and routes all messages.
type JuliusServiceBus struct {
	systems      []System
	messageQueue chan Message
	httpClient   *http.Client
	apiEndpoint  string
}

// NewJuliusServiceBus initializes the bus with a specific API endpoint.
func NewJuliusServiceBus(apiEndpoint string) *JuliusServiceBus {
	return &JuliusServiceBus{
		messageQueue: make(chan Message, 100), // Buffered channel for performance
		httpClient: &http.Client{
			Timeout: 10 * time.Second,
		},
		apiEndpoint: apiEndpoint,
	}
}

// RegisterSystem adds a system to the bus to begin receiving its messages.
func (jsb *JuliusServiceBus) RegisterSystem(sys System) {
	jsb.systems = append(jsb.systems, sys)
}

// Start begins the main message processing loop.
func (jsb *JuliusServiceBus) Start() {
	// Start a goroutine for each system to listen for messages.
	for _, sys := range jsb.systems {
		go jsb.listenForMessages(sys)
	}
	// Start a single goroutine to process messages from the queue.
	go jsb.processMessages()
}

// listenForMessages reads messages from a system's output channel and queues them.
func (jsb *JuliusServiceBus) listenForMessages(sys System) {
	for msg := range sys.Listen() {
		jsb.messageQueue <- msg
	}
}

// processMessages consumes the message queue and sends payloads to the API.
func (jsb *JuliusServiceBus) processMessages() {
	for msg := range jsb.messageQueue {
		fmt.Printf("Julius received message from %s, type: %s\n", msg.Source, msg.EventType)

		jsonPayload, err := json.Marshal(msg)
		if err != nil {
			log.Printf("Error marshaling message: %v", err)
			continue
		}

		// Send to the new software's API.
		resp, err := jsb.httpClient.Post(jsb.apiEndpoint+"/event", "application/json", bytes.NewBuffer(jsonPayload))
		if err != nil {
			log.Printf("Failed to post message to API: %v", err)
			continue
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			log.Printf("API returned non-OK status: %d", resp.StatusCode)
		}
	}
}

// MockPrometheus is a placeholder for your Prometheus Protocol system.
type MockPrometheus struct{}

func (mp *MockPrometheus) Listen() <-chan Message {
	// In a real scenario, this would be a channel from the Prometheus system.
	// We'll simulate data generation here.
	ch := make(chan Message)
	go func() {
		for {
			time.Sleep(5 * time.Second)
			ch <- Message{
				Source:    "PrometheusProtocol",
				EventType: "DataUpdate",
				Payload:   "Example Prometheus data",
			}
		}
	}()
	return ch
}

func main() {
	// The API endpoint of the new software, which you have built.
	apiEndpoint := "https://your_new_software_api/api/v1"

	// Initialize the Julius Service Bus.
	julius := NewJuliusServiceBus(apiEndpoint)

	// Register your core ecosystem components with Julius.
	// You would replace these with your actual system clients.
	julius.RegisterSystem(&MockPrometheus{})
	// julius.RegisterSystem(&VArchitect{})
	// julius.RegisterSystem(&CritterCraftUniverse{})

	// Start the bus to begin orchestrating your ecosystem.
	julius.Start()

	// Keep the main function running indefinitely.
	select {}
}
