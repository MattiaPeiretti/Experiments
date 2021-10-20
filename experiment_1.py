# Experiment #1 - Superposition
import csv
import numpy as np
import qiskit
from qiskit.tools.monitor import job_monitor

# Constants ----
IBMQ_BACKEND = "ibmq_armonk"
SHOTS_PER_JOB = 8192  # Max allowed amount of shots allowed by the backend
JOB_ITERATIONS = 10
NAME = "EXP1SUPPOS"


def setup_provider(backend):
    qiskit.IBMQ.save_account(open("IBMQ_account_token.txt", "r").read())
    qiskit.IBMQ.load_account()
    provider = qiskit.IBMQ.get_provider("ibm-q")
    return provider.get_backend(backend)


def build_circuit():
    qc = qiskit.QuantumCircuit(1, 1)  # Make a circuit with 1 QuBit and 1 bit.
    qc.u(np.pi / 2, 0, 0, 0)  # Rotate Q1 to |+⟩.
    qc.measure([0], [0])  # Measuring the qubit.
    # Saving the representation of the circuit to file.
    qc.draw("mpl", filename="./file.png")
    return qc


def generate_job_avg_graph(counts, filename):
    # Generate avg graph of the results.
    file = qiskit.visualization.plot_histogram(counts)
    file.savefig(filename)


def save_data_in_spreadsheet(data):
    header = [
        "Experiment",
        "Run",
        "Shots",
        "Timing",
        "Backend",
        "Results 1",
        "Results 0",
        "Graph file",
    ]
    with open(f"{NAME}_SHOTS{SHOTS_PER_JOB}_{IBMQ_BACKEND}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def main():
    backend = setup_provider(IBMQ_BACKEND)
    quantum_circuit = build_circuit()
    data = []
    for x in range(0, JOB_ITERATIONS):
        # Running the actual circuit
        job = qiskit.execute(quantum_circuit, backend=backend, shots=SHOTS_PER_JOB)
        job_monitor(job)

        # Grab the generic results from the job.
        result = job.result()

        # Sieving for the count results.
        counts = result.get_counts(quantum_circuit)

        print(
            f"""
        run, iterations, elapsed time, results, IBMQ Backend.
        {x}, {SHOTS_PER_JOB}, {result.time_taken} seconds, {counts}, {IBMQ_BACKEND}
        """
        )
        graph_filename = f"{NAME}_RUN{x}_SHOTS{SHOTS_PER_JOB}_{IBMQ_BACKEND}.png"
        generate_job_avg_graph(counts, graph_filename)
        data.append(
            [
                NAME,
                x,
                SHOTS_PER_JOB,
                result.time_taken,
                IBMQ_BACKEND,
                counts["1"],
                counts["0"],
                graph_filename,
            ]
        )
    save_data_in_spreadsheet(data)


if __name__ == "__main__":
    main()
