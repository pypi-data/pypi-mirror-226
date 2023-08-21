import socket

from jinja2_simple_tags import StandaloneTag


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def get_free_port(starting_port, max_port=None) -> int:
    port = starting_port
    while is_port_in_use(port):
        port += 1
        if max_port and port > max_port:
            raise RuntimeError("No free ports available")
    return str(port)


class GetFreePort(StandaloneTag):
    tags = {"get_free_port"}

    def render(self, starting_port: int, max_port: int = None):
        return get_free_port(starting_port, max_port)
