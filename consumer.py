#!/usr/bin/env python3
"""Kafka Consumer for Message Catch - Kubernetes Ready"""

import os
import sys
import json
import time
import signal
from confluent_kafka import Consumer, KafkaError

# Read from environment variables (K8s secret)
BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
GROUP_ID = os.getenv('GROUP_ID', 'message-catch-consumer-group')
TOPIC = os.getenv('KAFKA_TOPIC', 'BRANCO')

print(f"Starting Kafka Consumer...")
print(f"Bootstrap Servers: {BOOTSTRAP_SERVERS}")
print(f"Group ID: {GROUP_ID}")
print(f"Topic: {TOPIC}")

# Create health check file for liveness probe
HEALTH_FILE = '/tmp/healthy'

def create_health_file():
    """Create health check file"""
    try:
        with open(HEALTH_FILE, 'w') as f:
            f.write('healthy')
        print(f"✅ Health check file created: {HEALTH_FILE}")
    except Exception as e:
        print(f"⚠️ Failed to create health file: {e}")

def remove_health_file():
    """Remove health check file"""
    try:
        if os.path.exists(HEALTH_FILE):
            os.remove(HEALTH_FILE)
        print(f"❌ Health check file removed")
    except Exception as e:
        print(f"⚠️ Failed to remove health file: {e}")

# Graceful shutdown handler
running = True

def shutdown_handler(signum, frame):
    global running
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    running = False
    remove_health_file()

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

def consume_messages():
    """Main consumer loop"""
    global running
    
    # Kafka consumer configuration
    consumer_config = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'session.timeout.ms': 30000,
        'max.poll.interval.ms': 300000,
    }
    
    consumer = None
    
    try:
        # Create consumer
        consumer = Consumer(consumer_config)
        consumer.subscribe([TOPIC])
        print(f"✅ Consumer subscribed to topic: {TOPIC}")
        
        # Mark as healthy
        create_health_file()
        
        # Main consumption loop
        message_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition, not a critical error
                    continue
                else:
                    print(f"❌ Consumer error: {msg.error()}")
                    remove_health_file()
                    break
            
            try:
                # Process message
                message_count += 1
                value = msg.value().decode('utf-8')
                data = json.loads(value)
                
                print(f"\n📥 Message #{message_count} received:")
                print(f"   Topic: {msg.topic()}")
                print(f"   Partition: {msg.partition()}")
                print(f"   Offset: {msg.offset()}")
                print(f"   Data: {json.dumps(data, indent=2)}")
                
                # TODO: Process message (save to MongoDB, etc.)
                # For now, just acknowledge
                time.sleep(0.1)  # Simulate processing
                
                # Commit offset after successful processing
                consumer.commit(msg)
                print(f"✅ Message #{message_count} processed and committed")
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to decode JSON: {e}")
                print(f"   Raw value: {msg.value()}")
                # Still commit to avoid reprocessing
                consumer.commit(msg)
                
            except Exception as e:
                print(f"❌ Error processing message: {e}")
                # Don't commit - message will be reprocessed
                continue
        
        print(f"\n📊 Final stats: {message_count} messages processed")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        remove_health_file()
        sys.exit(1)
        
    finally:
        if consumer:
            print("🔒 Closing consumer...")
            consumer.close()
            print("✅ Consumer closed")
        remove_health_file()

if __name__ == "__main__":
    print("="*60)
    print("Message Catch - Kafka Consumer")
    print("="*60)
    consume_messages()
    print("\n👋 Consumer shutdown complete")
