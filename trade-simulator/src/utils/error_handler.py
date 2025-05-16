def handle_error(error):
    """Handles exceptions and logs error messages."""
    import logging

    logging.error(f"An error occurred: {str(error)}")
    # Additional error handling logic can be added here

def raise_custom_error(message):
    """Raises a custom exception with a given message."""
    raise Exception(message)