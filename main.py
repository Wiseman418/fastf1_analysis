import fastf1
import matplotlib.pyplot as plt

# Turn on the cache (this makes future runs faster)
fastf1.Cache.enable_cache('cache')

# create a function to take a user's inputs to allow the analysis of any race session
def speed_trace(year, track, session_type, driver):

    # load session
    session = fastf1.get_session(year, track, session_type)
    session.load()
    
    analysis_choice = input("Do you want to analyze the fastest lap or all laps? (fastest/all): ")

    laps = session.laps.pick_drivers(driver)
    
    if laps.empty:
        print(f"No laps found for driver '{driver}' in the {session_type}")
        return

    if analysis_choice == 'fastest':
        # Pick the fastest lap
        lap = laps.pick_fastest()
        # Get telemetry (speed, distance, etc.) for that lap
        tel = lap.get_telemetry()
        # Plot speed vs distance
        plt.plot(tel['Distance'], tel['Speed'])
        plt.xlabel('Distance (m)')
        plt.ylabel('Speed (km/h)')
        plt.title(f'{driver} Fastest Lap Speed Trace')
        plt.tight_layout()
        plt.show()
    elif analysis_choice == 'all':
        # Plot speed vs distance for all laps
        for _, lap in laps.iterlaps():
            tel = lap.get_telemetry()
            plt.plot(tel['Distance'], tel['Speed'], label=f'Lap {lap.LapNumber}')
        plt.xlabel('Distance (m)')
        plt.ylabel('Speed (km/h)')
        plt.title(f'{driver} All Laps Speed Trace')
        plt.legend()
        plt.show()
    else:
        print("Invalid choice. Please enter 'fastest' or 'all'.")

def tyre_strategy(year, track, session_type):
   
    # load session
    session = fastf1.get_session(year, track, session_type)
    session.load()

    # analyze tyre compounds used
    for driver in ['VER', 'HAM', 'LEC']:
        driver_laps = session.laps.pick_drivers(driver)

        print(f"\n{driver} Tyre Strategy:")
        for stint in driver_laps['Stint'].unique():
            stint_laps = driver_laps[driver_laps['Stint'] == stint]
            tyre_compound = stint_laps['Compound'].iloc[0]
            num_laps = len(stint_laps)
            print(f" Stint {int(stint)}: {tyre_compound:12s} - {num_laps} laps")

def main():
    choice = input("Do you want to analyze speed trace or tyre strategy? (speed/tyre): ")
    if choice == 'speed':
        year = int(input("Enter the year of the race (e.g., 2023): "))
        track = input("Enter the track name (e.g., 'Monza', 'Silverstone'): ")
        session_type = input("Enter the session type (e.g., 'FP1', 'FP2', 'FP3', 'Q', 'R'): ")
        driver = input("Enter the driver's code (e.g., 'VER' for Verstappen): ")
        speed_trace(year, track, session_type, driver)
    elif choice == 'tyre':
        year = int(input("Enter the year of the race (e.g., 2023): "))
        track = input("Enter the track name (e.g., 'Monza', 'Silverstone'): ")
        session_type = input("Enter the session type (e.g., 'FP1', 'FP2', 'FP3', 'Q', 'R'): ")
        tyre_strategy(year, track, session_type)
    else:
        print("Invalid choice. Please enter 'speed' or 'tyre'.")
    
main()

# speed_trace(year, track, session_type, driver)

