#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'
require 'kafka'
require 'time'
require 'optparse'

# Parse command line arguments
options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: #{$PROGRAM_NAME} [options]"

  opts.on('-d', '--directory DIR', 'Directory containing JSON files') do |d|
    options[:directory] = d
  end

  opts.on('-h', '--help', 'Show this help message') do
    puts opts
    exit
  end
end.parse!

def setup_producer()
  kafka = Kafka.new(seed_brokers: ['localhost:9092'])
  kafka.async_producer(
    delivery_threshold: 100,
    delivery_interval: 1
  )
rescue Kafka::ConnectionError => e
  puts "Failed to connect to Kafka: #{e.message}"
  exit 1
rescue StandardError => e
  puts "Unexpected error: #{e.message}"
  exit 1
end


def read_json_file(json_file)
  JSON.parse(File.read(json_file))
rescue JSON::ParserError => e
  puts "Failed to parse JSON file #{json_file}: #{e.message}"
  exit 1
rescue StandardError => e
  puts "Failed to read file #{json_file}: #{e.message}"
  exit 1
end

def replay_messages(json_file, producer, processes)
  topic = if File.basename(json_file).include?('sflow')
            'sflow'
          elsif File.basename(json_file).include?('event')
            'rb_event'
          else
            File.basename(json_file, '.json')
          end

  messages = read_json_file(json_file)

  # Skip first message if it starts with 'Waiting'
  messages.shift #if messages[0]['message']&.start_with?('Waiting')

  start_timestamp = messages[0]['timestamp']
  real_start_time = Time.now.to_f

  max_batch_size = 100
  last_delivery = Time.now
  batch = []

  messages.each do |message|
    elapsed_original = message['timestamp'] - start_timestamp
    current_time = Time.now.to_f
    sleep_time = real_start_time + elapsed_original - current_time
    sleep(sleep_time) if sleep_time.positive?

    producer.produce(message.to_json, topic: topic)
    batch << message

    next if Time.now - last_delivery < 60 && batch.size < max_batch_size
    producer.deliver_messages
    batch = []
    last_delivery = Time.now
  end

  # Deliver any remaining messages
  producer.deliver_messages if batch.any?
  producer.shutdown if processes.empty?
end

def replay_directory(directory)
  producer = setup_producer

  processes = []

  Dir.glob("#{directory}/*.json").each do |json_file|
    processes << Process.fork do
      replay_messages(json_file, producer, processes)
    end
  end

  processes.each { |pid| Process.wait(pid) }
end

if __FILE__ == $PROGRAM_NAME
  unless options[:directory]
    puts 'Error: Directory path is required'
    exit 1
  end

  replay_directory(options[:directory])
end
