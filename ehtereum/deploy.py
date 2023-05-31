import os
import sys

#THIS SCRIPT ASSUMES
#1. The contract is in contracts/
#2. You run this script from the root directory of a hardhat project
#3. You have a hardhat.config.js file in the root directory of the project with the content necessary to deploy the contract on sepolia.

#USAGE
#python3 scripts/generalDeploy.py <contractFileName> <arguments> <network>
#<contractFileName> is the name of the file with the contract you want to deploy
#<arguments> are the arguments you want to pass to the constructor of the contract, in order.
#<network> is the network you want to deploy to (default is localnet, you can specify sepolia)

#Use -no-deploy as the only argument to only create the script.



args = sys.argv[1:]
network = ""
NAME = ""
deploy = True

def main(): 
    global NAME, args
    if len(args) == 0:
        print("Please specify a name for the deployment script")
        return

    NAME, args = args[0], args[1:] 

    if NAME.find(".sol") != -1:
        NAME = NAME[:-4]

    match args[len(args)-1]:
        case "sepolia":
            global network
            network = "--network sepolia"
            args = args[:-1] 
        case "-no-deploy":
            global deploy
            deploy = False
            args = args[:1]

    writeScript(f"deploy{NAME}.ts")
    
    if deploy:
        os.system(f"npx hardhat run scripts/deploy{NAME}.ts {network}")
    else:
        print("Script created but not deployed")


def writeScript(file):
    a = makeScript()
    os.system(f"touch scripts/{file}")
    with open(f"scripts/{file}", "w") as f:
        f.write(a)

def makeScript():

    contractName, capitalizedContractName, realName = getContractName()
    variables, arguments = getVariables()

    imports = """import { ethers } from "hardhat";\n\n""" 
    mainpart = imports + f"""const contractName = "{realName}";\n""" 

    mainpart += variables + f"""\nasync function main() {{ 
    const {capitalizedContractName} = await ethers.getContractFactory(contractName);
    const {contractName} = await {capitalizedContractName}.deploy({arguments});

    await {contractName}.deployed();
    console.log(`${{ contractName }} deployed to ${{ {contractName}.address }}`);
}}\n"""  

    final = mainpart + """
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});"""

    return final

def getContractName():
    name = ""
    with open(f"contracts/{NAME}.sol", "r") as f:
        for line in f:
            if "contract " in line:
                name = line.split(" ")[1].split("{")[0]
    return name.lower(),  name.capitalize(), name

def getContractNameLower():
    return getContractName().lower()

def getContractNameCap():
    return getContractName().capitalize()

def getConstructorSignature():
    global NAME
    with open(f"contracts/{NAME}.sol", "r") as f:
        for line in f:
            if "constructor" in line:
                return line[line.find("(")+1:line.find(")")]

def cutSpaces(v):
    if v[0] == "":
        v.pop(0)
        cutSpaces(v)
    return v

def getVariables():
    variablenametypes = []
    arguments = ""
    content = False

    constructorSignature = getConstructorSignature().split(",")

    global args

    if len(args) > 0:
        content = True

    for elem in constructorSignature:
        v = elem.split(" ")
        cutSpaces(v)
        variablenametypes.append(v)

    variables = ""
    i = 0
    for elem in variablenametypes:
        
        if content: 
            if str(elem[0]).find("int") != -1:
                variables += f"const {elem[1]} = {args[i]}  //{elem[0]} in the contract;\n"
            else:
                variables += f"""const {elem[1]} = "{args[i]}" //{elem[0]} in the contract;\n"""
            arguments += f"{elem[1]}, "
            i += 1
        else:
            variables += f"const {elem[1]} = null  //change this, it's a {elem[0]};\n"
            arguments += f"{elem[1]}, "
            
    arguments = arguments[:-2]

    if len(arguments.split(",")) != len(args):
        global deploy
        deploy = False

    return variables, arguments 

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Please specify a name for the deployment script")
        exit()

    main()