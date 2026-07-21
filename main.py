import fastf1
import matplotlib.pyplot as plt

# Turn on the cache (this makes future runs faster)
fastf1.Cache.enable_cache('cache')

# create a function to take a user's inputs to allow the analysis of any race session
def analyze_session(year, track, session_type, driver):
    # take information for the session and load it
    year = int(input("Enter the year of the race"))
    track = input("Enter the track name")
    session_type = input("Enter the session type (R for race, Q for qualifying, S for sprint, FP1, FP2, FP3 for practice, SQ for sprint qualifying): ")
    driver = input("Enter the driver's last name")
    session = fastf1.get_session(year, track, session_type)
    session.load()
    analysis_choice = input("Do you want to analyze the fastest lap or all laps? (fastest/all): ")
    if analysis_choice == 'fastest':
        # Get all laps for the specified driver
        laps = session.laps.pick_driver(driver)
        # Pick the fastest lap
        lap = laps.pick_fastest()
        # Get telemetry (speed, distance, etc.) for that lap
        tel = lap.get_telemetry()
        # Plot speed vs distance
        plt.plot(tel['Distance'], tel['Speed'])
        plt.xlabel('Distance (m)')
        plt.ylabel('Speed (km/h)')
        plt.title(f'{driver} Fastest Lap Speed Trace')
        plt.show()
    elif analysis_choice == 'all':
        # Get all laps for the specified driver
        laps = session.laps.pick_driver(driver)
        # Plot speed vs distance for all laps
        for lap in laps.iterlaps():
            tel = lap.get_telemetry()
            plt.plot(tel['Distance'], tel['Speed'], label=f'Lap {lap.LapNumber}')
        plt.xlabel('Distance (m)')
        plt.ylabel('Speed (km/h)')
        plt.title(f'{driver} All Laps Speed Trace')
        plt.legend()
        plt.show()

analyze_session(year, track, session_type, driver)





"""
# Get all laps for one driver (VER = Verstappen)
laps = session.laps.pick_driver('VER')

# Pick his fastest lap
lap = laps.pick_fastest()

# Get telemetry (speed, distance, etc.) for that lap
tel = lap.get_telemetry()

# Plot speed vs distance
plt.plot(tel['Distance'], tel['Speed'])
plt.xlabel('Distance (m)')
plt.ylabel('Speed (km/h)')
plt.title('Verstappen Fastest Lap Speed Trace')
plt.show()
"""