from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    def __init__(self):
        super().__init__()

        self.previous_disaster = None

        self.lasting_disasters = [DisasterType.fire, DisasterType.blizzard, DisasterType.monster]

        self.disaster_to_decree = {
            DisasterType.fire: DecreeType.anti_fire_dogs,
            DisasterType.tornado: DecreeType.paperweights,
            DisasterType.blizzard: DecreeType.snow_shovels,
            DisasterType.earthquake: DecreeType.rubber_boots,
            DisasterType.monster: DecreeType.fishing_hook,
            DisasterType.ufo: DecreeType.cheese,
        }

        #For setting decrees
        self.decree = DecreeType.none
        self.previous_decree = DecreeType.none
        self.decree_lag = 0

    def team_name(self):
        return 'Team 2'

    def city_name(self):
        return '# TODO name city'

    def city_type(self):
        return CityType.popular

    def take_turn(self, turn, actions, city, disasters):
        avail_effort = city.population

        lasting_disasters = []
        for disaster in disasters:
            if disaster.type in self.lasting_disasters:
                lasting_disasters.append(disaster)

            self.previous_disaster = disaster
        try:
            lasting_disasters.sort(key=lambda x: lasting_disasters[0].effort_remaining)
        except IndexError:
            pass

        for i in range(len(lasting_disasters)):
                actions.add_effort(lasting_disasters[i], lasting_disasters[i].effort_remaining)
        try:
            lasting_disasters.sort(key=lambda x: lasting_disasters[0].effort_remaining)
        except IndexError:
            pass

        if city.structure < city.max_structure - 20:
            actions.add_effort(ActionType.repair_structure, (city.max_structure - city.structure) * 2)
            # add effort to repair city if structure below 50

        if city.population < city.structure:
            actions.add_effort(ActionType.regain_population, (city.structure - city.population) * 2)





        senses = []
        senses_name = []
        for i in city.sensors:
            senses.append(i.sensor_results)
            senses_name.append(i)

        senses_name[senses.index(max(senses))]

        print(
            "blizz " + str(city.sensors[SensorType.blizzard].sensor_results) \
            + "\nearth " + str(city.sensors[SensorType.earthquake].sensor_results) \
            + "\nfire " + str(city.sensors[SensorType.fire].sensor_results) \
            + "\nmonster " + str(city.sensors[SensorType.monster].sensor_results) \
            + "\ntornado " + str(city.sensors[SensorType.tornado].sensor_results) \
            + "\nufo " + str(city.sensors[SensorType.ufo].sensor_results)
            )
        print(str(self.previous_disaster) + "----------------")

        if self.decree_lag <= 4:
            if city.sensors[SensorType.earthquake].sensor_results >= .88:
                self.decree = self.disaster_to_decree[DisasterType.earthquake]
        actions.set_decree(self.decree)

