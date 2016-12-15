import math
from scipy.special import comb
from decimal import *


# !!!!!!!!!!!!!!
# answer: n0 is 24
# !!!!!!!!!!!!!!


probabilities = [Decimal(2/3), Decimal(1/3)]
ballsCounts = [5, 10, 100, 500, 1000, 2000]
epsilons = [Decimal(0.128), Decimal(0.138), Decimal(0.147)]


def calcEntropy():
    entropy = Decimal(0)
    for probability in probabilities:
        entropy += -probability * probability.ln() / Decimal(2).ln()
    return entropy


def calcSequencesCountByWhiteBallsCount(ballsCount, whiteBallsCount):
    return comb(ballsCount, whiteBallsCount, True)


def calcSummarizedProbability(sequencesCountByWhiteBallsCount, whiteBallsCount, ballsCount):
    whiteBallProbability = probabilities[0]
    return sequencesCountByWhiteBallsCount * (whiteBallProbability ** whiteBallsCount) * ((1 - whiteBallProbability) ** (ballsCount - whiteBallsCount))


def isTypical(entropy, e, ballsCount, sequencesCountByWhiteBallsCount, summarizedProbability):
    return 2**(-ballsCount*(entropy + e)) <= summarizedProbability/sequencesCountByWhiteBallsCount <= 2**(-ballsCount*(entropy - e))


def isCorrect(ballsCount, entropy, e, eSequencesCount):
    return (1 - e) * 2**(ballsCount*(entropy - e)) <= eSequencesCount <= 2**(ballsCount*(entropy + e))


def calcSequencesCountAndItsProbabilities(e, ballsCount, entropy):
    eSequencesCount = Decimal(0)
    eSequencesTotalProbability = Decimal(0)
    for whiteBallsCount in range(ballsCount + 1):
        whiteBallsCount = Decimal(whiteBallsCount)
        sequencesCountByWhiteBallsCount = calcSequencesCountByWhiteBallsCount(ballsCount, whiteBallsCount)  
        summarizedProbability = calcSummarizedProbability(sequencesCountByWhiteBallsCount, whiteBallsCount, ballsCount)
        typical = isTypical(entropy, e, ballsCount, sequencesCountByWhiteBallsCount, summarizedProbability)
        if (typical):
            eSequencesCount += sequencesCountByWhiteBallsCount
            eSequencesTotalProbability += summarizedProbability
    return eSequencesCount, eSequencesTotalProbability


def calcStatistics():
    entropy = calcEntropy()
    print('entropy: ' + str(entropy))

    for e in epsilons:
	    for ballsCount in ballsCounts:
	        print('ballsCount: ' + str(ballsCount))
	        print('epsilon: ' + str(e))

	        sequencesCount =  2**ballsCount
	        print('sequencesCount: ' + str(sequencesCount))

	        eSequencesCount, eSequencesTotalProbability = calcSequencesCountAndItsProbabilities(e, ballsCount, entropy)

	        print('eSequencesCount: ' + str(eSequencesCount))
	        print('eSequencesTotalProbability: ' + str(eSequencesTotalProbability))
	        eSequencesCountProportion = eSequencesCount / sequencesCount
	        print('eSequencesCountProportion: ' + str(eSequencesCountProportion))
	        correct = isCorrect(ballsCount, entropy, e, eSequencesCount)
	        print('correct: ' + str(correct))
	        print('eSequencesTotalProbability > 1 - e: ' + str(eSequencesTotalProbability > 1 - e))


def findMinBallsCount():
    entropy = calcEntropy()
    print('entropy: ' + str(entropy))

    e = epsilons[1]

    ballsCount = 10
    toStop = False

    while not toStop:
        print('ballsCount: ' + str(ballsCount))

        sequencesCount =  2**ballsCount
        print('sequencesCount: ' + str(sequencesCount))

        eSequencesCount, eSequencesTotalProbability = calcSequencesCountAndItsProbabilities(e, ballsCount, entropy)

        print('eSequencesCount: ' + str(eSequencesCount))
        print('eSequencesTotalProbability: ' + str(eSequencesTotalProbability))

        toStop = eSequencesTotalProbability > 1 - e
        print('toStop: ' + str(toStop))
        if toStop:
            break

        ballsCount += 1


def main():
    calcStatistics()
    findMinBallsCount()


if __name__ == '__main__':
    main()