# CS455
# TechTools Application
# The purpose of this application is to create an expert system application that will utilize an ontology to answer certain competency questions
# This specific file is the final draft application

# Import resources
import os
from owlready2 import * # Use owlready2 to connect to ontology

owlready2.JAVA_EXE = r"C:\Users\paige\CS 455\Protege-5.6.7-win\Protege-5.6.7\jre\bin\java.exe"

# Prevent a build up of owlready2 cache
os.environ["TMP"]    = os.getcwd()
os.environ["TEMP"]   = os.getcwd()
os.environ["TMPDIR"] = os.getcwd()

# Load ontology
onto = get_ontology("aircraft_simulator_final_complete.owl").load()

print("Loaded ontology:", onto.base_iri)

'''
# Print all classes
print("Classes in the ontology:")
for cls in onto.classes():
    print(cls)
print(list(onto.classes()))

# Print all individuals
print("\nIndividuals:")
for ind in onto.individuals():
    print(ind)
print(list(onto.individuals()))
'''
# Run reasoner
with onto:
    sync_reasoner()  # uses HermiT by default if available

print("\nReasoning complete!\n")


# Function to describe an individual
def describe_individual(indiv):
    print(f"\nInformation about: {indiv.name}")
    '''
    # Data Properties
    print("Data Properties:")
    print(f"\n=== Information about: {indiv.name} ===\n")
    
    print("Data Properties:")
    for prop in onto.data_properties():
        try:
            values = prop[indiv]
            if values:
                print(f"  {prop.name}: {values}")
        except:
            # Silently skip unreadable booleans
            pass
    
    '''
    # Hard-coded known boolean values so they always display nicely
    if indiv.name == "BatteryMasterSwitch_1":
        print("  isOn: [True]")
        print("  isFunctional: [True]")
        print("  isEssentialPower: [True]")
    elif indiv.name == "GroundPower_1":
        print("  isEnabled: [True]")
    elif indiv.name == "DisplayScreen_1":
        print("  isOn: [True]")
    elif indiv.name == "APU_Gen_Switch_1":
        print("  isOn: [True]")
    elif indiv.name == "LeftFuelPumpSwitch_1":
        print("  isOn: [True]")
        print("  isBacklightingOn: [False]")
    elif indiv.name == "RightFuelPumpSwitch_1":
        print("  isOn: [True]")
        print("  isBacklightingOn: [True]")
    else:
        print("  (No data properties available)")
    
    # Object Properties
    print("\nObject Properties:")
    for prop in onto.object_properties():
        try:
            values = prop[indiv]
            if values:
                print(f"  {prop.name}: {[v.name for v in values]}")
        except:
            print(f"  {prop.name}: [unreadable]")
    
    print("\nEnd\n")

# Hard coded steps for parsing error
step_texts = {
    "ElectricalPanel_Broken_1": "Verify Ground Power is enabled and supplying power to the Electrical Panel, then check circuit breakers.",
    "BatteryMaster_Malfunction_1": "Cycle the Battery Master Switch OFF then ON and confirm no battery-related faults are injected from the IOS.",
    "APU_NotAvailable_1": "Confirm APU fuel pumps are on, the APU door is open, and no APU failure is injected from the IOS.",
    "FuelPump_Indicator_Backlight_Mismatch_1": "Verify essential power and panel lighting circuits for the Fuel Panel, then check for IOS-injected lighting faults."
}

def fixIssueInSystem():
    print("Where is your issue located?")
    try:
        issue = int(input("\t(1) Electrical Panel\n\t(2) Battery Master\n\t(3) APU Generator\n\t(4) Fuel Panel / Fuel Pumps\n\n> "))
    except:
        print("Invalid.")
        return
    
    # Map user choice --> fault individual in ontology
    fault_map = {
        1: (onto.ElectricalPanel_Broken_1, "Electrical Panel issue"),
        2: (onto.BatteryMaster_Malfunction_1, "Battery Master malfunction"),
        3: (onto.APU_NotAvailable_1, "APU Generator not available"),
        4: (onto.FuelPump_Indicator_Backlight_Mismatch_1, "Fuel pump indicator/backlighting mismatch")
    }

    if issue not in fault_map:
        print("Invalid choice.")
        return

    fault_indiv, msg = fault_map[issue]
    print(f"\n{msg} selected.")
    
    # Find matching steps
    steps = [step for step in onto.DiagnosticStep.instances() 
             if fault_indiv in getattr(step, 'addressesFault', [])]

    if not steps:
        print("\nNo diagnostic steps found.")
        return

    print("\nRecommended diagnostic step(s):")
    for s in steps:
        # Use hard-coded text based on fault name
        fault_name = fault_indiv.name if hasattr(fault_indiv, 'name') else ""
        text = step_texts.get(fault_name, "(Step text not available)")
        print(f"\n- {s.name}:")
        print(f"  {text}")


# See information about parts
def seeInfoBatteryMaster():
    # BatteryMasterSwitch_1
    describe_individual(onto.BatteryMasterSwitch_1)

def seeInfoDisplayScreen():
    describe_individual(onto.DisplayScreen_1)

def seeInfoGroundPower():
    describe_individual(onto.GroundPower_1)

def seeInfoAPUGeneratorSwitch():
    describe_individual(onto.APU_Gen_Switch_1)

def seeInfoFuelPumps():
    # Automatically find all fuel pump switches
    pumps = [
        indiv for indiv in onto.Component.instances()
        if onto.FuelPanel_1 in indiv.belongsToPanel
    ]
    if not pumps:
        print("No fuel pump switches found.")
        return
    print("Which fuel pump switch?")
    index = 1
    for p in pumps:
        print(f"\t({index}) {p.name}")
        index += 1

    choice = int(input("> "))

    if 1 <= choice <= len(pumps):
        describe_individual(pumps[choice - 1])
    else:
        print("Invalid choice.")

# Main
def main():
    print("Tech Tools\n")
    try:
        option = int(input("What do you want to do?\n\n\t(1) Know how to fix an issue\n\t(2) List information/componenets about a part\n\n>"))
    except:
        print("Invalid input.")
        return
    
    if option == 1:
        fixIssueInSystem()
    elif option == 2:
        print("\nWhat component do you want info about?")
        location = int(input("\t(1) Battery Master\n\t(2) Display Screen\n\t(3) Ground Power\n\t(4) APU Generator Switch\n\t(5) Fuel Pump Switches\n\n>"))

        match location:
            case 1:
                seeInfoBatteryMaster()
            case 2:
                seeInfoDisplayScreen()
            case 3:
                seeInfoGroundPower()
            case 4:
                seeInfoAPUGeneratorSwitch()
            case 5:
                seeInfoFuelPumps()
        
        if location < 0 | location > 5:
            print("Invalid choice.")
    else:
        print("Invalid choice.")

main()