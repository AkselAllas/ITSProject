import ardrone

drone = ardrone.ARDrone()

drone.takeoff()
drone.land()

print(drone.navdata)
print(drone.navdata['demo']['battery'])

drone.image.show()

drone.halt()