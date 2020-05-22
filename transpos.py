import math
import random


msg = '''etmhbnboiagoriendvrmaokaswciroredudtiudrnlagyhingtvnoobesmetirxnetetahheatstcaqkuodornincsisotnhfgttinreapelsnlesiiptonottogwrsucpeahamnkwiguotronhsnaetterwgtchsiphaapdreebthoeoetnkrdshpryoeotwriastaotnnnhderietaaptltnethiermsltetehoetaesttahtkascwtnaorfeoenesnwoirantsirtpecdteeabcyieorvnrladflaoetthakatcgirnaacirsfmtehteoeatvrnuerfemdretohsmoisynieieewtesnstsesaatthntrittmeintletdocuvcaoeeprpeaordsdtiprhuttetactuakhtbtaermjyiottoefhlxepiossvoaerduintyrhtnteosdrweprdoptweiehhvrhiygcaacuocryhniteatnrptnelntaotltywhooternetisohhtoterwpeasottnniahdetefirncosreutdrucwtrhietosttowhdesofrtetohsalsahtutoesbmifbadldetaaomtgrehueebtiuldrteemieuercltyoslscfiaiialtonydnusrectwookesfyahvtwwaeeerropcrtdteetbsyheeevtnesooyrseffriconrcecdotrnebeeaowhvoeehvroetprwaepinltethslbafsnemedeaagndhadsitsoercndaditopnhnleaaterihsstoeipslbsiyiattuthonrieehemseaevasngtrwnokigiwitthndiincissunisotwfihcfoilirasdofmaiheliecmesrtnpoguhibtanesecdeeihddttafthiaectlhiylosuedubsothdewsnxntiitgksofscoahweveaytnroadstpausyimodhrdxiieblwlhepsitepdhortebliaaorrtsioedannmauafucntragiflciiiietsenagrfnmyfotrurhrerehninmcentxadrpeeeiamnottiinngvetehsrfikclooeailsaopnwgieenlwldesetniogiinfcytalhecnaeensrcyuirftoitphsaeorotiinlnfawlhyelosuodtnttheaetthakatclkdiletewynetornnogwneivcaiiislaitnhsslivbuaaplperaaoganddaronueasgneatridtonihgeerhbseetrdalnidonntonnorseuhettanhtewoirepagnuotplniaodusnentrawdishosotabflmtoersheeelendseasdsteh'''

qg = open('qgrams.txt', 'r')
qg = qg.readlines()
for n in range(len(qg)):
    qg[n] = qg[n].split()
qg = dict(qg)


def transpositionSolve(message):
    def score(string):
        string = string.upper()
        global qg
        s = 0
        for n in range(len(string) - 3):
            snip = string[n:n + 4]
            try:
                s += math.log10(int(qg[snip]))
            except KeyError:
                s += math.log10(0.5)
        return s

    def key_score(k):
        text = reArrange(k)
        return score(text)

    def reArrange(k):
        blocks = [message[x:x + keylength] for x in range(0, len(message), keylength)]
        for n, b in enumerate(blocks):
            if not len(b) < keylength:
                c = ''
                for count in k:
                    c += b[count]
                    blocks[n] = c
        return ''.join(blocks)

    def permute(k, n, keylength, pOfSplice=0.5):
        v2 = k[:]
        for _ in range(random.randint(0, n)):
            flip = random.random()
            if flip > pOfSplice:
                a = random.randint(0, keylength - 1)
                b = random.randint(0, keylength - 1)
                v2[a], v2[b] = v2[b], v2[a]
            else:
                while True:
                    # repeat until random selects a valid splice
                    a = random.randint(0, keylength - 1)
                    b = random.randint(0, keylength - 1)
                    if a < b:
                        splice = v2[a:b]
                        return random.choice(
                            [v2[0:a] + splice + v2[b:], splice + v2[0:a] + v2[b:], v2[0:a] + v2[b:] + splice])
        return v2

    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len([x for x in message if x.upper() in alphabet])
    print('Message length:', length)
    keylength = int(input('Keylength to try?'))
    randomnessBaseline = 4
    randomnessEndpoint = 20
    populationSize = 100
    key = list(range(keylength))
    population = []
    for _ in range(99):
        random.shuffle(key)
        population.append(key)
    gen_Number = 0
    previousBest = 0
    timeSincePreviousBest = 0
    rateOfRandomnessIncrease = 7  # lower is faster
    randomness = randomnessBaseline
    pOfSlice = 0.5
    print('Beginning Solve, with parameters:')
    print('Population Size:', populationSize)
    print('Baseline permutations:', randomnessBaseline)
    print('Generations to increase randomness:', rateOfRandomnessIncrease)
    print('Endpoint generations without improvement:', randomnessEndpoint)
    print()
    print('Press the button again at any time to end the solve.')
    while True:
        population = population + [permute(x, randomness, keylength, pOfSplice=pOfSlice) for x in population]
        population.sort(reverse=True, key=key_score)
        population = population[0:populationSize]

        print('Gen', gen_Number,
              reArrange(population[0])[0:20], 'r', randomness, 'score',
              int(key_score(population[0])), 'key',
              '.'.join([str(x) for x in population[0]]))

        gen_Number += 1
        if previousBest == key_score(population[0]):
            timeSincePreviousBest += 1
            if timeSincePreviousBest > rateOfRandomnessIncrease:
                randomness += 1
                timeSincePreviousBest = 0
        else:
            previousBest = key_score(population[0])
            randomness = randomnessBaseline

        if randomness > randomnessEndpoint:
            print('Best Guess:')
            print('Key:', '.'.join([str(x) for x in population[0]]))
            print()
            print(reArrange(population[0]))
            return reArrange(population[0])


transpositionSolve(msg)
