import click
from matplotlib import pyplot as plt
from pythonping import ping
import numpy as np
from rich.console import Console

# https://stackoverflow.com/questions/21981796/cannot-ping-aws-ec2-instance


def plot_latency_graph(latency_data, time_values):
    plt.style.use("seaborn")

    plt.figure(figsize=(10, 5))
    plt.tight_layout()

    plt.plot(time_values, latency_data, linestyle="solid")
    plt.xlabel("Time (in secs)")
    plt.ylabel("Latency (in ms)")

    plt.savefig('network_latency.png')
    plt.show()


# @click.command()
# @click.option('-c', '--count', default=4, help='Number of packets to be sent')
# @click.option('-S', '--segment', help='Number of segments', default=1)
# # @click.option('-s', '--size', help='Packet size for each packet sent', default=32)
# @click.option('-t', '--time', help='Send packets for what period of time (in secs)', default=4)
# # @click.option('-l', '--preload', help='Send number of packets without waiting for a response', default=3)
# @click.argument('host')
# def cli(host: str, count: int, time: int, segment: int):
def cli():
    latency_data = []
    count_data = []
    time_data = []
    host = input("Enter the host: ").strip()
    segment = int(input("Enter the number of segments: "))

    for _ in range(segment):
        count_data.append(
            int(input("Enter the number of packets to be sent: ")))
        time_data.append(int(
            input("Enter the time (in secs) for which packets are to be sent: ")))

    console = Console()
    with console.status("[bold green]Pinging...") as status:
        for count, time in zip(count_data, time_data):
            with open("output.txt", "w") as f:
                ping(host, verbose=True,
                     interval=time / count, count=count, out=f)

            with open("output.txt", "r") as f:
                data = f.read()

                for x in data.split():
                    if "ms" in x:
                        latency_data.append(float(x.replace("ms", "")))
                    if x == "Request":
                        latency_data.append(0)

    print("Latency Data: ", latency_data)
    print("Minimum Latency: ", min(latency_data))
    print("Maximum Latency: ", max(latency_data))
    print("Average Latency: ", round(
        sum(latency_data) / len(latency_data), 2))
    time_values = [round(x, 1) for x in np.arange(
        0, sum(time_data), sum(time_data) / sum(count_data))]
    plot_latency_graph(latency_data, time_values)


if __name__ == '__main__':
    cli()
