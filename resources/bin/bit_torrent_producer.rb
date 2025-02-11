#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'time'
require 'kafka'

FILENAME = 'bit_torrent.json'
MAX_BATCH_SIZE = 100
BATCH_INTERVAL = 60 # seconds

# Initialize Kafka producer
kafka = Kafka.new(seed_brokers: ['kafka://localhost:9092'])
producer = kafka.producer

def modify_timestamp(json_data)
  json_data['timestamp'] = Time.now.utc.iso8601
  json_data
end

def read_json_file(json_file)
  File.readlines(json_file).map { |line| JSON.parse(line) }
end

def replay_messages(json_file, producer)
  messages = read_json_file(json_file)

  start_timestamp = messages[0]['timestamp']
  real_start_time = Time.now.to_f

  batch = []
  last_delivery = Time.now

  messages.each do |message|
    # Sleep based on timestamp difference to simulate real-time replay
    elapsed_original = message['timestamp'] - start_timestamp
    current_time = Time.now.to_f
    sleep_time = real_start_time + elapsed_original - current_time
    sleep(sleep_time) if sleep_time.positive?

    # Modify the timestamp and add to batch
    modified_message = modify_timestamp(message)
    batch << modified_message.to_json

    # Deliver batch if conditions are met
    next unless (Time.now - last_delivery >= BATCH_INTERVAL) || (batch.size >= MAX_BATCH_SIZE)

    deliver_batch(producer, batch)
    batch.clear
    last_delivery = Time.now
  end

  # Deliver any remaining messages
  deliver_batch(producer, batch) unless batch.empty?

  # Close the producer
  producer.shutdown
end

def deliver_batch(producer, batch)
  batch.each { |message| producer.produce(message, topic: "rb_event_post_#{namespace_uuid}") }
  producer.deliver_messages
  puts "Delivered batch of #{batch.size} messages"
end

# Start the message replay process
replay_messages(FILENAME, producer)
