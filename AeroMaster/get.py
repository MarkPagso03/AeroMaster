import re, csv

# The user's input text (only a portion shown here for brevity)
input_text = '''
1.	What is the absolute ceiling of an airplane?
a. The altitude which produces zero rate of climb
b. The altitude that produces a rate of climb of 100 feet per minute
c. The maximum operating altitude as specified by the manufacturer
d. All of the above
2.	What is the definition of power?
a. The ability to do work
b. Work done per unit of time
c. Energy due to motion
d. Mass times acceleration
3.	Why should flight speeds above VNE be avoided?
a. Excessive induced drag will result in structural failure
b. A high-speed stall is most likely to occur
c. Control effectiveness is impaired to the point that the aircraft is uncontrollable
d. Design limit load factors may be exceeded if gusts are encountered
4.	It is the ratio between the span and the chord of the wing.
a. Taper Ratio
b. Aspect Ratio
c. MAC
d. Root Chord
5.	The induced drag coefficient, CDi is proportional with:
a. CL (maximum).
b. CL²
c. CL
d. √CL
6.	Which of the following wing planforms produces the lowest induced drag?
a. Circular
b. Rectangular
c. Elliptical
d. Tapered
7.	What must you do to remain in formation as your aircraft takes on fuel?
a. Maintain a constant AOA and TAS
b. Decrease AOA and increase TAS
c. Increase AOA and maintain constant TAS
d. Increase AOA and TAS
8.	What is the function of a swash plate in helicopter rotor blades?
a. Control pitch
b. Control speed
c. Control flap
d. Control lead and lag
9.	What produces the most lift at low speeds?
a. High camber
b. Low camber
c. Low aspect ratio
d. High aspect ratio
10.	What is the primary purpose of a feathering propeller?
a. Prevent further engine damage when an engine fails in flight
b. Prevent propeller damage when an engine fails in flight
c. Eliminate the drag created by a windmilling propeller when an engine fails in flight
d. Maintain the aircraft's speed
11.	What is the best method of speed reduction if hydroplaning is experienced on landing?
a. Apply aerodynamic braking to the fullest advantage
b. Apply full main wheel braking only
c. Apply nose wheel and main wheel braking alternately and abruptly
d. Avoid braking
12.	Which combination of atmospheric conditions will reduce aircraft takeoff and climb performance?
a. High temperature, high relative humidity, and high density altitude
b. High temperature, high relative humidity, and low density altitude
c. Low temperature, low relative humidity, and low density altitude
d. High temperature, low relative humidity, and low density altitude
13.	How does Mach number affect flight speed?
a. Mach number increases with altitude
b. Mach number decreases with altitude
c. Mach number remains constant regardless of altitude
d. Mach number is unrelated to flight speed
14.	The angle of attack at which CLmax is achieved is known as:
a. Critical angle of attack
b. Stagnation point
c. Neutral point
d. Dihedral angle
15.	What factor must be maximized for an airplane to fly a maximum angle of climb profile?
a. Thrust required (Tr.)
b. Thrust excess (Te.)
c. Power excess (Pe.)
d. Angle of attack (AOA.)
16.	What is the effect of an increase in cruise altitude (from sea level to 15,000 feet. on the maximum range of an airplane?
a. Max range increases
b. Max range decreases
c. Max range will not change
d. Max range fluctuates
17.	What control surface controls the pitching moment around the airplane's CG?
a. The ailerons on the trailing edge of the wing
b. The elevator on the trailing edge of the horizontal stabilizer
c. The spoilers on the upper surface of the wing
d. The rudder attached to the trailing edge of the vertical stabilizer
18.	What aerodynamic phenomenon is responsible for the "region of reverse command"?
a. Increase of parasite drag with increased velocities
b. Increase of induced drag with decreased velocities
c. Decrease of wingtip vortices with higher angle of attack
d. Increase of the lift-to-drag ratio with decreasing velocities
19.	The AOA where the lift-to-drag ratio is maximum is the AOA for:
a. Max range for a prop
b. Max range for a jet
c. Max endurance for a prop
d. Max lift and minimum drag
20.	Increasing weight in a propeller-driven aircraft will:
a. Result in an increase in the TAS and decrease in the angle of attack for maximum range
b. Result in a decrease of the TAS for maximum range
c. Have no effect on the TAS at which the aircraft will fly for maximum range
d. Result in the aircraft flying at a greater TAS and the same AOA for maximum range
21.	What effect does sweepback have on the stall characteristics of a wing?
a. The root stalls first
b. The tip stalls first
c. The stall occurs simultaneously along the span
d. It eliminates stall entirely
22.	What is the effect of an increase in aspect ratio on induced drag?
a. Increases induced drag
b. Decreases induced drag
c. Has no effect on induced drag
d. Increases wave drag
23.	The primary advantage of a high aspect ratio wing is:
a. Higher maneuverability
b. Lower induced drag
c. Greater structural strength
d. Higher roll rate
24.	What happens to the center of pressure as the angle of attack increases?
a. Moves forward
b. Moves aft
c. Remains constant
d. Moves downward
25.	Which aerodynamic control is most responsible for yaw?
a. Elevator
b. Rudder
c. Aileron
d. Flaps
26.	What is the primary cause of adverse yaw?
a. Increased lift on the upgoing wing
b. Increased induced drag on the down going wing
c. Decreased induced drag on the raised wing
d. Decreased drag on the descending wing
27.	When an aircraft is in a steady-state, unaccelerated level flight, which forces are in equilibrium?
a. Lift and drag
b. Lift and weight, thrust and drag
c. Lift and thrust
d. Weight and drag
28.	The aspect ratio of a wing is calculated by:
a. Wing area divided by wingspan
b. Wingspan divided by wing thickness
c. Wingspan divided by chord
d. Wing area divided by wing chord
29.	What is the critical Mach number?
a. The speed at which an aircraft reaches the sound barrier
b. The speed at which airflow over a portion of the aircraft reaches Mach 1
c. The speed at which shock waves disappear
d. The speed at which supersonic airflow is achieved over the entire aircraft
30.	What flight condition must an aircraft be placed in to spin?
a. High angle of attack
b. Partially stalled with one wing low
c. Stalled
d. In a steep diving spiral
31.	What happens to stall speed as weight increases?
a. Increases
b. Decreases
c. Remains constant
d. Increases only in ground effect
32.	What is Dutch roll?
a. Yaw and pitch oscillation
b. Yaw and roll oscillation
c. Pitch and roll oscillation
d. Pure yaw oscillation
33.	The interference drag is created as a result of:
a. Addition of induced and parasite drag
b. Downwash behind the wing
c. Interaction between airplane parts
d. Separation of the induced vortex
34.	In a supersonic airstream, which flow properties decrease as the fluid flows across an expansion wave?
a. Pressure and mass density
b. Pressure and Mach number
c. Mass density and velocity
d. Velocity and Mach number
35.	How does altitude affect true airspeed (TAS). for a given indicated airspeed (IAS).?
a. TAS decreases with altitude
b. TAS increases with altitude
c. TAS remains constant
d. TAS is unrelated to altitude
36.	When does a shock stall occur?
a. At low subsonic speeds due to separation of the boundary layer
b. When the shock wave moves forward, causing excessive drag
c. When the shock wave moves aft, increasing lift
d. At the moment of reaching transonic speed
37.	What factor determines the speed of sound in the atmosphere?
a. Altitude
b. Temperature
c. Humidity
d. Air pressure
38.	Which of the following decreases as altitude increases?
a. True airspeed
b. Indicated airspeed
c. Mach number
d. Speed of sound
39.	The primary function of the horizontal stabilizer is to provide:
a. Directional stability
b. Lateral stability
c. Longitudinal stability
d. Lift for pitch control
40.	What is the primary cause of induced drag?
a. Shock waves
b. Wingtip vortices
c. Friction between airflow and the aircraft’s surface
d. Pressure distribution around the fuselage
41.	When the Reynolds number is above 4000, the flow is:
a. Laminar
b. Turbulent
c. Supersonic
d. Critical
42.	The term "washout" in wing design refers to:
a. A gradual decrease in wing thickness toward the tip
b. A reduction in the angle of incidence toward the wingtip
c. The increase of lift at the wing root
d. The transition from laminar to turbulent flow
43.	A Venturi tube is used to measure:
a. Airspeed
b. Density
c. Pressure differences
d. Mach number
44.	What happens to static pressure as air moves through the throat of a Venturi tube?
a. Increases
b. Decreases
c. Remains the same
d. First decreases, then increases
45.	Why does an aircraft experience an increase in drag when flying near the speed of sound?
a. Shock waves form, increasing pressure drag
b. Increased airspeed increases parasitic drag
c. Air viscosity decreases
d. The boundary layer becomes turbulent
46.	The primary cause of wave drag is:
a. Skin friction
b. Shock waves
c. Wingtip vortices
d. Air viscosity
47.	What is the primary function of leading-edge slats?
a. To delay flow separation and reduce stall speed
b. To decrease lift at low speeds
c. To increase drag for landing
d. To reduce wave drag
48.	What effect does increasing altitude have on an aircraft's Mach number for a given true airspeed?
a. Mach number decreases
b. Mach number remains constant
c. Mach number increases
d. Mach number is independent of altitude
49.	What is the effect of a forward center of gravity on stall speed?
a. Increases stall speed
b. Decreases stall speed
c. Has no effect
d. Increases lift
50.	How can an aircraft counteract Mach tuck?
a. Use of ailerons
b. Use of Mach trim system
c. Increasing throttle
d. Deploying leading-edge slats

'''

pattern1 = input_text.replace("\n\n", "\n").strip()

print(pattern1)
# Regex to extract all the question lines (excluding options)
pattern = re.findall(
    r"\d+\.\s+(.*?)\na\.\s*(.*?)\nb\.\s*(.*?)\nc\.\s*(.*?)\nd\.\s*(.*?)(?=\n\d+\.|\Z)",
    pattern1,
    re.DOTALL
)
'''

letters = re.findall(r'[A-D]', input_text)
for letter in letters:
    print(letter)


# Save to CSV: question, option_a, option_b, option_c, option_d
'''
with open("AERO Problems.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "option_a", "option_b", "option_c", "option_d"])  # header
    for match in pattern:
        question, a, b, c, d = match
        writer.writerow([question.strip(), a.strip(), b.strip(), c.strip(), d.strip()])

print("✅ done.")
