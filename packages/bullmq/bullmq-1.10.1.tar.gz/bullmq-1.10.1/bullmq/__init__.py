"""
BullMQ

A background job processor and message queue for Python based on Redis.
"""
__version__ = "1.10.1"
__author__ = 'Taskforce.sh Inc.'
__credits__ = 'Taskforce.sh Inc.'

from bullmq.queue import Queue
from bullmq.job import Job
from bullmq.worker import Worker
from bullmq.custom_errors import WaitingChildrenError
