import sys
from flask import Flask, request
from cloudevent import CloudEventService

if(len(sys.argv) < 2):
    print('Missing argument: please inform the broker address')
    exit()

broker_address = sys.argv[1]
source = "cloud-aggregator"
message_type = "cloud-to-edge-model"
data = { "fed_model": "cloud-aggregated-model-file" }

#broker_address = "broker-ingress.knative-eventing.svc.cluster.local/fedlearning/default"
#broker_address = "localhost:8081"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    cloud_event = CloudEventService()
    event = cloud_event.receive_message(request)

    print(
        f"Found {event['id']} from {event['source']} with type "
        f"{event['type']} and specversion {event['specversion']}"
    )    

    cloud_event.send_message(broker_address, source, message_type, data)

    # Return 204 - No-content
    return "", 204


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)