utils_module = None


def logger():
    """Use the logger through a dynamic import to avoid circular imports."""
    global utils_module
    if utils_module is None:
        import src.utils as utils_module
    return utils_module.logger
