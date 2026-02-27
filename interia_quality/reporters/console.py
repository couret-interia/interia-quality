"""Console reporter placeholder (currently handled by engine)."""
def report(data):
    """
    Display the given data structure as a raw console output.

    The console reporter is intentionally minimal: formatting is delegated
    to upstream tools or other reporters (HTML, JSON, etc.).
    """
    print(data)
