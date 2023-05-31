import os
import sys
import subprocess
import argparse

#THIS SCRIPT ASSUMES
#1. The contract is in contracts/
#2. You run this script from the root directory of a hardhat project
#3. You have a hardhat.config.js file in the root directory of the project with the content necessary to deploy the contract on sepolia.

#  USAGE
#  Run the script as follows:
#  python3 scripts/autoScript.py <contractName> <contractArguments> --network <network>
#  contractName: name of the contract to deploy, without the .sol extension
#  contractArguments: arguments to pass to the contract constructor, separated by spaces
#  network: network to deploy on. If not specified, it will deploy on hardhat localnet
#  You can put --no-deploy to only create the script without deploying it


network = ""
NAME = ""
stopDeploy = True

parser = argparse.ArgumentParser(description='Deploy script')
parser.add_argument('name', type=str, help='name for the deployment script')
parser.add_argument('contract_arguments', nargs='*', help='arguments to pass to the contract constructor')
parser.add_argument('--network', type=str, default='hardhat', help='network to deploy on')
parser.add_argument('--no-deploy', action='store_true', help='do not deploy')
args = parser.parse_args()
contract_args = parser.parse_args().contract_arguments

def main():

    setName(args.name)
    setNetwork()
    constructorSignature = getConstructorSignature()

    writeScript(f"deploy{NAME}.ts", constructorSignature)

    strarguments = list(zip(constructorSignature, contract_args))

    global stopDeploy
    if not args.no_deploy and (not stopDeploy):
        print(f"Deploying contract {NAME} in {network} network with constructor arguments {strarguments}")
        subprocess.run(["npx", "hardhat", "run", f"scripts/deploy{NAME}.ts","--network" ,network])
    else:
        print("Script created but not deployed")

def writeScript(file, constructorSignature):
    a = makeScript(constructorSignature)
    os.system(f"touch scripts/{file}")
    with open(f"scripts/{file}", "w") as f:
        f.write(a)

def setName(name):
    global NAME
    NAME = args.name
    if NAME.endswith(".sol"):
        NAME = NAME[:-4]

def setNetwork():
    global network
    if args.network == "sepolia":
        network = "sepolia"
    elif not args.no_deploy:
        network = "hardhat"

def makeScript(constructorSignature):

    contractName, capitalizedContractName, realName = getContractName()

    if len(contract_args) != len(constructorSignature) and len(contract_args) != 0:
        print("Wrong number of arguments, exiting...")
        exit()

    variables, arguments = getVariables(constructorSignature)

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

def getConstructorSignature():
    global NAME
    with open(f"contracts/{NAME}.sol", "r") as f:
        for line in f:
            if "constructor" in line:
                return line[line.find("(")+1:line.find(")")].split(",")

def cutSpaces(v):
    if v[0] == "":
        v.pop(0)
        cutSpaces(v)
    return v

def getVariables(constructorSignature):
    variablenametypes = []
    arguments = ""
    content = False

    global contract_args

    if len(contract_args) > 0 and len(constructorSignature) == len(contract_args):
        content = True
        global stopDeploy 
        stopDeploy = False
    
    for elem in constructorSignature:
        v = elem.split(" ")
        cutSpaces(v)
        variablenametypes.append(v)

    variables = ""
    i = 0
    for elem in variablenametypes:
        
        if content: 
            if str(elem[0]).find("int") != -1:
                variables += f"const {elem[1]} = {contract_args[i]}  //{elem[0]} in the contract;\n"
            else:
                variables += f"""const {elem[1]} = "{contract_args[i]}" //{elem[0]} in the contract;\n"""
            arguments += f"{elem[1]}, "
            i += 1
        else:
            variables += f"const {elem[1]} = null  //change this, it's a {elem[0]};\n"
            arguments += f"{elem[1]}, "

    arguments = arguments[:-2]

    return variables, arguments 

if __name__ == "__main__":

    if len(sys.argv) == 0:
        print("Please specify a name for the deployment script")
        exit()
        
    main()
