import sys

print()
print("Welcome to the steel plate bending analysis tool!")
print()
analysis = input("Will the plate be analyzed for major axis bending or minor axis bending? (major/minor): ")

if analysis.lower() in ("minor","major"):
    print("You selected " + analysis.lower() + ".")
else:
    print()
    print('Analysis failed. Please run again and enter "minor" or "major".')
    sys.exit()

# Geometric Input
t = float(input("What is the plate thickness (in.)? "))
print("The plate thickness is: t = " + str(t) + " in.")
d = float(input("What is the plate depth (in.)? "))
print("The plate depth is: d = " + str(d) + " in.")
Lb = float(input("What is the plate length (in.)? "))
print("The plate length is: Lb = " + str(Lb) + " in.")
e = float(input("What is the eccentricity of the load from bottom of plate (in.)? "))
print("The eccentricity is: e = " + str(e) + " in.")
P_max = float(input("What is the maximum applied lateral load (kip)? "))
print("The maximum applied lateral load is: P_max = " + str(P_max) + " kip")

# Constants
# Yield Strength (ksi)
Fy = float(36)
# Modulus of Elasticity (ksi)
E = float(29000)
# Lateral-torsional buckling modification factor
Cb = float(1)

def major_axis():
    print()
    print("The plate will be analyzed for major axis bending.")

    # Modulus Calculation
    print()
    Z = float(((t * d * d)) / 4)
    print("The plastic section modulus is: Z = " + str(Z.__round__(2)) + " in.^3")
    S = float(((t * d * d)) / 6)
    print("The elastic section modulus is: S = " + str(S.__round__(2)) + " in.^3")

    # Check yielding for rectangular bars bent about minor axis (AISC F11-1)
    print()
    Lbd_t2 = float(Lb * d)/(t*t)
    E08_Fy = float((0.08*E)/Fy)
    E19_Fy = float((1.9*E)/Fy)
    My = float(Fy * S)/12
    Mp = float(Fy * Z)/12
    if Lbd_t2 <= E08_Fy:
        My_1_6 = float((1.6 * Fy * S)/12)
        print("1.6My = " + str(My_1_6.__round__(2)) + " k-ft")
        Mp = float((Z * Fy)/12)
        print("Mp = " + str(Mp.__round__(2)) + " k-ft")
        print()
        print("Nominal Moment = Minimum of 1.6My and Mp:")
        Mn = min(Mp, My_1_6)
        print("Mn = " + str(Mn.__round__(2)) + " k-ft")

    # Check lateral torsional buckling (AISC F11-2)
    else:
        if Lbd_t2 <= E19_Fy and E08_Fy < Lbd_t2:
            Mn = min(float(Cb*(1.52 - 0.274 * (Lbd_t2) * (Fy / E)) * My), Mp)
        else:
            if E19_Fy < Lbd_t2:
                Fcr = float((1.9*E*Cb)/Lbd_t2)
                print("Fcr = " + str(Fcr))
                Mn = min((Fcr * S), Mp)
        print("Mn = " + str(Mn.__round__(2)) + " k-ft")

    # Determine maximum allowable applied load
    print()
    P_all = float((Mn/1.67)/(e/12))
    print("Maximum allowable lateral load: P_all = " + str(P_all.__round__(2)) + " kip")

    # Bending Strength Unity Check
    print()
    Unity = P_max/P_all
    print("Bending Unity Strength = P_max/P_all = " + str(Unity.__round__(2)))

    if Unity <= 1:
        print("Pass")
    else:
        print("Fail")

def minor_axis():
    print()
    print("The plate will be analyzed for minor axis bending.")

    # Modulus Calculation
    print()
    Z = float(((d * t * t)) / 4)
    print("The plastic section modulus is: Z = " + str(Z.__round__(2)) + " in.^3")
    S = float(((d * t * t)) / 6)
    print("The elastic section modulus is: S = " + str(S.__round__(2)) + " in.^3")

    # Check yielding for rectangular bars bent about minor axis (AISC F11-1)
    print()
    My_1_6 = float((1.6 * Fy * S)/12)
    print("1.6My = " + str(My_1_6.__round__(2)) + " k-ft")
    Mp = float((Z * Fy)/12)
    print("Mp = " + str(Mp.__round__(2)) + " k-ft")
    print()
    print("Nominal Moment = Minimum of 1.6My and Mp:")
    Mn = min(Mp, My_1_6)
    print("Mn = " + str(Mn.__round__(2)) + " k-ft")

    # Determine maximum allowable applied load
    print()
    P_all = ((Mn/1.67)/(e/12))
    print("Maximum allowable lateral load: P_all = " + str(P_all.__round__(2)) + " kip")

    # Bending Strength Unity Check
    print()
    Unity = P_max/P_all
    print("Bending Unity Strength = P_max/P_all = " + str(Unity.__round__(2)))

    if Unity <= 1:
        print("Pass")
    else:
        print("Fail")

if analysis.lower() == "major":
    major_axis()
    print()
    print("The plate has been analyzed for major axis bending.")
    print("Analysis complete. Thank you.")

elif analysis.lower() == "minor":
    minor_axis()
    print()
    print("The plate has been analyzed for minor axis bending.")
    print("Analysis complete. Thank you.")




