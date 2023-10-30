import random
from qiskit import QuantumCircuit, Aer, execute

def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 'x':
        qc.h(0)
    return qc

def measure_qubit(qc, basis):
    if basis == 'x':
        qc.h(0)
    qc.measure(0, 0)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1, memory=True)
    result = job.result()
    return int(result.get_memory()[0])

def generate_random_number():
    num_bits = 100
    seven_digit_binary = 24  # We need at least 24 bits for a 7-digit number.
    
    alice_bits = [random.choice([0, 1]) for _ in range(num_bits)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]
    bob_bases = [random.choice(['+', 'x']) for _ in range(num_bits)]

    alice_qubits = [prepare_qubit(alice_bits[i], alice_bases[i]) for i in range(num_bits)]

    bob_results = [measure_qubit(alice_qubits[i], bob_bases[i]) for i in range(num_bits)]

    matching_bases_indices = [i for i in range(num_bits) if alice_bases[i] == bob_bases[i]]

    key = []
    for i in matching_bases_indices:
        key.append(bob_results[i])
        if len(key) == seven_digit_binary:  # Stop once we have enough bits.
            break

    binary_key_str = ''.join([str(bit) for bit in key])
    random_number = int(binary_key_str, 2)

    random_number_str = str(random_number)
    if len(random_number_str) > 7:
        random_number_str = random_number_str[:7]
    elif len(random_number_str) < 7:
        random_number_str = random_number_str.zfill(7)

    return int(random_number_str)

if __name__ == '__main__':
    random_number = generate_random_number()
    print("Your ", random_number)
