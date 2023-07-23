# """
# This module defines API client singletons and guard-functions.
# """

# import os
# import logging
# import grpc

# from google.cloud import ndb
# from google.cloud import tasks
# from google.cloud.tasks_v2.services.cloud_tasks.transports.grpc import (
#     CloudTasksGrpcTransport,
# )

# from google.cloud import pubsub_v1 as pubsub

# # from google.cloud.pubsub_v1 import PushConfig
# from google.pubsub_v1 import PushConfig

# logger = logging.getLogger(__name__)

# _client_ndb = None
# _client_cloudtasks = None
# _client_pubsub_publisher = None
# _client_pubsub_subscriber = None


# def get_client_datastore():
#     """Create/Retrieve the singleton ndb client instance.

#     Returns:
#         ndb.Client: The NDB client object.
#     """

#     global _client_ndb

#     if not _client_ndb:
#         _client_ndb = ndb.Client()

#     return _client_ndb


# def get_client_cloudtasks():
#     """Create/Retrieve the singleton Cloud Tasks client instance.

#     Returns:
#         tasks.CloudTasksClient: The Cloud Tasks client object.
#     """

#     global _client_cloudtasks

#     if not _client_cloudtasks:

#         logger.info("Initiating Cloud Tasks client")

#         # Use insecure connection when using Datastore Emulator, otherwise
#         # use secure connection
#         emulator = bool(os.getenv("CLOUDTASKS_EMULATOR_HOST"))

#         if emulator:
#             logger.warning("Using Cloud Tasks emulator")
#             channel = grpc.insecure_channel(os.getenv("CLOUDTASKS_EMULATOR_HOST"))
#             transport = CloudTasksGrpcTransport(channel=channel)
#             _client_cloudtasks = tasks.CloudTasksClient(transport=transport)
#         else:
#             _client_cloudtasks = tasks.CloudTasksClient()

#     return _client_cloudtasks


# def get_client_pubsub_subscriber() -> pubsub.SubscriberClient:
#     """Retrieve a Cloud PubSub subscriber client singleton (potentially by first instantiating it).

#     Returns:
#         pubsub.SubscriberClient: Cloud PubSub subscriber client.
#     """

#     global _client_pubsub_subscriber

#     if not _client_pubsub_subscriber:
#         _client_pubsub_subscriber = pubsub.SubscriberClient()

#     return _client_pubsub_subscriber


# def get_client_pubsub_publisher() -> pubsub.PublisherClient:
#     """Retrieve a Cloud PubSub publisher client singleton (potentially by first instantiating it).

#     Returns:
#         pubsub.PublisherClient: Cloud PubSub publisher client.
#     """

#     global _client_pubsub_publisher

#     if not _client_pubsub_publisher:
#         _client_pubsub_publisher = pubsub.PublisherClient()

#     return _client_pubsub_publisher


# def create_subscription_push_config(endpoint: str) -> PushConfig:
#     return PushConfig(push_endpoint=endpoint)
