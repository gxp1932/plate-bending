# Program for the evaluation and design of a steel plate in minor axis bending
# AISC Manual of Steel Construction (ASD), 14th Ed, 2011
#
# Geometric Input
# t = float(input("What is the plate thickness (in.)? "))
# print("The plate thickness is: t = " + str(t) + " in.")
# d = float(input("What is the plate depth (in.)? "))
# print("The plate depth is: d = " + str(d) + " in.")
# Lb = float(input("What is the plate length (in.)? "))
# print("The plate length is: Lb = " + str(Lb) + " in.")
# e = float(input("What is the eccentricity of the load from bottom of plate (in.)? "))
# print("The eccentricity is: e = " + str(e) + " in.")
# P_max = float(input("What is the maximum applied lateral load (kip)? "))
# print("The maximum applied lateral load is: P_max = " + str(P_max) + " kip")
#
# # Constants
# # Yield Strength (ksi)
# Fy = float(36)
# # Modulus of Elasticity (ksi)
# E = float(29000)
# # Lateral-torsional buckling modification factor
# Cb = float(1)
#
#
# # Modulus Calculation
# print()
# Z = float(((d*t*t))/4)
# print("The plastic section modulus is: Z = " + str(Z.__round__(2)) + " in.^3")
# S = float(((d*t*t))/6)
# print("The elastic section modulus is: S = " + str(S.__round__(2)) + " in.^3")
#
# # Check yielding for rectangular bars bent about minor axis (AISC F11-1)
# print()
# My_1_6 = float((1.6 * Fy * S) / 12)
# print("1.6My = " + str(My_1_6.__round__(2)) + " k-ft")
# Mp = float((Z * Fy) / 12)
# print("Mp = " + str(Mp.__round__(2)) + " k-ft")
# print()
# print("Nominal Moment = Minimum of 1.6My and Mp:")
# Mn = min(Mp, My_1_6)
# print("Mn = " + str(Mn.__round__(2)) + " k-ft")
#
# # Determine maximum allowable applied load
# print()
# P_all = ((Mn / 1.67) / (e / 12))
# print("Maximum allowable lateral load: P_all = " + str(P_all.__round__(2)) + " kip")
#
# # Bending Strength Unity Check
# print()
# Unity = P_max / P_all
# print("Bending Unity Strength = P_max/P_all = " + str(Unity.__round__(2)))
#
# if Unity <= 1:
#     print("Pass")
# else:
#     print("Fail")
