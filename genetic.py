import random
import statistics
import time
import sys
from deck_v2 import Deck

def _generate_parent(length, geneSet, tokens, get_fitness):
    # length = 60
    # geneSet = decklist, but as a set
    # get_fitness = the sim, where fitness == number of triggers
    genes = []
    for card in geneSet:
        if 'Mountain' in card['name']:
            genes = [card,] * length
            break
    #genes = ''.join(genes) # I want the genes to be an array, not a string.
    parent = Deck(genes, tokens)
    print(f"The parent deck is: {parent.get_human_names(parent._deck_list)}")
    fitness = get_fitness(parent)
    return Chromosome(parent._deck_list, fitness)


def _mutate(parent, geneSet, tokens, get_fitness, num_mutations):
    childGenes = list(parent.Genes)
    index = random.randrange(0, len(parent.Genes))
    mutated = 0
    mutation_attempts = 0
    while mutated < num_mutations:
        mutation_attempts += 1
        if mutation_attempts >= 1000: 
            print("Mutation attempts exceeded 1000. Exiting.")
            sys.exit()
        newGene = random.choice(geneSet)
        # newGene is a card.
        #print(f"The gene we are trying to mutate into: {newGene['name']}")
        less_than_four = True
        if not 'Mountain' in newGene['name'] and childGenes.count(newGene) >= 4:
            less_than_four = False

        if childGenes[index] != newGene and less_than_four:
            mutated += 1
            childGenes[index] = newGene
            #print(f"Replace {childGenes[index]['name']} with {newGene['name']}")
    child = Deck(childGenes, tokens)
    fitness = get_fitness(child)
    return Chromosome(child._deck_list, fitness)


def get_best(get_fitness, targetLen, optimalFitness, geneSet, tokens, display):
    # get_fitness : the sim, where fitness == number of triggers
    # targetLen : 60
    # optimalFitness : the maxiumum number of triggers? Or 20?
    # geneSet : decklist, but as a set
    # display : the print function
    generation = 0
    failed_mutations = 0
    random.seed()
    bestParent = _generate_parent(targetLen, geneSet, tokens, get_fitness)
    display(bestParent)
    if bestParent.Fitness >= optimalFitness:
        return bestParent
    while True:
        if failed_mutations % 10 == 0:
            print(f"\rChild number {failed_mutations}...", end="")
        if failed_mutations > 100000:
            print("\n\nFailed mutations exceeded 10000. Exiting.")
            print(f"Total generations: {generation}")
            display(bestParent)
            sys.exit()
        child = _mutate(bestParent, geneSet, tokens, get_fitness, random.randint(0,1)+random.randint(0,1)+random.randint(0,1))
        if bestParent.Fitness >= child.Fitness:
            failed_mutations += 1
            continue
        display(child)
        generation += 1
        failed_mutations = 0
        if child.Fitness >= optimalFitness:
            print(f"Total generations: {generation}")
            return child
        bestParent = child


class Chromosome:
    Genes = None # The deck-list. Not the DECK.
    Fitness = None
    
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{0} {1:3.2f} {2:3.2f}".format(1 + i, mean, statistics.stdev(timings, mean) if i > 1 else 0))