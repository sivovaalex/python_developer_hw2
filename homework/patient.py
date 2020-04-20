class Patient:
    def __init__(self, *args, **kwargs):
        pass

    def create(*args, **kwargs):
        raise NotImplementedError()

    def save(self):
        pass


class PatientCollection:
    def __init__(self, log_file):
        pass

    def limit(self, n):
        raise NotImplementedError()
