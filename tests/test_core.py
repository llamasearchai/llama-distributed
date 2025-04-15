"""Tests for the llama-distributed package (Celery tasks)."""

import os

import pytest

# Try importing the package and tasks
try:
    import llama_distributed
    from llama_distributed.celery_app import app as celery_app
    from llama_distributed.tasks import add, debug_task, process_data
except ImportError as e:
    pytest.fail(f"Failed to import llama_distributed components: {e}", pytrace=False)

# Check if Redis is likely available (based on environment variable set in CI)
# Skip integration tests if Redis URL is not set
REDIS_URL = os.environ.get("LLAMA_CELERY_REDIS_URL")
pytestmark = pytest.mark.skipif(
    not REDIS_URL,
    reason="LLAMA_CELERY_REDIS_URL env var not set, skipping Celery integration tests",
)


# Configure Celery for testing (use testing mode)
@pytest.fixture(scope="session", autouse=True)
def setup_celery_for_testing():
    celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
    # task_always_eager=True runs tasks locally, synchronously
    # task_eager_propagates=True propagates exceptions from tasks


def test_import():
    """Test that the main package can be imported."""
    assert llama_distributed is not None


def test_version():
    """Test that the package has a version attribute."""
    assert hasattr(llama_distributed, "__version__")
    assert isinstance(llama_distributed.__version__, str)


def test_add_task():
    """Test the add task executes correctly."""
    result = add.delay(5, 3)  # .delay() runs synchronously due to task_always_eager
    assert result.state == "SUCCESS"
    assert result.result == 8


def test_process_data_task():
    """Test the process_data task executes and returns expected string."""
    data_id = "test-id-123"
    result = process_data.delay(data_id)
    assert result.state == "SUCCESS"
    assert data_id in result.result
    assert "Successfully processed" in result.result


def test_debug_task(capsys):
    """Test the debug task executes and prints request info."""
    result = debug_task.delay()
    captured = capsys.readouterr()
    assert result.state == "SUCCESS"
    assert "Request:" in captured.out
    assert "debug_task" in captured.out  # Check if task name is in the request repr


# Add more tests later:
# - Test tasks that depend on other Llama components (using mocks)
# - Test error handling within tasks
# - Test task routing if specific queues are used
# - Test task retries

# If you want to run the tests, you can use the following command:
# pytest tests/test_core.py

# If you want to run the tests with coverage, you can use the following command:
# pytest --cov=llama_distributed tests/test_core.py
