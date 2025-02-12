#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'time'
require 'kafka'

FILENAME = '/usr/lib/redborder/producers/json/bit_torrent.json'

# Initialize Kafka producer
kafka = Kafka.new(['localhost:9092'])
producer = kafka.producer
NAMESPACE_UUID = '352369f8-60fb-4b72-a603-d1d8393cca0a'
def modify_timestamp(json_data, real_last_time)
  puts json_data
  json_data['timestamp'] = json_data['timestamp'] + real_last_time
  json_data
end

def read_json_file(json_file)
  File.readlines(json_file).map { |line| JSON.parse(line) }
end

def replay_messages(json_file, producer)
  messages = read_json_file(json_file)
  real_last_time = messages.last['timestamp']

  messages.each do |message|
    # sleep_time = 
    # sleep(sleep_time) if sleep_time.positive?

    # Modify the timestamp and add to batch
    modified_message = modify_timestamp(message, real_last_time)

    begin
      producer.produce(modified_message.to_json, topic: 'rb_event_post_' + NAMESPACE_UUID)
      producer.deliver_messages
    rescue => e
      puts "Error delivering message: #{e.message}"
      sleep 1 # Add delay before retrying
      retry
    end    
    puts "Delivered message"
  end

  # Close the producer
  producer.shutdown
end

# Start the message replay process
replay_messages(FILENAME, producer)
