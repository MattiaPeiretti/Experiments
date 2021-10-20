import qiskit


def list_backends():
    qiskit.IBMQ.save_account(open("IBMQ_account_token.txt", "r").read())
    qiskit.IBMQ.load_account()

    provider = qiskit.IBMQ.get_provider("ibm-q")

    for backend in provider.backends():
        try:
            qubit_count = len(backend.properties().qubits)
        except:
            qubit_count = "simulated"

        print(
            f"{backend.name()} has {backend.status().pending_jobs} queued and {qubit_count} qubits"
        )


if __name__ == "__main__":
    list_backends()
