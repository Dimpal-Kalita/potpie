import time
import asyncio
import logging
from typing import Optional

# Global variables for rate limiting api API calls
API_COOLDOWN_SECONDS = 0.0
last_api_call_timestamp: Optional[float] = None


async def check_and_wait_for_cooldown() -> None:
    """
    Check if we need to wait before making another API call.
    """
    global last_api_call_timestamp, API_COOLDOWN_SECONDS


    current_time = time.time()

    if last_api_call_timestamp is not None:
        elapsed = current_time - last_api_call_timestamp
        if elapsed < API_COOLDOWN_SECONDS:
            wait_time = API_COOLDOWN_SECONDS - elapsed
            logging.info(f"Rate limiting api API call, waiting {wait_time:.2f} seconds")
            await asyncio.sleep(wait_time)

    # Update timestamp after waiting
    last_api_call_timestamp = time.time()


async def set_cooldown_duration(seconds: float) -> dict:
    """
    Set the cooldown duration between API calls.

    Args:
        seconds: The new cooldown duration in seconds

    Returns:
        A dictionary with a success message
    """
    global API_COOLDOWN_SECONDS

    if seconds < 0:
        raise ValueError("Cooldown duration cannot be negative")

    API_COOLDOWN_SECONDS = seconds
    return {"message": f"api API cooldown set to {seconds} seconds"}


async def get_cooldown_duration() -> dict:
    """
    Get the current cooldown duration between API calls.

    Returns:
        A dictionary with the current cooldown duration
    """
    global API_COOLDOWN_SECONDS
    return {"cooldown_seconds": API_COOLDOWN_SECONDS}