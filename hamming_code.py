import numpy as np

class HammingCode:
    def __init__(self, m):
        self.m = m
        self.n = 2 ** m - 1
        self.r = m
        self.generator_matrix = self.get_generator_matrix()
        self.check_matrix = self.get_check_matrix()

    def get_generator_matrix(self):
        # Erstellung der Identitätsmatrix
        I = np.identity(self.n - self.r, dtype=int)
        # Erstellung der Paritätsmatrix
        P = np.array([list(np.binary_repr(i, width=self.r)) for i in range(1, self.n - self.r + 1)], dtype=int)
        return np.concatenate((I, P), axis=1)

    def get_check_matrix(self):
        # Erstellung der Paritätsmatrix
        P = np.array([list(np.binary_repr(i, width=self.r)) for i in range(1, self.n - self.r + 1)], dtype=int)
        # Erstellung der Identitätsmatrix
        I = np.identity(self.r, dtype=int)
        return np.concatenate((P.T, I), axis=1)

    def encode(self, word):
        # Umwandlung des Wortes in einen Vektor
        word_vec = np.array([int(bit) for bit in word])
        # Codierung
        return np.dot(word_vec, self.generator_matrix) % 2

    def decode(self, codeword):
        # Berechnung des Syndroms
        syndrome = np.dot(codeword, self.check_matrix.T) % 2
        if np.count_nonzero(syndrome) == 0:
            return codeword[:self.n - self.r]
        else:
            # Fehlerkorrektur (vereinfacht, funktioniert nur für einzelne Fehler)
            error_position = int(''.join(map(str, syndrome)), 2) - 1
            corrected_codeword = codeword.copy()
            corrected_codeword[error_position] ^= 1
            return corrected_codeword[:self.n - self.r]

    def check(self, codeword):
        # Berechnung des Syndroms
        syndrome = np.dot(codeword, self.check_matrix.T) % 2
        return np.count_nonzero(syndrome) == 0

# Beispielgebrauch
hamming = HammingCode(3)  # für ein m = 3
print("Generatormatrix:\n", hamming.get_generator_matrix())
print("Prüfmatrix:\n", hamming.get_check_matrix())

# Codewort erzeugen
word = '1101'
codewort = hamming.encode(word)
print("Codewort:", codewort)

# Decodieren
#decoded = hamming.decode(codewort)
#print("Decodiertes Wort:", decoded)

# Überprüfung
#valid = hamming.check(codewort)
#print("Ist das Codewort gültig?", valid)

# Einführung eines Fehlers im Codewort
fehlerhaftes_codewort = codewort.copy()
fehlerhaftes_codewort[2] ^= 1  # Umkehrung des Bits an Position 2

# Decodierung und Korrektur des fehlerhaften Codeworts
korrigiertes_codewort = hamming.decode(fehlerhaftes_codewort)
print("Korrigiertes Codewort:", korrigiertes_codewort)
