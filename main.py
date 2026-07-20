import fastf1
import matplotlib.pyplot as plt

# Turn on the cache (this makes future runs faster)
fastf1.Cache.enable_cache('cache')

# Load a race session: year, track name, and 'R' for race
session = fastf1.get_session(2024, 'Bahrain', 'R')
session.load()

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
