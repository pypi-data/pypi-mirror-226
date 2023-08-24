"""Module for basic labjack interactions."""
import time

from labjack import ljm


class DaqLabjack:
    """Basic class to use labjack as a data acquisition system (daq)."""

    def __init__(self) -> None:
        """Open connection to labjack."""
        self.handle = ljm.openS("T7", "ANY", "ANY")
        self.counters: dict[str, str] = {}
        self.main_counter: str | None = None

    def read_single_port(self, port_name: str) -> float:
        """Read value from labjack port."""
        value = ljm.eReadName(self.handle, port_name)
        return value

    def read_multiple_ports(self, port_names: list) -> list:
        values = ljm.eReadNames(self.handle, len(port_names), port_names)
        return values

    def add_counter(self, counter_name: str, port_name: str) -> None:
        """Set up counter on a port."""
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        ljm.eWriteName(self.handle, f"{port_name}_EF_INDEX", 8)
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 1)
        print(f"Counter enabled: {port_name}")
        self.counters[counter_name] = port_name

    def remove_counter(self, counter_name: str) -> None:
        """Deactivate counter."""
        port_name = self.counters[counter_name]
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        del self.counters[counter_name]

    def read_single_counter_by_port(self, port_name: str) -> int:
        """Read value from a counter using the name of its port (e.g. DIO2)."""
        count: float = ljm.eReadName(self.handle, f"{port_name}_EF_READ_A")
        count: int = int(count)
        return count

    def read_single_counter_by_name(self, counter_name: str) -> int:
        """Read value from a counter using user-specified name."""
        port_name = self.counters[counter_name]
        count = self.read_single_counter_by_port(port_name)
        return count

    def read_all_counters(self) -> dict:
        """Read all currently configured counters."""
        counter_names = list(self.counters.keys())
        counter_ports = [f"{port}_EF_READ_A" for port in self.counters.values()]
        values = self.read_multiple_ports(counter_ports)
        result = {name: val for name, val in zip(counter_names, values)}
        return result

    def set_main_counter(self, counter_name: str) -> None:
        """Set name of main counter."""
        if counter_name in self.counters.keys():
            self.main_counter = counter_name
        else:
            raise KeyError(f"Counter {counter_name} not added!")

    def block_until_new_count(self, counter_name: str) -> None:
        """Block script advancement until a new count has been registered."""
        last_count = self.read_single_counter_by_name(counter_name)
        while True:
            new_count = self.read_single_counter_by_name(counter_name)
            if new_count != last_count:
                break

    def read_main_counter(self) -> int:
        """Read value of main counter."""
        count = self.read_single_counter_by_name(self.main_counter)
        return count

    def wait_for_main_counter(self) -> None:
        """Hold script until main counter has increased."""
        self.block_until_new_count(self.main_counter)

    def send_ttl(self, port_name: str = "DAC0", duration_ms: float = 1) -> None:
        """Send a simple TTL pulse."""
        ljm.eWriteName(self.handle, port_name, 10)
        time.sleep(duration_ms / 1000)
        ljm.eWriteName(self.handle, port_name, 0)

