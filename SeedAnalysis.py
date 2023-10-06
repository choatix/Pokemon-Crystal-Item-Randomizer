import RunCLI


def main():

    cliProcessor = RunCLI.ArgumentParser()

    cliProcessor.seed = None

    #seedFile = "C://Users/Alex/Downloads/SPOILER_roundtournamentmatchoutput.txt"
    seedFile = "C://Users/Alex/Downloads/round6tournamentmatchoutput.txt"
    sFile = open(seedFile)
    lines = sFile.readlines()
    seedLines = [ line.split(":")[1].strip() for line in lines if "numeric seed is" in line and "" in line]
    sFile.close()

    #seedFile = "C://Users/Alex/Downloads/round2tournamentmatchoutput.txt"
    #sFile = open(seedFile)
    #lines = sFile.readlines()
    seedLines2 = []
    #seedLines2 = [line.split(":")[1].strip() for line in lines if "numeric seed is" in line and "" in line]
    #sFile.close()

    for s in seedLines2:
       seedLines.append(s)

    #seedLines = ["283170698874552135158281221494035204284"]

    totalResults = {}

    for seed in seedLines:
        cliProcessor.seednumeric = seed
        cliProcessor.main()
        cliProcessor.PerformChecks()

        check_results = cliProcessor.check_results
        if check_results is not None:
            for key in check_results.keys():
                if key not in totalResults:
                    totalResults[key] = 0

                if check_results[key]:
                    totalResults[key] += 1

    print(totalResults)



if __name__ == '__main__':
    main()