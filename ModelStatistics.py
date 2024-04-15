class ModelStatistics:
    def __init__(self, numOfModel, averageF1Score, maxF1Score, maxF1ScoreID, minF1Score, minF1ScoreID, averageNumberOfTrainingImagesPerModel):
        self.numOfModel = numOfModel
        self.averageF1Score = averageF1Score
        self.maxF1Score = maxF1Score
        self.maxF1ScoreID = maxF1ScoreID
        self.minF1Score = minF1Score
        self.minF1ScoreID = minF1ScoreID
        self.averageNumberOfTrainingImagesPerModel = averageNumberOfTrainingImagesPerModel