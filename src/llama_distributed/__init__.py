"""
llama_distributed: A cloud-native distributed query processor for llama_vector shards.

This package orchestrates llama_vector shards with MLX-accelerated collective communication,
using asyncio for concurrency, CRDTs for metadata synchronization, and advanced routing
and optimization capabilities.
"""

from .api import APIHandler
from .balancer import EnergyAwareLoadBalancer
from .client import ShardClient
from .collective import MLXCollective
from .credentials import SecureCredentialManager
from .kubernetes import KubernetesManager
from .metadata import ShardMetadata
from .optimizer import QueryOptimizer
from .processor import DistributedQueryProcessor
from .ranker import FederatedRanker
from .router import NeuralRouter
from .server import Server
from .tee import TEESimulator

__version__ = "0.1.0"
