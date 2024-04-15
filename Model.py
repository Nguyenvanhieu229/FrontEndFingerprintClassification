class Model:
    def __init__(self, id=None, trainingDate=None, accuracy=0, precision=0, recall=0, f1_score=0, state="inactive", path="default", creationManager = None):
        self.id = id
        self.trainingDate = trainingDate
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score
        self.state = state
        self.path = path
        self.creationManager = creationManager

