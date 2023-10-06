import RunCLI
import Gym

cliProcessor = RunCLI.ArgumentParser()
cliProcessor.mode = "Modes/Custom/EasyJohtoNoKanto.yml"
cliProcessor.attempts = 1
cliProcessor.main()

beatability = cliProcessor.instance.GetAllAccessible()

reachableItems = beatability[0]
itemTypes = [ item for item in reachableItems.items() if (item[1].IsItem or (type(item[1]) == Gym.Gym))
              and not item[1].Dummy ]

checkName = [ i[0] for i in itemTypes]
for item in checkName:
    print("    - "+item)





