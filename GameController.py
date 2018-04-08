import ReadScreen
import keyboard
import time
import numpy as np


def generateindividual(size):
    individual = []
    for i in range(int(size)):
        tmp = np.random.random()
        if tmp < 0.5:
            individual.append(-1)
        else:
            individual.append(1)
    return individual


def generatepopulation(size, maxindividualsize):
    population = []
    for i in range(size):
        population.append(generateindividual(maxindividualsize))
    return population


def breed(population, expectedlenght):
    while len(population) < expectedlenght:
        alfaparrent = int(np.random.random() * len(population))
        betaparrent = int(np.random.random() * len(population))
        while alfaparrent == betaparrent:
            betaparrent = int(np.random.random() * len(population))
        alfa = int(np.random.random() * len(population[alfaparrent]))
        beta = int(np.random.random() * len(population[betaparrent]))
        while beta < alfa:
            beta = int(np.random.random() * len(population[betaparrent]))
        child = []
        crossover = np.random.random()
        if crossover < 0.5:
            for i in range(alfa):
                child.append(population[alfaparrent][i])
            for i in range(alfa, len(population[betaparrent])):
                child.append(population[betaparrent][i])
        else:
            for i in range(alfa):
                child.append(population[alfaparrent][i])
            for i in range(alfa, beta):
                child.append(population[betaparrent][i])
            for i in range(beta, len(population[betaparrent])):
                child.append(population[alfaparrent][i])
        population.append(child)
    return population


def mutate(population):
    individualselect = int(np.random.random() * len(population))
    select = int(np.random.random() * len(population[individualselect]))
    if population[individualselect][select] == 1:
        population[individualselect][select] = -1
    else:
        population[individualselect][select] = 1
    return population


def generatenextpopulation(population, fitnesses):
    Survivors = []
    fitnesses, population = zip(*sorted(zip(fitnesses, population)))
    population = list(population)
    # sorts population based on fitnesses
    while len(Survivors) < len(fitnesses) * 0.4:
        summ = 0
        for index, individual in enumerate(population):
            summ += (index + 1)
        Chances = [0] * len(population)
        for x in range(len(population)):
            Chances[x] = (x + 1) / summ
        LuckyNumber = np.random.random()
        # LuckyNumber is a number between 0 and 1 that chooses the survivors
        Luck = Chances[0]
        i = 0
        while LuckyNumber > Luck:
            i += 1
            Luck += Chances[i]
        Survivors.append(population[i])
        del population[i]
        # deletes the Survived individual so it
        # won't be selected again in the future
    population = Survivors
    population = breed(population, 5)
    mutationrate = 0.6
    mutationchance = np.random.random()
    while mutationchance < mutationrate:
        population = mutate(population)
        mutationchance = np.random.random()
    return population


def generatesolution(solution):
    moves = []
    if solution < 0:
        for i in range(int(abs(solution))):
            moves.append(-1)
    elif solution > 0:
        for i in range(int(abs(solution))):
            moves.append(1)
    return moves


def main():
    Height, Width = ReadScreen.findscreen()
    solutions = []
    maxscore = 0
    lifeloss = False
    testing = False
    testrun = 0
    while maxscore < 10:
        if ReadScreen.screenconfirm(Height, Width):
            population = generatepopulation(5, 15)
            ballfind = False
            generation = 0
            print('Max Score Gained: ', maxscore)
            while not ballfind:
                fitnesses = []
                p = 0
                print('Generation: ', generation)
                while p < len(population) and not ballfind:
                    gamerunning = False
                    if len(solutions) > 0 and lifeloss:
                        if not testing:
                            for index, solution in enumerate(solutions):
                                keyboard.press('space')
                                gamerunning = True
                                time.sleep(0.05)
                                keyboard.release('space')
                                moves = generatesolution(solution)
                                print(index, '  ', moves)
                                for i in moves:
                                    if i == 1:
                                        keyboard.press('right')
                                        time.sleep(0.05)
                                        keyboard.release('right')
                                    else:
                                        keyboard.press('left')
                                        time.sleep(0.05)
                                        keyboard.release('left')
                                time.sleep(3.35)
                        testrun = 0
                        accept = 0
                        while testing and testrun < 3:
                            print('Testing new solution...')
                            for index, solution in enumerate(solutions):
                                keyboard.press('space')
                                gamerunning = True
                                time.sleep(0.05)
                                keyboard.release('space')
                                moves = generatesolution(solution)
                                print(index, '  ', moves)
                                for i in moves:
                                    if i == 1:
                                        keyboard.press('right')
                                        time.sleep(0.05)
                                        keyboard.release('right')
                                    else:
                                        keyboard.press('left')
                                        time.sleep(0.05)
                                        keyboard.release('left')
                                time.sleep(3.35)
                            testrun += 1
                            _, _, _, score, _, _ = ReadScreen.main(Height, Width)
                            print('Solution score: ', score)
                            time.sleep(5)
                            if score >= len(solutions):
                                accept += 1
                            if accept == 2:
                                testing = False
                                print("Solution accepted")
                            lifeloss = True
                        if testrun == 3 and testing:
                            print("Solution deleted!")
                            del solutions[len(solutions) - 1]
                            maxscore -= 1
                            testing = False
                    if testrun == 0:
                        ballfind = False
                        individual = population[p]
                        # print(sum(population[p]))
                        for i in individual:
                            if i == 1:
                                keyboard.press('right')
                                time.sleep(0.05)
                                keyboard.release('right')
                            else:
                                keyboard.press('left')
                                time.sleep(0.05)
                                keyboard.release('left')
                        keyboard.press('space')
                        gamerunning = True
                        time.sleep(0.05)
                        keyboard.release('space')
                        #if len(solutions) != 0:
                        time.sleep(0.40)
                        if ReadScreen.screenconfirm(Height, Width):
                            fitness, lifeloss, ballfind, score, scoregain, scoreloss = ReadScreen.main(Height, Width)
                            if lifeloss:
                                print('Fitness: ', fitness)
                                fitnesses.append(fitness)
                        else:
                            fitnesses.append(-1)
                            Height, Width = ReadScreen.findscreen()
                        p += 1
                if fitness != 100 and testrun == 0:
                    population = generatenextpopulation(population, fitnesses)
                    generation += 1
                elif fitness == 100 and testrun == 0:
                    maxscore += 1
                    print('New score: ', maxscore)
                    solutions.append(sum(population[p - 1]))
                    testing = True
                    _, lifeloss, _, _, scoregain, scoreloss = ReadScreen.main(Height, Width)
                    iteration = 0
                    while not lifeloss and iteration < 5:
                        # waits for the ball to go out for synchronization purposes
                        _, lifeloss, _, _, _, _ = ReadScreen.main(Height, Width)
                        iteration += 1
                    print(solutions)
                testrun = 0
        else:
            Height, Width = ReadScreen.findscreen()


if __name__ == '__main__':
    main()
