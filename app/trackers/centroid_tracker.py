from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
from app.config import MAX_OBJECT_DIST

class CentroidTracker:
    def __init__(self, max_disappearance=3):

        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        self.max_disappearance = max_disappearance

    def register(self, centroid):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        if len(rects) == 0:
            # loop through existing tracked objects and mark them as disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] = 1

                # if reached max_disappearance
                if self.disappeared[objectID] > self.max_disappearance:
                    self.deregister(objectID)

            return self.objects

        # initialize for input centroids for the current frame
        input_centroids = np.zeros((len(rects), 2), dtype="int")

        for (i, (start_x, start_y, end_x, end_y)) in enumerate(rects):
            cX = int((start_x + end_x) / 2.0)
            cY = int((start_y + end_y) / 2.0)
            input_centroids[i] = (cX, cY)

        # if we are not tracking anything atm, register them
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i])
        # otherwise, match with already tracking objects
        else:
            objectIDs = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            #
            D = dist.cdist(np.array(object_centroids), input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            # print(D.min(axis=1))


            usedRows = set()
            usedCols = set()

            for row, col in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue
                if D[row, col] > MAX_OBJECT_DIST:
                    self.register(input_centroids[col])
                    # print(D[row,col])
                    continue
                objectID = objectIDs[row]
                self.objects[objectID] = input_centroids[col]
                self.disappeared[objectID] = 0

                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # any objects has disappeared
            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1

                    if self.disappeared[objectID] > self.max_disappearance:
                        self.deregister(objectID)
            # otherwise, register new objects
            else:
                for col in unusedCols:
                    self.register(input_centroids[col])

        return self.objects
