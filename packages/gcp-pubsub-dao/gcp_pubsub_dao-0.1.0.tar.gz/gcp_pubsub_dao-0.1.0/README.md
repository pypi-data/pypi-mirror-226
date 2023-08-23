# Ash DAL
The library provides DAO classes for GCP pubsub publisher/subscriber.

## Installation

### PyPi

*To be added*

## Usage
```python
from gcp_pubsub_dao import PubSubSubscriberDAO, Message

dao = PubSubSubscriberDAO(project_id="prodect-dev", subscription_id="subscription")
messages: Message = dao.get_messages(messages_count=2)

for message in messages:
    print(message.data)
    
dao.ack_messages(ack_ids=[message[0].ack_id])      
dao.nack_messages(ack_ids=[message[1].ack_id])     

dao.close()     # to clean up connections
```

```python
from gcp_pubsub_dao import PubSubPublisherDAO

dao = PubSubPublisherDAO(project_id="prodect-dev")
try:
    dao.publish_message(topic_name="topic", payload=b"asdfsdf", attributes={"kitId": "AW12345678"})
except Exception as ex:
    print(ex)
```