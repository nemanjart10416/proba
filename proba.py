import random,math

number_of_chromosomes = 10


def fitnes_function(x):
    no_blades = x[0]
    length_blades = x[1]
    quality_of_blades = x[2]+x[3]+x[4]+x[5]+x[6]+x[7]+x[8]+x[9]
    fitness_value = (round((no_blades + length_blades) * 12.3 * math.pi) + quality_of_blades)/3
    return fitness_value

def napravi_populaciju(number_of_chromosomes):
    population = []
    for i in range(number_of_chromosomes):
        rand_gene = []
        for j in range(10):
            rand_gene.append(round(random.uniform(-10, 10)))
        obj = {"index":i,"fitness":fitnes_function(rand_gene),"hromozom":rand_gene}
        population.append(obj)
    return population

def fitness_scaling(population):
    #pronalazak najmanjeg indeksa
    min = population[0]["fitness"]
    for i in population:
        if min > i["fitness"]:
            min = i["fitness"]

    if min <= 0:
        for i in range(len(population)):
            population[i]["fitness"]+=abs(min)+1

def sortiraj_populaciju(population):
    for i in population:
        for j in range(len(population)-1):
            if population[j]["fitness"] < population[j+1]["fitness"]:
                pom = population[j]
                population[j] = population[j+1]
                population[j+1] = pom

def normalize_fitnes_values(population):
    fitnes_values=[]
    for i in population:
        fitnes_values.append(i["fitness"])
    normalized_values=[]
    s=sum(fitnes_values)
    j=0
    for i in fitnes_values:
        normalized_values.append(fitnes_values[j]/s)
        j+=1
    return normalized_values

def calculate_cumulative_sums(normalzied_fitness_values):
    cumulative_sums=[]
    for i in normalzied_fitness_values:
        cumulative_sums.append(0)

    for i in range(len(normalzied_fitness_values)):
        for j in range(len(normalzied_fitness_values)):
            if j >= i:
                cumulative_sums[i] = cumulative_sums[i] + normalzied_fitness_values[j]

    return cumulative_sums

def chose_parrents(cumulative_sums):
    parent1=0
    parent2=0

    while parent1==parent2:
        r = random.random()
        for i in range(len(cumulative_sums)):
            if r <= cumulative_sums[i]:
                parent1 = i
        #izbor drugog
        r = random.random()
        for j in range(len(cumulative_sums)):
            if r <= cumulative_sums[j]:
                parent2 = j

    return [parent1,parent2]

def uzmi_odabrane(indexes,population):
    return [population[indexes[0]],population[indexes[1]]]

def status(population,odabrani):
    min=population[0]["fitness"]
    max=population[0]["fitness"]
    for i in population:
        if min > i["fitness"]:
            min = i["fitness"]
        if max < i["fitness"]:
            max = i["fitness"]
    print "odabran1: "+str(odabrani[0])
    print "odabran2: " + str(odabrani[1])
    print "najbolji "+str(max)
    print "najgori "+str(min)

def crossover(parrent1,parrent2):
    dete1={}
    dete2={}
    parrent1_chromozome=parrent1["hromozom"]
    parrent2_chromozome = parrent2["hromozom"]
    probability_of_crossover = 0.5
    #single point or double point crossover
    cross=random.random()

    d1_chromozomi=[]
    d2_chromozomi = []
    if cross < 0.5:#single point crossover
        random_point = random.randrange(0, len(parrent1_chromozome) - 1)
        for i in range(len(parrent1_chromozome)):
            if i <random_point:
                d1_chromozomi.append(parrent1_chromozome[i])
                d2_chromozomi.append(parrent2_chromozome[i])
            else:
                d1_chromozomi.append(parrent2_chromozome[i])
                d2_chromozomi.append(parrent1_chromozome[i])

    else:#double point crossover
        point1 = 0
        point2 = 0
        while point1 == point2:
            point1 = random.randrange(0, len(parrent1_chromozome) - 1)
            point2 = random.randrange(0, len(parrent2_chromozome) - 1)
        minimum = min(point1, point2)
        maximum = max(point1, point2)

        for i in range(len(parrent1_chromozome)):
            if i < minimum:
                d1_chromozomi.append(parrent1_chromozome[i])
                d2_chromozomi.append(parrent2_chromozome[i])
            elif i >= minimum and i < maximum:
                d1_chromozomi.append(parrent2_chromozome[i])
                d2_chromozomi.append(parrent1_chromozome[i])
            else:
                d1_chromozomi.append(parrent1_chromozome[i])
                d2_chromozomi.append(parrent2_chromozome[i])
    dete1 = {"index": -1, "hromozom": d1_chromozomi, "fitness": fitnes_function(d1_chromozomi)}
    dete2 = {"index": -1, "hromozom": d2_chromozomi, "fitness": fitnes_function(d2_chromozomi)}

    return [dete1,dete2]

def selection(original_population):
    population=original_population
    #rresavanje negativnih fitnesa
    fitness_scaling(population)
    #sortiranje populacije
    sortiraj_populaciju(population)
    #normalize fitness values
    normalized_fitness_values=normalize_fitnes_values(population)
    #cumulative sums
    cumulative_sums = calculate_cumulative_sums(normalized_fitness_values)

    novi = []
    #for i in range(len(population)/2):
    for i in range(len(population)/2):
        parrent_indexess = chose_parrents(cumulative_sums)
        odabrani = uzmi_odabrane(parrent_indexess,population)
        #status(population,odabrani)
        i+=1

        deca=crossover(odabrani[0],odabrani[1])
        novi.append(deca[0])
        novi.append(deca[1])

    return novi
    #print "dete 1: "+str(deca[0])
    #print "dete 2: " + str(deca[1])

def izvestaj(population,generacija):
    min=population[0]["fitness"]
    max = population[0]["fitness"]
    for i in population:
        if min > i["fitness"]:
            min = i["fitness"]
        if max < i["fitness"]:
            max = i["fitness"]
    print "generacija "+str(generacija)+" | najbolji: "+str(max)+" | najgori: "+str(min)+" | velicina populacije: "+str(len(population))
    print "-------------------------------------------------------------------------"
    if max > generalno_najbolji["fitness"]:
        generalno_najbolji["fitness"] = max
        generalno_najbolji["generacija"] = generacija
    if min < generalno_najgori["fitness"]:
        generalno_najgori["fitness"] = min
        generalno_najgori["generacija"] = generacija

broj=0
#pravljenje populacije
original_population = napravi_populaciju(number_of_chromosomes)

generalno_najbolji={"fitness":original_population[0]["fitness"],"generacija":0}
generalno_najgori={"fitness":original_population[0]["fitness"],"generacija":0}

for i in range(10):
    izvestaj(original_population,broj)
    original_population=selection(original_population)
    broj+=1

print "----------------------"
print "najbolji: "+str(generalno_najbolji["fitness"])+" iz generacije: "+str(generalno_najbolji["generacija"])
print "najgori: "+str(generalno_najgori["fitness"])+" iz generacije: "+str(generalno_najgori["generacija"])
#selekcija
#selection(original_population)
