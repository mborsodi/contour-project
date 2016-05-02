import music21
from vis.analyzers.indexers import noterest
import numpy as np
import pprint as pp
import os


def getNotes(piece):

    score = music21.converter.parse(piece)
    notes = noterest.NoteRestIndexer(score).run()
    return notes

def getContour(size, notes):

    notes = [x for x in notes if x != 'Rest']
    contour = []
    contour.append(notes[0])

    if size == 'all':
        size = len(notes)

    for i in range(1, len(notes)):
        if len(contour) < size and notes[i] != contour[len(contour)-1]:
            contour.append(notes[i])

    contour = list(map(music21.note.Note, contour))
    
    return contour


def cont_num(contour):

    cseg = [0] * len(contour)

    for i in range(len(contour)):
        notes = []
        for x in range(len(contour)):
            if (music21.interval.getAbsoluteHigherNote(contour[i], contour[x]) == contour[i]) and (contour[i].nameWithOctave != contour[x].nameWithOctave) and (contour[x].nameWithOctave not in notes):
                notes.append(contour[x].nameWithOctave)
                cseg[i] += 1

    return cseg


def COM_matrix(contour):

    com = []
    for x in contour:
        com.append([])

    for i in range(len(contour)):
        for x in range(len(contour)):
            if contour[i] == contour[x]:
                com[i].append("0")
            elif contour[i] > contour[x]:
                com[i].append("-")
            else:
                com[i].append("+")

    return com


def compare(contour1, contour2):

    count = 0
    l = len(contour1)
    for row in range(l):
        for c1, c2 in zip(contour1[row], contour2[row]):
            if c1 == c2:
                count += 1

    count = (count-l)/2
    total = (l*(l-1))/2
    return count/total


def compare_list(contours):

    total = 0
    for x in len(contours):
        for y in len(contours):
            if x is not y:
                total += compare(contour[x], contour[y])

    return total/len(contours)


def reduce_c(contour, depth):

    def maxc(contour):
        max_list = [0]
        contour = list(map(music21.note.Note, contour))
        for x in range(len(contour)-2):
            if contour[x].nameWithOctave != contour[x+1].nameWithOctave:
                if (music21.interval.getAbsoluteHigherNote(contour[x], contour[x+1]) == contour[x+1] and music21.interval.getAbsoluteHigherNote(contour[x+1], contour[x+2]) == contour[x+1]):
                    max_list.append(x+1)

        max_list.append(len(contour)-1)
        return max_list

    def minc(contour):
        min_list = [0]
        contour = list(map(music21.note.Note, contour))
        for x in range(len(contour)-2):
            if contour[x].nameWithOctave != contour[x+1].nameWithOctave:
                if (music21.interval.getAbsoluteLowerNote(contour[x], contour[x+1]) == contour[x+1] and music21.interval.getAbsoluteLowerNote(contour[x+1], contour[x+2]) == contour[x+1]):
                    min_list.append(x+1)

        min_list.append(len(contour)-1)
        return min_list

    max2 = maxc(contour)
    min2 = minc(contour)
    
    while depth > 1:
        maxcon = [contour[x] for x in max2]
        mincon = [contour[x] for x in min2]
          
        max1 = maxc(maxcon)
        min1 = minc(mincon)
        max2 = [max2[x] for x in max1]
        min2 = [min2[x] for x in min1]
        depth -= 1
     
    max2.extend(min2)
    max2 = list(set(max2))
    max2.sort()
    return [contour[x] for x in max2]


def composers():

    beet = os.listdir('themes/Beethoven')
    if '.DS_Store' in beet:
        beet.remove('.DS_Store')
    moz = os.listdir('themes/Mozart')
    if '.DS_Store' in moz:
        moz.remove('.DS_Store')

    beethoven = []
    mozart = []
    for piece in beet:
        beethoven.extend(os.listdir('themes/Beethoven/' + piece))
    for piece in moz:
        mozart.extend(os.listdir('themes/Mozart/' + piece))

    while '.DS_Store' in beethoven:
        beethoven.remove('.DS_Store')

    while '.DS_Store' in mozart:
        mozart.remove('.DS_Store')

    b = {'name': 'Beethoven', 'files': beethoven}
    m = {'name': 'Mozart', 'files': mozart}
    return (b, m)


def pieces():

    beet = os.listdir('themes/Beethoven')
    while '.DS_Store' in beet:
        beet.remove('.DS_Store')
    moz = os.listdir('themes/Mozart')
    if '.DS_Store' in moz:
        moz.remove('.DS_Store')

    toReturn = []

    for piece in beet:
        files = os.listdir('themes/Beethoven/' + piece)
        if '.DS_Store' in beet:
            files.remove('.DS_Store')
        toReturn.append({'name': piece, 'files': files})

    for piece in moz:
        files = os.listdir('themes/Mozart/' + piece)
        if '.DS_Store' in moz:
            files.remove('.DS_Store')
        toReturn.append({'name': piece, 'files': files})

    return toReturn


composers = composers()
beethoven = composers[0]
mozart = composers[1]

print('beethoven:', len(beethoven['files']))
print('mozart:', len(mozart['files']))

for piece in pieces():
    print(piece['name'])
    print(len(piece['files']))
    















































