import fastf1
import matplotlib.pyplot as plt
import seaborn as sns
import fastf1.plotting

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

def lap_time_evolution(year, track, session_type, driver):
    # load session
    session = fastf1.get_session(year, track, session_type)
    session.load()

    driver_laps = session.laps.pick_drivers(driver)

    no_pits = driver_laps[
        driver_laps['PitOutTime'].isnull() &
        driver_laps['PitInTime'].isnull()]
    
    #quick_laps = no_pits.pick_quicklaps()

    no_pits['TrackStatus'] = no_pits['TrackStatus'].astype(str)

    mask = no_pits['TrackStatus'].str.contains('4|6', regex=True)
    clean_laps = no_pits[~mask]

    lap_times = clean_laps['LapTime'].dt.total_seconds() 

    compound_colours = {
        'SOFT': 'red',
        'MEDIUM': 'yellow',
        'HARD': 'white',
        'INTERMEDIATE': 'green',
        'WET': 'blue'}

    colours = [compound_colours.get(lap['Compound'], 'grey') for _, lap in clean_laps.iterrows()]

    plt.figure(figsize=(12, 6))
    plt.scatter(clean_laps['LapNumber'], lap_times, c=colours, edgecolors='black')
    plt.plot(clean_laps['LapNumber'], lap_times, color='black', linestyle='--', alpha=0.5)
    plt.xlabel('Lap Number')
    plt.xlim(1, clean_laps['LapNumber'].max() + 1)
    plt.ylabel('Lap Time (s)')
    plt.title(f'{driver} Lap Time Evolution')
    plt.grid(True)
    plt.show()

def lap_time_distributions():
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

    year = int(input("Enter the year of the race (e.g., 2023): "))
    track = input("Enter the track name (e.g., 'Monza', 'Silverstone'): ")
    session_type = input("Enter the session type (e.g., 'FP1', 'FP2', 'FP3', 'Q', 'R'): ")

    # Load the race session
    session = fastf1.get_session(year, track, session_type)
    session.load()

    drivers = session.drivers
    # Filter out slow laps (yellow flag, VSC, pitstops etc.)
    driver_laps = session.laps.pick_quicklaps()
    driver_laps = driver_laps.reset_index()

    # To plot the drivers by finishing order,
    # we need to get their three-letter abbreviations in the finishing order
    finishing_order = [session.get_driver(i)["Abbreviation"] for i in drivers]
    print(finishing_order)

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Seaborn doesn't have proper timedelta support,
    # so we have to convert timedelta to float (in seconds)
    driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

    # First create the violin plots to show the distributions
    sns.violinplot(data=driver_laps,
               x="Driver",
               y="LapTime(s)",
               hue="Driver",
               inner=None,
               density_norm="area",
               order=finishing_order,
               palette=fastf1.plotting.get_driver_color_mapping(session=session)
               )

    # Then use the swarm plot to show the actual laptimes
    sns.swarmplot(data=driver_laps,
              x="Driver",
              y="LapTime(s)",
              order=finishing_order,
              hue="Compound",
              palette=fastf1.plotting.get_compound_mapping(session=session),
              hue_order=["SOFT", "MEDIUM", "HARD"],
              linewidth=0,
              size=4,
              )

    # Make the plot more aesthetic
    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle(f"{year} {track} Grand Prix Lap Time Distributions")
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()


    
def main():
    choice = input("Do you want to analyze speed trace, tyre strategy, lap time evolution, or lap time distributions? (speed/tyre/lap/distribution): ")
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
    elif choice == 'lap':
        year = int(input("Enter the year of the race (e.g., 2023): "))
        track = input("Enter the track name (e.g., 'Monza', 'Silverstone'): ")
        session_type = input("Enter the session type (e.g., 'FP1', 'FP2', 'FP3', 'Q', 'R'): ")
        driver = input("Enter the driver's code (e.g., 'VER' for Verstappen): ")
        lap_time_evolution(year, track, session_type, driver)
    elif choice == 'distribution':
        lap_time_distributions()
    else:
        print("Invalid choice. Please enter 'speed', 'tyre', 'lap', or 'distribution'.")

main()