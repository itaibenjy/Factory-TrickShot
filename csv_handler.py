import json
import os
import pandas


def matrixToCsv(matrix, level):
    """Recieve a matrix that represents a level and the level number
    and save it in the right place"""
    df = pandas.DataFrame(matrix)
    df.to_csv(os.path.join(
        'levels', f'level_{level}.csv'), index=False, header=False)


def csvMatrixReader(level):
    """Recieve a level and extract the data from the correct csv as a 2D matrix"""
    data = pandas.read_csv(os.path.join(
        'levels', f'level_{level}.csv'), sep=',', header=None)
    matrix = []
    i = 0
    for row in data.iterrows():
        matrix.append([])
        for item in row[1]:
            matrix[i].append(item)
        i += 1
    return matrix


