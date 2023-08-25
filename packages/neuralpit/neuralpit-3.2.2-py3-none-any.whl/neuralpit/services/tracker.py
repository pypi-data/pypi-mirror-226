import boto3
import time
import json

firehouse = boto3.client('firehose',region_name='ap-southeast-2')

class NeuralPitUsageTracker:

    def __init__(self, stream):
        self._stream = stream

    def trackUsage(self,record):
        firehouse.put_record(
            DeliveryStreamName=self._stream,
            Record={
                'Data': json.dumps(record)
            }
        )

