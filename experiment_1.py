# Experiment #1 - Superposition

import time
import numpy as np
import qiskit 
from qiskit.tools.monitor import job_monitor

qiskit.IBMQ.save_account(open("IBMQ_account_token.txt","r").read())
qiskit.IBMQ.load_account()

provider = qiskit.IBMQ.get_provider("ibm-q")

for backend in provider.backends():
    try:
        qubit_count = len(backend.properties().qubits)
    except:
        qubit_count = "simulated"

    print(f"{backend.name()} has {backend.status().pending_jobs} queued and {qubit_count} qubits")


CIRCUIT_ITERATIONS = 8192 # Seems to be the max shots

backend = provider.get_backend(input("Which backend to use (enter name):"))

Qcircuit = qiskit.QuantumCircuit(1, 1)          # Make a cuircit with 1 QuBit and 1 bit.
Qcircuit.u(np.pi/2, 0, 0, 0)                    # Rotate Q1 to |+⟩.
Qcircuit.measure([0], [0])                      # Measuring the qubit.


# Runnig the actual circuit
job = qiskit.execute(Qcircuit, backend=backend, shots=CIRCUIT_ITERATIONS)
job_monitor(job)


# Grab the generic results from the job.
result = job.result()

# Sieving for the count results.
counts = result.get_counts(Qcircuit)

print(f"""
Job iterated over {CIRCUIT_ITERATIONS} in {result.time_taken} seconds.
With results
{counts}    

""")

# Saving the rapprensetation of the circuit to file.
Qcircuit.draw("mpl", filename='./file.png')

#Generate avg graph of the results.
a = qiskit.visualization.plot_histogram(counts)
a.savefig('avg_results.png')